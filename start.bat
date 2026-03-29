@echo off
REM ============================================================
REM   NeuroSenti 2.0 - Windows Startup Script
REM   Starts both FastAPI Backend and Streamlit Frontend
REM ============================================================

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Activate virtual environment
echo.
echo 🔧 Activating Virtual Environment...
call "%SCRIPT_DIR%venv\Scripts\activate.bat"

if errorlevel 1 (
    echo ❌ Failed to activate virtual environment!
    exit /b 1
)

echo ✅ Virtual environment activated

REM Start FastAPI Backend in a new terminal window
echo.
echo 🚀 Starting FastAPI Backend on Port 8000...
start cmd /k "cd /d %SCRIPT_DIR% && title FastAPI Backend && venv\Scripts\python.exe -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload"

REM Wait for backend to start
echo ⏳ Waiting for backend to initialize (3 seconds)...
timeout /t 3 /nobreak

REM Start Streamlit Frontend in a new terminal window
echo.
echo 🎨 Starting Streamlit Frontend on Port 8501...
start cmd /k "cd /d %SCRIPT_DIR% && title Streamlit Frontend && venv\Scripts\streamlit.exe run frontend/app.py --server.port 8501 --server.address 127.0.0.1"

REM Display access information
echo.
echo ============================================================
echo ✅ NeuroSenti 2.0 is starting!
echo.
echo 📌 Backend (FastAPI):  http://127.0.0.1:8000
echo 📌 Frontend (Streamlit): http://127.0.0.1:8501
echo 📌 API Docs:           http://127.0.0.1:8000/docs
echo.
echo 🛑 To stop the application:
echo    - Close the FastAPI Backend window
echo    - Close the Streamlit Frontend window
echo ============================================================
echo.
pause
