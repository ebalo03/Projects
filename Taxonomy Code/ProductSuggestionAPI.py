import pandas as pd
import csv
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from bs4 import BeautifulSoup
import re
tqdm.pandas()
import ast
import time
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Paste headers and cookies here
headers = {
}

def api_call(category):
    try:
        response = requests.post(
            URL,
            headers=headers,
            data=data,
        )
        return response

    except Exception as e:
        print("Error: ", e)
        return None


# Main function that integrates Selenium and requests
def main():
    # Load the input CSV
    df = pd.read_csv('Unique Brand Opportunity Final.csv') # Replace
    df_split = pd.read_csv('US Taxonomy Split.csv') # remains constant unless language is different

    output_filename = 'Brand Suggestions JSON.csv'  # Replace

    # Merging to account for split last node
    merged_df = pd.merge(df, df_split, left_on='Unique Categories', right_on='Category', how='left')

    # Cleaning dataframe
    merged_df = merged_df.drop_duplicates(subset=['Split Category'])

    start_index = 0  # Initialize start index for looping

    # Load checkpoint if exists
    checkpoint_filename = 'checkpoint.txt'
    try:
        with open(checkpoint_filename, 'r') as checkpoint_file:
            start_index = int(checkpoint_file.read().strip())
    except FileNotFoundError:
        pass

    # Open output CSV file
    with open(output_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Split Category", "Unique Categories", "Response JSON"])

        # Iterate through categories, starting from checkpoint
        for index, row in tqdm(merged_df[start_index:].iterrows(), total=merged_df.shape[0] - start_index):
            current_index = start_index + index
            category = row['Split Category']
            unique_category = row.get('Unique Categories', '')

            response = api_call(category)

            if response and response.status_code == 200:
                data = response.text # or response.json()
                writer.writerow([category, unique_category, json.dumps(data)])

                # Save checkpoint
                with open(checkpoint_filename, 'w') as checkpoint_file:
                    checkpoint_file.write(str(current_index + 1))  # Save next index as the checkpoint
            else:
                print(
                    f"Failed to retrieve data for category '{category}' with status code {response.status_code if response else 'N/A'}")

            # Wait between requests
            time.sleep(randint(0, 1))


if __name__ == '__main__':
    main()