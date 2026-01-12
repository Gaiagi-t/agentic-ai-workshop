# 🤖 Agentic AI Workshop - IFAB

Webapp interattiva per workshop sull'analisi di processi aziendali con Agentic AI.

## 📋 Descrizione

Questa applicazione guida i partecipanti attraverso un'analisi strutturata di processi aziendali prima e dopo l'introduzione dell'Agentic AI, seguendo il framework AS-IS → TO-BE → Analisi.

### Funzionalità principali

- ✍️ **Input testuale e vocale** (tramite Whisper API)
- 📊 **Analisi AI automatica** con Claude 3.5 Sonnet
- 📈 **Visualizzazioni interattive** dei risultati
- 💾 **Export/Import progetto** in formato JSON
- 🎨 **Branding IFAB** personalizzato
- 🔄 **Navigazione step-by-step** con progress tracking

## 🚀 Installazione

### Prerequisiti

- Python 3.8+
- Account Anthropic (per Claude API)
- Account OpenAI (per Whisper API - opzionale per input vocale)

### Setup

1. **Clona o scarica il progetto**

```bash
cd agentic-ai-workshop
```

2. **Crea un ambiente virtuale**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Installa le dipendenze**

```bash
pip install -r requirements.txt
```

4. **Configura le API Keys**

Apri [config.py](config.py) e aggiungi la tua OpenAI API key (se vuoi usare l'input vocale):

```python
OPENAI_API_KEY = "sk-..."  # La tua API key OpenAI
```

> La API key Anthropic è già configurata nel file.

## ▶️ Avvio

```bash
streamlit run app.py
```

L'applicazione si aprirà automaticamente nel browser all'indirizzo `http://localhost:8501`

## 📖 Struttura del Progetto

```
agentic-ai-workshop/
├── app.py                      # App principale
├── config.py                   # Configurazione e API keys
├── requirements.txt            # Dipendenze Python
├── README.md                   # Questo file
├── .streamlit/
│   └── config.toml            # Configurazione tema Streamlit
└── utils/
    ├── __init__.py
    ├── questions.py           # Definizione domande
    ├── data_manager.py        # Export/Import dati
    ├── voice_input.py         # Input vocale con Whisper
    ├── ai_analysis.py         # Analisi AI con Claude
    └── visualizations.py      # Grafici e visualizzazioni
```

## 🎯 Utilizzo

### 1. Sezione AS-IS
Analizza il processo attuale rispondendo a:
- Qual è il processo?
- Quali sono gli step?
- Chi li esegue?
- Quali strumenti vengono usati?
- Quanto tempo richiede?
- Quali sono i problemi?

### 2. Sezione TO-BE
Immagina il processo con Agentic AI:
- Visione del nuovo processo
- Agenti AI necessari
- Input/Output
- Azioni autonome e limiti
- Dati e sistemi
- Flusso agentico
- Benefici e rischi

### 3. Analisi Finale
Genera automaticamente:
- Valutazione fattibilità tecnica
- Analisi Sostituzione vs Augmentation
- Risparmio di tempo e costi
- Identificazione rischi
- Roadmap implementazione
- Raccomandazioni personalizzate
- Score complessivo del progetto

## 🎤 Input Vocale

Per abilitare l'input vocale:

1. Configura la tua OpenAI API key in [config.py](config.py)
2. Nell'app, vai alla tab "🎤 Parla"
3. Clicca per registrare la tua risposta
4. La trascrizione apparirà automaticamente

> **Costo**: ~$0.006/minuto di audio con Whisper

## 💾 Salvataggio e Caricamento

- **Esporta progetto**: Scarica un file JSON con tutte le risposte
- **Importa progetto**: Carica un file JSON precedentemente salvato
- I file JSON includono metadati, risposte e analisi

## 🎨 Personalizzazione

### Colori IFAB

I colori del brand sono definiti in [config.py](config.py):

```python
COLORS = {
    "primary": "#1E3A8A",      # Navy blue
    "secondary": "#F97316",    # Orange
    "background": "#F8FAFC",   # Light gray
    # ...
}
```

### Template Flussi Agentici

I template dei flussi sono configurabili in [config.py](config.py):

- Single Agent
- Multi-Agent Sequenziale
- Multi-Agent Parallelo
- Orchestrator
- Router con Escalation
- Loop con Feedback

## 🔧 Troubleshooting

### Errore: "No module named 'anthropic'"
```bash
pip install --upgrade anthropic
```

### Errore: "OpenAI API key not found"
Configura la chiave in [config.py](config.py) oppure inseriscila nell'app

### L'app non si avvia
```bash
# Verifica che Streamlit sia installato
streamlit --version

# Reinstalla le dipendenze
pip install -r requirements.txt --force-reinstall
```

## 📝 Note per il Workshop

### Modalità Live (proiettata)
- Font e contrasti ottimizzati per proiezione
- Progress bar visibile
- Ogni partecipante può seguire sullo schermo

### Modalità Individuale
- Ogni partecipante può usare la propria istanza
- Possibilità di salvare/caricare i propri progetti
- Lavoro asincrono supportato

## 🤝 Contributi

Per bug, suggerimenti o miglioramenti, contatta il team IFAB.

## 📄 Licenza

© 2024 IFAB - International Foundation Big Data & Artificial Intelligence for Human Development

---

**Developed with ❤️ for IFAB Workshop**

Per supporto: [www.ifabfoundation.org](https://www.ifabfoundation.org)
