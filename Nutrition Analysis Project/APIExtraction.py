import csv
import pandas as pd
import re
import requests
from config import app_id, app_key
import random
import schedule
import time

def remove_parentheses(text):
    # Remove content in parentheses from ingredient column
    return re.sub(r'\s*\(.*?\)\s*', ' ', text)

def clean_ingredient_lst(data):
    all_ingredients = []

    # remove duplicates from ingredient list
    for ingredient_lst in data['Cleaned_Ingredients']:
        # convert string to list if necessary
        if isinstance(ingredient_lst, str):
            ingredient_lst = eval(ingredient_lst)

        # Loop through each ingredient in the list
        for ingredient in ingredient_lst:
            all_ingredients.append(ingredient)

    # remove duplicates
    all_ingredients = list(set(all_ingredients))

    return all_ingredients

def fetch_nutrition_data(ingredient):
    # API endpoint and parameters
    url = 'https://api.edamam.com/api/nutrition-data'
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'ingr': ingredient
    }

    # Send GET request
    response = requests.get(url, params=params)

    return response.json()

def clean_nutrition_data(ingredient, raw_data):
    # extract important info from JSON
    cleaned_data = {
        'ingredient': ingredient,
        'calories': raw_data.get('calories', 0),
        'carbs': raw_data.get('totalNutrients', {}).get('CHOCDF', {}).get('quantity', 0),
        'fiber': raw_data.get('totalNutrients', {}).get('FIBTG', {}).get('quantity', 0),
        'sugar': raw_data.get('totalNutrients', {}).get('SUGAR', {}).get('quantity', 0),
        'protein': raw_data.get('totalNutrients', {}).get('PROCNT', {}).get('quantity', 0),
        'total fat': raw_data.get('totalNutrients', {}).get('FAT', {}).get('quantity', 0),
        'trans fats': raw_data.get('totalNutrients', {}).get('FATRN', {}).get('quantity', 0),
        'saturated fats': raw_data.get('totalNutrients', {}).get('FASAT', {}).get('quantity', 0),
        'sodium': raw_data.get('totalNutrients', {}).get('NA', {}).get('quantity', 0),
        'cholesterol': raw_data.get('totalNutrients', {}).get('CHOLE', {}).get('quantity', 0),
        'CO2 Emission': raw_data.get('co2EmissionsClass', 0)

    }
    return cleaned_data

def main():
    # Importing ingredient CSV for API requests
    data = pd.read_csv('Food Ingredients and Recipe Dataset with Image Name Mapping.csv', encoding='utf-8')
    data['Cleaned_Ingredients'] = data['Cleaned_Ingredients'].apply(remove_parentheses)
    ingredient_lst = clean_ingredient_lst(data)

    # CSV for output
    output_file = 'nutrition_data.csv'
    fieldnames = ['ingredient', 'calories', 'carbs', 'fiber', 'sugar', 'protein', 'total fat', 'trans fats', 'saturated fats', 'sodium', 'cholesterol', 'CO2 Emission']

    # creating headers
    with open(output_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    # Loop through each ingredient in the list
    for ingredient in ingredient_lst[:]:
        # extracting data from API
        response = fetch_nutrition_data(ingredient)

        raw_data = response
        cleaned_data = clean_nutrition_data(ingredient, raw_data)

        # save data
        with open(output_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(cleaned_data)

if __name__ == '__main__':
    main()

