import pandas as pd
from pymongo import MongoClient

# MongoDB connection details
mongo_uri = "mongodb+srv://Ding:dky1995@cluster0.dnm2fcn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
database_name = "CSVdb"
collection_name = "CSVcol"

# Connect to MongoDB
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

# File paths
file_paths = [
    "/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed1.csv",
    "/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed2.csv",
    "/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed3.csv"
]

# Iterate over file paths, read each CSV, and insert into MongoDB
for file_path in file_paths:
    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Remove _id column if it exists to avoid duplicate key errors
    if '_id' in df.columns:
        df = df.drop(columns=['_id'])
    
    # Convert DataFrame to dictionary
    data_dict = df.to_dict("records")
    
    # Insert data into MongoDB collection
    collection.insert_many(data_dict)

print("Data inserted successfully")
