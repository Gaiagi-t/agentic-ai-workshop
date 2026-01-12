# 🚀 Quick Start Guide

## Installazione Rapida

```bash
# 1. Naviga nella directory del progetto
cd agentic-ai-workshop

# 2. Crea ambiente virtuale
python -m venv venv

# 3. Attiva ambiente virtuale
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Installa dipendenze
pip install -r requirements.txt

# 5. Avvia l'app
streamlit run app.py
```

## ⚙️ Configurazione API Keys

### API Key Anthropic (Claude) - GIÀ CONFIGURATA ✅
La chiave è già presente in `config.py`

### API Key OpenAI (Whisper) - OPZIONALE
Per l'input vocale, aggiungi la tua chiave in `config.py`:

```python
OPENAI_API_KEY = "sk-..."
```

Oppure configurala direttamente nell'interfaccia dell'app.

## 📱 Prima Esecuzione

1. Apri il browser all'indirizzo mostrato (di solito `http://localhost:8501`)
2. Vedrai la schermata principale con il logo IFAB
3. Inizia dalla sezione **AS-IS** nella sidebar
4. Rispondi alle domande usando:
   - Tab **✍️ Scrivi** per input testuale
   - Tab **🎤 Parla** per input vocale (richiede OpenAI API key)

## 📊 Flusso di Lavoro

```
AS-IS (6 domande)
    ↓
TO-BE (12 domande)
    ↓
Analisi Finale (AI-powered)
```

## 💾 Funzionalità Chiave

- **Salta domande opzionali**: usa il bottone "⏭️ Salta"
- **Naviga avanti/indietro**: usa "➡️ Avanti" e "⬅️ Indietro"
- **Salva progetto**: usa "📥 Esporta Progetto (JSON)" nella sidebar
- **Carica progetto**: usa "📤 Importa Progetto" nella sidebar
- **Genera analisi AI**: completa AS-IS e TO-BE, poi vai su "Analisi Finale"

## 🎯 Template Flussi Agentici

Nella domanda sul flusso agentico, puoi scegliere tra:

1. **Single Agent**: Un agente gestisce tutto
2. **Multi-Agent Sequenziale**: Agenti in catena
3. **Multi-Agent Parallelo**: Agenti in parallelo
4. **Orchestrator**: Un orchestratore coordina gli altri
5. **Router con Escalation**: Routing intelligente con escalation
6. **Loop con Feedback**: Cicli iterativi di miglioramento

## 🐛 Risoluzione Problemi Comuni

### App non si avvia
```bash
# Verifica installazione Streamlit
streamlit --version

# Reinstalla dipendenze
pip install -r requirements.txt --force-reinstall
```

### Errore "No module named..."
```bash
# Assicurati che l'ambiente virtuale sia attivo
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

pip install -r requirements.txt
```

### Input vocale non funziona
1. Verifica che OpenAI API key sia configurata
2. Controlla la connessione internet
3. Se usi browser Safari, prova con Chrome

## 📞 Supporto

Per problemi o domande:
- Email: info@ifabfoundation.org
- Website: www.ifabfoundation.org

---

**Buon workshop! 🎓**
