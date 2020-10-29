# ll functions

import os
import re
import glob
import pandas as pd
from pandas.core.common import flatten

## FUNCTION TO EXTRACT FILENAMES FROM PATHS
##########################################
def get_filenames(paths):
    filenames = []
    for path in paths:
        path = path.split('/')[-1].split('\\')[-1]
        #path = path.split('\\')[-1]
        #print(path)
        filenames.append(os.path.splitext(path)[0])
    return(filenames)

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

## FUNCTION TO GET OUTPUT (EXCERPT OR CATEGORIES) FOR ONE DATAFRAME
###########################################
def get_output_by_index_one_df (df, column, pattern, data= 'categories', removeHeader = True):

    text = df[column].iloc[0]

    # extract everything between brackets
    full_list = re.findall(pattern, text) # Search for all brackets (and store their content)
    #print('full list: {}'.format(full_list))
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


## FUNCTION TO GET OUTPUT (EXCERPT OR CATEGORIES) FOR ONE TEXT
###########################################
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
    #print('filename: {}'.format(file_name))

    return (output_df)
#########################################

## FUNCTION TO GET OUTPUT (EXCERPT OR CATEGORIES) FOR ALL TEXTS
##########################################
def get_output_by_index_all_texts (alltexts, filenames, year_column = True , pattern='\<(.*?)\>', removeHeader = True,saveAsCSV=False):
    # empty list
    dataframe_list = []
    # creates pattern dataframes for each text
    for text_index in range(len(alltexts)):
        temp = get_output_by_index_one_text (text = alltexts[text_index],pattern = pattern, removeHeader = True, 
                        file_name = filenames[text_index])
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
    print("Complete dataframe exported as 'complete_df.csv'\n")
    return(complete_df)

##########################################


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