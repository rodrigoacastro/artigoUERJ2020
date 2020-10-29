# This script reads the tagged texts from the years 2015, 2016, 2017 and 2018 
# and extracts their categories per text

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

from all_functions import *

""" 
def get_filenames(paths):
    filenames = []
    for path in paths:
        path = path.split('/')[-1].split('\\')[-1]
        #path = path.split('\\')[-1]
        #print(path)
        filenames.append(os.path.splitext(path)[0])
    return(filenames)
 """
# collecting filenames
filenames2015 = get_filenames(paths2015)
filenames2016 = get_filenames(paths2016)
filenames2017 = get_filenames(paths2017)
filenames2018 = get_filenames(paths2018)

all_filenames = filenames2015 + filenames2016 + filenames2017 + filenames2018
print('all_filenames: {}'.format(all_filenames))


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
#print('\n', all_texts, '\n')

print('Numero de textos: ')
print(len(all_texts), '\n')

new_df = pd.DataFrame()
new_df['filename'] = all_filenames
new_df['text'] = all_texts

#print(new_df.head())

# collecting year
#   extract year between brackets (in the regex group) - pattern <(.*) year (.*) ->

## FUNCTION TO MAKE REGEX WITH A BASE AND A CATEGORY
##########################################
def regex_maker(category_name, regex_base):
    regex_base = '\<.*\>(?=\<({})\>)'
    output = regex_base.format(category_name)
    return(output)
##########################################

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

    for text in text_list:
        match_type = re.findall(regex, text) 
        #print('match_type before if = {}'.format(match_type))
        if len (match_type) > 0:
        #if match_type != '':
            # print('type between brackets')
            new_list.append(match_type)
            #print('match_type after if = {}'.format(match_type))
    return (new_list)   
###########################################

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

###############################################


regex_INTER = regex_maker (category_name = 'INTER', regex_base = '(\<.*\>)?=\<({})\>')

regex_INSER = regex_maker (category_name = 'INSER', regex_base = '\<(.*)\>(?=\<({})\>)')

regex_INTRA = regex_maker (category_name = 'INTRA', regex_base = '\<.*\>(?=\<({})\>)')
#################################################


## FUNCTION TO GET OUTPUT (EXCERPT OR CATEGORIES) FROM PATTERNS
###########################################
def get_output_by_index (patterns,data= 'categories'):
    # data = patterns or categories
     
    if data == 'excerpts':
        # even numbers pair index
        pair_index = list(range(0,len(patterns),2))
    elif data == 'categories':
        # odd numbers pair index
        pair_index = list(range(1,len(patterns),2))
    else:
        print("The argument data must be equal to 'excerpts' or 'categories'\n") 

    a = patterns
    b = pair_index

    # extract output patterns
    output = [ a[i] for i in b]
    return(output)

####################################################

#text_excerpts = get_excerpts_by_index(patterns=relevant_patterns)

###############################################

def get_output_by_index_one_df (df, column, pattern, data= 'categories', removeHeader = True):

    text = df[column].iloc[0]

    # extract everything between brackets
    full_list = re.findall(pattern, text) # Search for all brackets (and store their content)
    print('full list: {}'.format(full_list))
    # remove headers
    if removeHeader == True:
        relevant_patterns = full_list[3:]
        print('relevant_patterns: {}'.format(relevant_patterns))
    elif removeHeader == False:
        relevant_patterns = full_list
        print('relevant_patterns: {}'.format(relevant_patterns))

    else:
        print('The argument removeHeader must be True or False.')

    # extract excerpts
    even_index = list(range(0,len(relevant_patterns),2))
    print('even_index: {}'.format(even_index))

    output_excerpts = [ relevant_patterns[i] for i in even_index]
    print('output excerpts: {}'.format(output_excerpts))

    # extract categories
    odd_index = list(range(1,len(relevant_patterns),2))
    print('odd_index: {}'.format(odd_index))

    output_categories = [ relevant_patterns[i] for i in odd_index]
    print('output categories: {}'.format(output_categories))

    # output
    output_df = pd.DataFrame()
    output_df['excerpt'] = output_excerpts
    output_df['categories'] = output_categories

    return (output_df)
#########################################

# applying

# patterns_df = get_output_by_index_one_df (df = new_df2, column = 'text',pattern = '\<(.*?)\>', removeHeader = True)
# print('patterns_df: \n')
# print(patterns_df)

###############################################

###############################################

def get_output_by_index_one_text (text, pattern, data= 'categories', removeHeader = True, file_name = 'filename'):

    # check if the argument text is a string
    if not isinstance(text, str):
        print('The argument text must be a string')

    # extract everything between brackets
    full_list = re.findall(pattern, text) # Search for all brackets (and store their content)
    # print('full list: {}'.format(full_list))
    # remove headers
    if removeHeader == True:
        relevant_patterns = full_list[3:]
        # print('relevant_patterns: {}'.format(relevant_patterns))
    elif removeHeader == False:
        relevant_patterns = full_list
        # print('relevant_patterns: {}'.format(relevant_patterns))

    else:
        print('The argument removeHeader must be True or False.')

    # extract excerpts
    even_index = list(range(0,len(relevant_patterns),2))
    # print('even_index: {}'.format(even_index))

    output_excerpts = [ relevant_patterns[i] for i in even_index]
    # print('output excerpts: {}'.format(output_excerpts))

    # extract categories
    odd_index = list(range(1,len(relevant_patterns),2))
    # print('odd_index: {}'.format(odd_index))

    output_categories = [ relevant_patterns[i] for i in odd_index]
    # print('output categories: {}'.format(output_categories))

    # output
    output_df = pd.DataFrame()
    output_df['filename'] = [file_name] * len(output_categories)
    output_df['excerpt'] = output_excerpts
    output_df['categories'] = output_categories
    print('filename: {}'.format(file_name))

    return (output_df)
#########################################

patterns_text = get_output_by_index_one_text (text = all_texts[2],pattern = '\<(.*?)\>', removeHeader = True, 
                    file_name = all_filenames[2])
print('patterns_text: \n')
print(patterns_text)


###################################
dataframe_list = []
for text_index in range(len(all_texts)):
    temp = get_output_by_index_one_text (text = all_texts[text_index],pattern = '\<(.*?)\>', removeHeader = True, 
                    file_name = all_filenames[text_index])
    dataframe_list.append(temp)

text_pattern = pd.concat (dataframe_list)
print(text_pattern)

##########################################
def get_output_by_index_all_texts (alltexts, filenames, year_column = True , pattern='\<(.*?)\>', removeHeader = True,saveAsCSV=False):
    # empty list
    dataframe_list = []
    # creates pattern dataframes for each text
    for text_index in range(len(alltexts)):
        temp = get_output_by_index_one_text (text = alltexts[text_index],pattern = pattern, removeHeader = True, 
                        file_name = all_filenames[text_index])
        # collect them in a list
        dataframe_list.append(temp)

        # concatenate them together
        text_pattern = pd.concat (dataframe_list)

        # if year_column is requested, the calculations are done to include it in the dataframe
        if year_column == True:

        # create dataframe with filenames and years: df_filenames_years

            years = []

           # REGEX_LIST OF YEARS
            available_years = [2015, 2016, 2017, 2018]
            match_year = '\<.*?({}).*?\>'

            year_regex_list = regex_list_maker (regex = match_year, work_list = available_years)

            for regex in year_regex_list:
                #print('regex = {}'.format(regex))
                temp = collect_info_regex (regex = regex, text_list = alltexts)
                #print('temp = {}'.format(temp))
                if len(temp) > 0:
                    years.append(temp)

            years = list(flatten(years)) 
 
    df_filenames_years = pd.DataFrame()
    df_filenames_years['filename'] = filenames
    df_filenames_years['year'] = years
        
    # joining text_patterns with df_filenames_years to make a more complete dataframe
    complete_df = pd.merge(left=text_pattern, right=df_filenames_years, how='left', 
                            left_on='filename', right_on='filename')
    # set column names                        
    complete_df.columns = ['filename','excerpt','category','year']
    #print(complete_df)  
    # set column order
    complete_df = complete_df[['filename','year','excerpt','category']]                      

    if saveAsCSV:
        complete_df.to_csv('complete_df.csv', index = False, sep='|')

    #return (text_pattern)
    return(complete_df)

##########################################

#get_output_by_index_all_texts (alltexts = all_texts, pattern = '\<(.*?)\>', filenames = all_filenames, 
#                    removeHeader = True, saveAsCSV=False)

get_output_by_index_all_texts (alltexts = all_texts, pattern = '\<(.*?)\>', filenames = all_filenames, 
                    year_column = True,removeHeader = True, saveAsCSV=True)