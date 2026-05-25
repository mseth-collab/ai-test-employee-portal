@echo off
cd /d "%~dp0.."
echo.
echo  Healthcare Clinic Bot - Starting...
echo  Browser will open at http://127.0.0.1:8001
echo  Press Ctrl+C to stop.
echo.
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m healthcare_clinic_bot
) else (
    python -m healthcare_clinic_bot
)
pause
