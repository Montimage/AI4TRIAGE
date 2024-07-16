import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder

def split_preserving_special_format(s):
    pattern = r"\[.*?\]"  # Regular expression to match any characters between [ and ]
    special_strings = re.findall(pattern, s)  # Find all matching strings
    
    # Replace specially formatted strings with placeholders to avoid splitting them
    for i, special_string in enumerate(special_strings):
        s = s.replace(special_string, f"SPECIAL{i}", 1)
        
    # Split the string using a comma as the delimiter
    split_strings = s.split(',')
    
    # Restore the placeholders to the original specially formatted strings
    for i, special_string in enumerate(special_strings):
        split_strings = [x if f"SPECIAL{i}" not in x else special_string for x in split_strings]
    return split_strings

def process_file(input_file_path, output_file_path):
    df = pd.read_csv(input_file_path, header=None)
    split_data = df[0].apply(split_preserving_special_format)
    split_df = pd.DataFrame(split_data.tolist())
    headers = split_df.iloc[0]
    split_df = split_df[1:]
    split_df.columns = headers
    missing_ratio = split_df.isnull().mean()
    threshold = 0.5
    columns_to_drop = missing_ratio[missing_ratio > threshold].index
    data_cleaned = split_df.drop(columns=columns_to_drop)
    numeric_columns = data_cleaned.select_dtypes(include=['number']).columns
    categorical_columns = data_cleaned.select_dtypes(exclude=['number']).columns
    for col in numeric_columns:
        data_cleaned[col].fillna(data_cleaned[col].median(), inplace=True)
    for col in categorical_columns:
        mode_value = data_cleaned[col].mode()[0]
        data_cleaned[col].fillna(mode_value, inplace=True)
    label_encoder = LabelEncoder()
    for col in categorical_columns:
        data_cleaned[col] = label_encoder.fit_transform(data_cleaned[col].astype(str))
    data_cleaned.to_csv(output_file_path, index=False)
    print(f"Processed file saved to: {output_file_path}")

files_to_process = [
    ('/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/anonimized_my_app_cortex_xdr (alertas xdr)_sampled .csv', '/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed1.csv'),
    ('/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/anonimized_my_app_netskope (proxy)_sampled.csv', '/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed2.csv'),
    ('/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/anonimized_my_app_proofpoint (mail)_sampled.csv', '/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed3.csv')
]

for input_file, output_file in files_to_process:
    process_file(input_file, output_file)
    
from pymongo import MongoClient

mongo_uri = "mongodb+srv://Ding:dky1995@cluster0.dnm2fcn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
database_name = "CSVdb"
collection_name = "CSVcol"

client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

file_paths = [
    "/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed1.csv",
    "/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed2.csv",
    "/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed3.csv"
]

for file_path in file_paths:
    df = pd.read_csv(file_path)
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)

print("Data inserted successfully")
