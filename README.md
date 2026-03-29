# 🧠 NeuroSenti 2.0: Hybrid Sentiment Analysis Engine

**NeuroSenti 2.0** is a production-ready Sentiment Analysis system built using a Hybrid **CNN-BiLSTM** architecture. It is deployed using **FastAPI** (Backend) and **Streamlit** (Frontend), containerized with **Docker**.

## 📂 Project Structure
- `api/`: FastAPI backend handling model inference.
- `frontend/`: Streamlit UI for user interaction.
- `models/`: Contains the trained `.h5` model and `.pkl` tokenizer.

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt