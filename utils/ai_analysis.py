import streamlit as st
from anthropic import Anthropic
import config

def analyze_with_claude(answers):
    """
    Perform comprehensive analysis using Claude API

    Args:
        answers: Dictionary of all user answers

    Returns:
        dict: Analysis results with multiple sections
    """

    client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

    # Prepare the analysis prompt
    prompt = build_analysis_prompt(answers)

    # Try different models in order of accessibility
    models_to_try = [
        "claude-3-haiku-20240307",  # Most accessible and economical
        "claude-3-sonnet-20240229",  # Good balance
        "claude-3-opus-20240229",    # Most powerful but may have restrictions
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            with st.spinner(f"🤖 Tentativo con {model_name}..."):
                message = client.messages.create(
                    model=model_name,
                    max_tokens=4000,
                    temperature=0.7,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

            analysis_text = message.content[0].text

            # Parse the analysis into structured sections
            analysis_results = parse_analysis_response(analysis_text)

            st.success(f"✅ Analisi completata con {model_name}")
            return analysis_results

        except Exception as e:
            last_error = str(e)
            st.warning(f"⚠️ {model_name} non disponibile, provo il successivo...")
            continue

    # If all models failed
    st.error(f"""
    ❌ **Impossibile generare l'analisi AI**

    Tutti i modelli Claude hanno restituito errore.

    **Ultimo errore:** {last_error}

    **Possibili cause:**
    1. **API key non valida** - Verifica su https://console.anthropic.com/
    2. **Credito esaurito** - Controlla il saldo del tuo account
    3. **Account senza accesso** - Alcuni account hanno restrizioni sui modelli
    4. **API key scaduta** - Potrebbe essere necessario generarne una nuova

    **Soluzione:**
    - Vai su https://console.anthropic.com/settings/keys
    - Verifica che la API key sia attiva
    - Controlla il credito disponibile
    - Prova a generare una nuova API key se necessario
    """)
    return None

def build_analysis_prompt(answers):
    """Build a comprehensive prompt for Claude analysis"""

    # Extract AS-IS information
    as_is_processo = answers.get("as_is_processo", "Non specificato")
    as_is_step = answers.get("as_is_step", "Non specificato")
    as_is_problemi = answers.get("as_is_problemi", "Non specificato")

    # Extract TO-BE information
    to_be_visione = answers.get("to_be_visione", "Non specificato")
    to_be_agenti = answers.get("to_be_agenti", "Non specificato")
    to_be_azioni_limiti = answers.get("to_be_azioni_limiti", "Non specificato")
    to_be_benefici = answers.get("to_be_benefici", "Non specificato")
    to_be_rischi = answers.get("to_be_rischi", "Non specificato")

    prompt = f"""Sei un esperto consulente in trasformazione digitale e Agentic AI.
Devi analizzare un progetto di reimplementazione di un processo aziendale con l'AI.

# PROCESSO AS-IS (Situazione Attuale)

**Processo:** {as_is_processo}

**Step del processo:**
{as_is_step}

**Problemi e criticità:**
{as_is_problemi}

**Strumenti attuali:** {answers.get("as_is_strumenti", "Non specificato")}

**Tempo stimato AS-IS:** {answers.get("as_is_tempo", "Non specificato")}

---

# PROCESSO TO-BE (Con Agentic AI)

**Visione:** {to_be_visione}

**Agenti AI previsti:**
{to_be_agenti}

**Azioni autonome e limiti:**
{to_be_azioni_limiti}

**Dati e sistemi:**
{answers.get("to_be_dati_sistemi", "Non specificato")}

**Tool da integrare:**
{answers.get("to_be_tool", "Non specificato")}

**Flusso agentico:**
{answers.get("to_be_flusso", "Non specificato")}

**Benefici previsti:**
{to_be_benefici}

**Rischi identificati:**
{to_be_rischi}

**Soluzioni esistenti:**
{answers.get("to_be_soluzioni", "Non specificato")}

**System Prompt:**
{answers.get("to_be_system_prompt", "Non specificato")}

---

# COMPITO

Fornisci un'analisi approfondita e strutturata del progetto, seguendo ESATTAMENTE questo formato con i titoli indicati:

## FATTIBILITÀ TECNICA
[Valuta la fattibilità tecnica del progetto su scala 1-5 e spiega. Considera: complessità tecnica, disponibilità di dati, integrazioni necessarie, maturità delle tecnologie]

## ANALISI IMPATTO: SOSTITUZIONE VS AUGMENTATION
[Analizza se il progetto è orientato alla sostituzione completa del lavoro umano o all'augmentation (supporto). Considera: complessità del task, necessità di giudizio umano, rischio errori AI, impatto sul cliente, margine di errore ammesso. Fornisci una chiara raccomandazione.]

## RISPARMIO DI TEMPO STIMATO
[Calcola il risparmio di tempo confrontando AS-IS e TO-BE, se possibile. Fornisci stime percentuali o quantitative.]

## RIDUZIONE COSTI
[Analizza quali costi potrebbero essere ridotti: personale, errori, ritardi, inefficienze]

## ATTIVITÀ ELIMINATE O OTTIMIZZATE
[Elenca le specifiche attività che verranno eliminate o significativamente velocizzate]

## RISCHI E CRITICITÀ
[Identifica i principali rischi: tecnici, organizzativi, legali, privacy/GDPR, resistenza al cambiamento. Valuta la gravità di ciascuno.]

## FORMAZIONE NECESSARIA
[Specifica che tipo di formazione sarà necessaria per chi utilizzerà il sistema e per chi lo gestirà]

## PROBLEMI LEGALI E PRIVACY
[Analizza aspetti GDPR, privacy, responsabilità legale, audit trail, compliance]

## ROADMAP IMPLEMENTAZIONE
[Suggerisci se partire con un pilota, un MVP, o implementazione completa. Definisci fasi consigliate.]

## DIAGRAMMA FLUSSO AGENTICO
[Genera un diagramma Mermaid del flusso agentico proposto. Usa la sintassi Mermaid flowchart con:
- Nodi per gli agenti AI
- Nodi per le decisioni e azioni autonome
- Frecce per il flusso
- Colori per distinguere agenti, umani, sistemi esterni
Esempio formato:
```mermaid
flowchart TD
    A[Utente Input] --> B[Agente 1: Analisi]
    B --> C{{Decisione AI}}
    C -->|Autonomo| D[Azione Automatica]
    C -->|Escalation| E[Review Umano]
```
]

## RACCOMANDAZIONI FINALI
[Fornisci 3-5 raccomandazioni chiave e concrete per il successo del progetto]

## SCORE COMPLESSIVO
[Assegna uno score finale al progetto su scala 1-10 considerando: fattibilità, impatto, rischi, costi/benefici. Spiega il punteggio.]

Rispondi in italiano, in modo professionale ma accessibile. Usa esempi concreti quando possibile."""

    return prompt

def parse_analysis_response(analysis_text):
    """Parse Claude's response into structured sections"""

    sections = {}

    # Define section markers
    section_markers = [
        "FATTIBILITÀ TECNICA",
        "ANALISI IMPATTO: SOSTITUZIONE VS AUGMENTATION",
        "RISPARMIO DI TEMPO STIMATO",
        "RIDUZIONE COSTI",
        "ATTIVITÀ ELIMINATE O OTTIMIZZATE",
        "RISCHI E CRITICITÀ",
        "FORMAZIONE NECESSARIA",
        "PROBLEMI LEGALI E PRIVACY",
        "ROADMAP IMPLEMENTAZIONE",
        "DIAGRAMMA FLUSSO AGENTICO",
        "RACCOMANDAZIONI FINALI",
        "SCORE COMPLESSIVO"
    ]

    # Split text by sections
    current_section = "introduction"
    current_content = []

    lines = analysis_text.split('\n')

    for line in lines:
        # Check if line is a section header
        is_header = False
        for marker in section_markers:
            if marker in line and line.startswith('#'):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section - normalize key (remove accents)
                key = marker.lower().replace(' ', '_').replace(':', '')
                # Remove accents for consistent keys
                accent_map = {
                    'à': 'a', 'è': 'e', 'é': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
                    'á': 'a', 'í': 'i', 'ó': 'o', 'ú': 'u'
                }
                for accent, plain in accent_map.items():
                    key = key.replace(accent, plain)
                current_section = key
                current_content = []
                is_header = True
                break

        if not is_header and line.strip():
            current_content.append(line)

    # Save last section
    if current_content:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections

def extract_score(analysis_results):
    """Extract numerical score from analysis"""

    score_section = analysis_results.get("score_complessivo", "")

    # Try to find score like "8/10" or "Score: 8"
    import re

    # Pattern 1: "X/10"
    match = re.search(r'(\d+)/10', score_section)
    if match:
        return int(match.group(1))

    # Pattern 2: "Score: X" or "Punteggio: X"
    match = re.search(r'(?:Score|Punteggio):\s*(\d+)', score_section, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Pattern 3: Just a number at the start
    match = re.search(r'^(\d+)', score_section.strip())
    if match:
        score = int(match.group(1))
        if 1 <= score <= 10:
            return score

    return None

def get_feasibility_level(analysis_results):
    """Extract feasibility level from analysis"""

    feasibility_section = analysis_results.get("fattibilita_tecnica", "")

    # Look for patterns like "3/5" or "Level 3"
    import re

    match = re.search(r'(\d+)/5', feasibility_section)
    if match:
        return int(match.group(1))

    match = re.search(r'(?:Level|Livello):\s*(\d+)', feasibility_section, re.IGNORECASE)
    if match:
        return int(match.group(1))

    return None

def generate_quick_insights(answers):
    """Generate quick insights without full AI analysis"""

    insights = []

    # Check if process is defined
    if not answers.get("as_is_processo"):
        insights.append({
            "type": "warning",
            "title": "Processo non definito",
            "message": "Definisci il processo AS-IS per iniziare l'analisi"
        })

    # Check if benefits are defined
    if answers.get("to_be_benefici"):
        insights.append({
            "type": "success",
            "title": "Benefici identificati",
            "message": "Hai definito i benefici attesi dal progetto"
        })

    # Check if risks are considered
    if answers.get("to_be_rischi"):
        insights.append({
            "type": "info",
            "title": "Rischi identificati",
            "message": "Hai considerato i rischi potenziali"
        })

    # Check if system prompt is drafted
    if answers.get("to_be_system_prompt"):
        insights.append({
            "type": "success",
            "title": "System Prompt definito",
            "message": "Hai iniziato a definire le istruzioni per gli agenti AI"
        })

    return insights
