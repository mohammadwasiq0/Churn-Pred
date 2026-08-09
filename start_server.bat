@echo off
echo Starting Churn Prediction Backend Server...
call venv\Scripts\activate
python -m uvicorn api.main:app --host 127.0.0.0 --port 8000 --reload
pause
