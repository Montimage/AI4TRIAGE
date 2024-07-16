import pandas as pd
import re # regular expression
# Regular expressions are powerful tools used to match and manipulate specific patterns in strings. By importing the re module, you can use regular expressions to search, replace, split, and process strings.
from sklearn.preprocessing import LabelEncoder

def split_preserving_special_format(s):
    """
    Split the string while preserving specially formatted strings.
    Specially formatted strings are those enclosed in square brackets.
    """
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
    # Read the CSV file without header
    df = pd.read_csv(input_file_path, header=None)

    # Apply the splitting function to the data
    split_data = df[0].apply(split_preserving_special_format)  # Apply splitting function to the first column

    # Convert the split data into a DataFrame
    split_df = pd.DataFrame(split_data.tolist())  # Convert Series to DataFrame

    # Calculate the missing value ratio for each column
    missing_ratio = split_df.isnull().mean()  # Calculate the missing value ratio (NAN)

    # Determine the threshold for dropping columns with majority missing values
    threshold = 0.5  # Set threshold to 50%
    columns_to_drop = missing_ratio[missing_ratio > threshold].index  # Find columns with missing ratio exceeding the threshold

    # Drop these columns
    data_cleaned = split_df.drop(columns=columns_to_drop)  # Drop these columns

    # Identify numeric and categorical columns in the remaining columns
    numeric_columns = data_cleaned.select_dtypes(include=['number']).columns  # Find numeric columns
    categorical_columns = data_cleaned.select_dtypes(exclude=['number']).columns  # Find categorical columns

    # Fill missing values in numeric columns with median
    for col in numeric_columns:
        data_cleaned[col].fillna(data_cleaned[col].median(), inplace=True)  # Fill with median

    # Fill missing values in categorical columns with mode
    for col in categorical_columns:
        mode_value = data_cleaned[col].mode()[0]  # Calculate mode
        data_cleaned[col].fillna(mode_value, inplace=True)  # Fill with mode

    # Apply label encoding
    label_encoder = LabelEncoder()  # Create LabelEncoder instance
    for col in categorical_columns:
        data_cleaned[col] = label_encoder.fit_transform(data_cleaned[col].astype(str))  # Apply label encoding to categorical columns
        
    # Set column names
    data_cleaned.columns = split_df.iloc[0,:] 

    # Save the processed DataFrame to a CSV file
    data_cleaned.to_csv(output_file_path, index=False)  # Save to CSV without index

    # Print the output file path
    print(f"Processed file saved to: {output_file_path}")

# Process the first file
process_file('/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/anonimized_my_app_cortex_xdr (alertas xdr)_sampled .csv', 
             '/home/ubuntu/Ai4Triage_intern/CSVfile/csv1-3small/processed_data.csv')
