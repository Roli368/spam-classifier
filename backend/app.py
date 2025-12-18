from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
from utils import preprocess_text

app = FastAPI(title="Spam Detection API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("model/spam_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

TRUSTED_KEYWORDS = [
    "github",
    "google",
    "microsoft",
    "otp",
    "one time password",
    "authentication code",
    "verification code",
    "do not share"
]

@app.post("/predict")
def predict(data: dict):
    message = data["message"]          # ✅ message defined HERE
    text = message.lower()             # ✅ now valid

    # ✅ RULE-BASED OVERRIDE
    if any(k in text for k in TRUSTED_KEYWORDS):
        return {
            "prediction": "Ham",
            "confidence": 1.0,
            "note": "Trusted security message (rule-based override)"
        }

    # ML prediction
    processed = preprocess_text(message)
    vector = vectorizer.transform([processed]).toarray()

    prediction = model.predict(vector)[0]
    confidence = max(model.predict_proba(vector)[0])

    return {
        "prediction": "Spam" if prediction == 1 else "Ham",
        "confidence": round(confidence, 2)
    }

