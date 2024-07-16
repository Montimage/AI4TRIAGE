import pandas as pd 
df=pd.read_csv('/home/ubuntu/Ai4Triage_intern/String_to_number/Data.csv')
# using .get_dummies function to convert
# the categorical datatype to numerical 
# and storing the returned dataFrame
# in a new variable df1
df1 = pd.get_dummies(df['Purchased'])

# using pd.concat to concatenate the dataframes 
# df and df1 and storing the concatenated 
# dataFrame in df.
df = pd.concat([df, df1], axis=1).reindex(df.index)

# removing the column 'Purchased' from df 
# as it is of no use now.
df.drop('Purchased', axis=1, inplace=True)

# printing df
print(df)
