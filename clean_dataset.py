import os
import pandas as pd

print("=" * 50)
print("JOB FRAUD DETECTION - DATA CLEANING")
print("=" * 50)

# Step 1: Load the dataset
file_path = os.path.join(
    "JobFraudDetection",
    "dataset",
    "fake_job_postings.csv"
)

df = pd.read_csv(file_path)

print("\nOriginal dataset shape:", df.shape)

# Step 2: Check duplicate records
duplicates = df.duplicated().sum()
print("Duplicate records:", duplicates)

# Remove duplicate rows
df = df.drop_duplicates()

# Step 3: Fill missing text values
text_columns = [
    "title",
    "location",
    "department",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function"
]

for column in text_columns:
    df[column] = df[column].fillna("Not specified")

# Step 4: Fill missing salary values
df["salary_range"] = df["salary_range"].fillna("Not specified")

# Step 5: Check remaining missing values
print("\nRemaining missing values:")
print(df.isnull().sum())

# Step 6: Check fraud distribution
print("\nFraud distribution after cleaning:")
print(df["fraudulent"].value_counts())

# Step 7: Save cleaned dataset
output_folder = os.path.join(
    "JobFraudDetection",
    "dataset"
)

os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(
    output_folder,
    "cleaned_job_postings.csv"
)

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("Saved location:", output_path)
print("Final dataset shape:", df.shape)

print("\n" + "=" * 50)
print("DATA CLEANING COMPLETED")
print("=" * 50)