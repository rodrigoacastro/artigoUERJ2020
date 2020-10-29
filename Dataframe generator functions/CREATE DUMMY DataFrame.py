# CREATE DUMMY DataFrame

# https://erikrood.com/Python_References/change_order_dataframe_columns_final.html

import pandas as pd
import numpy as np


raw_data = {'name': ['Willard Morris', 'Al Jennings', 'Omar Mullins', 'Spencer McDaniel'],
        'age': [20, 19, 22, 21],
        'favorite_color': ['blue', 'red', 'yellow', "green"],
        'grade': [88, 92, 95, 70]}
df = pd.DataFrame(raw_data, index = ['Willard Morris', 'Al Jennings', 'Omar Mullins', 'Spencer McDaniel'])
df

# change order of the columns

#now 'age' will appear at the end of our df
df = df[['favorite_color','grade','name','age']]
df.head()