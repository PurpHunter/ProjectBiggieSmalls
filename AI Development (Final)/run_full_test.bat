@echo off
setlocal

REM Always run from project root
cd /d %~dp0

REM Path to local venv
set VENV_PATH=federated-ai\Scripts\activate.bat

if not exist "%VENV_PATH%" (
    echo ERROR: Virtual environment not found.
    echo Please create it first.
    pause
    exit /b
)

echo =====================================
echo Activating virtual environment
echo =====================================

REM ---- AUTH SERVER ----
start cmd /k "call %VENV_PATH% && python auth\auth_server.py"

REM ---- FEDERATED SERVER ----
start cmd /k "call %VENV_PATH% && python federated_learning\federated_server.py"

REM ---- AI SERVER ----
start cmd /k "call %VENV_PATH% && python central_server\ai_server.py"

echo Waiting for servers...
timeout /t 10 >nul

REM ---- DEVICES ----
start cmd /k "call %VENV_PATH% && python devices\device_A\federated_client.py"
start cmd /k "call %VENV_PATH% && python devices\device_B\federated_client.py"
start cmd /k "call %VENV_PATH% && python devices\device_C\federated_client.py"

echo Waiting for federated updates...
timeout /t 15 >nul

REM ---- POST PROCESS ----
call %VENV_PATH%
python federated_learning\build_vectorizer.py
python federated_learning\export_model.py

echo =====================================
echo ALL SYSTEMS RUNNING
echo =====================================
pause
