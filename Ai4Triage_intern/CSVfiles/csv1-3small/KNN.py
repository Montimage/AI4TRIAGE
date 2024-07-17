import numpy as np  # Used for numerical computations
import pandas as pd 
from sklearn.model_selection import train_test_split  # To split the data into training and testing sets
from sklearn.neighbors import KNeighborsClassifier  # KNN classifier
from sklearn.metrics import classification_report, accuracy_score  # To evaluate model performance

data_cleaned = pd.read_csv('/home/ubuntu/AI4TRIAGE/Ai4Triage_intern/CSVfiles/csv1-3small/processed1.csv')

# Assuming 'alert_type' is the label column name, replace it with the actual column name if different
target_column_name = ['matching_service_rule_id']  # Label column name

# Assuming the list of feature column names is as follows, replace it with actual feature column names
feature_column_names = ['bioc_category_enum_key', 'alert_type', 'category', 'name','mitre_techniques','mitre_tactics_names','mitre_techniques_names']  # List of feature column names

# Select feature columns
X = data_cleaned[feature_column_names]

# Select label column
y = data_cleaned[target_column_name]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)  # Use 20% of the data as the test set
# random_state=42 ensures that the split results are consistent every time the code is run

# Create an instance of the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)  # Choose 5 nearest neighbors for prediction; n_neighbors can be adjusted as needed

# Train the model
knn.fit(X_train, y_train)

# Predict the test set results
y_pred = knn.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
