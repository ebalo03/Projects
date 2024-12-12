import time
import json
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import csv

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key='API Key'
)

def write_to_csv(rows, filename):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(rows)

def openai_request(assistant_id, input_string):
    run = client.beta.threads.create_and_run(
        assistant_id=assistant_id,
        thread={"messages": [{"role": "user", "content": input_string}]}
    )

    time.sleep(1)
    retrieve_run = client.beta.threads.runs.retrieve(
        thread_id=run.thread_id,
        run_id=run.id
    )

    while retrieve_run.status != "completed":
        time.sleep(1)
        retrieve_run = client.beta.threads.runs.retrieve(
            thread_id=run.thread_id,
            run_id=run.id
        )
    time.sleep(1)

    run_steps = client.beta.threads.runs.steps.list(
        thread_id=run.thread_id,
        run_id=run.id
    )

    message = client.beta.threads.messages.retrieve(
        thread_id=run.thread_id,
        message_id=run_steps.data[0].step_details.message_creation.message_id,
    )
    response_content = message.content[0].text.value  # or however you get the response content
    json_ = response_content.replace('json', '').replace('`', '')
    #print(f'We matched the following: {json_}')
    return json.loads(json_)

def cut_category_levels(df):
    # Before AI assistant (only if nodes have a length getter than 2)
    # Split the 'Category' column by ' > ', keep only the first two parts, and join them back together
    df['Shortened Category'] = df['Full Category'].str.split(' > ').apply(lambda x: ' > '.join(x[:2]))
    df_for_base_analysis = df.drop_duplicates(subset='Shortened Category', keep='first')

    return df, df_for_base_analysis

def rematch_base_categories(df1, df2, output_file):
    # After AI assistant
    merged_df = pd.merge(df1, df2, left_on='Shortened Category', right_on='Brand Subcategory', how='outer')
    merged_df = merged_df.drop(columns=['Shortened Category', 'Brand Subcategory'])
    merged_df.to_csv(output_file, index=False)


def main():
    # Preprocessing: original categories (correctly formatted)
    account_name = 'Brand Name'
    df = pd.read_csv(f'{account_name} Categories Cleaned.csv')

    # Use shortened categories for the base category analysis
    dataframes = cut_category_levels(df)
    df_shortened_names = dataframes[0] # dataframe with original categories and shortened categories, used to rematch
    brand_df = dataframes[1] # dataframe with de-duplicated short categories, used for AI assistant

    # Load the Google taxonomy subcategories
    with open('taxonomy.en-US.txt', 'r') as file:
        google_categories = [(line.strip()) for line in file.readlines() if not line.startswith('#')]

    # define base categories
    google_category_parts = [line.split(' > ') for line in google_categories]
    base_categories = list(set([parts[0] for parts in google_category_parts if parts]))

    output_file = f'{account_name} Base Categories.csv'

    # Initialize the CSV file with headers (if it's a new file)
    write_to_csv(['Brand Subcategory', 'Google Base Category'], output_file)

    # Define the start index if restarting
    start_index = 0

    # Iterate over each brand subcategory starting from start_index
    for brand_category in tqdm(brand_df["Shortened Category"][start_index:],
                               total=len(brand_df["Shortened Category"][start_index:])):

        # Prepare the input string with the brand subcategory and a chunk of Google subcategories
        input_string = json.dumps({
            'brand_subcategory': brand_category,
            'google_base_category': base_categories
        })

        # Use OpenAI to find the best match for the current brand subcategory and chunk
        try:
            response = openai_request('Assistant ID', input_string)
            print(response)

            # Write each matched pair to the CSV
            for match in response:
                google_base_category_result = match.get('Google Base Category', '')
                brand_category_result = match.get('Brand Subcategory', '')
                write_to_csv([brand_category_result, google_base_category_result], output_file)

        except Exception as e:
            print(f"Error: {e}")

    # Rematch base categories to original categories
    df_base = pd.read_csv(output_file) # output from base category matching
    rematch_base_categories(df_shortened_names, df_base, f'{account_name} Categories For Step 2.csv')

if __name__ == '__main__':
    main()