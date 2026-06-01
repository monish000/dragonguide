@echo off
SETLOCAL

echo.
echo  ============================================================
echo   DragonGuide - Automated Setup (Windows)
echo  ============================================================
echo.

REM Check Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] Python not found. Install from https://python.org
    pause & exit /b 1
)

REM Create virtual environment
echo [1/4] Creating virtual environment (Python 3.11)...
py -3.11 -m venv venv 2>nul || python -m venv venv
CALL venv\Scripts\activate.bat

REM Install dependencies
echo [2/4] Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo        Done.

REM Check .env
echo [3/4] Checking .env file...
IF NOT EXIST .env (
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo        .env created. EDIT IT and add your OpenAI API key before continuing.
    pause
) ELSE (
    findstr /C:"your_openai_api_key_here" .env >nul 2>&1
    IF NOT ERRORLEVEL 1 (
        echo        WARNING: .env still has placeholder key. Edit .env now.
        pause
    ) ELSE (
        echo        .env OK.
    )
)

REM Check data folder
echo [4/4] Checking data/ folder...
dir /b data\*.pdf data\*.txt >nul 2>&1
IF ERRORLEVEL 1 (
    echo.
    echo  [!] No PDF or TXT files found in data\.
    echo      Add Drexel policy documents to the data\ folder.
    echo.
) ELSE (
    echo        Documents found. Refreshing from Drexel.edu ...
    set PYTHONIOENCODING=utf-8
    python download_docs.py
    python ingest.py
)

echo.
echo  ============================================================
echo   Setup complete!
echo   Launch with:  streamlit run main.py
echo  ============================================================
echo.
CALL venv\Scripts\activate.bat
pause
ENDLOCAL
