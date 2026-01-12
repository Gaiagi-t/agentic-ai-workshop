@echo off
REM Script per avviare l'app con HTTPS locale

echo ========================================
echo Agentic AI Workshop - Avvio con HTTPS
echo ========================================
echo.

REM Verifica se i certificati esistono
if not exist "cert.pem" (
    echo [ERRORE] Certificato SSL non trovato!
    echo.
    echo Genera prima i certificati con:
    echo   generate-ssl-cert.bat
    echo.
    pause
    exit /b 1
)

if not exist "key.pem" (
    echo [ERRORE] Chiave privata SSL non trovata!
    echo.
    echo Genera prima i certificati con:
    echo   generate-ssl-cert.bat
    echo.
    pause
    exit /b 1
)

REM Attiva ambiente virtuale
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

echo [OK] Certificati SSL trovati
echo.

REM Trova IP locale
echo Cerco il tuo indirizzo IP locale...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)

:found_ip
set IP=%IP: =%
echo.
echo ========================================
echo Server in avvio...
echo ========================================
echo.
echo Locale (questo computer):
echo   https://localhost:8501
echo   https://127.0.0.1:8501
echo.
echo Rete locale (altri dispositivi):
echo   https://%IP%:8501
echo.
echo IMPORTANTE:
echo Il browser mostrera' un WARNING (certificato non fidato).
echo.
echo Come procedere:
echo 1. Click su "Avanzate" o "Advanced"
echo 2. Click su "Procedi su localhost (non sicuro)" o "Proceed to localhost (unsafe)"
echo 3. Il microfono funzionera'!
echo.
echo ========================================
echo.

REM Avvia Streamlit con HTTPS
streamlit run app.py --server.address=0.0.0.0
