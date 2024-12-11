# Recipe Nutrition Database

## Overview
This project aims to build a comprehensive recipe nutrition database by integrating a recipe dataset with nutritional data obtained from API requests. The primary objective is to optimize data organization and enable efficient analysis of nutritional information.

## Features
- **Recipe Dataset Integration:** Processes and organizes raw recipe data from a CSV file.
- **Nutritional Data Retrieval:** Extracts nutritional information using API requests for each recipe.
- **Database Management:** Stores the combined data in a SQLite database for easy querying and management.
- **Data Cleaning:** Ensures consistency and accuracy in the dataset by cleaning and structuring the data.

## Technologies Used
- **Programming Language:** Python
- **Database:** SQLite
- **Libraries:**
  - Pandas (for data manipulation)
  - Requests (for API interaction)

## Current Files
1. **`config.py`:** Contains configuration settings, such as API keys and endpoints.
2. **`APIExtraction.py`:** Handles the API requests to retrieve nutritional information for recipes.
3. **`DataCleaning.py`:** Cleans and preprocesses the recipe and nutritional data.
4. **`Ingredients.db`:** SQLite database file storing the processed recipe and nutritional data.
5. **`Food Ingredients and Recipe Dataset with Image Name Mapping.csv`:** Raw recipe data in CSV format.
6. **`nutrition_data.csv`:** Nutritional data retrieved from the API.

## Project Status
This project is currently in progress. Key milestones include:
1. Finalizing data cleaning procedures.
2. Enhancing the API extraction script for better error handling and efficiency.
3. Integrating the cleaned data into the SQLite database.

## How to Run
1. Clone the repository to your local machine.
2. Ensure Python and required libraries are installed.
3. Update `config.py` with your API credentials.
4. Execute `APIExtraction.py` to fetch nutritional data.
5. Run `DataCleaning.py` to clean and preprocess the data.
6. Run `csv_to_db.py` to import original data and nutrition data into SQL.
7. Query the SQLite database (`Ingredients.db`) for analysis.

---
