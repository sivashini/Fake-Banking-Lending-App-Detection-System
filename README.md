# 🛡️Fake Banking & Digital Lending App Detection System

---

## 🚨 The Problem

Fake banking and digital lending apps are one of the **fastest-growing financial fraud vectors in India**. Attackers distribute malicious APK files disguised as trusted banks like **SBI, HDFC, and ICICI** via WhatsApp links and third-party websites.

Once installed, these apps can:

* Steal login credentials through phishing UI screens
* Intercept OTPs using SMS permission abuse
* Trap users in predatory loan schemes
* Operate silently until financial damage is done

---

## 💡 Solution Overview

```
APK Submitted
     │
     ▼
Permission Extraction (AndroidManifest.xml)
     │
     ▼
Binary Feature Vector 
[READ_SMS=1, SEND_SMS=1, RECORD_AUDIO=1, ...]
     │
     ▼
MLP Classifier (trained on dataset)
     │
     ▼
Risk Score (0–100)
     │
  ┌──────────────┬──────────────┬
  ▼              ▼              ▼
0–35           36–70           71–100
Safe           Suspicious      Malicious
Allow          Warn + Review   Block + Alert
```

---

## 📊 Dataset

* **Source:** *A Dataset for Fake Android Anti-Malware Detection*
* Contains labeled data for:

  * Fake apps
  * Genuine apps
* Used for training the ML model to classify app behavior

---

## ⚙️ Key Features

* 🔍 **Pre-installation Detection**
  Scans APK permissions before installation

* ⚡ **Real-time Risk Scoring**
  Generates a score from **0 to 100**

* 🧠 **ML-Based Classification**
  Uses an **MLP (Multi-Layer Perceptron)** model

* 📈 **SHAP Explainability**
  Shows which permissions caused the risk

* 🔒 **Privacy-Preserving**
  Only permission data is processed (no personal data)

* 🔗 **REST API (FastAPI)**
  Easily integrates with banking systems

* 🚨 **Real-time Alerting**
  Sends alerts to fraud teams and generates reports

---

## 🛠️ Installation & Setup

### 1️⃣ Run the API

```bash
uvicorn api.main:app --reload
```

* API URL: http://localhost:8000
* Docs: http://localhost:8000/docs

---

### 2️⃣ Check an App via API

```bash
curl -X POST http://localhost:8000/check-app \
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
```

---

## 📥 Sample Response

```json
{
  "risk_score": 87,
  "verdict": "MALICIOUS",
  "dangerous_permissions": [
    "READ_SMS",
    "SEND_SMS",
    "RECORD_AUDIO"
  ],
  "action": "App blocked. Bank fraud team alerted."
}
```

---

## 📊 Risk Scoring System

| Score Range | Verdict    | Action                                |
| ----------- | ---------- | ------------------------------------- |
| 0 – 35      | Safe       | Allow installation                    |
| 36 – 70     | Suspicious | Warn user + manual review             |
| 71 – 100    | Malicious  | Block app + alert fraud team + report |

---

## 🎯 Benefits

* Prevents financial fraud before installation
* Protects user credentials and OTPs
* Enables proactive fraud detection
* Strengthens trust in digital banking systems

---

## 🔮 Future Enhancements

* Integration with Google Play Protect / App Stores
* Deep learning-based malware detection
* Real-time APK scanning from URLs
* User feedback learning system

---

