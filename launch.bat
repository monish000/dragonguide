@echo off
echo.
echo  ============================================================
echo   DragonGuide — Launch App
echo  ============================================================
echo.
cd /d "%~dp0"
CALL venv\Scripts\activate.bat 2>nul || (
    echo  [!] Virtual environment not found. Run setup.bat first.
    pause & exit /b 1
)
set PYTHONIOENCODING=utf-8
streamlit run main.py
