# 🚀 Guida al Deployment - Agentic AI Workshop

Questa guida spiega come rendere l'app disponibile ad altri utenti.

---

## Opzione 1️⃣: Streamlit Cloud (Raccomandato - Gratis)

### ✅ Pro
- Completamente gratuito
- Deploy in 2 minuti
- URL pubblico automatico (es. `https://your-app.streamlit.app`)
- Auto-aggiornamenti da GitHub
- SSL/HTTPS automatico

### 📋 Requisiti
- Account GitHub (gratuito)
- Account Streamlit Cloud (gratuito - login con GitHub)

### 🎯 Step-by-Step

#### 1. Prepara il repository GitHub

```bash
# Se non hai ancora un repo GitHub
git init
git add .
git commit -m "Initial commit - Agentic AI Workshop"

# Crea repo su github.com e poi:
git remote add origin https://github.com/TUO_USERNAME/agentic-ai-workshop.git
git push -u origin main
```

#### 2. Deploy su Streamlit Cloud

1. Vai su [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Seleziona:
   - **Repository:** `TUO_USERNAME/agentic-ai-workshop`
   - **Branch:** `main`
   - **Main file:** `app.py` (per V1) o `app_v2.py` (per V2)
4. Click **"Advanced settings"** → **"Secrets"**
5. Aggiungi le API keys:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   OPENAI_API_KEY = "sk-proj-..."
   ```
6. Click **"Deploy"**
7. Attendi 2-3 minuti ⏱️
8. ✅ App live! URL: `https://your-app.streamlit.app`

#### 3. Condividi l'URL

Manda l'URL ai tuoi utenti:
- **V1:** `https://your-app-v1.streamlit.app`
- **V2:** `https://your-app-v2.streamlit.app`

### 🔒 Gestione API Keys

**Opzione A: API Keys Centrali (più semplice)**
- Tu inserisci le API keys nelle secrets di Streamlit Cloud
- Tutti gli utenti usano le tue API keys
- ⚠️ Tu paghi per tutti gli utenti

**Opzione B: API Keys per Utente (più sicuro)**
- Rimuovi le API keys da `config.py`
- Gli utenti inseriscono le loro API keys nell'app
- Ogni utente paga per sé

Per abilitare Opzione B, modifica [config.py](config.py):
```python
# Lascia vuoto - utenti inseriranno le loro keys
ANTHROPIC_API_KEY = ""
OPENAI_API_KEY = ""
```

---

## Opzione 2️⃣: Docker + Cloud Provider

### ✅ Pro
- Controllo completo
- Scalabile
- Funziona su AWS, Azure, Google Cloud, DigitalOcean, etc.

### 📋 Requisiti
- Docker installato
- Account cloud provider (AWS/Azure/GCP/DigitalOcean)

### 🎯 Deployment Locale (Test)

#### 1. Crea file .env

```bash
# Copia l'esempio
cp .env.example .env

# Modifica .env e inserisci le tue API keys
nano .env
```

#### 2. Build e Run con Docker Compose

```bash
# Build
docker-compose build

# Avvia V1 (porta 8501)
docker-compose up app-v1

# Avvia V2 (porta 8502)
docker-compose up app-v2

# Avvia entrambe
docker-compose up
```

#### 3. Accedi all'app

- **V1:** http://localhost:8501
- **V2:** http://localhost:8502

### 🌐 Deployment su Cloud

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p docker agentic-ai-workshop

# Deploy
eb create agentic-ai-env
eb open
```

#### Google Cloud Run
```bash
# Build immagine
gcloud builds submit --tag gcr.io/PROJECT_ID/agentic-ai-workshop

# Deploy
gcloud run deploy --image gcr.io/PROJECT_ID/agentic-ai-workshop --platform managed
```

#### DigitalOcean App Platform
1. Vai su [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)
2. Click **"Create App"**
3. Connetti GitHub repo
4. Seleziona Dockerfile
5. Aggiungi environment variables (API keys)
6. Deploy! 🚀

---

## Opzione 3️⃣: Condivisione Locale (LAN/VPN)

### ✅ Pro
- Nessun costo cloud
- Dati rimangono interni
- Ideale per workshop in presenza

### 🎯 Setup

#### 1. Avvia l'app con indirizzo pubblico

```bash
# Invece di:
streamlit run app.py

# Usa:
streamlit run app.py --server.address=0.0.0.0
```

#### 2. Trova il tuo IP locale

**Windows:**
```cmd
ipconfig
# Cerca "IPv4 Address" (es. 192.168.1.100)
```

**Mac/Linux:**
```bash
ifconfig
# Cerca "inet" (es. 192.168.1.100)
```

#### 3. Condividi l'URL

Gli utenti sulla stessa rete possono accedere a:
```
http://192.168.1.100:8501
```

### 🔒 Sicurezza
Per accesso esterno via VPN:
- Configura Tailscale/ZeroTier
- Oppure usa ngrok:
  ```bash
  ngrok http 8501
  ```

---

## Opzione 4️⃣: GitHub + Istruzioni Setup

### ✅ Pro
- Utenti installano in locale
- Massima privacy
- Nessun costo

### 📋 Aggiorna README.md

Aggiungi istruzioni chiare:

```markdown
## 🚀 Quick Start per Utenti

### 1. Clona il repository
git clone https://github.com/TUO_USERNAME/agentic-ai-workshop.git
cd agentic-ai-workshop

### 2. Installa dipendenze
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

### 3. Configura API Keys
Copia config.py.example in config.py e inserisci le tue API keys

### 4. Avvia l'app
streamlit run app.py
```

---

## 🎯 Raccomandazioni

| Scenario | Soluzione Raccomandata |
|----------|------------------------|
| **Workshop pubblico (1-100 utenti)** | Streamlit Cloud (Opzione A) |
| **Enterprise/Azienda** | Docker + Cloud Provider |
| **Workshop in presenza** | Condivisione Locale |
| **Open source/Community** | GitHub + Istruzioni |
| **Demo veloce** | Streamlit Cloud |
| **Massima privacy** | Docker self-hosted |

---

## 📊 Costi Stimati

### Streamlit Cloud (Opzione A - API keys centrali)

**Con 50 utenti/giorno:**
- Streamlit Cloud: **Gratis** ✅
- Anthropic API (Claude):
  - V1: ~€0.02/analisi → €1/giorno
  - V2: ~€0.01/analisi → €0.50/giorno
- OpenAI API (Whisper): ~€0.006/minuto → €0.30/giorno

**Totale:** ~€1.80/giorno (€54/mese)

### Cloud Provider (Docker)
- AWS Fargate: ~€20-50/mese
- Google Cloud Run: ~€15-40/mese
- DigitalOcean App: €12-25/mese

---

## 🔐 Sicurezza

### Protezione API Keys

Se usi API keys centrali, limita l'uso:

**Anthropic Console:**
1. Vai su [console.anthropic.com](https://console.anthropic.com)
2. Settings → Limits
3. Imposta budget mensile (es. €100/mese)

**OpenAI Platform:**
1. Vai su [platform.openai.com/usage](https://platform.openai.com/usage)
2. Settings → Limits
3. Imposta hard limit (es. €50/mese)

### Autenticazione Utenti

Per limitare l'accesso, usa `streamlit-authenticator`:

```python
# pip install streamlit-authenticator
import streamlit_authenticator as stauth

# Aggiungi login in app.py
```

---

## 📞 Supporto

Per problemi di deployment:
1. Check [Streamlit Community Forum](https://discuss.streamlit.io)
2. Check [GitHub Issues](https://github.com/TUO_USERNAME/agentic-ai-workshop/issues)
3. Contatta l'amministratore

---

**Buon deployment! 🚀**
