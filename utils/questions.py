# Question definitions for the workshop

QUESTIONS = {
    "AS-IS": [
        {
            "id": "as_is_processo",
            "numero": 1,
            "testo": "Qual è il processo che stai analizzando?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Esempi: gestione ordini, gestione reclami, selezione del personale, redazione di offerte commerciali",
            "placeholder": "Descrivi il processo aziendale che vuoi analizzare..."
        },
        {
            "id": "as_is_step",
            "numero": 2,
            "testo": "Quali sono i singoli passi (step)?",
            "tipo": "multi_step",
            "obbligatorio": True,
            "help": "Scrivili uno per riga. Puoi aggiungere/rimuovere step dinamicamente.",
            "placeholder": "Esempio: 1. Ricezione richiesta cliente\n2. Verifica disponibilità\n3. Preparazione preventivo..."
        },
        {
            "id": "as_is_ruoli",
            "numero": 3,
            "testo": "Chi esegue attualmente ciascun passo?",
            "tipo": "table",
            "obbligatorio": True,
            "help": "Specifica i ruoli, non solo i nomi (es. HR, Customer Service, Sales Manager)",
            "columns": ["Step", "Ruolo Responsabile", "N. Persone Coinvolte"]
        },
        {
            "id": "as_is_strumenti",
            "numero": 4,
            "testo": "Quali strumenti o software vengono usati?",
            "tipo": "text_area",
            "obbligatorio": False,
            "help": "Esempi: Excel, CRM, Outlook, ERP, software specifici",
            "placeholder": "Elenca gli strumenti utilizzati..."
        },
        {
            "id": "as_is_tempo",
            "numero": 5,
            "testo": "Quanto tempo richiede ogni passo?",
            "tipo": "table",
            "obbligatorio": False,
            "help": "Anche stime 'a spanne' vanno bene (es. 10 minuti, 2 giorni)",
            "columns": ["Step", "Tempo Stimato", "Unità (min/ore/giorni)"]
        },
        {
            "id": "as_is_problemi",
            "numero": 6,
            "testo": "Quali sono i problemi e le criticità?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Esempi: passaggi ripetitivi, errori frequenti, ritardi, troppe attività manuali, colli di bottiglia",
            "placeholder": "Descrivi i principali problemi e inefficienze del processo attuale..."
        }
    ],

    "TO-BE": [
        {
            "id": "to_be_visione",
            "numero": 1,
            "testo": "Come immagini il nuovo processo con l'agentic AI?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Descrivi la tua visione del processo trasformato",
            "placeholder": "Descrivi come sarà il processo dopo l'introduzione dell'AI..."
        },
        {
            "id": "to_be_agenti",
            "numero": 2,
            "testo": "Quanti e quali agenti AI immagini? Qual è/sono il/i suo/i obiettivo/i?",
            "tipo": "multi_agent",
            "obbligatorio": True,
            "help": "Esempi: Agentic Lead (arricchimento lead), Agentic Knowledge (consultazione KB), Agentic Support (gestione ticket)",
            "fields": ["Nome Agente", "Obiettivo/Scopo", "Tipologia"]
        },
        {
            "id": "to_be_input_output",
            "numero": 3,
            "testo": "Quali input riceve e quali output produce?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Specifica formati, canali, documenti generati per ciascun agente",
            "placeholder": "Esempio: Input: Email cliente, documenti PDF. Output: Risposta strutturata, ticket aggiornato..."
        },
        {
            "id": "to_be_azioni_limiti",
            "numero": 4,
            "testo": "Quali azioni deve sapere eseguire in autonomia e con quali limiti?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Decisioni consentite, intervento umano necessario, soglie di confidenza, cosa NON può fare, escalation umana",
            "placeholder": "Esempio: Può rispondere autonomamente a domande standard, ma deve escalare se confidenza < 80%..."
        },
        {
            "id": "to_be_dati_sistemi",
            "numero": 5,
            "testo": "Su quali dati e sistemi lavora?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Fonti dati e permessi (CRM, ticketing, database), API, log, audit trail",
            "placeholder": "Esempio: Accesso in lettura al CRM Salesforce, database clienti, knowledge base interna..."
        },
        {
            "id": "to_be_tool",
            "numero": 6,
            "testo": "Quali tool deve integrare?",
            "tipo": "text_area",
            "obbligatorio": False,
            "help": "Esempi: Calendari, email, database, API esterne, sistemi di pagamento",
            "placeholder": "Elenca i tool e le integrazioni necessarie..."
        },
        {
            "id": "to_be_flusso",
            "numero": 7,
            "testo": "Quale flusso agentico state immaginando?",
            "tipo": "agentic_flow_selector",
            "obbligatorio": True,
            "help": "Seleziona un template: single agent, multi agent sequenziale/parallelo, orchestratore, router, loop feedback"
        },
        {
            "id": "to_be_soluzioni",
            "numero": 8,
            "testo": "Esistono già soluzioni da acquistare adatte e affidabili?",
            "tipo": "text_area",
            "obbligatorio": False,
            "help": "Se sì, quali? Indicare vendor, prodotti, costi stimati",
            "placeholder": "Esempio: Intercom AI Agent, Zendesk AI, custom con LangChain..."
        },
        {
            "id": "to_be_tempo",
            "numero": 9,
            "testo": "Quanto tempo richiederà ogni step nel TO-BE?",
            "tipo": "table",
            "obbligatorio": False,
            "help": "Idealmente minore rispetto all'AS-IS. Anche stime vanno bene.",
            "columns": ["Step", "Tempo Stimato", "Unità (min/ore/giorni)"]
        },
        {
            "id": "to_be_benefici",
            "numero": 10,
            "testo": "Quali benefici prevedi?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Esempi: meno errori, più velocità, minor costo, meno carico di lavoro, migliore customer experience",
            "placeholder": "Descrivi i benefici attesi dall'implementazione..."
        },
        {
            "id": "to_be_rischi",
            "numero": 11,
            "testo": "Ci sono rischi o ostacoli da gestire?",
            "tipo": "text_area",
            "obbligatorio": True,
            "help": "Esempi: resistenze interne, costi iniziali, privacy/GDPR, training necessario, change management",
            "placeholder": "Identifica i principali rischi e ostacoli..."
        },
        {
            "id": "to_be_system_prompt",
            "numero": 12,
            "testo": "Abbozziamo un system prompt?",
            "tipo": "text_area",
            "obbligatorio": False,
            "help": "Prova a scrivere le istruzioni che daresti all'agente AI principale",
            "placeholder": "Sei un assistente AI che...",
            "rows": 8
        }
    ],

    "CONFRONTO": [
        {
            "id": "confronto_tempo",
            "testo": "Qual è il guadagno in tempo?",
            "tipo": "calculated"
        },
        {
            "id": "confronto_costi",
            "testo": "Quali costi si riducono?",
            "tipo": "ai_generated"
        },
        {
            "id": "confronto_attivita",
            "testo": "Ci sono attività eliminate o rese più veloci?",
            "tipo": "ai_generated"
        },
        {
            "id": "confronto_formazione",
            "testo": "Serve formazione?",
            "tipo": "ai_generated"
        },
        {
            "id": "confronto_privacy",
            "testo": "Ci sono problemi legali o di privacy?",
            "tipo": "ai_generated"
        },
        {
            "id": "confronto_fattibilita",
            "testo": "Il progetto è realizzabile subito o richiede fasi pilota?",
            "tipo": "ai_generated"
        },
        {
            "id": "confronto_impatto",
            "testo": "Sostituzione vs Augmentation - Quale impatto ha il tuo progetto?",
            "tipo": "ai_analysis"
        }
    ]
}

def get_total_questions():
    """Returns total number of questions across all sections"""
    return len(QUESTIONS["AS-IS"]) + len(QUESTIONS["TO-BE"])

def get_question_by_id(question_id):
    """Returns question object by ID"""
    for section in QUESTIONS.values():
        for q in section:
            if q.get("id") == question_id:
                return q
    return None

def get_section_progress(section_name, answered_questions):
    """Calculate progress for a specific section"""
    section_questions = QUESTIONS.get(section_name, [])
    total = len(section_questions)
    answered = sum(1 for q in section_questions if q.get("id") in answered_questions)
    return answered, total
