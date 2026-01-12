# 🔧 Fix per errore "unexpected keyword argument 'proxies'"

## Problema
La libreria `anthropic` versione 0.20.0 è troppo vecchia e incompatibile.

## Soluzione

Esegui questi comandi nel terminale:

```bash
# 1. Assicurati che il venv sia attivo
venv\Scripts\activate

# 2. Aggiorna le librerie
pip install --upgrade anthropic openai streamlit

# 3. Oppure reinstalla tutto dai requirements aggiornati
pip install -r requirements.txt --upgrade

# 4. Verifica le versioni installate
pip list | findstr "anthropic openai streamlit"
```

## Versioni Corrette

Dopo l'aggiornamento dovresti avere:
- `anthropic >= 0.30.0` (o più recente)
- `openai >= 1.30.0` (o più recente)
- `streamlit >= 1.31.0` (o più recente)

## Test

Dopo l'aggiornamento, riavvia l'app:

```bash
streamlit run app.py
```

L'errore dovrebbe essere risolto!
