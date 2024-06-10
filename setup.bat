@echo off
SET VENV_DIR=venv

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Create virtual environment
IF NOT EXIST %VENV_DIR% (
    python -m venv %VENV_DIR%
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        exit /b 1
    )
)

REM Activate virtual environment
CALL %VENV_DIR%\Scripts\activate
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    exit /b 1
)

REM Install requirements
IF EXIST requirements.txt (
    pip install -r requirements.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install required packages.
        exit /b 1
    )
) ELSE (
    echo requirements.txt not found.
    exit /b 1
)

REM Deactivate virtual environment
deactivate
