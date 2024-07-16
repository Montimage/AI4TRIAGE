import pandas as pd
df=pd.read_csv('/home/ubuntu/Ai4Triage_intern/String_to_number/Data.csv')
# Importing LabelEncoder from Sklearn 
# library from preprocessing Module.
from sklearn.preprocessing import LabelEncoder
# Creating a instance of label Encoder.
le = LabelEncoder()
# Using .fit_transform function to fit label
# encoder and return encoded label
label = le.fit_transform(df['Purchased'])
# removing the column 'Purchased' from df
# as it is of no use now.
df.drop("Purchased", axis=1, inplace=True)
 
# Appending the array to our dataFrame 
# with column name 'Purchased'
df["Purchased"] = label
 
# printing Dataframe
print(df)