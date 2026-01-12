# 🔒 Setup HTTPS Locale - Guida Rapida

Questa guida ti aiuta a configurare HTTPS sulla tua rete locale per far funzionare il microfono su altri dispositivi.

---

## 🚀 Quick Start (3 Passi)

### **Passo 1: Genera Certificati SSL**

**Windows:**
```cmd
# Doppio click su:
generate-ssl-cert.bat
```

**Mac/Linux:**
```bash
chmod +x generate-ssl-cert.sh
./generate-ssl-cert.sh
```

Questo crea 2 file:
- `cert.pem` - Certificato pubblico
- `key.pem` - Chiave privata

---

### **Passo 2: Abilita HTTPS in Streamlit**

Apri [.streamlit/config.toml](.streamlit/config.toml) e **decommenta** le ultime 2 righe:

**Prima:**
```toml
# sslCertFile = "cert.pem"
# sslKeyFile = "key.pem"
```

**Dopo:**
```toml
sslCertFile = "cert.pem"
sslKeyFile = "key.pem"
```

✅ Salva il file.

---

### **Passo 3: Avvia l'App con HTTPS**

**Windows:**
```cmd
# Doppio click su:
start-with-https.bat
```

**Mac/Linux:**
```bash
chmod +x start-with-https.sh
./start-with-https.sh
```

Vedrai:
```
Locale (questo computer):
  https://localhost:8501

Rete locale (altri dispositivi):
  https://192.168.1.16:8501
          👆 Condividi questo URL!
```

---

## 🌐 Accedere dall'App

### Dal tuo computer:
1. Apri browser
2. Vai su `https://localhost:8501`
3. ✅ Funziona!

### Da altri dispositivi (smartphone, tablet, altro PC):
1. Apri browser
2. Vai su `https://192.168.1.16:8501` (usa il TUO IP)
3. ⚠️ **Vedrai un WARNING:** "La connessione non è privata" o "Your connection is not private"
4. ✅ **Click su "Avanzate" → "Procedi ugualmente"**
5. ✅ Ora il microfono funziona!

---

## ❓ FAQ

### **Q: Perché il browser mostra un warning?**

**A:** Perché il certificato è "self-signed" (auto-firmato), non emesso da una Certificate Authority ufficiale. È normale e sicuro in questo contesto.

---

### **Q: Come accettare il certificato sul browser?**

**Chrome/Edge:**
1. Click su "Avanzate" o "Advanced"
2. Click su "Procedi su localhost (non sicuro)" o "Proceed to localhost (unsafe)"

**Firefox:**
1. Click su "Avanzate" o "Advanced"
2. Click su "Accetta il rischio e continua" o "Accept the Risk and Continue"

**Safari (iOS):**
1. Click su "Mostra dettagli" o "Show Details"
2. Click su "visita questo sito web" o "visit this website"
3. Conferma

---

### **Q: Ogni volta devo accettare il warning?**

**A:** Dipende dal browser:
- **Desktop:** Il browser ricorda la scelta (solo la prima volta)
- **Mobile:** Potrebbe chiedere ogni volta (dipende dal browser e sistema operativo)

---

### **Q: Il certificato ha una scadenza?**

**A:** Sì, il certificato generato è valido per **365 giorni**. Dopo un anno, devi rigenerare i certificati:

```bash
# Elimina vecchi certificati
rm cert.pem key.pem

# Rigenera
./generate-ssl-cert.bat  # Windows
./generate-ssl-cert.sh   # Mac/Linux
```

---

### **Q: Posso usare questo setup in produzione?**

**A:** ❌ **No!** Questo setup è solo per:
- Workshop locali
- Test su rete locale
- Demo interne

Per produzione, usa:
- **Streamlit Cloud** (HTTPS automatico, certificato ufficiale)
- **Cloud Provider** con certificato Let's Encrypt
- Vedi [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

### **Q: Non ho OpenSSL, cosa faccio?**

**Windows:**
- **Opzione 1:** Installa Git for Windows (include OpenSSL): [git-scm.com/download/win](https://git-scm.com/download/win)
- **Opzione 2:** Usa Git Bash (se già installato) per eseguire `generate-ssl-cert.sh`
- **Opzione 3:** Scarica OpenSSL standalone: [slproweb.com/products/Win32OpenSSL.html](https://slproweb.com/products/Win32OpenSSL.html)

**Mac:**
```bash
brew install openssl
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install openssl
```

---

### **Q: Come trovo il mio IP locale?**

**Windows:**
```cmd
ipconfig
# Cerca "Indirizzo IPv4" o "IPv4 Address"
# Es. 192.168.1.16
```

**Mac:**
```bash
ifconfig | grep "inet "
# Es. inet 192.168.1.16
```

**Linux:**
```bash
ip addr show
# Oppure:
hostname -I
```

---

### **Q: Il microfono non funziona ancora, cosa faccio?**

**Controlla:**
1. ✅ Stai usando `https://` (NON `http://`)
2. ✅ Hai accettato il certificato nel browser
3. ✅ Il browser chiede permesso per il microfono (clicca "Consenti")
4. ✅ Il microfono funziona in altre app (Zoom, Meet, ecc.)
5. ✅ I file `cert.pem` e `key.pem` esistono nella cartella del progetto
6. ✅ Le righe `sslCertFile` e `sslKeyFile` in `config.toml` sono **decommentate** (senza `#`)

---

## 🔄 Tornare a HTTP (senza HTTPS)

Se vuoi tornare a HTTP normale:

**Opzione 1: Commenta le righe in config.toml**

Apri [.streamlit/config.toml](.streamlit/config.toml):

```toml
# sslCertFile = "cert.pem"  # ← Aggiungi # all'inizio
# sslKeyFile = "key.pem"    # ← Aggiungi # all'inizio
```

**Opzione 2: Avvia con comando normale**

```bash
streamlit run app.py
# Invece di:
# streamlit run app.py --server.address=0.0.0.0
```

Accedi con `http://localhost:8501` (ma il microfono NON funzionerà su rete locale).

---

## 📊 Confronto Soluzioni

| Caratteristica | HTTPS Locale | ngrok | Streamlit Cloud |
|----------------|--------------|-------|-----------------|
| **Setup iniziale** | 5 minuti | 5 minuti | 5 minuti |
| **URL stabile** | ✅ Sì | ❌ Cambia | ✅ Sì |
| **Internet richiesto** | ❌ No | ✅ Sì | ✅ Sì |
| **Warning browser** | ⚠️ Sì | ✅ No | ✅ No |
| **Accesso pubblico** | ❌ Solo LAN | ✅ Sì | ✅ Sì |
| **Costo** | Gratis | Gratis | Gratis |
| **Microfono funziona** | ✅ Sì | ✅ Sì | ✅ Sì |

**Raccomandazione:**
- **Workshop in presenza (LAN):** HTTPS Locale (questa guida)
- **Workshop online/remoto:** ngrok o Streamlit Cloud
- **Produzione:** Streamlit Cloud

---

## 🛠️ Troubleshooting

### **Errore: "Address already in use"**

Un'altra istanza di Streamlit è già in esecuzione.

**Fix:**
```bash
# Trova processo
netstat -ano | findstr :8501  # Windows
lsof -i :8501                 # Mac/Linux

# Killa processo
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Mac/Linux
```

---

### **Errore: "ssl.SSLError: [SSL] PEM lib"**

I file `cert.pem` o `key.pem` sono corrotti o mancanti.

**Fix:**
```bash
# Elimina e rigenera
rm cert.pem key.pem
./generate-ssl-cert.bat  # Windows
./generate-ssl-cert.sh   # Mac/Linux
```

---

### **Browser: "NET::ERR_CERT_AUTHORITY_INVALID"**

È normale con certificati self-signed.

**Fix:** Click su "Avanzate" → "Procedi ugualmente" (vedi sopra)

---

## 📞 Supporto

Per altri problemi, vedi:
- [MICROPHONE_FIX.md](MICROPHONE_FIX.md) - Guida completa microfono
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Altre soluzioni deployment

---

**Buon workshop con HTTPS! 🔒✨**
