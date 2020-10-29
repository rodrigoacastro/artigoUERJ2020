# This script reads the tagged texts from the years 2015, 2016, 2017 and 2018 
# and extracts their categories per text and per year

import os
import re
import glob
import pandas as pd
from pandas.core.common import flatten

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


def get_filenames(paths):
    filenames = []
    for path in paths:
        path = path.split('/')[-1].split('\\')[-1]
        #path = path.split('\\')[-1]
        #print(path)
        filenames.append(os.path.splitext(path)[0])
    return(filenames)

# collecting filenames
filenames2015 = get_filenames(paths2015)
filenames2016 = get_filenames(paths2016)
filenames2017 = get_filenames(paths2017)
filenames2018 = get_filenames(paths2018)

all_filenames = filenames2015 + filenames2016 + filenames2017 + filenames2018
#print('all_filenames: {}'.format(all_filenames))


# saves all filenames in a single file

with open('AllFiles.txt', 'w') as filehandle:
    for listitem in all_filenames:
        filehandle.write('%s\n' % listitem)
    filehandle.write('\n') # linebreak

# Saves all filenames per year in 'AllFilesPerYear.txt'

with open('AllFilesPerYear.txt', 'w') as filehandle:
    filehandle.write('Textos 2015\n')
    for listitem in filenames2015:
        filehandle.write('%s\n' % listitem)
    filehandle.write('\n') # linebreak

    filehandle.write('Textos 2016\n')
    for listitem in filenames2016:
        filehandle.write('%s\n' % listitem)
    filehandle.write('\n') # linebreak

    filehandle.write('Textos 2017\n')
    for listitem in filenames2017:
        filehandle.write('%s\n' % listitem)
    filehandle.write('\n') # linebreak

    filehandle.write('Textos 2018\n')
    for listitem in filenames2018:
        filehandle.write('%s\n' % listitem)
    filehandle.write('\n') # linebreak
    
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

print('Textos: ')
# print('\n', all_texts, '\n')

print('Numero de textos: ')
#print(len(all_texts), '\n')

#### FUNCTION TO MAKE REGEX LIST BASED ON REGEX AND LIST
##############################################################################################
def regex_list_maker (regex, work_list):
    new_list = []
    for item in work_list:
        new_list.append(regex.format(item))
    return(new_list)
##############################################################################################


## FUNCTION TO COLLECT INFO FROM ALL TEXTS
###########################################
def collect_info_regex (regex, text_list):
    new_list = []

    for text in all_texts:
        match_type = re.findall(regex, text) 
        #print('match_type before if = {}'.format(match_type))
        if len (match_type) > 0:
        #if match_type != '':
            # print('type between brackets')
            new_list.append(match_type)
            #print('match_type after if = {}'.format(match_type))
    return (new_list)   
###########################################


## FUNCTION TO COUNT CATEGORIES ALL TEXTS
###########################################

def count_category_regex (category, text_list, filenames):
    new_list = []
    #count = 0
    counts = []

    for text in text_list:
       count = text.count(category)
       counts.append(count)
      
    # save results as dataframe
    result = pd.DataFrame()
    result ['filename'] = filenames
    result["count"] = counts    
    
    return(result)

######################################################

## FUNCTION TO MAKE REGEX WITH A BASE AND A CATEGORY
##########################################
def regex_maker(category_name, regex_base):
    regex_base = '\<.*\>(?=\<({})\>)'
    output = regex_base.format(category_name)
    return(output)
##########################################
#regex_base = '\<.*\>(?=\<({})\>)'

regex_INTER = regex_maker (category_name = 'INTER', regex_base = '\<(.*)\>(?=\<({})\>)')

regex_INSER = regex_maker (category_name = 'INSER', regex_base = '\<(.*)\>(?=\<({})\>)')

regex_INTRA = regex_maker (category_name = 'INTRA', regex_base = '\<.*\>(?=\<({})\>)')

# applying function

#result_INTER = count_category_regex2 (regex = regex_INTER, text_list = all_texts, filenames = all_filenames)
result_INTER = count_category_regex (category = 'INTER', text_list = all_texts, filenames = all_filenames)
# print(result_INTER)

result_INSER = count_category_regex (category = 'INSER', text_list = all_texts, filenames = all_filenames)
# print(result_INSER)

result_INTRA = count_category_regex (category = 'INTRA', text_list = all_texts, filenames = all_filenames)
# print(result_INTRA)



# collecting text type
#   extract text type between brackets (in the regex group) - pattern < ---- Type ---->

regex_type = '\<\s?-+\s?(.*?)\s?-+\s?\>'

text_types = collect_info_regex (regex = regex_type, text_list = all_texts)
text_types = list(flatten(text_types))
# print(text_types)

# collecting year
#   extract year between brackets (in the regex group) - pattern <(.*) year (.*) ->

# REGEX_LIST OF YEARS
years = [2015, 2016, 2017, 2018]
match_year = '\<.*?({}).*?\>'

year_regex_list = regex_list_maker (regex = match_year, work_list = years)
print('year_regex_list = {}'.format(year_regex_list))
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

all_years = list(flatten(all_years))
#print('all_years = {}'.format(all_years))



###### CREATING FINAL DATAFRAME


df = pd.DataFrame()
df ['filename'] = all_filenames
df["year"] = all_years
df['type'] = text_types
df['INTER'] = result_INTER['count']
df['INSER'] = result_INSER['count']
df['INTRA']= result_INTRA['count']

print(df)

# save_final df as csv

df.to_csv("dataframe_counts.csv",index=False)

# counting data per year
df_per_year = pd.DataFrame(df.groupby(by='year',sort=False).sum()).reset_index()
df_per_year['total'] = df['INTER'] + df['INSER'] + df['INTRA']
print(df_per_year)
df_per_year.to_csv('df_per_year.csv',index=False)

# counting relative frequency per year

df_per_year_rel_freq = pd.DataFrame(df.groupby(by='year',sort=False).sum())
df_per_year_rel_freq['total'] = df_per_year_rel_freq['INTER'] + df_per_year_rel_freq['INSER'] + df_per_year_rel_freq['INTRA']
#df_per_year_rel_freq = df_per_year_rel_freq / df_per_year_rel_freq['total']
#print(df_per_year_rel_freq.select_dtypes(include=['int64']))
df_per_year_rel_freq['INTER'] = round (100* (df_per_year_rel_freq['INTER'] / df_per_year_rel_freq['total']),2)
df_per_year_rel_freq['INSER'] = round (100* (df_per_year_rel_freq['INSER'] / df_per_year_rel_freq['total']),2)
df_per_year_rel_freq['INTRA'] = round (100* (df_per_year_rel_freq['INTRA'] / df_per_year_rel_freq['total']),2)
df_per_year_rel_freq['total'] = round (100* (df_per_year_rel_freq['total'] / df_per_year_rel_freq['total']),2)

df_per_year_rel_freq.reset_index(inplace=True)

print(df_per_year_rel_freq)


# exporting file as csv
df_per_year_rel_freq.to_csv('df_per_year_rel_freq.csv',index=False)


##### THE END


# THE ONLY THING MISSING WAS EXTRACTING THE CATEGORIES TO A FILE OR DATAFRAME/SPREADSHEET
# This is done in extract_all_semantic_patterns.py