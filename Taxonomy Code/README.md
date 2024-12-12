# Taxonomy Cleaning and Category Matching

This repository contains Python scripts for processing and refining brand taxonomy files to align with Google's taxonomy. The workflow is divided into multiple steps, each of which addresses a specific aspect of the taxonomy cleaning and matching process.

## File Descriptions

### 1. `OriginalTaxonomyCleaning.py`
- **Purpose**: Formats the brand taxonomy file to align with Google’s taxonomy structure.

---

### 2. `step1_BaseCategory.py`
- **Purpose**: 
  - Shortens the category name and matches it to potential base categories from Google’s taxonomy.
  - Maps the shortened categories and their corresponding base categories to the full category names from the original data.

---

### 3. `step2_CategoryMatch.py`
- **Purpose**: Matches a category against a filtered portion of Google’s taxonomy based on the base category identified in Step 1.

---

### 4. `step3_FindCategoryOpportunity.py`
- **Purpose**: Identifies adjacent subcategories related to the matched categories.
- **Outputs**: 
  - **Brand Opportunity Final**: Contains the output from Step 2 along with all opportunity categories.
  - **Unique Brand Opportunity Final**: A deduplicated list of opportunity categories.

---

### 5. `ProductSuggestionAPI.py`
- **Purpose**: 
  - Validates potential categories by querying the company’s search API.
  - Checks if products in the suggested categories are available on the website.

## Usage
1. Start with `OriginalTaxonomyCleaning.py` to standardize the brand taxonomy file.
2. Use `step1_BaseCategory.py` to identify base categories and map them to the full category names.
3. Execute `step2_CategoryMatch.py` to refine category matches using Google’s taxonomy.
4. Run `step3_FindCategoryOpportunity.py` to explore additional subcategory opportunities.
5. Finally, use `ProductSuggestionAPI.py` to verify category suggestions by checking for product availability.

## Requirements
- Python 3.x
- Required Python libraries (install via `requirements.txt` if available)
- API credentials (if applicable for `ProductSuggestionAPI.py`)

## Outputs
- Refined taxonomy files
- Finalized category matches
- Brand opportunity reports (both comprehensive and deduplicated)

## Contributing
Feel free to open an issue or submit a pull request for enhancements or bug fixes. Ensure that your code is well-documented and adheres to the project’s coding standards.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
