
@echo off
echo ===================================================
echo   Environment Fixer - Installing Python
echo ===================================================

echo This script will attempt to install Python 3.11 using 'winget'.
echo You may see a prompt asking for permission.
echo.
pause

echo.
echo [1/2] Installing Python 3.11...
winget install -e --id Python.Python.3.11 --scope machine
if %errorlevel% neq 0 (
    echo.
    echo Winget failed using system scope. Trying user scope...
    winget install -e --id Python.Python.3.11 --scope user
)

echo.
echo [2/2] Verifying Installation...
rem Refresh environment variables (poor man's refresh for batch)
set "PATH=%PATH%;C:\Program Files\Python311\;%LOCALAPPDATA%\Programs\Python\Python311\"

python --version
if %errorlevel% neq 0 (
    echo Python installed but not waiting in this shell.
    echo Please CLOSE this window and run 'run_app.bat' again.
) else (
    echo Python found!
    echo.
    echo Launching 'run_app.bat' now...
    call run_app.bat
)

pause
