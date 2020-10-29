import pandas as pd



import pandas as pd

# collect data separately as lists

filename = ['filename1','filename2','filename3']
year = [2017,2016,2016]
INTER = [0,1,0]
INSER = [1,0,0]
INTRA = [0,2,0]

# join the lists in a dataframe

df = pd.DataFrame()
df ['filename'] = filename
df["year"] = year
df['INTER'] = INTER
df['INSER'] = INSER
df['INTRA']= INTRA

print(df)