# NeuroSenti 2.0 - Project Setup & Run Guide

## ✅ Project Status

### Files & Dependencies
- ✅ **Model Files Found**: `neuro_senti_best.h5` (23.26 MB) + `tokenizer.pkl` (5.24 MB)
- ✅ **Backend**: FastAPI API configured and ready
- ✅ **Frontend**: Streamlit UI configured and ready
- ✅ **Dependencies**: All packages in requirements.txt installed
- ✅ **Python Environment**: Virtual environment active (Python 3.13.9)

### Code Status
- ✅ **API (main.py)**: No errors found
- ✅ **Frontend (app.py)**: No errors found
- ✅ **Import Issues**: Resolved

---

## 🚀 Quick Start

### Option 1: Windows Batch Script (Easiest)
Double-click `start.bat` - It will:
1. Activate virtual environment
2. Start FastAPI Backend in one window (port 8000)
3. Start Streamlit Frontend in another window (port 8501)
4. Open both applications automatically

### Option 2: Manual Terminal Commands

#### Terminal 1 - Backend (FastAPI)
```cmd
venv\Scripts\activate.bat
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

#### Terminal 2 - Frontend (Streamlit)
```cmd
venv\Scripts\activate.bat
streamlit run frontend/app.py --server.port 8501 --server.address 127.0.0.1
```

### Option 3: Linux/Mac (Bash Script)
```bash
chmod +x start.sh
./start.sh
```

---

## 🌐 Access Points

Once running:
- **Frontend UI**: http://127.0.0.1:8501
- **Backend API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs (Interactive Swagger UI)
- **API Redoc**: http://127.0.0.1:8000/redoc

---

## 📂 Project Structure

```
NeuroSenti 2.0/
├── api/                    # FastAPI Backend
│   ├── main.py            # Core API endpoints
│   └── dependencies.py    # API dependencies (empty)
├── frontend/              # Streamlit Frontend
│   └── app.py            # UI for predictions
├── src/                   # Training & processing utilities
│   ├── train_model.py
│   ├── evaluate.py
│   └── data_cleaning.py
├── Processing files/      # Raw data & model artifacts
│   └── NeuroSenti_Final_Submission/
│       ├── neuro_senti_best.h5 ✅ Model (23.26 MB)
│       ├── tokenizer.pkl        ✅ Tokenizer (5.24 MB)
│       └── neuro_senti_advanced.png
├── data/                  # Cleaned data
│   └── imdb_cleaned_data.csv
├── venv/                  # Virtual Environment (active)
├── requirements.txt       # All dependencies
├── Dockerfile            # For Docker deployment
├── start.bat             # Windows startup script ⭐
├── start.sh              # Linux/Mac startup script
└── README.md
```

---

## 🔧 Architecture

**NeuroSenti 2.0** uses:
- **Model**: Hybrid CNN-BiLSTM Neural Network
- **Backend**: FastAPI (REST API)
- **Frontend**: Streamlit (Web UI)
- **Deployment**: Docker support included

---

## 🧪 Test the API

### Using cURL
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This movie was absolutely amazing! The cinematography was stunning and the plot kept me engaged throughout."}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"text": "This movie was absolutely amazing!"}
)
print(response.json())
```

### Expected Response
```json
{
  "input_text": "This movie was absolutely amazing!",
  "sentiment": "Positive",
  "confidence_score": 95.67,
  "latency_seconds": 0.0123,
  "model": "Bi-LSTM v2.0"
}
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check port 8000 is not already in use: `netstat -ano | findstr :8000`
- Verify virtual environment is activated
- Check `requirements.txt` packages are installed

### Frontend won't connect to backend
- Ensure FastAPI is running (should see ✅ loading message)
- Check both are on same localhost (127.0.0.1)
- API_URL in `frontend/app.py` should be `http://127.0.0.1:8000/predict`

### Model loading fails
- Verify model files exist in `Processing files/NeuroSenti_Final_Submission/`
- Check file permissions
- Ensure TensorFlow (2.20.0) is installed

---

## 📦 Installed Packages

Core packages:
- **fastapi** (0.128.0)
- **tensorflow** (2.20.0)
- **streamlit** (1.53.0)
- **uvicorn** (0.40.0)
- Plus all dependencies in `requirements.txt`

---

## ✨ Ready to Run!

Everything is configured and ready. Choose your startup method above and enjoy NeuroSenti 2.0! 🎉
