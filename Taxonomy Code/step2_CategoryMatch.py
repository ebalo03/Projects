import time
import json
from openai import OpenAI
import pandas as pd
from tqdm import tqdm
import csv
import ast
import os

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

def save_progress(progress_file, index):
    with open(progress_file, 'w') as file:
        file.write(str(index))

def load_progress(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as file:
            return int(file.read().strip())
    return 0

def main():
    # Load the brand subcategories CSV
    account_name = 'Brand'
    base_category_df = pd.read_csv(f'{account_name} Categories For Step 2.csv')
    base_category_df = base_category_df.loc[base_category_df['Google Base Category'] != 'No Match']

    # Load the Google taxonomy subcategories
    with open('taxonomy.en-US.txt', 'r') as file:
        google_categories = [(line.strip()) for line in file.readlines() if not line.startswith('#')]

    output_file = f'{account_name} All Categories Matched.csv'
    progress_file = f'{account_name} progress.txt'
    max_retries = 3

    # Initialize the CSV file with headers (if it's a new file)
    # write_to_csv(['Brand Subcategory', 'Google Subcategory'], output_file)

    # Group Google categories by base category
    category_hierarchy = {}
    for line in google_categories:
        parts = line.split(' > ')
        base = parts[0]
        if base not in category_hierarchy:
            category_hierarchy[base] = []
        category_hierarchy[base].append(line)

    # Load the last processed index
    start_index = load_progress(progress_file)

    # Iterate over each brand subcategory starting from the saved index
    for idx, (brand_category, base_categories) in enumerate(
        tqdm(base_category_df[["Full Category", "Google Base Category"]].iloc[start_index:].values,
             total=len(base_category_df) - start_index),
        start=start_index):

        # Ensure base categories is a list
        base_categories = ast.literal_eval(base_categories)

        google_subcategories = []
        for base_category in base_categories:
            # Collect Google subcategories for each base category in the list
            google_subcategories.extend(category_hierarchy.get(base_category, []))

        # Skip if there are no matching Google subcategories
        if not google_subcategories:
            print(f"No Google subcategories found for base categories: {base_categories}")
            continue

        # Prepare the input string with the brand subcategory and filtered Google subcategories
        input_string = json.dumps({
            'brand_subcategory': brand_category,
            'base_category': base_categories,
            'google_subcategories': google_subcategories
        })

        # Retry loop for making requests
        for attempt in range(max_retries):
            try:
                response = openai_request('Assistant ID', input_string)

                # Write each matched pair to the CSV
                for match in response:
                    google_category_result = match.get('Google Subcategory', '')
                    brand_category_result = match.get('Brand Subcategory', '')
                    write_to_csv([brand_category_result, google_category_result], output_file)

                # Save progress after success
                save_progress(progress_file, idx)
                # Break out of the retry loop on success
                break

            except Exception as e:
                print(f"No match found for {brand_category} on attempt {attempt + 1}. Error: {e}")

                # If the last attempt fails, log "not found"
                if attempt == max_retries - 1:
                    print(f"Max retries reached. Logging 'not found' for {brand_category}.")
                    write_to_csv([brand_category, "not found", "not found"], output_file)
                    # Save progress after a failure
                    save_progress(progress_file, idx)

if __name__ == '__main__':
    main()