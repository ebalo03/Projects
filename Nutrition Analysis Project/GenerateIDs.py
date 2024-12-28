import pandas as pd
import re

# Load CSVs
recipes_df = pd.read_csv('Food Ingredients and Recipe Dataset with Image Name Mapping Original.csv')
ingredients_df = pd.read_csv('nutrition_data.csv')

# Cleaning functions from APIExtraction.py
def remove_parentheses(text):
    # Remove content in parentheses from ingredient column
    return re.sub(r'\s*\(.*?\)\s*', ' ', text).strip()

def clean_ingredient_lst(data):
    all_ingredients = []

    # remove duplicates from ingredient list
    for ingredient_lst in data['Cleaned_Ingredients']:
        # convert string to list if necessary
        if isinstance(ingredient_lst, str):
            ingredient_lst = eval(ingredient_lst)

        # Loop through each ingredient in the list
        for ingredient in ingredient_lst:
            # Clean the ingredient
            clean_ingredient = remove_parentheses(ingredient)
            all_ingredients.append(clean_ingredient)

    # remove duplicates
    all_ingredients = list(set(all_ingredients))
    return all_ingredients

# Add Recipe_ID and Ingredient_ID to recipes dataset
recipes_df['Recipe_ID'] = range(1, len(recipes_df) + 1)
ingredients_df['Ingredient_ID'] = range(1, len(ingredients_df) + 1)

# Apply cleaning methods to ingredient list of recipe data
recipes_df['Ingredients_List'] = recipes_df['Cleaned_Ingredients'].apply(
    lambda x: [remove_parentheses(ingredient) for ingredient in eval(x)] if isinstance(x, str) else []
)

# Expand/explode ingredients for mapping
exploded_recipes = recipes_df.explode('Ingredients_List')
exploded_recipes = exploded_recipes[['Recipe_ID', 'Ingredients_List']]

# Creating a mapping of Recipe_ID and Ingredient_ID
mapping_table = exploded_recipes.merge(
    ingredients_df[['ingredient', 'Ingredient_ID']],
    left_on='Ingredients_List',
    right_on='ingredient',
    how='inner'
)[['Recipe_ID', 'Ingredient_ID']]

# Group all Recipe_IDs associated with each ingredient into a list
ingredient_to_recipes = mapping_table.groupby('Ingredient_ID')['Recipe_ID'].apply(list).reset_index()

# Merge the Recipe_ID list back into ingredients_df
# Each ingredient will be matched to all recipes it's included in
ingredients_df = ingredients_df.merge(
    ingredient_to_recipes,
    on='Ingredient_ID',
    how='left'
)

# Dropping unnecessary columns
recipes_df = recipes_df.drop(columns=['Ingredients_List', 'Unnamed: 0'])
ingredients_df = ingredients_df.explode('Recipe_ID')

# Save updated datasets
mapping_table.to_csv('recipe_ingredient_mapping.csv', index=False)
recipes_df.to_csv('updated_recipes.csv', index=False)
ingredients_df.to_csv('updated_ingredients.csv', index=False)
