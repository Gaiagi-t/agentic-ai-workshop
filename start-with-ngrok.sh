#!/bin/bash
# Script per avviare l'app con ngrok (HTTPS pubblico)

echo "========================================"
echo "Agentic AI Workshop - Avvio con ngrok"
echo "========================================"
echo ""

# Attiva ambiente virtuale
source venv/bin/activate

# Avvia Streamlit in background
echo "[1/2] Avvio Streamlit..."
streamlit run app.py --server.port=8501 &

# Aspetta 3 secondi
sleep 3

# Avvia ngrok
echo "[2/2] Avvio ngrok tunnel HTTPS..."
echo ""
echo "IMPORTANTE: Copia l'URL HTTPS che appare sotto (es. https://abc123.ngrok.io)"
echo "Condividi quell'URL con i tuoi utenti!"
echo ""
echo "Il microfono funzionerà perché usa HTTPS!"
echo ""

ngrok http 8501
