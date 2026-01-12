#!/bin/bash
# Script per generare certificato SSL self-signed

echo "========================================"
echo "Generazione Certificato SSL Self-Signed"
echo "========================================"
echo ""

# Verifica se OpenSSL è installato
if ! command -v openssl &> /dev/null; then
    echo "[ERRORE] OpenSSL non trovato!"
    echo ""
    echo "Installalo con:"
    echo "  Ubuntu/Debian: sudo apt-get install openssl"
    echo "  macOS: brew install openssl"
    echo ""
    exit 1
fi

echo "Generazione certificato SSL (valido per 365 giorni)..."
echo ""

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes \
    -subj "/C=IT/ST=Italy/L=City/O=IFAB/OU=Workshop/CN=localhost"

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Certificato generato con successo!"
    echo "========================================"
    echo ""
    echo "File creati:"
    echo "- cert.pem (certificato pubblico)"
    echo "- key.pem (chiave privata)"
    echo ""
    echo "PROSSIMO PASSO:"
    echo "1. Configura Streamlit (già fatto automaticamente)"
    echo "2. Avvia l'app con: streamlit run app.py --server.address=0.0.0.0"
    echo "3. Accedi da altri dispositivi con: https://TUO_IP:8501"
    echo ""
    echo "Trova il tuo IP con: ifconfig | grep 'inet '"
    echo ""
    echo "NOTA: Il browser mostrerà un warning (certificato non fidato)."
    echo "Click su 'Avanzate' e 'Procedi ugualmente' per accettare."
    echo ""
else
    echo ""
    echo "[ERRORE] Generazione certificato fallita."
    echo ""
    exit 1
fi
