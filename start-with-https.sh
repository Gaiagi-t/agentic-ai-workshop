#!/bin/bash
# Script per avviare l'app con HTTPS locale

echo "========================================"
echo "Agentic AI Workshop - Avvio con HTTPS"
echo "========================================"
echo ""

# Verifica se i certificati esistono
if [ ! -f "cert.pem" ]; then
    echo "[ERRORE] Certificato SSL non trovato!"
    echo ""
    echo "Genera prima i certificati con:"
    echo "  ./generate-ssl-cert.sh"
    echo ""
    exit 1
fi

if [ ! -f "key.pem" ]; then
    echo "[ERRORE] Chiave privata SSL non trovata!"
    echo ""
    echo "Genera prima i certificati con:"
    echo "  ./generate-ssl-cert.sh"
    echo ""
    exit 1
fi

# Attiva ambiente virtuale
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

echo "[OK] Certificati SSL trovati"
echo ""

# Trova IP locale
IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

echo "========================================"
echo "Server in avvio..."
echo "========================================"
echo ""
echo "Locale (questo computer):"
echo "  https://localhost:8501"
echo "  https://127.0.0.1:8501"
echo ""
echo "Rete locale (altri dispositivi):"
echo "  https://$IP:8501"
echo ""
echo "IMPORTANTE:"
echo "Il browser mostrerà un WARNING (certificato non fidato)."
echo ""
echo "Come procedere:"
echo "1. Click su 'Avanzate' o 'Advanced'"
echo "2. Click su 'Procedi su localhost (non sicuro)' o 'Proceed to localhost (unsafe)'"
echo "3. Il microfono funzionerà!"
echo ""
echo "========================================"
echo ""

# Avvia Streamlit con HTTPS
streamlit run app.py --server.address=0.0.0.0
