import pandas as pd
import re

def split_preserving_special_format(s):
    pattern = r"\[.*?\]"
    special_strings = re.findall(pattern, s)
    for i, special_string in enumerate(special_strings):
        s = s.replace(special_string, f"SPECIAL{i}", 1)
    split_strings = s.split(',')
    for i, special_string in enumerate(special_strings):
        split_strings = [x if f"SPECIAL{i}" not in x else special_string for x in split_strings]
    return split_strings

def process_csv(input_file, output_file):
    df = pd.read_csv(input_file, header=None)
    split_data = df[0].apply(split_preserving_special_format)
    split_df = pd.DataFrame(split_data.tolist())
    split_df.to_csv(output_file, index=False)
    return output_file

# File paths and output paths
files_to_process = [
    ('/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/anonimized_my_app_cortex_xdr (alertas xdr)_sampled .csv', '/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/organized1.csv'),
    ('/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/anonimized_my_app_netskope (proxy)_sampled.csv', '/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/organized2.csv'),
    ('/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/anonimized_my_app_proofpoint (mail)_sampled.csv', '/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/organized3.csv')
]

# Process all files
processed_files = []
for input_file, output_file in files_to_process:
    processed_file = process_csv(input_file, output_file)
    processed_files.append(processed_file)

# Print all output file paths
for file in processed_files:
    print(file)
