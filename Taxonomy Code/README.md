# Taxonomy Cleaning and Category Matching

This repository contains Python scripts for processing and refining brand taxonomy files to align with Google's taxonomy. The workflow is divided into multiple steps, each of which addresses a specific aspect of the taxonomy cleaning and matching process. The goal is to find category opportunities for retailers.

## File Descriptions

### 1. `step1_BaseCategory.py`
- **Purpose**: 
  - Shortens the category name and matches it to potential base categories from Google’s taxonomy.
  - Maps the shortened categories and their corresponding base categories to the full category names from the original data.

---

### 2. `step2_CategoryMatch.py`
- **Purpose**: Matches a category against a filtered portion of Google’s taxonomy based on the base category identified in Step 1.

---

### 3. `step3_FindCategoryOpportunity.py`
- **Purpose**: Identifies adjacent subcategories related to the matched categories.
- **Outputs**: 
  - **Brand Opportunity Final**: Contains the output from Step 2 along with all opportunity categories.
  - **Unique Brand Opportunity Final**: A deduplicated list of opportunity categories.

---

### 4. `ProductSuggestionAPI.py`
- **Purpose**: 
  - Validates potential categories by querying the company’s search API.
  - Checks if products in the suggested categories are available on the website.

## Usage
1. Use `step1_BaseCategory.py` to identify base categories and map them to the full category names.
2. Execute `step2_CategoryMatch.py` to refine category matches using Google’s taxonomy.
3. Run `step3_FindCategoryOpportunity.py` to explore additional subcategory opportunities.
4. Finally, use `ProductSuggestionAPI.py` to verify category suggestions by checking for product availability.

## Outputs
- Refined taxonomy files
- Finalized category matches
- Brand opportunity reports (both comprehensive and deduplicated)

