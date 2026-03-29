#!/bin/bash

# 1. Start FastAPI in background (&)
echo "🚀 Starting FastAPI Backend..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# 2. Wait for a few seconds
sleep 5

# 3. Start Streamlit in foreground
echo "🎨 Starting Streamlit Frontend..."
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0