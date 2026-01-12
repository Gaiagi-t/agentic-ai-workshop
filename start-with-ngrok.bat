@echo off
REM Script per avviare l'app con ngrok (HTTPS pubblico)

echo ========================================
echo Agentic AI Workshop - Avvio con ngrok
echo ========================================
echo.

REM Attiva ambiente virtuale
call venv\Scripts\activate.bat

REM Avvia Streamlit in background
echo [1/2] Avvio Streamlit...
start /B streamlit run app.py --server.port=8501

REM Aspetta 3 secondi
timeout /t 3 /nobreak >nul

REM Avvia ngrok
echo [2/2] Avvio ngrok tunnel HTTPS...
echo.
echo IMPORTANTE: Copia l'URL HTTPS che appare sotto (es. https://abc123.ngrok.io)
echo Condividi quell'URL con i tuoi utenti!
echo.
echo Il microfono funzionera' perche' usa HTTPS!
echo.

ngrok http 8501
