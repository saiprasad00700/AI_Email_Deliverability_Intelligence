# 🚀 AI Email Deliverability Intelligence Platform

An end-to-end **AI-powered email analytics platform** that predicts email deliverability using **XGBoost**, provides **SQL-based campaign analytics**, stores prediction history in **MySQL**, and includes an **offline AI assistant powered by Llama 3.2 (Ollama)**.

---

## 📌 Project Overview

Email deliverability is one of the most important factors in email marketing. Even well-designed campaigns can fail if emails land in spam instead of the inbox.

This platform helps marketers and analysts:

* Predict the deliverability of email campaigns before sending them.
* Analyze campaign performance using SQL dashboards.
* Store every prediction for future analysis.
* Ask AI-powered technical and deliverability questions completely offline.

---

## 🎯 Problem Statement

Marketing teams often face questions such as:

* Will this campaign reach users' inboxes?
* Which campaign factors affect deliverability?
* How can bounce rate and sender reputation be improved?
* How do SPF, DKIM, and DMARC impact email delivery?

This project combines **Machine Learning, SQL, Business Intelligence, and Generative AI** into one unified application.

---

# ✨ Key Features

### 🤖 AI Deliverability Prediction

* Multi-class email deliverability prediction
* XGBoost classification model
* Confidence score for every prediction
* Probability distribution visualization
* Interactive Streamlit interface

### 📊 SQL Analytics Dashboard

* Client analytics
* Open rate analysis
* Bounce rate trends
* Complaint analysis
* Business-focused SQL queries
* KPI metrics

### 📜 Prediction History

* Automatically stores every prediction in MySQL
* Search by client category
* Filter by prediction status
* Download history as CSV
* Delete prediction history

### 💬 AI Chat Assistant (Offline)

Powered by **Llama 3.2 + Ollama**

Supports questions about:

* Email Deliverability
* SPF, DKIM & DMARC
* Python
* SQL
* Machine Learning
* Campaign Analytics
* General technical concepts

**No OpenAI API required. Runs completely offline.**

---

# 🏗️ System Architecture

```text
                 Email Campaign Dataset
                          │
                          ▼
                Feature Engineering
                          │
                          ▼
          Preprocessing (Ordinal Encoder)
                          │
                          ▼
            XGBoost Classification Model
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
   AI Prediction    SQL Analytics    AI Chat (Llama 3.2)
          │
          ▼
 Prediction History (MySQL)
```

---

# 🧠 Machine Learning Pipeline

1. Data Acquisition
2. Data Profiling
3. Feature Engineering
4. Data Cleaning
5. Ordinal Encoding
6. Model Training (XGBoost)
7. Model Evaluation
8. Streamlit Deployment
9. Prediction Storage (MySQL)

---

# 🛠️ Technologies Used

| Category         | Technology                |
| ---------------- | ------------------------- |
| Programming      | Python                    |
| Machine Learning | XGBoost, Scikit-learn     |
| Data Processing  | Pandas, NumPy             |
| Visualization    | Plotly                    |
| Web App          | Streamlit                 |
| Database         | MySQL                     |
| Local LLM        | Ollama + Llama 3.2        |
| Model Storage    | Joblib                    |
| IDE              | VS Code, Jupyter Notebook |

---

# 📂 Project Structure

```text
AI_Email_Deliverability_Intelligence/

├── app.py
│
├── pages/
│   ├── 01_SQL_Analytics.py
│   ├── 02_AI_Prediction.py
│   ├── 03_AI_Chat.py
│   └── 04_Prediction_History.py
│
├── models/
│   ├── xgboost_model_v3.pkl
│   ├── preprocessor_v3.pkl
│   ├── label_encoder_v3.pkl
│   └── schema_v3.pkl
│
├── notebooks/
│   ├── 01_Data_Acquisition.ipynb
│   ├── 02_Data_Profiling.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   └── 06_Model_Training_V3.ipynb
│
├── utils/
│   └── db.py
│
├── assets/
├── reports/
├── data/
└── README.md
```

---

# 📊 Deliverability Classes

The model predicts one of four deliverability statuses.

| Status       | Meaning                                            |
| ------------ | -------------------------------------------------- |
| 🟢 Excellent | Very high inbox placement probability              |
| 🔵 Good      | Good deliverability with minor improvements needed |
| 🟡 Warning   | Moderate risk of delivery issues                   |
| 🔴 Critical  | High probability of spam or delivery failure       |

---

# 💻 Application Pages

## 1. SQL Analytics

Provides business intelligence using SQL queries.

**Includes:**

* Total clients
* Campaign performance
* Open rate metrics
* Bounce analysis
* Complaint trends

---

## 2. AI Prediction

Users enter campaign information such as:

* Client category
* Campaign type
* Subscribers
* Unique opens
* Bounce rates
* Audience validity
* Sending hour

The application returns:

* Deliverability status
* Confidence score
* Probability chart
* Automatic database storage

---

## 3. AI Chat

An offline AI assistant powered by **Llama 3.2**.

Example questions:

* What is DKIM?
* Explain SPF vs DMARC.
* How do I reduce bounce rate?
* What is XGBoost?
* Explain SQL JOINs.

---

## 4. Prediction History

Every prediction is stored in **MySQL**.

Features include:

* Search
* Filter
* CSV Export
* Delete History
* Summary KPIs

---

# 📈 Machine Learning Model

| Item           | Value                      |
| -------------- | -------------------------- |
| Algorithm      | XGBoost Classifier         |
| Problem Type   | Multi-class Classification |
| Encoder        | Ordinal Encoder            |
| Target Classes | 4                          |
| Deployment     | Streamlit                  |

---

# 🚀 Installation Guide

## 1. Clone Repository

```bash
git clone https://github.com/saiprasad00700/AI_Email_Deliverability_Intelligence.git

cd AI_Email_Deliverability_Intelligence
```

## 2. Install Requirements

```bash
pip install -r requirements.txt
```

## 3. Configure MySQL

Create a database:

```sql
CREATE DATABASE email_deliverability_db;
```

Update `utils/db.py` with your MySQL credentials.

## 4. Install Ollama

Download and install **Ollama**.

Pull the model:

```bash
ollama pull llama3.2:3b
```

## 5. Run Streamlit

```bash
streamlit run app.py
```

The application will automatically create the prediction history table.

---

# 📷 Screenshots

Add these images inside `assets/screenshots/`.

| Screenshot         | File Name                |
| ------------------ | ------------------------ |
| Home Page          | `home.png`               |
| SQL Dashboard      | `sql_dashboard.png`      |
| AI Prediction      | `prediction_input.png`   |
| Prediction Result  | `prediction_result.png`  |
| AI Chat            | `ai_chat.png`            |
| Prediction History | `prediction_history.png` |

---

# 🌍 Real-World Impact

This project demonstrates how AI can improve email marketing by combining predictive analytics with business intelligence.

### Business Benefits

* Reduce spam placement
* Improve sender reputation
* Monitor campaign quality
* Maintain prediction history
* Enable data-driven marketing decisions

---

# 🔮 Future Enhancements

* User authentication
* SHAP explainable AI
* Campaign recommendation engine
* PDF report generation
* Email optimization suggestions
* Multi-language AI assistant

---

# 👨‍💻 Author

**Saiprasad Nukala**

**Skills:** Python • SQL • Machine Learning • XGBoost • Streamlit • MySQL • Generative AI • Ollama

GitHub: **saiprasad00700**

---

## ⭐ If you found this project useful, consider giving it a Star!
