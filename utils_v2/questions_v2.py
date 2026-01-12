"""
Agentic AI Workshop V2 - Executive Edition
8 Domande Strategiche (vs 18 V1) per completamento in 30-45 minuti

Ottimizzato per:
- Executive/Manager (linguaggio business, no gergo tecnico)
- Discovery rapida (identificare opportunità AI)
- Engagement attivo (4 momenti "aha!" distribuiti)
"""

# ============================================================================
# FASE 1: DISCOVERY (Q1-Q3) - 10-15 minuti
# ============================================================================

QUESTIONS_V2 = [
    # ========================================================================
    # Q1 - PROCESSO & PROBLEMA
    # ========================================================================
    {
        "id": "q1_problem",
        "numero": 1,
        "fase": "Discovery",
        "testo": "Quale processo vuoi trasformare e quale problema principale vuoi risolvere?",
        "tipo": "text_area",
        "rows": 4,
        "placeholder": "Esempio: 'Gestione reclami clienti - I clienti aspettano troppo per ricevere risposte' oppure 'Selezione CV - Sprechiamo giorni su candidati non qualificati'",
        "help": "💡 Focus sul problema concreto che vuoi risolvere, non solo sulla descrizione del processo",
        "obbligatorio": True,
        "insight_trigger": True,
        "insight_type": "process_classification",
        "note": "Fusione di AS-IS Q1 (processo) + Q6 (problemi). Focus su pain point."
    },

    # ========================================================================
    # Q2 - VISIONE RISULTATO
    # ========================================================================
    {
        "id": "q2_vision",
        "numero": 2,
        "fase": "Discovery",
        "testo": "Come vorresti che funzionasse idealmente? Descrivi il risultato che vuoi ottenere.",
        "tipo": "text_area",
        "rows": 4,
        "placeholder": "Esempio: 'Il cliente riceve una risposta personalizzata in 5 minuti, non 2 giorni' oppure 'I candidati più adatti emergono automaticamente in 1 ora'",
        "help": "💡 Pensa al valore finale per il tuo cliente o team, non alla tecnologia",
        "obbligatorio": True,
        "insight_trigger": True,
        "insight_type": "vision_analysis",
        "note": "TO-BE Q1 semplificata. Focus su outcome, non su architettura."
    },

    # ========================================================================
    # Q3 - AI vs UMANO (Autonomia e Limiti)
    # ========================================================================
    {
        "id": "q3_ai_vs_human",
        "numero": 3,
        "fase": "Discovery",
        "testo": "Quali decisioni può prendere l'AI in autonomia? Dove è indispensabile il tocco umano?",
        "tipo": "two_column_input",
        "columns": {
            "ai_decisions": {
                "label": "🤖 L'AI può decidere autonomamente",
                "placeholder": "Esempi:\n- Rispondere a domande frequenti\n- Classificare l'urgenza\n- Cercare informazioni nel database\n- Generare bozze di risposta",
                "rows": 5
            },
            "human_decisions": {
                "label": "👤 Serve l'intervento umano",
                "placeholder": "Esempi:\n- Casi sensibili o complessi\n- Decisioni strategiche importanti\n- Situazioni fuori standard\n- Approvazione finale",
                "rows": 5
            }
        },
        "help": "💡 Distinguere cosa è routine (AI) da cosa richiede giudizio umano (Human)",
        "obbligatorio": True,
        "insight_trigger": True,
        "insight_type": "as_is_to_be_comparison",
        "note": "TO-BE Q4 riformulata. Introduce concetto Augmentation vs Sostituzione senza gergo. TRIGGER: AHA! #2 - Visualizzazione comparativa"
    },

    # ========================================================================
    # FASE 2: DESIGN ESSENZIALE (Q4-Q6) - 10-15 minuti
    # ========================================================================

    # ========================================================================
    # Q4 - DATI & SISTEMI
    # ========================================================================
    {
        "id": "q4_data_systems",
        "numero": 4,
        "fase": "Design",
        "testo": "Di quali informazioni ha bisogno l'AI per funzionare?",
        "tipo": "checkbox_with_other",
        "options": [
            {"value": "crm", "label": "Database clienti (CRM)", "description": "Anagrafica clienti, storico interazioni, preferenze"},
            {"value": "tickets", "label": "Storico conversazioni/ticket", "description": "Email, chat, telefonate precedenti"},
            {"value": "docs", "label": "Documenti e policy aziendali", "description": "Manuali, FAQ, procedure interne"},
            {"value": "product", "label": "Dati di prodotto/servizio", "description": "Catalogo, specifiche tecniche, prezzi"},
            {"value": "external", "label": "Fonti esterne", "description": "Web, API terze parti, database pubblici"},
            {"value": "other", "label": "Altro (specifica sotto)", "description": ""}
        ],
        "other_field": {
            "placeholder": "Specifica altre fonti di dati necessarie...",
            "rows": 2
        },
        "help": "💡 Seleziona tutte le fonti di dati che l'AI dovrebbe consultare. Evita termini tecnici come 'API' - pensa alle informazioni concrete.",
        "obbligatorio": True,
        "insight_trigger": False,
        "note": "TO-BE Q5 semplificata. No 'data sources' ma 'informazioni'. Checkbox per velocità."
    },

    # ========================================================================
    # Q5 - FLUSSO SEMPLIFICATO
    # ========================================================================
    {
        "id": "q5_flow",
        "numero": 5,
        "fase": "Design",
        "testo": "Come immagini il flusso di lavoro con l'AI?",
        "tipo": "visual_selector",
        "options": [
            {
                "value": "single_agent",
                "label": "🤖 Assistente Unico",
                "title": "Un solo AI Agent gestisce tutto end-to-end",
                "description": "L'AI riceve la richiesta, analizza, cerca informazioni, e produce il risultato finale in un unico flusso.",
                "use_cases": "Ideale per: Processi semplici, FAQ automatiche, classificazione documenti",
                "automation_rate": "70-90%",
                "mermaid_diagram": """flowchart LR
    A[Input Utente] --> B[AI Agent]
    B --> C{Analisi}
    C --> D[Ricerca Info]
    D --> E[Genera Risposta]
    E --> F[Output]"""
            },
            {
                "value": "multi_agent",
                "label": "🔄 Team di Specialisti",
                "title": "Più AI Agent collaborano tra loro",
                "description": "Diversi AI Agent specializzati collaborano: uno legge, uno cerca, uno elabora, uno redige. Ognuno fa la sua parte.",
                "use_cases": "Ideale per: Processi articolati, sub-task distinti, workflow complessi",
                "automation_rate": "60-80%",
                "mermaid_diagram": """flowchart LR
    A[Input] --> B[Agent 1: Analisi]
    B --> C[Agent 2: Ricerca]
    C --> D[Agent 3: Elaborazione]
    D --> E[Agent 4: Redazione]
    E --> F[Output]"""
            },
            {
                "value": "router",
                "label": "🚦 Router Intelligente",
                "title": "L'AI decide: automazione o escalation umana",
                "description": "L'AI valuta la complessità del caso. Se è semplice, lo gestisce autonomamente. Se è complesso, lo passa a un operatore esperto.",
                "use_cases": "Ideale per: Mix casi semplici/complessi, necessità di review umana, rischio variabile",
                "automation_rate": "40-70%",
                "mermaid_diagram": """flowchart TD
    A[Input] --> B[AI Router]
    B --> C{{Complessità?}}
    C -->|Bassa| D[AI Gestisce]
    C -->|Alta| E[Operatore Umano]
    D --> F[Output Automatico]
    E --> G[Output con Review]"""
            }
        ],
        "help": "💡 Scegli l'approccio che meglio si adatta al tuo processo. Ogni opzione ha pro e contro.",
        "obbligatorio": True,
        "insight_trigger": True,
        "insight_type": "interactive_demo",
        "note": "TO-BE Q7 visual-first. Ridotto da 6 a 3 template. Cards grandi con diagrammi. TRIGGER: AHA! #3 - Demo interattiva"
    },

    # ========================================================================
    # Q6 - RISCHI & VINCOLI
    # ========================================================================
    {
        "id": "q6_risks",
        "numero": 6,
        "fase": "Design",
        "testo": "Quali ostacoli prevedi? (Così possiamo affrontarli da subito)",
        "tipo": "checkbox_with_notes",
        "options": [
            {
                "value": "team_resistance",
                "label": "Resistenza del team",
                "description": "Preoccupazioni dei colleghi, paura di perdere il lavoro"
            },
            {
                "value": "budget",
                "label": "Costi iniziali e budget limitato",
                "description": "Difficoltà a giustificare investimento iniziale"
            },
            {
                "value": "privacy_gdpr",
                "label": "Privacy e conformità GDPR",
                "description": "Dati sensibili, consent, audit trail"
            },
            {
                "value": "data_quality",
                "label": "Qualità dei dati insufficiente",
                "description": "Dati incompleti, non strutturati, datati"
            },
            {
                "value": "complexity",
                "label": "Complessità tecnica dell'implementazione",
                "description": "Mancanza di competenze interne, integrazioni difficili"
            },
            {
                "value": "other",
                "label": "Altro (specifica sotto)",
                "description": ""
            }
        ],
        "notes_field": {
            "placeholder": "Aggiungi dettagli su rischi specifici che hai identificato...",
            "rows": 3
        },
        "help": "💡 Non preoccuparti - identificare i rischi ora ti aiuta a mitigarli. Non ci sono ostacoli insormontabili!",
        "obbligatorio": False,
        "insight_trigger": False,
        "note": "TO-BE Q11 reframed positivo. Frame come 'planning', non 'blocchi'. Checkbox per velocità."
    },

    # ========================================================================
    # FASE 3: FATTIBILITÀ & ROI (Q7-Q8) - 5-10 minuti
    # ========================================================================

    # ========================================================================
    # Q7 - METRICHE DI SUCCESSO
    # ========================================================================
    {
        "id": "q7_metrics",
        "numero": 7,
        "fase": "ROI",
        "testo": "Come misurerai il successo di questo progetto?",
        "tipo": "metric_selector",
        "subtitle": "Seleziona 2-3 metriche principali che userai per valutare il risultato",
        "options": [
            {
                "value": "response_time",
                "label": "⏱️ Tempo di risposta",
                "description": "Riduzione del tempo da richiesta a risposta",
                "input_type": "range",
                "input_config": {
                    "label_from": "Da (tempo attuale)",
                    "label_to": "A (obiettivo)",
                    "placeholder_from": "es. 2 giorni",
                    "placeholder_to": "es. 5 minuti"
                }
            },
            {
                "value": "cost_reduction",
                "label": "💰 Riduzione costi operativi",
                "description": "Percentuale di riduzione dei costi",
                "input_type": "percentage",
                "input_config": {
                    "label": "Riduzione attesa",
                    "placeholder": "es. 40%"
                }
            },
            {
                "value": "satisfaction",
                "label": "😊 Soddisfazione cliente (NPS/CSAT)",
                "description": "Miglioramento della soddisfazione misurata",
                "input_type": "score",
                "input_config": {
                    "label": "Miglioramento atteso",
                    "placeholder": "es. da 3.5 a 4.5/5"
                }
            },
            {
                "value": "time_saved",
                "label": "⏰ Ore di lavoro liberate",
                "description": "Tempo risparmiato dal team per attività a maggior valore",
                "input_type": "hours",
                "input_config": {
                    "label": "Ore liberate/settimana",
                    "placeholder": "es. 20 ore"
                }
            },
            {
                "value": "error_reduction",
                "label": "✅ Riduzione errori",
                "description": "Percentuale di riduzione errori operativi",
                "input_type": "percentage_range",
                "input_config": {
                    "label_from": "Errori attuali",
                    "label_to": "Obiettivo",
                    "placeholder_from": "es. 15%",
                    "placeholder_to": "es. 3%"
                }
            },
            {
                "value": "revenue",
                "label": "📈 Impatto sul fatturato",
                "description": "Incremento revenue o opportunità generate",
                "input_type": "currency",
                "input_config": {
                    "label": "Incremento stimato annuale",
                    "placeholder": "es. +€50.000"
                }
            }
        ],
        "help": "💡 Executive vogliono numeri concreti! Scegli metriche misurabili e quantificabili.",
        "obbligatorio": True,
        "min_selection": 2,
        "max_selection": 3,
        "insight_trigger": False,
        "note": "NUOVA domanda critica per executive. Focus su ROI misurabile, non solo 'miglioramenti' vaghi."
    },

    # ========================================================================
    # Q8 - TIMELINE & COMMITMENT
    # ========================================================================
    {
        "id": "q8_timeline",
        "numero": 8,
        "fase": "ROI",
        "testo": "Quando vorresti partire e con quale approccio?",
        "tipo": "timeline_selector",
        "approaches": [
            {
                "value": "pilot",
                "label": "🚀 Pilota Veloce (2-4 settimane)",
                "title": "Start rapido con scope limitato",
                "description": "Test su un solo use case o 20% del volume. Validazione veloce dell'idea prima di investire di più.",
                "pros": ["Rischio basso", "Feedback rapido", "Investimento minimo"],
                "cons": ["Scope ridotto", "Non scalabile da subito"],
                "typical_budget": "<€10k",
                "timeline": "2-4 settimane",
                "effort": "Basso"
            },
            {
                "value": "mvp",
                "label": "⚡ MVP Funzionale (2-3 mesi)",
                "title": "Soluzione completa ma essenziale",
                "description": "Implementazione del processo completo con funzionalità core. Pronto per uso reale ma senza fronzoli.",
                "pros": ["Soluzione end-to-end", "Usabile da subito", "Scalabile"],
                "cons": ["Richiede commitment", "Investimento medio"],
                "typical_budget": "€10-50k",
                "timeline": "2-3 mesi",
                "effort": "Medio"
            },
            {
                "value": "gradual",
                "label": "📊 Trasformazione Graduale (6-12 mesi)",
                "title": "Implementazione a fasi multiple",
                "description": "Approccio strutturato con rollout progressivo. Inizia con pilota, scala gradualmente, integra feedback continuo.",
                "pros": ["Rischio controllato", "Change management efficace", "Ottimizzazione continua"],
                "cons": ["Tempo più lungo", "Commitment esteso"],
                "typical_budget": "€50-100k+",
                "timeline": "6-12 mesi",
                "effort": "Alto"
            }
        ],
        "additional_fields": {
            "start_date": {
                "type": "date_picker",
                "label": "📅 Data target inizio",
                "help": "Quando vorresti idealmente partire?"
            },
            "budget_range": {
                "type": "budget_slider",
                "label": "💰 Budget indicativo",
                "options": [
                    {"value": "low", "label": "<€10k", "description": "Budget limitato, pilota"},
                    {"value": "medium", "label": "€10-50k", "description": "MVP funzionale"},
                    {"value": "high", "label": "€50-100k", "description": "Soluzione completa"},
                    {"value": "enterprise", "label": ">€100k", "description": "Trasformazione enterprise"}
                ]
            }
        },
        "help": "💡 Scegli l'approccio che si adatta al tuo contesto. Non c'è una risposta giusta - dipende da risk appetite e urgenza.",
        "obbligatorio": True,
        "insight_trigger": True,
        "insight_type": "final_analysis",
        "note": "NUOVA domanda action-oriented. Trasforma 'fattibilità teorica' in commitment concreto. TRIGGER: AHA! #4 - Analisi finale completa"
    }
]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_total_questions_v2():
    """Ritorna il numero totale di domande V2"""
    return len(QUESTIONS_V2)


def get_questions_by_phase(fase):
    """
    Ritorna domande filtrate per fase

    Args:
        fase: "Discovery", "Design", "ROI"

    Returns:
        List di domande per quella fase
    """
    return [q for q in QUESTIONS_V2 if q["fase"] == fase]


def get_question_by_id(question_id):
    """
    Ritorna domanda per ID

    Args:
        question_id: ID della domanda

    Returns:
        Dict della domanda o None
    """
    for q in QUESTIONS_V2:
        if q["id"] == question_id:
            return q
    return None


def get_insight_triggers():
    """
    Ritorna lista di domande che triggano insights

    Returns:
        List di question IDs con insight_trigger=True
    """
    return [q["id"] for q in QUESTIONS_V2 if q.get("insight_trigger", False)]


def get_progress_stats_v2(answers):
    """
    Calcola statistiche di completamento

    Args:
        answers: Dict di risposte {question_id: answer}

    Returns:
        Dict con statistiche
    """
    total = len(QUESTIONS_V2)
    required = [q for q in QUESTIONS_V2 if q.get("obbligatorio", False)]
    required_count = len(required)

    answered = len([q for q in QUESTIONS_V2 if q["id"] in answers and answers[q["id"]]])
    required_answered = len([q for q in required if q["id"] in answers and answers[q["id"]]])

    return {
        "total": total,
        "answered": answered,
        "percentage": int((answered / total) * 100) if total > 0 else 0,
        "required_total": required_count,
        "required_answered": required_answered,
        "required_percentage": int((required_answered / required_count) * 100) if required_count > 0 else 0,
        "is_complete": required_answered == required_count
    }


# ============================================================================
# VALIDATION
# ============================================================================

def validate_answer_v2(question, answer):
    """
    Valida una risposta

    Args:
        question: Dict domanda
        answer: Risposta utente

    Returns:
        tuple (is_valid: bool, error_message: str)
    """
    # Check obbligatorietà
    if question.get("obbligatorio", False):
        if not answer or (isinstance(answer, str) and not answer.strip()):
            return False, "Questa domanda è obbligatoria"

    # Validazioni specifiche per tipo
    if question["tipo"] == "metric_selector":
        min_sel = question.get("min_selection", 1)
        max_sel = question.get("max_selection", 10)

        if isinstance(answer, list):
            if len(answer) < min_sel:
                return False, f"Seleziona almeno {min_sel} metrica/e"
            if len(answer) > max_sel:
                return False, f"Seleziona massimo {max_sel} metriche"

    return True, ""
