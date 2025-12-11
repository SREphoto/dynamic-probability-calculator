
@echo off
echo ===================================================
echo   Dynamic Probability Calculator - Launcher
echo ===================================================

echo [1/3] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not found! Please install Python 3.10+ and add it to your PATH.
    pause
    exit /b
)

echo [2/3] Installing/Verifying Dependencies...
pip install streamlit pandas numpy plotly scipy
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies.
    pause
    exit /b
)

echo [3/3] Starting Application...
echo.
echo The app should open in your default browser.
echo If it closes immediately, check the errors below.
echo.
streamlit run main.py

if %errorlevel% neq 0 (
    echo.
    echo ===================================================
    echo   CRITICAL ERROR
    echo ===================================================
    echo Streamlit failed to run. Please check the error message above.
)

pause
