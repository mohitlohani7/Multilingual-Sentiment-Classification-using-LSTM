from fastapi import FastAPI
from pydantic import BaseModel
import tensorflow as tf
import pickle
import numpy as np
import time
import json
import os

# ================================
# APP INIT
# ================================
app = FastAPI()

# ================================
# BASE PATH RESOLUTION (PRODUCTION SAFE)
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # api/
PROJECT_ROOT = os.path.dirname(BASE_DIR)                       # NeuroSenti 2.0/

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "Processing files",
    "NeuroSenti_Final_Submission",
    "neuro_senti_best.h5"
)

TOKENIZER_PATH = os.path.join(
    PROJECT_ROOT,
    "Processing files",
    "NeuroSenti_Final_Submission",
    "tokenizer.pkl"
)

FEEDBACK_FILE = os.path.join(PROJECT_ROOT, "feedback_data.json")

MAX_LEN = 200
CONFIDENCE_THRESHOLD = 0.80


# ================================
# LOAD MODEL & TOKENIZER
# ================================
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

if not os.path.exists(TOKENIZER_PATH):
    raise FileNotFoundError(f"Tokenizer file not found at: {TOKENIZER_PATH}")

model = tf.keras.models.load_model(MODEL_PATH)

with open(TOKENIZER_PATH, "rb") as f:
    tokenizer = pickle.load(f)


# ================================
# REQUEST SCHEMA
# ================================
class TextInput(BaseModel):
    text: str


# ================================
# FEEDBACK MEMORY UTILITIES
# ================================
def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_override(text: str):
    feedbacks = load_feedback()
    for fb in feedbacks:
        if fb.get("text", "").strip().lower() == text.strip().lower():
            return fb.get("correct_label")
    return None


# ================================
# PREDICTION ENDPOINT
# ================================
@app.post("/predict")
def predict_sentiment(input: TextInput):
    start = time.time()

    # 1️⃣ Check user feedback memory first
    override = find_override(input.text)
    if override:
        return {
            "sentiment": override,
            "confidence": 1.0,
            "source": "user_feedback_memory",
            "latency_seconds": round(time.time() - start, 3)
        }

    # 2️⃣ Tokenization & Padding
    seq = tokenizer.texts_to_sequences([input.text])
    padded = tf.keras.preprocessing.sequence.pad_sequences(
        seq, maxlen=MAX_LEN
    )

    # 3️⃣ Model Prediction
    raw_score = float(model.predict(padded, verbose=0)[0][0])

    # 4️⃣ Threshold Logic
    sentiment = "Positive" if raw_score >= CONFIDENCE_THRESHOLD else "Negative"

    return {
        "sentiment": sentiment,
        "confidence": round(raw_score, 3),
        "threshold_used": CONFIDENCE_THRESHOLD,
        "source": "ml_model_thresholded",
        "latency_seconds": round(time.time() - start, 3)
    }


# ================================
# FEEDBACK ENDPOINT
# ================================
@app.post("/feedback")
def store_feedback(data: dict):
    feedback = load_feedback()
    feedback.append(data)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedback, f, indent=2)

    return {"message": "Feedback stored successfully"}