import pandas as pd
import sqlite3
import re

df_nutrition = pd.read_csv("nutrition_data.csv")
df_recipes = pd.read_csv("Food Ingredients and Recipe Dataset with Image Name Mapping.csv")

# cleaning ingredient list to match nutrition data
df_recipes = df_recipes.drop(columns=['Unnamed: 0']) # drop extra index col
df_recipes['Cleaned_Ingredients'] = df_recipes['Cleaned_Ingredients'].apply(lambda ingredient_lst: re.sub(r'\s*\(.*?\)\s*', ' ', ingredient_lst))

# connect to SQLite
conn = sqlite3.connect("Ingredients.db")

# write data to a new table
df_nutrition.to_sql("Nutrition Facts", conn, if_exists="replace", index=False)
df_recipes.to_sql("Recipes", conn, if_exists="replace", index=False)

# close the connection
conn.close()