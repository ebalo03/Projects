import pandas as pd
import sqlite3

df_nutrition = pd.read_csv("updated_ingredients.csv")
df_recipes = pd.read_csv("updated_recipes.csv")

# connect to SQLite
conn = sqlite3.connect("Ingredients.db")

# write data to a new table
df_nutrition.to_sql("Nutrition Facts", conn, if_exists="replace", index=False)
df_recipes.to_sql("Recipes", conn, if_exists="replace", index=False)

# close the connection
conn.close()
