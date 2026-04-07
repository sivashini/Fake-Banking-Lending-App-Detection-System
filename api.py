from fastapi import FastAPI
from pydantic import BaseModel
import joblib, numpy as np

app = FastAPI()
model = joblib.load("fake_app_model.pkl")
selected_features = joblib.load("selected_features.pkl")

class AppPermissions(BaseModel):
    permissions: dict  # e.g. {"READ_SMS": 1, "CAMERA": 0, ...}

@app.post("/check-app")
def check_app(data: AppPermissions):
    vec = np.array([data.permissions.get(f, 0) for f in selected_features])
    prob = model.predict_proba([vec])[0][1]
    score = int(prob * 100)
    verdict = "SAFE" if score <= 35 else "SUSPICIOUS" if score <= 70 else "MALICIOUS"
    
    # Real-time alert if malicious
    if score > 70:
        print(f"🚨 ALERT: Malicious app detected! Score={score}")
    
    return {
        "risk_score": score,
        "verdict": verdict,
        "dangerous_permissions": [
            f for f in selected_features
            if data.permissions.get(f, 0) == 1 and
               f in ["READ_SMS","SEND_SMS","READ_CONTACTS","RECORD_AUDIO","READ_CALL_LOG"]
        ]
    }
