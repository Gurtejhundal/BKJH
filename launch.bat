@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Bibi Kaulan Ji Hospital Website

set "HOST=127.0.0.1"
set "PORT=8000"
set "VENV_PY=.venv\Scripts\python.exe"

echo.
echo Starting Bibi Kaulan Ji Hospital website...
echo Project folder: %CD%
echo.

if not exist "%VENV_PY%" (
  echo Local virtual environment was not found. Creating .venv...
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3 -m venv .venv
  ) else (
    where python >nul 2>nul
    if errorlevel 1 goto missing_python
    python -m venv .venv
  )
)

if not exist "%VENV_PY%" goto venv_failed

echo Installing required packages...
"%VENV_PY%" -m pip install -r requirements.txt
if errorlevel 1 goto install_failed

echo Applying database migrations...
"%VENV_PY%" manage.py migrate
if errorlevel 1 goto migrate_failed

echo.
echo Website URL: http://%HOST%:%PORT%/
if /I not "%NO_BROWSER%"=="1" start "" "http://%HOST%:%PORT%/"
echo Press CTRL+C to stop the server.
echo.
"%VENV_PY%" manage.py runserver %HOST%:%PORT%
goto finished

:missing_python
echo.
echo ERROR: Python was not found.
echo Install Python 3, then run this launcher again.
goto failed

:venv_failed
echo.
echo ERROR: Could not create the local .venv environment.
goto failed

:install_failed
echo.
echo ERROR: Package installation failed.
echo Check your internet connection and requirements.txt, then try again.
goto failed

:migrate_failed
echo.
echo ERROR: Database migration failed.
goto failed

:failed
echo.
pause
exit /b 1

:finished
echo.
echo Server stopped.
pause
endlocal
