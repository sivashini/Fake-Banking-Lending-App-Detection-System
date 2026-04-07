**The Problem
**Fake banking and digital lending apps are one of the fastest-growing financial fraud vectors in India. Attackers distribute APKs disguised as trusted banks (SBI, HDFC, ICICI) via WhatsApp links and third-party sites. Once installed, they:

Steal login credentials through phishing UI screens
Intercept OTPs via SMS permission abuse
Trap victims in predatory debt traps through fake lending flows
Operate invisibly until the damage is done


Solution Overview
APK Submitted
     │
     ▼
Permission Extraction (AndroidManifest.xml)
     │
     ▼
Binary Feature Vector [READ_SMS=1, SEND_SMS=1, RECORD_AUDIO=1 ...]
     │
     ▼
MLP Classifier (trained on peer-reviewed dataset)
     │
     ▼
Risk Score 0–100
     │
  ┌──┴──────────────┐
  │                 │
0–35             36–70            71–100
Safe             Suspicious       Malicious
Allow            Warn + Review    Block + Alert

Dataset
Source: A Dataset for Fake Android Anti-Malware Detection — Saeed Seraj et al., published at ACM WIMS 2020 Conference.

Binary permission features per app (86 permission columns)
Labels: 1 = malicious, 0 = benign
Class balancing applied via SMOTE
Feature selection: top 30 permissions via Chi-squared test


Model Performance (Actual Results)
ModelAccuracyROC-AUCMLP (chosen)84.77%0.8968Random Forest84.20%0.8997XGBoost84.20%0.8882SVM81.90%0.8465
Final model: MLP — highest accuracy (84.77%), strong ROC-AUC (0.8968), and validated by the original dataset paper authors.

Features

Pre-installation detection — scans APK permissions before the user installs
Real-time risk scoring — 0 to 100 score with Safe / Suspicious / Malicious verdict
SHAP explainability — shows exactly which permissions triggered the verdict
Privacy-preserving — only permission hash is sent to API, no user data
REST API — FastAPI endpoint ready for bank system integration
Real-time alerting — webhook to fraud team + CERT-In report auto-generation
Verified whitelist — RBI-registered bank apps bypass ML check via certificate hash


Project Structure
fakeshield/
│
├── data/
│   └── fake_antimalware_dataset.csv      # Raw dataset from Kaggle
│
├── notebooks/
│   ├── 01_eda.ipynb                      # Exploratory data analysis
│   ├── 02_preprocessing.ipynb            # SMOTE, feature selection
│   ├── 03_model_training.ipynb           # Train all 4 models + compare
│   └── 04_shap_explainability.ipynb      # SHAP plots and analysis
│
├── models/
│   ├── mlp_model.pkl                     # Trained MLP (final model)
│   ├── random_forest_model.pkl           # Trained Random Forest
│   └── selected_features.pkl             # Top 30 Chi2 features
│
├── api/
│   ├── main.py                           # FastAPI application
│   ├── predictor.py                      # Inference logic
│   └── schemas.py                        # Pydantic request/response models
│
├── src/
│   ├── preprocess.py                     # SMOTE + feature selection pipeline
│   ├── train.py                          # Model training script
│   └── evaluate.py                       # Metrics + SHAP analysis
│
├── requirements.txt
├── README.md
└── LICENSE

Installation
bash# Clone the repository
git clone https://github.com/yourusername/fakeshield.git
cd fakeshield

# Create virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

Requirements
pandas
numpy
scikit-learn
xgboost
imbalanced-learn
shap
matplotlib
seaborn
fastapi
uvicorn
joblib
pydantic

Usage
Train the model
bashpython src/train.py
This will:

Load the dataset
Apply SMOTE for class balancing
Select top 30 features via Chi-squared test
Train MLP, Random Forest, XGBoost, and SVM
Save the best model to models/mlp_model.pkl

Run the API
bashuvicorn api.main:app --reload
API runs at http://localhost:8000 — interactive docs at http://localhost:8000/docs
Check an app via API
bashcurl -X POST http://localhost:8000/check-app \
  -H "Content-Type: application/json" \
  -d '{
    "permissions": {
      "READ_SMS": 1,
      "SEND_SMS": 1,
      "RECORD_AUDIO": 1,
      "READ_CONTACTS": 1,
      "INTERNET": 1,
      "CAMERA": 0
    }
  }'
Response:
json{
  "risk_score": 87,
  "verdict": "MALICIOUS",
  "dangerous_permissions": ["READ_SMS", "SEND_SMS", "RECORD_AUDIO"],
  "action": "App blocked. Bank fraud team alerted."
}

How the Risk Score Works
Score RangeVerdictAction0 – 35SafeAllow installation36 – 70SuspiciousShow warning to user, send for manual review71 – 100MaliciousBlock app, alert bank fraud team, generate CERT-In report
