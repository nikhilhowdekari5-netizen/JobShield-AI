import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

print("=" * 55)
print(" JOB FRAUD DETECTION - MODEL TRAINING")
print("=" * 55)

# 1. Load the cleaned dataset
data_path = os.path.join(
    "JobFraudDetection",
    "dataset",
    "cleaned_job_postings.csv"
)

df = pd.read_csv(data_path)

print("\nDataset loaded:", df.shape)

# 2. Select useful text columns
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

# Combine text columns into one text field
df["combined_text"] = (
    df[text_columns]
    .fillna("Not specified")
    .astype(str)
    .agg(" ".join, axis=1)
)

# 3. Prepare input and target
X = df["combined_text"]
y = df["fraudulent"].astype(int)

print("\nTotal job postings:", len(df))
print("Legitimate jobs:", int((y == 0).sum()))
print("Fraudulent jobs:", int((y == 1).sum()))

# 4. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining examples:", len(X_train))
print("Testing examples:", len(X_test))

# 5. Create the Machine Learning pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            stop_words="english",
            max_features=50000,
            ngram_range=(1, 2),
            min_df=2
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        )
    )
])

# 6. Train the model
print("\nTraining the model. Please wait...")

model.fit(X_train, y_train)

print("Model training completed!")

# 7. Make predictions on unseen test examples
y_pred = model.predict(X_test)

# 8. Evaluate model performance
print("\n" + "=" * 55)
print(" MODEL EVALUATION")
print("=" * 55)

print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
print(f"Precision: {precision_score(y_test, y_pred, zero_division=0):.4f}")
print(f"Recall   : {recall_score(y_test, y_pred, zero_division=0):.4f}")
print(f"F1-score : {f1_score(y_test, y_pred, zero_division=0):.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Legitimate", "Fraudulent"],
        zero_division=0
    )
)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# 9. Save the trained model
model_folder = "JobFraudDetection"
os.makedirs(model_folder, exist_ok=True)

model_path = os.path.join(
    model_folder,
    "job_fraud_model.pkl"
)

joblib.dump(model, model_path)

print("\nTrained model saved successfully!")
print("Model location:", model_path)

print("\n" + "=" * 55)
print(" MODEL TRAINING COMPLETED")
print("=" * 55)