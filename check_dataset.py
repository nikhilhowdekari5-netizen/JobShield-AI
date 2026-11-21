import pandas as pd

# Load the dataset
file_path = "JobFraudDetection/dataset/fake_job_postings.csv"

df = pd.read_csv(file_path)

# Display basic information
print("\n========== DATASET LOADED ==========")

print("\nFirst 5 job postings:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nFraud distribution:")
print(df["fraudulent"].value_counts())

print("\n========== DATASET CHECK COMPLETE ==========") 