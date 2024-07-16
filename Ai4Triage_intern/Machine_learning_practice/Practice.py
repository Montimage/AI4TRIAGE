import pandas as pd
loan_data = pd.read_csv("/home/ubuntu/Ai4Triage_intern/Machine_learning_practice/datalab_export_2024-07-04 11_48_26.csv")
loan_data.head()
# Check column types
print(loan_data.dtypes)