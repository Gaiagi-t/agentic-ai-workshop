@echo off
REM Script per generare certificato SSL self-signed

echo ========================================
echo Generazione Certificato SSL Self-Signed
echo ========================================
echo.

echo Generazione certificato SSL (valido per 365 giorni)...
echo.

REM Prova con openssl standard
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=IT/ST=Italy/L=City/O=IFAB/OU=Workshop/CN=localhost" 2>nul

if exist cert.pem (
    if exist key.pem (
        echo.
        echo ========================================
        echo Certificato generato con successo!
        echo ========================================
        echo.
        echo File creati:
        echo - cert.pem ^(certificato pubblico^)
        echo - key.pem ^(chiave privata^)
        echo.
        echo PROSSIMO PASSO:
        echo 1. Configura Streamlit ^(gia fatto automaticamente^)
        echo 2. Avvia l'app con: start-with-https.bat
        echo 3. Accedi da altri dispositivi con: https://TUO_IP:8501
        echo.
        echo NOTA: Il browser mostrera un warning ^(certificato non fidato^).
        echo Click su "Avanzate" e "Procedi ugualmente" per accettare.
        echo.
        goto :success
    )
)

REM Se fallisce, prova con Git Bash
echo [INFO] Openssl non trovato in PATH, provo con Git Bash...
echo.

if exist "C:\Program Files\Git\usr\bin\openssl.exe" (
    "C:\Program Files\Git\usr\bin\openssl.exe" req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=IT/ST=Italy/L=City/O=IFAB/OU=Workshop/CN=localhost"

    if exist cert.pem (
        if exist key.pem (
            echo.
            echo ========================================
            echo Certificato generato con successo!
            echo ========================================
            echo.
            echo File creati con Git Bash OpenSSL
            echo - cert.pem ^(certificato pubblico^)
            echo - key.pem ^(chiave privata^)
            echo.
            goto :success
        )
    )
)

REM Se ancora fallisce
echo.
echo ========================================
echo [ERRORE] OpenSSL non trovato!
echo ========================================
echo.
echo Opzioni:
echo 1. Installa Git for Windows ^(include OpenSSL^)
echo    Download: https://git-scm.com/download/win
echo.
echo 2. Usa Git Bash manualmente:
echo    - Apri Git Bash
echo    - cd C:\Users\GaiaGambarelli\agentic-ai-workshop
echo    - ./generate-ssl-cert.sh
echo.
echo 3. Usa ngrok invece ^(piu semplice^):
echo    Vedi MICROPHONE_FIX.md
echo.
pause
exit /b 1

:success
pause
