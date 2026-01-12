# Configuration file for Agentic AI Workshop App
import os

# API Keys - Read from st.secrets (Streamlit Cloud) or environment variables
def get_api_key(key_name):
    """Get API key from Streamlit secrets or environment variables"""
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except:
        pass
    return os.environ.get(key_name, "")

ANTHROPIC_API_KEY = get_api_key("ANTHROPIC_API_KEY")
OPENAI_API_KEY = get_api_key("OPENAI_API_KEY")

# IFAB Brand Colors (from official website www.ifabfoundation.org)
COLORS = {
    "primary": "#1b98e0",      # Main Blue (IFAB signature color)
    "secondary": "#25B7D3",    # Teal/Cyan accent
    "accent": "#DBCB4F",       # Yellow accent
    "dark_blue": "#004e7a",    # Dark blue
    "navy": "#0345A5",         # Navy blue
    "footer_bg": "#021f54",    # Very dark navy (footer)
    "background": "#ffffff",   # White background
    "text": "#333333",         # Dark gray text
    "text_secondary": "#999999", # Secondary text gray
    "success": "#10B981",      # Green for success states
    "warning": "#DBCB4F",      # Yellow for warnings (IFAB accent)
    "danger": "#EF4444",       # Red for errors
    "border": "#E2E8F0",       # Border color
}

# IFAB Information
IFAB_INFO = {
    "name": "IFAB - International Foundation Big Data & Artificial Intelligence for Human Development",
    "website": "www.ifabfoundation.org",
    "address": "Via Galliera 32, 40121 Bologna",
}

# App Configuration
APP_CONFIG = {
    "title": "REINVENTARE I PROCESSI AZIENDALI CON L'AGENTIC AI",
    "page_icon": "🤖",
    "layout": "wide",
}

# Agentic Flow Templates
AGENTIC_FLOW_TEMPLATES = [
    {
        "name": "Single Agent",
        "description": "Un singolo agente AI gestisce l'intero processo end-to-end",
        "icon": "🤖",
        "mermaid": """graph TD
    A[Input] --> B[Agente AI]
    B --> C{Decisione}
    C --> D[Azione 1]
    C --> E[Azione 2]
    D --> F[Output]
    E --> F
    G[Human Oversight] -.-> B"""
    },
    {
        "name": "Multi-Agent",
        "description": "Piu agenti specializzati collaborano, ognuno con competenze specifiche",
        "icon": "👥",
        "mermaid": """graph LR
    A[Input] --> B[Agente Analisi]
    B --> C[Agente Elaborazione]
    C --> D[Agente Validazione]
    D --> E[Output]
    F[Memoria Condivisa] -.-> B
    F -.-> C
    F -.-> D"""
    },
    {
        "name": "Instradamento (Routing)",
        "description": "Un router classifica e indirizza le richieste all'agente piu adatto",
        "icon": "🔀",
        "mermaid": """graph TD
    A[Input] --> B{Router/Classifier}
    B -->|Tipo A| C[Agente Specialista A]
    B -->|Tipo B| D[Agente Specialista B]
    B -->|Tipo C| E[Agente Specialista C]
    B -->|Complesso| F[Human Expert]
    C --> G[Output]
    D --> G
    E --> G
    F --> G"""
    },
    {
        "name": "Parallelizzazione",
        "description": "Task diviso in sotto-task eseguiti in parallelo e poi aggregati",
        "icon": "⚡",
        "mermaid": """graph TD
    A[Input] --> B[Splitter]
    B --> C[Agente 1]
    B --> D[Agente 2]
    B --> E[Agente 3]
    C --> F[Aggregatore]
    D --> F
    E --> F
    F --> G[Output]
    style C fill:#e1f5fe
    style D fill:#e1f5fe
    style E fill:#e1f5fe"""
    },
    {
        "name": "Orchestrazione",
        "description": "Un orchestratore centrale coordina dinamicamente agenti specializzati",
        "icon": "🎯",
        "mermaid": """graph TD
    A[Input] --> B[Orchestratore]
    B --> C[Agente Ricerca]
    B --> D[Agente Analisi]
    B --> E[Agente Scrittura]
    C --> B
    D --> B
    E --> B
    B --> F{Task Completo?}
    F -->|No| B
    F -->|Si| G[Output]"""
    },
    {
        "name": "Valutazione/Ottimizzazione",
        "description": "Loop iterativo con valutazione qualita e ottimizzazione continua",
        "icon": "🔄",
        "mermaid": """graph TD
    A[Input] --> B[Agente Generatore]
    B --> C[Agente Valutatore]
    C --> D{Score OK?}
    D -->|No, Score Basso| E[Feedback Specifico]
    E --> B
    D -->|Si, Score Alto| F[Output Ottimizzato]
    G[Criteri Qualita] -.-> C"""
    },
    {
        "name": "Prompt Chain (Gate Condizionali)",
        "description": "Ragionamento sequenziale con checkpoint e decisioni condizionali",
        "icon": "⛓️",
        "mermaid": """graph TD
    A[Input] --> B[Step 1: Comprensione]
    B --> C{Gate 1: Chiaro?}
    C -->|No| D[Richiedi Chiarimenti]
    D --> B
    C -->|Si| E[Step 2: Analisi]
    E --> F{Gate 2: Dati Sufficienti?}
    F -->|No| G[Raccogli Dati]
    G --> E
    F -->|Si| H[Step 3: Elaborazione]
    H --> I{Gate 3: Valido?}
    I -->|No| J[Correggi]
    J --> H
    I -->|Si| K[Output Finale]"""
    }
]
