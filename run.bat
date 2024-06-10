@echo off
SETLOCAL

SET VENV_DIR=venv

REM Create virtual environment if it doesn't exist
IF NOT EXIST "%VENV_DIR%" (
    CALL setup.bat
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to create virtual environment.
        exit /b 1
    )
)

REM Activate virtual environment
CALL "%VENV_DIR%\Scripts\activate"
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    exit /b 1
)

REM Run src/main.py
python src/main.py
IF %ERRORLEVEL% NEQ 0 (
    echo src/main.py encountered an error.
    CALL deactivate >nul 2>&1
    exit /b 1
)

echo Both scripts ran successfully

REM Deactivate virtual environment
CALL deactivate >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to deactivate virtual environment.
    exit /b 1
)

ENDLOCAL
