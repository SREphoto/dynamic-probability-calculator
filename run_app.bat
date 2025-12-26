
@echo off
setlocal
echo ===================================================
echo   Dynamic Probability Calculator - Launcher V2
echo ===================================================

REM 1. Try standard 'python' command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto :FOUND_PYTHON
)

REM 2. Try 'py' launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto :FOUND_PYTHON
)

REM 3. Try common install locations
if exist "C:\Python312\python.exe" (
    set PYTHON_CMD="C:\Python312\python.exe"
    goto :FOUND_PYTHON
)
if exist "C:\Python311\python.exe" (
    set PYTHON_CMD="C:\Python311\python.exe"
    goto :FOUND_PYTHON
)
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    goto :FOUND_PYTHON
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    goto :FOUND_PYTHON
)

echo.
echo [ERROR] Python not found in PATH or standard locations.
echo Please install Python from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:FOUND_PYTHON
echo Using Python: %PYTHON_CMD%

echo.
echo [STEP 1] Installing/Upgrading Dependencies...
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install streamlit pandas numpy plotly scipy

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies.
    echo Please check your internet connection or permission settings.
    pause
    exit /b 1
)

echo.
echo [STEP 2] Launching Application...
%PYTHON_CMD% -m streamlit run main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application crashed or failed to start.
)

pause
