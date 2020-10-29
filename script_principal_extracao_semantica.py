# Pipeline to open the data from the folder 'dados' and generate the results, followed by graphs

print('\n\nProcessing the categories and saving them\n')

# Processing the categories and saving them
from processing_categories_FINAL import *
print('\n\nExtracting all semantic patterns and saving them\n')

# Extracting all semantic patterns and saving them
from extract_all_semantic_patterns_FINAL import *

print('\n\nCreating graphs and saving them\n')

# Creating graphs and saving them
from graphs import *