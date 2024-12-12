import pandas as pd
import csv

def group_by_category(df):
    # Group by 'Group_Column' and aggregate 'Values_Column' into a list
    # Not currently using
    grouped_df = df.groupby('Brand Subcategory')['Google Subcategory'].agg(list).reset_index()

    return grouped_df

def find_sister_category(category, google_categories, original_category):
    matches = []
    # splitting Google taxonomy to count levels
    category_parts = category.split(' > ')
    category_length = len(category_parts)

    # splitting original taxonomy to count levels
    original_category_parts = original_category.split(' > ')
    original_category_length = len(original_category_parts)

    # Loop over each google category
    for google_category_name in google_categories:
        google_category_parts = google_category_name.split(' > ')
        google_length = len(google_category_parts)

        # Check if structure matches up to the second-to-last part
        if google_length == category_length and category_parts[:-1] == google_category_parts[:-1] and google_category_parts != category_parts and google_length != 1:
            matches.append(google_category_name)

    return matches, category_length, original_category_length

def check_occurrences(df, col1, col2):
    # Filter rows where items in col1 do not appear in col2
    mask = ~df[col1].isin(df[col2])
    return df[mask]

def main():
    account_name = "Brand Name"
    matched_data = pd.read_csv(f'{account_name} All Categories Matched.csv')

    # cleaning data
    matched_data = matched_data.drop_duplicates()
    matched_data = matched_data.loc[matched_data['Google Subcategory'] != 'No Match']

    # Load the Google taxonomy subcategories
    with open('taxonomy.en-US.txt', 'r') as file:
        google_categories = [(line.strip()) for line in file.readlines() if not line.startswith('#')]

    # finding similar categories of the same tier and tracking google category levels
    matched_data[['Opportunity Categories', 'Google Category Level', 'Original Category Level']] = matched_data.apply(
        lambda row: pd.Series(
            find_sister_category(row['Google Subcategory'], google_categories, row['Brand Subcategory'])),
        axis=1
    )

    # separating sister category col from list to rows
    matched_data = matched_data.explode('Opportunity Categories').reset_index(drop=True)

    # Apply the function
    final_df = check_occurrences(matched_data, 'Opportunity Categories', 'Google Subcategory')
    final_df = final_df.dropna(subset=['Opportunity Categories'])

    # print(matched_data.head())
    final_df.to_csv(f'{account_name} Opportunity Final.csv', index=False)

    # only saving unique categories
    unique_categories = final_df['Opportunity Categories'].unique()
    unique_df = pd.DataFrame(unique_categories, columns=['Unique Categories'])
    unique_df.to_csv(f'{account_name} Unique Brand Opportunity Final.csv', index=False)

if __name__ == '__main__':
    main()