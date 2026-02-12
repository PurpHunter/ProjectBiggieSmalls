@echo off
title Federated AI Launcher

echo ==============================
echo  Starting Federated AI System
echo ==============================

REM Go to project root
cd /d "%~dp0"

REM -----------------------------
REM Create venv if missing
REM -----------------------------
if not exist "federated-ai\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3 -m venv federated-ai
)

set PY_EXE=%~dp0federated-ai\Scripts\python.exe
set PIP_EXE=%~dp0federated-ai\Scripts\pip.exe

REM -----------------------------
REM Install dependencies
REM -----------------------------
echo Installing dependencies...
%PIP_EXE% install --quiet --upgrade pip >nul
%PIP_EXE% install --quiet flask flask-cors requests numpy >nul

REM -----------------------------
REM Start Auth Server
REM -----------------------------
echo Starting Auth Server...
start "Auth Server" cmd /k ""%PY_EXE%" auth\auth_server.py"

REM -----------------------------
REM Start Federated Server
REM -----------------------------
echo Starting Federated Server...
start "Federated Server" cmd /k ""%PY_EXE%" federated_learning\federated_server.py"

REM -----------------------------
REM Start AI Server
REM -----------------------------
echo Starting AI Server...
start "AI Server" cmd /k ""%PY_EXE%" central_server\ai_server.py"

REM -----------------------------
REM Wait for servers
REM -----------------------------
echo Waiting for servers...
timeout /t 8 >nul

REM -----------------------------
REM Start Device Clients
REM -----------------------------
echo Starting Device A...
start "Device A" cmd /k ""%PY_EXE%" devices\device_A\federated_client.py"

echo Starting Device B...
start "Device B" cmd /k ""%PY_EXE%" devices\device_B\federated_client.py"

echo Starting Device C...
start "Device C" cmd /k ""%PY_EXE%" devices\device_C\federated_client.py"

echo.
echo ==============================
echo All services started.
echo ==============================
pause
