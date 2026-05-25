@echo off
cd /d "%~dp0.."
echo.
echo  BestFrAIend - Starting...
echo  Open http://127.0.0.1:8003 in your browser
echo  Press Ctrl+C to stop.
echo.
if exist ".venv\Scripts\python.exe" (
    .venv\Scripts\python.exe -m bestfraiend
) else (
    python -m bestfraiend
)
pause
