# 🎤 Guida: Far Funzionare il Microfono su Rete Locale

## 🚨 Il Problema

Quando accedi all'app tramite **Network URL** (es. `http://192.168.1.16:8501`), il microfono **non funziona**.

### Perché?

I browser moderni **bloccano l'accesso al microfono** su connessioni HTTP non-localhost per motivi di sicurezza.

**Il microfono funziona solo con:**
- ✅ `http://localhost:8501` (locale)
- ✅ `https://qualsiasi-dominio.com` (HTTPS)
- ❌ `http://192.168.1.16:8501` (HTTP rete locale) ← **Non funziona!**

---

## ✅ Soluzioni

### **Soluzione 1: ngrok (RACCOMANDATO - 5 minuti) 🚀**

ngrok crea un tunnel HTTPS pubblico che permette al microfono di funzionare.

#### Setup Iniziale (una volta sola)

1. **Scarica ngrok:**
   - Vai su [ngrok.com/download](https://ngrok.com/download)
   - Scarica per Windows/Mac/Linux
   - Estrai il file (es. `ngrok.exe`)
   - Mettilo in una cartella nel PATH, oppure nella cartella del progetto

2. **Registrati gratis:**
   - Crea account su [ngrok.com](https://ngrok.com)
   - Copia il tuo authtoken
   - Esegui: `ngrok authtoken TUO_TOKEN`

#### Uso Quotidiano

**Windows:**
```cmd
# Clicca su start-with-ngrok.bat
# Oppure:
ngrok http 8501
```

**Mac/Linux:**
```bash
chmod +x start-with-ngrok.sh
./start-with-ngrok.sh
```

#### Cosa Succede

```
ngrok by @inconshreveable

Session Status                online
Account                       Your Name (Plan: Free)
Forwarding                    https://abc123.ngrok.io -> http://localhost:8501

👆 COPIA QUESTO URL HTTPS E CONDIVIDILO!
```

**Condividi:** `https://abc123.ngrok.io`

✅ **Il microfono funziona!** (perché usa HTTPS)

#### Pro e Contro

✅ **Pro:**
- Setup in 5 minuti
- HTTPS automatico
- URL pubblico (accessibile da internet)
- Gratis per uso base

❌ **Contro:**
- URL cambia ad ogni riavvio (es. `abc123.ngrok.io` → `xyz789.ngrok.io`)
- Piano Free: massimo 60 connessioni/minuto
- Dipendenza da servizio esterno

---

### **Soluzione 2: HTTPS Locale con Certificato Self-Signed 🔒**

Configura Streamlit per usare HTTPS su rete locale.

#### Setup

1. **Genera certificato SSL:**

**Windows (PowerShell come Amministratore):**
```powershell
# Installa OpenSSL (se non ce l'hai)
# Oppure usa Git Bash

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**Mac/Linux:**
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

Quando chiede informazioni, premi INVIO per accettare default.

2. **Configura Streamlit:**

Crea o modifica [.streamlit/config.toml](.streamlit/config.toml):

```toml
[server]
enableCORS = false
enableXsrfProtection = false
sslCertFile = "cert.pem"
sslKeyFile = "key.pem"
```

3. **Avvia l'app:**

```bash
streamlit run app.py --server.address=0.0.0.0
```

4. **Accedi da altro dispositivo:**

```
https://192.168.1.16:8501
```

⚠️ **Il browser mostrerà warning** (certificato non fidato) - clicca "Avanzate" → "Procedi ugualmente"

#### Pro e Contro

✅ **Pro:**
- Funziona offline
- Nessuna dipendenza esterna
- URL stabile

❌ **Contro:**
- Warning del browser (certificato self-signed)
- Setup più complesso
- Gli utenti devono accettare il warning

---

### **Soluzione 3: Tailscale Funnel (Per Team) 🌐**

Se hai un team che usa Tailscale VPN.

#### Setup

1. **Installa Tailscale:**
   - [tailscale.com/download](https://tailscale.com/download)

2. **Avvia Streamlit:**
   ```bash
   streamlit run app.py
   ```

3. **Esponi con Funnel:**
   ```bash
   tailscale funnel 8501
   ```

4. **Condividi URL:**
   ```
   https://your-machine.tailnet-name.ts.net
   ```

✅ HTTPS automatico, nessun certificato da gestire!

---

### **Soluzione 4: Solo Testo (Fallback) ✍️**

Se non puoi usare HTTPS, **disabilita il microfono** e usa solo input testuale.

#### Modifica app

In [utils/voice_input.py](utils/voice_input.py), commenta la funzione voice:

```python
def render_voice_or_text_input(...):
    # Create tabs for voice and text input
    # tab1, tab2 = st.tabs(["✍️ Scrivi", "🎤 Parla"])  # DISABILITATO

    # Solo tab testuale
    user_input = st.text_area(
        question_text,
        value=st.session_state.answers.get(question_id, ""),
        placeholder=placeholder,
        help=help_text,
        height=rows * 30,
        key=f"text_{question_id}"
    )

    return user_input
```

✅ Funziona su qualsiasi HTTP, ma **niente input vocale**.

---

## 🎯 Raccomandazione per Caso d'Uso

| Scenario | Soluzione Migliore |
|----------|-------------------|
| **Workshop veloce (1-2 ore)** | ngrok (Soluzione 1) |
| **Workshop ricorrente** | Streamlit Cloud (vedi DEPLOYMENT_GUIDE.md) |
| **Team interno con VPN** | Tailscale Funnel (Soluzione 3) |
| **Offline/senza internet** | HTTPS Self-Signed (Soluzione 2) |
| **Nessuna alternativa** | Solo Testo (Soluzione 4) |

---

## 📋 Quick Start: ngrok (5 minuti)

```bash
# 1. Scarica ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# 2. Registrati e autentica
ngrok authtoken TUO_TOKEN_DA_NGROK_COM

# 3. Avvia Streamlit
streamlit run app.py &

# 4. Avvia ngrok
ngrok http 8501

# 5. Copia URL HTTPS e condividi!
```

**Windows:** Doppio click su `start-with-ngrok.bat`

---

## 🐛 Troubleshooting

### "This site can't provide a secure connection" con HTTPS locale

**Causa:** Certificato self-signed non fidato

**Fix:**
1. Click su "Advanced" nel browser
2. Click su "Proceed to 192.168.1.16 (unsafe)"
3. ✅ Il microfono ora funziona

### ngrok: "ERR_NGROK_108"

**Causa:** Troppi tunnel aperti (Free plan: max 1)

**Fix:**
```bash
# Chiudi tutti i tunnel
killall ngrok

# Riavvia
ngrok http 8501
```

### Il microfono non funziona neanche con ngrok

**Controlla:**
1. ✅ Stai usando l'URL **HTTPS** di ngrok (non HTTP)
2. ✅ Il browser chiede permesso microfono (clicca "Consenti")
3. ✅ Il microfono funziona in altre app (Google Meet, Zoom)

---

## 💡 Suggerimento Pro

Per workshop frequenti, usa **Streamlit Cloud** (vedi [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)):

- ✅ HTTPS automatico
- ✅ URL permanente
- ✅ Zero configurazione
- ✅ Gratis

Setup in 5 minuti, microfono funziona sempre! 🎤✨

---

**Problemi?** Apri un issue su GitHub o contatta l'amministratore.
