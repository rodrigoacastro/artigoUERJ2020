# This script reads the tagged texts from the years 2015, 2016, 2017 and 2018 
# and extracts their categories per text

import os
import re
import glob
import pandas as pd

# import all functions from all_functions.py
from all_functions import *

# collecting file paths
paths2015 = glob.glob("dados/2015/*.txt")
paths2016 = glob.glob("dados/2016/*.txt")
paths2017 = glob.glob("dados/2017/*.txt")
paths2018 = glob.glob("dados/2018/*.txt")

# join all paths in a new list

all_paths = paths2015 +  paths2016 + paths2017 + paths2018
#print('all paths: {}\n\n'.format(all_paths))

# extract all paths in a folder without .txt
#documents = [f[:-4] for f in os.listdir() if f[-4:] == '.txt']
documents2015 = [f[:-4] for f in paths2015 if f[-4:] == '.txt']
documents2016 = [f[:-4] for f in paths2016 if f[-4:] == '.txt']
documents2017 = [f[:-4] for f in paths2017 if f[-4:] == '.txt']
documents2018 = [f[:-4] for f in paths2018 if f[-4:] == '.txt']

# join lists

documents = documents2015 +  documents2016 + documents2017 + documents2018
# print('all documents: {}'.format(documents))

# collecting filenames
filenames2015 = get_filenames(paths2015)
filenames2016 = get_filenames(paths2016)
filenames2017 = get_filenames(paths2017)
filenames2018 = get_filenames(paths2018)

all_filenames = filenames2015 + filenames2016 + filenames2017 + filenames2018
# print('all_filenames: {}'.format(all_filenames))


# read texts from files and store in a list

# define empty list
all_texts = []
print('\n\nall_texts created\n')

# open file and read the content in a list (one text equals one string)
for path in all_paths:

    # files are encoded as UTF-8 BOM (if UTF-8, use 'utf-8' as encoding)
    with open(path, 'r', encoding='utf-8-sig') as filehandle:
        current_text = filehandle.read().replace("\n", " ")

        # add item to the list
        all_texts.append(current_text)

#print('Textos: ')
#print('\n', all_texts, '\n')

print('Total number of texts: ')
print(len(all_texts), '\n')

new_df = pd.DataFrame()
new_df['filename'] = all_filenames
new_df['text'] = all_texts

#print(new_df.head())

# collecting year
#   extract year between brackets (in the regex group) - pattern <(.*) year (.*) ->

# REGEX_LIST OF YEARS
years = [2015, 2016, 2017, 2018]
match_year = '\<.*?({}).*?\>'

year_regex_list = regex_list_maker (regex = match_year, work_list = years)
#print('year_regex_list = {}'.format(year_regex_list))

# regex: \<.*?(2015).*?\>
# regex: \<.*?(2016).*?\>
# regex: \<.*?(2017).*?\>
# regex: \<.*?(2018).*?\>


# loop to take data from all years (2015, 2016, 2017, 2018)
all_years = []
for regex in year_regex_list:
    # print('regex = {}'.format(regex))
    temp = collect_info_regex (regex = regex, text_list = all_texts)
    #print('temp = {}'.format(temp))
    if len(temp) > 0:
        all_years.append(temp)

all_years = [item for sublist in all_years for item in sublist]

# fixing years coming in lists instead of numbers
for item in range(len(all_years)):
    all_years[item] = all_years[item][0]
#print('all_years = {}'.format(all_years))

###############################################


regex_INTER = regex_maker (category_name = 'INTER', regex_base = '(\<.*\>)?=\<({})\>')

regex_SENT = regex_maker (category_name = 'SENT', regex_base = '\<(.*)\>(?=\<({})\>)')

regex_INTRA = regex_maker (category_name = 'INTRA', regex_base = '\<.*\>(?=\<({})\>)')
#################################################

# applying

# patterns_df = get_output_by_index_one_df (df = new_df2, column = 'text',pattern = '\<(.*?)\>', removeHeader = True)
# print('patterns_df: \n')
# print(patterns_df)

###############################################

patterns_text = get_output_by_index_one_text (text = all_texts[2],pattern = '\<(.*?)\>', removeHeader = True, 
                    file_name = all_filenames[2])
#print('patterns_text: \n')
#print(patterns_text)


###################################

get_output_by_index_all_texts (alltexts = all_texts, pattern = '\<(.*?)\>', filenames = all_filenames, 
                    year_column = True,removeHeader = True, saveAsCSV=True)

#################################################################################