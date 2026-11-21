🛡️ JobShield AI – Job Fraud Detection Platform

An AI-powered web application that detects fraudulent job postings using Machine Learning. JobShield AI helps users identify suspicious job opportunities and make safer career decisions.

📌 Project Overview

Online job platforms contain both legitimate and fraudulent job postings. Fake job advertisements can mislead job seekers and cause financial loss.

JobShield AI uses Natural Language Processing (NLP) and Machine Learning to analyze job descriptions and predict whether a job posting is **Real or Fraudulent**.

## 🎯 Objectives

- Detect fraudulent job postings automatically.
- Help job seekers identify suspicious opportunities.
- Apply Machine Learning to real-world problems.
- Provide an easy-to-use web interface for job fraud detection.

## ✨ Features

- **Job Fraud Detection:** Predict whether a job posting is real or fake.
- **Machine Learning:** Uses TF-IDF and Logistic Regression.
- **User Authentication:** Login functionality.
- **Admin Dashboard:** Administrative interface.
- **Prediction History:** Maintains previous prediction records.
- **Web Interface:** Simple and user-friendly Flask application.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Flask | Web Framework |
| Scikit-learn | Machine Learning |
| Pandas | Data Processing |
| NumPy | Numerical Operations |
| TF-IDF | Text Feature Extraction |
| Logistic Regression | Classification Algorithm |
| HTML & CSS | Frontend |
| SQLite | Database |
| VS Code | Development Environment |

## 🤖 Machine Learning Approach

The project uses the following workflow:

1. **Data Collection:** Job posting dataset.
2. **Data Preprocessing:** Cleaning and preparing job descriptions.
3. **Feature Extraction:** TF-IDF converts text into numerical features.
4. **Model Training:** Logistic Regression learns patterns from the dataset.
5. **Prediction:** The trained model predicts whether a job posting is legitimate or fraudulent.
6. **Evaluation:** Model performance is measured using classification metrics.

## 📊 Model Performance

The trained model achieved the following results:

| Evaluation Metric | Score |
|---|---:|
| Accuracy | 98.46% |
| Precision | 79.80% |
| Recall | 91.33% |
| F1-Score | 85.18% |

**Note:** These are the evaluation results obtained during model testing.

## 📂 Project Structure

```text
JobShield-AI/
│
├── JobFraudDetection/
│   ├── app.py
│   ├── job_fraud_model.pkl
│   ├── job_history.db
│   │
│   ├── dataset/
│   │   ├── cleaned_job_postings.csv
│   │   ├── fake_job_postings.csv
│   │   └── check_dataset.py
│   │
│   ├── check_dataset.py
│   ├── clean_dataset.py
│   ├── create_admin.py
│   └── train_model.py
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/nikhilhowdekari5-netizen/JobShield-AI.git
```

### 2. Open the Project

```bash
cd JobShield-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

Navigate to the folder containing `app.py` and execute:

```bash
python app.py
```

Open the local Flask address displayed in your terminal in your browser.

## 🔮 Future Improvements

- Integrate advanced Machine Learning models.
- Improve fraud detection accuracy.
- Add more detailed fraud analysis.
- Develop a responsive user interface.
- Deploy the application online.

## 👨‍💻 Developer

**Nikhil Howdekari**

B.Tech – Data Science

GitHub: [nikhilhowdekari5-netizen](https://github.com/nikhilhowdekari5-netizen)

---

⭐ If you find this project interesting, consider giving this repository a star!