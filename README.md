**The Problem**
Fake banking and digital lending apps are one of the fastest-growing financial fraud vectors in India. Attackers distribute APKs disguised as trusted banks (SBI, HDFC, ICICI) via WhatsApp links and third-party sites. Once installed, they:

Steal login credentials through phishing UI screens
Intercept OTPs via SMS permission abuse
Trap victims in predatory debt traps through fake lending flows
Operate invisibly until the damage is done


**Solution Overview**
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

**Dataset**
Source: A Dataset for Fake Android Anti-Malware Detection.

**Features**
Pre-installation detection — scans APK permissions before the user installs
Real-time risk scoring — 0 to 100 score with Safe / Suspicious / Malicious verdict
SHAP explainability — shows exactly which permissions triggered the verdict
Privacy-preserving — only permission hash is sent to API, no user data
REST API — FastAPI endpoint ready for bank system integration
Real-time alerting — webhook to fraud team + CERT-In report auto-generation

**Installation**

**Run the API**
bashuvicorn api.main:app --reload
API runs at http://localhost:8000 — interactive docs at http://localhost:8000/docs

**Check an app via API**
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
**Response:**
json{
  "risk_score": 87,
  "verdict": "MALICIOUS",
  "dangerous_permissions": ["READ_SMS", "SEND_SMS", "RECORD_AUDIO"],
  "action": "App blocked. Bank fraud team alerted."
}


Score RangeVerdictAction0 – 35SafeAllow installation36 – 70SuspiciousShow warning to user, send for manual review71 – 100MaliciousBlock app, alert bank fraud team, generate CERT-In report
