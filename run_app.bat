@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Please create the virtual environment first:
  echo   py -m venv .venv
  echo   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  exit /b 1
)
start "FastAPI Backend" cmd /k "cd /d \"%~dp0\" ^&^& .\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul
start "Streamlit Frontend" cmd /k "cd /d \"%~dp0\" ^&^& .\.venv\Scripts\python.exe -m streamlit run app.py"
endlocal
