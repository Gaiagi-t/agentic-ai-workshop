"""
Agentic AI Workshop V2 - Analisi Educativa
Genera analisi in 4 layer per executive:
1. Executive Summary (Score + ROI + Next Step)
2. Ragionamento (PERCHÉ quelle conclusioni)
3. Roadmap Dettagliata (fasi concrete)
4. Action Plan (checklist + vendor suggestions)

Differenze da V1:
- Non solo OUTPUT ma spiega il RAGIONAMENTO
- ROI numerico con calcoli espliciti
- Next steps concreti, non generici
- Personalizzato sul profilo di rischio
"""

import streamlit as st
from anthropic import Anthropic
import config
import re


def analyze_with_claude_v2(answers):
    """
    Genera analisi completa V2 con 4 layer educativi

    Args:
        answers: Dict di risposte {question_id: answer_value}

    Returns:
        Dict con analisi strutturata in 4 layer + metadati
    """
    client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

    # Build prompt V2
    prompt = build_analysis_prompt_v2(answers)

    # Try different models (stessa strategia di V1)
    models_to_try = [
        "claude-3-haiku-20240307",  # Most accessible and economical
        "claude-3-sonnet-20240229",  # Good balance
        "claude-3-opus-20240229",    # Most powerful but may have restrictions
    ]

    last_error = None

    for model_name in models_to_try:
        try:
            with st.spinner(f"🤖 Analisi in corso con {model_name}..."):
                message = client.messages.create(
                    model=model_name,
                    max_tokens=4000,  # Compatibile con tutti i modelli
                    temperature=0.7,  # Stesso di V1
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }]
                )

            analysis_text = message.content[0].text

            # Parse in 4 layer
            parsed = parse_analysis_v2(analysis_text)

            # Arricchisci con calcoli numerici
            parsed["roi_detailed"] = calculate_roi_breakdown(answers, parsed)
            parsed["model_used"] = model_name

            st.success(f"✅ Analisi completata con {model_name}")
            return parsed

        except Exception as e:
            last_error = str(e)
            st.warning(f"⚠️ {model_name} non disponibile, provo fallback...")
            continue

    # Se tutti falliscono
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


def build_analysis_prompt_v2(answers):
    """
    Costruisce prompt V2 strutturato per analisi educativa

    Differenze da V1:
    - Richiede esplicitamente il RAGIONAMENTO
    - Richiede ROI con calcoli espliciti
    - Richiede action plan concreto
    - Richiede vendor suggestions

    Args:
        answers: Dict risposte

    Returns:
        str: Prompt completo
    """

    # Estrai risposte dalle 8 domande V2
    q1_problem = answers.get('q1_problem', 'Non specificato')
    q2_vision = answers.get('q2_vision', 'Non specificato')

    # Q3 ha due colonne
    q3_ai = answers.get('q3_ai_vs_human', {}).get('ai_decisions', 'Non specificato')
    q3_human = answers.get('q3_ai_vs_human', {}).get('human_decisions', 'Non specificato')

    # Q4 checkbox
    q4_data = answers.get('q4_data_systems', {})
    if isinstance(q4_data, dict):
        selected_data = [opt['label'] for opt in q4_data.get('selected', [])]
        other_data = q4_data.get('other', '')
        q4_data_str = ", ".join(selected_data)
        if other_data:
            q4_data_str += f" + {other_data}"
    else:
        q4_data_str = str(q4_data)

    # Q5 flow
    q5_flow = answers.get('q5_flow', 'Non specificato')

    # Q6 risks
    q6_risks = answers.get('q6_risks', {})
    if isinstance(q6_risks, dict):
        selected_risks = [opt['label'] for opt in q6_risks.get('selected', [])]
        notes_risks = q6_risks.get('notes', '')
        q6_risks_str = ", ".join(selected_risks)
        if notes_risks:
            q6_risks_str += f" | Note: {notes_risks}"
    else:
        q6_risks_str = str(q6_risks)

    # Q7 metrics
    q7_metrics = answers.get('q7_metrics', [])
    if isinstance(q7_metrics, list):
        metrics_str = "\n".join([f"- {m.get('label', m)}" for m in q7_metrics])
    else:
        metrics_str = str(q7_metrics)

    # Q8 timeline
    q8_timeline = answers.get('q8_timeline', {})
    approach = q8_timeline.get('approach', 'Non specificato')
    start_date = q8_timeline.get('start_date', 'Non specificato')
    budget = q8_timeline.get('budget_range', 'Non specificato')

    prompt = f"""Sei un consulente esperto in Agentic AI per executive e manager.
Devi analizzare un progetto di trasformazione AI e fornire un'analisi:
- **EDUCATIVA** (spiega il ragionamento, non solo conclusioni)
- **AZIONABILE** (next steps concreti e specifici, non generici)
- **NUMERICA** (ROI con calcoli espliciti e assunzioni trasparenti)

Il tuo pubblico è composto da executive/manager (non tecnici), quindi:
- NO gergo tecnico (evita: API, orchestration, tool, endpoint, etc.)
- SÌ linguaggio business (usa: benefici, ROI, decisioni, rischi, valore)
- Focus su COSA e PERCHÉ, meno su COME tecnico

---

# DATI PROGETTO RACCOLTI (8 domande)

## FASE 1: DISCOVERY

**Q1 - Processo e Problema:**
{q1_problem}

**Q2 - Visione Risultato Ideale:**
{q2_vision}

**Q3 - Decisioni AI vs Umane:**
- 🤖 L'AI può decidere autonomamente: {q3_ai}
- 👤 Serve l'intervento umano: {q3_human}

## FASE 2: DESIGN

**Q4 - Dati e Sistemi Disponibili:**
{q4_data_str}

**Q5 - Flusso di Lavoro Scelto:**
{q5_flow}

**Q6 - Rischi e Ostacoli Identificati:**
{q6_risks_str}

## FASE 3: ROI & TIMELINE

**Q7 - Metriche di Successo:**
{metrics_str}

**Q8 - Timeline e Budget:**
- Approccio: {approach}
- Data inizio target: {start_date}
- Budget indicativo: {budget}

---

# OUTPUT RICHIESTO

Fornisci l'analisi seguendo **ESATTAMENTE** questa struttura:

---

## LAYER 1: EXECUTIVE SUMMARY

### Score Complessivo
[Assegna uno score da 1 a 10]
**Score: X/10** 🟢 [ALTA/MEDIA/BASSA FATTIBILITÀ]

### Punti di Forza
[Elenca 3 punti di forza concreti del progetto]
- ...
- ...
- ...

### Attenzioni
[Elenca 2-3 aspetti da monitorare o rischi da mitigare]
- ...
- ...

### ROI Stimato
**Risparmio anno 1:** €[X]
**Investimento stimato:** €[Y]
**Break-even:** [Z] mesi
**ROI a 12 mesi:** [%]

### Prossimo Passo Concreto
[Indica UNA azione specifica e immediata da fare]
Esempio: "Pilota di 4 settimane su 20% dei casi a partire da [data suggerita]"

---

## LAYER 2: RAGIONAMENTO

### 1. Analisi Complessità
**Complessità processo: [BASSA/MEDIA/ALTA]**

[Spiega PERCHÉ hai assegnato questo livello]
Fattori considerati:
- [Fattore 1 con spiegazione]
- [Fattore 2 con spiegazione]
- [Fattore 3 con spiegazione]

### 2. Valutazione Dati
**Qualità dati disponibili: [X/10]**

[Spiega la valutazione]
- Dati disponibili: [lista]
- Qualità stimata: [motivazione]
- Gap da colmare: [se presenti]

### 3. Profilo di Rischio
**Rischio progetto: [BASSO/MEDIO/ALTO]**

[Spiega PERCHÉ]
Fattori di rischio considerati:
- [Fattore 1 con impatto]
- [Fattore 2 con impatto]
- [Fattore 3 con impatto]

Mitigazioni suggerite:
- [Azione mitigativa 1]
- [Azione mitigativa 2]

### 4. Calcolo ROI
**Assunzioni:**
- Volume attività: [X] task/giorno (stimato da descrizione processo)
- Tempo medio attuale (AS-IS): [Y] minuti/task
- Tempo medio con AI (TO-BE): [Z] minuti/task
- Costo orario team: €[W]/ora (media settore)
- Tasso adozione realistico: [%]

**Calcolo passo-passo:**
```
Risparmio tempo per task = Y - Z minuti
Risparmio giornaliero = [X task] × [risparmio] minuti
Risparmio in ore/giorno = [calcolo]
Costo risparmiato/giorno = [ore] × €[W]/ora = €[A]
Risparmio annuale (250 giorni) = €[A] × 250 = €[B]
Con tasso adozione [%] = €[B] × [%] = €[C] (risparmio realistico)
```

Investimento stimato:
- Setup iniziale: €[X]
- Costi ricorrenti anno 1: €[Y]
- **Totale anno 1:** €[Z]

**Break-even:** [Mesi per recuperare investimento]
**ROI a 12 mesi:** [(Risparmio - Investimento) / Investimento × 100]%

---

## LAYER 3: ROADMAP DETTAGLIATA

### FASE 1: PILOTA (Settimane 1-4)
**Obiettivo:** [Cosa vuoi dimostrare con il pilota]

**Attività:**
- [ ] [Attività concreta 1]
- [ ] [Attività concreta 2]
- [ ] [Attività concreta 3]
- [ ] [Attività concreta 4]

**Metriche di successo:**
- [Metrica 1]: Target [valore]
- [Metrica 2]: Target [valore]

**Budget fase 1:** €[X]

### FASE 2: SCALE (Mesi 2-3)
**Obiettivo:** [Espansione graduale]

**Attività:**
- [ ] [Attività 1]
- [ ] [Attività 2]
- [ ] [Attività 3]

**Metriche di successo:**
- [Metrica 1]: Target [valore]
- [Metrica 2]: Target [valore]

**Budget fase 2:** €[Y]

### FASE 3: FULL DEPLOYMENT (Mese 4+)
**Obiettivo:** [Copertura completa e ottimizzazione]

**Attività:**
- [ ] [Attività 1]
- [ ] [Attività 2]
- [ ] [Attività 3]

**Metriche di successo:**
- [Metrica 1]: Target [valore]
- [Metrica 2]: Target [valore]

**Budget fase 3:** €[Z]

---

## LAYER 4: ACTION PLAN

### Questa Settimana
- [ ] [Azione concreta e immediata 1]
- [ ] [Azione concreta e immediata 2]
- [ ] [Azione concreta e immediata 3]

### Prossime 2 Settimane
- [ ] [Azione 1]
- [ ] [Azione 2]
- [ ] [Azione 3]

### Mese 1
- [ ] [Milestone 1]
- [ ] [Milestone 2]

### Vendor/Partner Suggeriti
[Basandoti sul tipo di processo e budget, suggerisci 3 vendor/piattaforme concrete]

**1. [Nome Vendor/Piattaforma]**
- **Perché adatto:** [Motivazione specifica per questo caso]
- **Best for:** [Tipo di use case]
- **Budget range:** [€X-Y]
- **Setup time:** [tempistica]

**2. [Nome Vendor/Piattaforma]**
- **Perché adatto:** [Motivazione]
- **Best for:** [Use case]
- **Budget range:** [€X-Y]
- **Setup time:** [tempistica]

**3. [Nome Vendor/Piattaforma]**
- **Perché adatto:** [Motivazione]
- **Best for:** [Use case]
- **Budget range:** [€X-Y]
- **Setup time:** [tempistica]

---

**IMPORTANTE:**
- Rispondi in ITALIANO
- Usa tono professionale ma accessibile
- Numeri concreti (anche se stimati, mostra il calcolo)
- NO gergo tecnico
- Esempi concreti quando possibile
- Azioni specifiche, non vaghe ("Contatta X" non "Valuta opzioni")
"""

    return prompt


def parse_analysis_v2(analysis_text):
    """
    Parse response di Claude in struttura 4-layer

    Args:
        analysis_text: Testo completo da Claude

    Returns:
        Dict con 4 layer strutturati
    """
    sections = {}

    # === LAYER 1: EXECUTIVE SUMMARY ===
    layer1 = extract_section_between(analysis_text, "LAYER 1: EXECUTIVE SUMMARY", "LAYER 2:")
    if layer1:
        sections["executive_summary"] = layer1
        sections["score"] = extract_score_v2(layer1)
        sections["strengths"] = extract_bullets(layer1, "Punti di Forza")
        sections["cautions"] = extract_bullets(layer1, "Attenzioni")
        sections["roi_summary"] = extract_roi_summary_v2(layer1)
        sections["next_step"] = extract_next_step_v2(layer1)

    # === LAYER 2: RAGIONAMENTO ===
    layer2 = extract_section_between(analysis_text, "LAYER 2: RAGIONAMENTO", "LAYER 3:")
    if layer2:
        sections["reasoning"] = layer2
        sections["complexity_analysis"] = extract_subsection_v2(layer2, "1. Analisi Complessità")
        sections["data_quality"] = extract_subsection_v2(layer2, "2. Valutazione Dati")
        sections["risk_profile"] = extract_subsection_v2(layer2, "3. Profilo di Rischio")
        sections["roi_calculation"] = extract_subsection_v2(layer2, "4. Calcolo ROI")

    # === LAYER 3: ROADMAP ===
    layer3 = extract_section_between(analysis_text, "LAYER 3: ROADMAP DETTAGLIATA", "LAYER 4:")
    if layer3:
        sections["roadmap"] = layer3
        sections["phase_1"] = extract_phase_v2(layer3, "FASE 1: PILOTA")
        sections["phase_2"] = extract_phase_v2(layer3, "FASE 2: SCALE")
        sections["phase_3"] = extract_phase_v2(layer3, "FASE 3: FULL DEPLOYMENT")

    # === LAYER 4: ACTION PLAN ===
    layer4 = extract_section_between(analysis_text, "LAYER 4: ACTION PLAN", "---")
    if not layer4:
        # Se non trova fine con ---, prendi tutto il resto
        layer4 = analysis_text.split("LAYER 4: ACTION PLAN")[-1] if "LAYER 4: ACTION PLAN" in analysis_text else ""

    if layer4:
        sections["action_plan"] = layer4
        sections["actions_week"] = extract_checklist_v2(layer4, "Questa Settimana")
        sections["actions_2weeks"] = extract_checklist_v2(layer4, "Prossime 2 Settimane")
        sections["actions_month1"] = extract_checklist_v2(layer4, "Mese 1")
        sections["vendors"] = extract_vendors_v2(layer4)

    return sections


# ============================================================================
# HELPER FUNCTIONS PER PARSING
# ============================================================================

def extract_section_between(text, start_marker, end_marker):
    """Estrae testo tra due marker"""
    if start_marker not in text:
        return ""

    start_idx = text.find(start_marker)
    if end_marker and end_marker in text[start_idx:]:
        end_idx = text.find(end_marker, start_idx)
        return text[start_idx:end_idx].strip()
    else:
        return text[start_idx:].strip()


def extract_score_v2(text):
    """Estrae score numerico da LAYER 1"""
    # Pattern: "Score: X/10" o "**Score: X/10**"
    match = re.search(r'\*?\*?Score:?\s*(\d+)/10', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def extract_bullets(text, section_title):
    """Estrae bullet points da una sezione"""
    bullets = []
    if section_title not in text:
        return bullets

    # Trova la sezione
    section_start = text.find(section_title)
    section_text = text[section_start:section_start + 500]  # Max 500 char

    # Estrai linee che iniziano con - o *
    lines = section_text.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('-') or stripped.startswith('*'):
            bullet = stripped.lstrip('-*').strip()
            if bullet:
                bullets.append(bullet)

    return bullets


def extract_roi_summary_v2(text):
    """Estrae summary ROI da LAYER 1"""
    roi = {}

    # Risparmio anno 1
    match = re.search(r'Risparmio anno 1:?\s*€?([0-9.,]+[kK]?)', text, re.IGNORECASE)
    if match:
        roi['risparmio_anno1'] = match.group(1)

    # Investimento
    match = re.search(r'Investimento.*?:?\s*€?([0-9.,]+[kK]?)', text, re.IGNORECASE)
    if match:
        roi['investimento'] = match.group(1)

    # Break-even
    match = re.search(r'Break-even:?\s*(\d+)\s*mes[ei]', text, re.IGNORECASE)
    if match:
        roi['breakeven_mesi'] = int(match.group(1))

    # ROI 12 mesi
    match = re.search(r'ROI.*?12 mesi:?\s*(\d+)%', text, re.IGNORECASE)
    if match:
        roi['roi_12mesi'] = int(match.group(1))

    return roi


def extract_next_step_v2(text):
    """Estrae prossimo passo concreto da LAYER 1"""
    if "Prossimo Passo" in text:
        section_start = text.find("Prossimo Passo")
        section_text = text[section_start:section_start + 300]
        lines = section_text.split('\n')
        for line in lines[1:]:  # Skip title
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                return stripped
    return ""


def extract_subsection_v2(text, subsection_title):
    """Estrae una subsection da LAYER 2"""
    if subsection_title not in text:
        return ""

    start_idx = text.find(subsection_title)
    # Trova prossima subsection (inizia con ### o numero)
    remaining = text[start_idx + len(subsection_title):]
    next_section = re.search(r'\n###|\n\d+\.', remaining)

    if next_section:
        end_idx = start_idx + len(subsection_title) + next_section.start()
        return text[start_idx:end_idx].strip()
    else:
        # Prendi fino a 800 char
        return text[start_idx:start_idx + 800].strip()


def extract_phase_v2(text, phase_title):
    """Estrae fase da LAYER 3"""
    if phase_title not in text:
        return {}

    start_idx = text.find(phase_title)
    # Trova prossima fase
    remaining = text[start_idx + len(phase_title):]
    next_phase = re.search(r'\nFASE \d+:', remaining)

    if next_phase:
        end_idx = start_idx + len(phase_title) + next_phase.start()
        phase_text = text[start_idx:end_idx]
    else:
        phase_text = text[start_idx:start_idx + 800]

    # Parse fase
    phase = {
        "title": phase_title,
        "objective": "",
        "activities": [],
        "metrics": [],
        "budget": ""
    }

    # Obiettivo
    if "Obiettivo:" in phase_text:
        obj_match = re.search(r'Obiettivo:\s*(.+)', phase_text)
        if obj_match:
            phase["objective"] = obj_match.group(1).strip()

    # Attività (checklist)
    activities = re.findall(r'- \[ \] (.+)', phase_text)
    phase["activities"] = activities

    # Metriche
    metrics = re.findall(r'- (.+): Target (.+)', phase_text)
    phase["metrics"] = [{"metric": m[0], "target": m[1]} for m in metrics]

    # Budget
    budget_match = re.search(r'Budget.*?€([0-9.,]+[kK]?)', phase_text, re.IGNORECASE)
    if budget_match:
        phase["budget"] = budget_match.group(1)

    return phase


def extract_checklist_v2(text, timeframe):
    """Estrae checklist da LAYER 4"""
    if timeframe not in text:
        return []

    start_idx = text.find(timeframe)
    section_text = text[start_idx:start_idx + 500]

    # Trova checklist items
    items = re.findall(r'- \[ \] (.+)', section_text)
    return items


def extract_vendors_v2(text):
    """Estrae vendor suggestions da LAYER 4"""
    vendors = []

    if "Vendor/Partner" not in text:
        return vendors

    # Trova sezione vendor
    vendor_section_idx = text.find("Vendor/Partner")
    vendor_text = text[vendor_section_idx:]

    # Pattern per vendor (numero + nome)
    vendor_blocks = re.findall(r'\*?\*?(\d+)\.\s*\[?([^\]]+)\]?\*?\*?\s*\n((?:.*\n){0,8})', vendor_text)

    for num, name, details in vendor_blocks:
        vendor = {"name": name.strip(), "details": details.strip()}

        # Estrai campi specifici
        why_match = re.search(r'Perché adatto:(.+)', details)
        if why_match:
            vendor["why"] = why_match.group(1).strip()

        best_match = re.search(r'Best for:(.+)', details)
        if best_match:
            vendor["best_for"] = best_match.group(1).strip()

        budget_match = re.search(r'Budget range:(.+)', details, re.IGNORECASE)
        if budget_match:
            vendor["budget_range"] = budget_match.group(1).strip()

        setup_match = re.search(r'Setup time:(.+)', details, re.IGNORECASE)
        if setup_match:
            vendor["setup_time"] = setup_match.group(1).strip()

        vendors.append(vendor)

    return vendors[:3]  # Max 3


def calculate_roi_breakdown(answers, parsed_analysis):
    """
    Calcola ROI dettagliato con breakdown mensile
    (Placeholder - da implementare con logica più sofisticata)

    Args:
        answers: Risposte utente
        parsed_analysis: Analisi già parsata

    Returns:
        Dict con breakdown ROI mensile
    """
    # TODO: Implementare logica di calcolo dettagliata
    # Per ora ritorna placeholder

    roi_summary = parsed_analysis.get("roi_summary", {})

    return {
        "monthly_savings": [0] * 12,  # Placeholder
        "cumulative_roi": [0] * 12,
        "break_even_month": roi_summary.get("breakeven_mesi", 6),
        "total_roi_1year": roi_summary.get("roi_12mesi", 0)
    }
