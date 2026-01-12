# 🐛 Bug Fix - Changelog

## Versione 1.1.0 - 04/01/2025

### Bug Risolti

#### 1. ✅ Input Vocale Whisper Non Funzionante
**Problema:** L'input vocale richiedeva di configurare manualmente la API key OpenAI anche se era già presente in `config.py`.

**Soluzione:**
- Modificato `utils/voice_input.py` per usare la chiave da `config.OPENAI_API_KEY` come fallback
- Ora la chiave viene cercata prima in `session_state`, poi in `config`
- L'input vocale funziona immediatamente senza configurazione aggiuntiva

**File modificati:**
- `utils/voice_input.py` (righe 6, 11, 77)

---

#### 2. ✅ Bottone "Avanti" Non Cliccabile
**Problema:** Dopo aver inserito risposte, il bottone "Avanti" rimaneva disabilitato.

**Soluzione:**
- Modificata la logica di aggiornamento di `session_state.answers` per sincronizzare sempre il valore corrente
- Migliorato il controllo `can_proceed` per verificare che la risposta non sia vuota (considerando anche spazi)
- Applicato il fix sia alla sezione AS-IS che TO-BE

**File modificati:**
- `app.py` (righe 188, 302-306, 362-366)

---

#### 3. ✅ Import Progetto Non Abilita Analisi
**Problema:** Importando un progetto con analisi già completata, non si poteva accedere direttamente alla sezione "Analisi Finale".

**Soluzione:**
- Modificato `utils/data_manager.py` per settare `show_analysis = True` quando viene importato un file con analisi
- Ora dopo l'import, se l'analisi è presente, viene abilitata automaticamente la visualizzazione

**File modificati:**
- `utils/data_manager.py` (righe 39-44)

---

## Come Testare

1. **Test Input Vocale:**
   - Vai nella tab "🎤 Parla" di una domanda
   - L'input vocale dovrebbe funzionare senza richiedere configurazione
   - Registra un audio e verifica la trascrizione

2. **Test Bottone Avanti:**
   - Inserisci una risposta in una domanda obbligatoria
   - Il bottone "Avanti ➡️" dovrebbe diventare cliccabile immediatamente
   - Prova sia con domande text_area che multi_step/table/multi_agent

3. **Test Import con Analisi:**
   - Completa AS-IS e TO-BE
   - Genera l'analisi
   - Esporta il progetto
   - Ricarica la pagina
   - Importa il progetto
   - Verifica che la sezione "Analisi Finale" sia accessibile dalla sidebar

---

## Versioni Dipendenze

Assicurati di aver aggiornato le librerie:

```bash
pip install --upgrade anthropic openai streamlit
```

Versioni minime richieste:
- `anthropic >= 0.30.0`
- `openai >= 1.30.0`
- `streamlit >= 1.31.0`

---

## Note Aggiuntive

- Tutti i fix sono retrocompatibili
- Non è necessario rigenerare progetti esistenti
- L'API key OpenAI in `config.py` è ora utilizzata automaticamente
