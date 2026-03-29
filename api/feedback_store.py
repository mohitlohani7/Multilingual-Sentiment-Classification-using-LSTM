import json
import os

FEEDBACK_FILE = "feedback_data.json"


def load_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return []
    with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_override(text: str):
    feedbacks = load_feedback()
    for fb in feedbacks:
        if fb["text"].strip().lower() == text.strip().lower():
            return fb["correct_label"]
    return None
