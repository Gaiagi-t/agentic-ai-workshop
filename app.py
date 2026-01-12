import streamlit as st
import config
from utils.questions import QUESTIONS, get_total_questions
from utils.data_manager import download_button, upload_button, render_answers_sidebar, get_progress_stats
from utils.voice_input import render_voice_or_text_input
from utils.ai_analysis import analyze_with_claude, extract_score, generate_quick_insights
from utils.visualizations import (
    create_progress_chart, create_score_gauge, create_impact_matrix,
    render_mermaid_diagram, create_workflow_comparison, create_feasibility_radar,
    create_risk_heatmap
)
from utils.kb_table import render_kb_table
from utils.export import render_pdf_download_button

# Page configuration
st.set_page_config(
    page_title=config.APP_CONFIG["title"],
    page_icon=config.APP_CONFIG["page_icon"],
    layout=config.APP_CONFIG["layout"],
    initial_sidebar_state="expanded"
)

# Custom CSS for IFAB branding
st.markdown(f"""
<style>
    /* IFAB Brand Colors */
    :root {{
        --primary-color: {config.COLORS['primary']};
        --secondary-color: {config.COLORS['secondary']};
        --background-color: {config.COLORS['background']};
        --text-color: {config.COLORS['text']};
    }}

    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, {config.COLORS['primary']} 0%, {config.COLORS['dark_blue']} 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }}

    .main-header h1 {{
        color: white !important;
        margin-bottom: 0.5rem;
    }}

    .ifab-logo {{
        font-size: 2.5rem;
        font-weight: bold;
        color: white;
        font-family: 'Arial', sans-serif;
    }}

    /* Progress bar styling */
    .stProgress > div > div > div > div {{
        background-color: {config.COLORS['secondary']};
    }}

    /* Button styling */
    .stButton>button {{
        background-color: {config.COLORS['primary']};
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }}

    .stButton>button:hover {{
        background-color: {config.COLORS['secondary']};
    }}

    /* Question card */
    .question-card {{
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid {config.COLORS['primary']};
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {config.COLORS['text_secondary']};
        font-size: 0.9rem;
        border-top: 1px solid {config.COLORS['border']};
        margin-top: 3rem;
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'answers' not in st.session_state:
        st.session_state.answers = {}

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0

    if 'current_section' not in st.session_state:
        st.session_state.current_section = "AS-IS"

    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None


init_session_state()

# Header
st.markdown(f"""
<div class="main-header">
    <div class="ifab-logo">IFAB</div>
    <h1>{config.APP_CONFIG['title']}</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem;">
        Workshop Interattivo - Analisi AS-IS → TO-BE
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Navigazione")

    # Section selector
    # Get current section, default to AS-IS
    current_section = st.session_state.get("current_section", "AS-IS")

    section = st.radio(
        "Sezione",
        ["AS-IS", "TO-BE", "Analisi Finale"],
        index=["AS-IS", "TO-BE", "Analisi Finale"].index(current_section) if current_section in ["AS-IS", "TO-BE", "Analisi Finale"] else 0
    )

    st.divider()

    # Progress stats
    render_answers_sidebar()

    st.divider()

    # Export/Import
    st.markdown("### 💾 Gestione Progetto")
    download_button()
    upload_button()

    st.divider()

    # Info
    st.markdown("### ℹ️ Info")
    st.caption(f"""
    {config.IFAB_INFO['name']}

    📍 {config.IFAB_INFO['address']}

    🌐 {config.IFAB_INFO['website']}
    """)

# Main content area
def render_question(question, section_name):
    """Render a single question with appropriate input type"""

    st.markdown(f"""
    <div class="question-card">
        <h3>Domanda {question.get('numero', '')}</h3>
        <p style="font-size: 1.1rem; margin-bottom: 1rem;">{question['testo']}</p>
    </div>
    """, unsafe_allow_html=True)

    question_id = question["id"]

    # Show help text
    if question.get("help"):
        st.info(f"💡 {question['help']}")

    # Render KB table AFTER question title, BEFORE input (more visible and editable)
    render_kb_table(section_name, question["id"], st.session_state.answers)

    # Different input types
    if question["tipo"] == "text_area":
        answer = render_voice_or_text_input(
            question_id,
            "",  # Label already shown above
            placeholder=question.get("placeholder", ""),
            help_text=question.get("help", ""),
            rows=question.get("rows", 4)
        )
        # Only update if answer is not None (voice input handles its own save)
        if answer is not None:
            st.session_state.answers[question_id] = answer

    elif question["tipo"] == "multi_step":
        st.markdown("**Inserisci gli step del processo (uno per riga):**")
        answer = render_voice_or_text_input(
            question_id,
            "",
            placeholder=question.get("placeholder", ""),
            help_text=question.get("help", ""),
            rows=6
        )
        if answer is not None:
            st.session_state.answers[question_id] = answer

    elif question["tipo"] == "table":
        st.markdown("**Compila la tabella:**")
        answer = render_voice_or_text_input(
            question_id,
            "",
            placeholder=f"Esempio:\n{', '.join(question.get('columns', []))}",
            help_text=question.get("help", ""),
            rows=5
        )
        if answer is not None:
            st.session_state.answers[question_id] = answer

    elif question["tipo"] == "multi_agent":
        st.markdown("**Descrivi gli agenti AI:**")
        answer = render_voice_or_text_input(
            question_id,
            "",
            placeholder="Esempio:\n1. Agente Lead: arricchimento automatico lead\n2. Agente Support: gestione ticket...",
            help_text=question.get("help", ""),
            rows=6
        )
        if answer is not None:
            st.session_state.answers[question_id] = answer

    elif question["tipo"] == "agentic_flow_selector":
        st.markdown("**Seleziona il tipo di flusso agentico:**")

        # Display template options
        template_names = [t["name"] for t in config.AGENTIC_FLOW_TEMPLATES]

        selected = st.selectbox(
            "Tipo di flusso",
            options=template_names,
            index=0,
            key=f"input_{question_id}",
            label_visibility="collapsed"
        )

        # Show template details
        selected_template = next(
            (t for t in config.AGENTIC_FLOW_TEMPLATES if t["name"] == selected),
            None
        )

        if selected_template:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"## {selected_template['icon']}")
            with col2:
                st.markdown(f"**{selected_template['name']}**")
                st.caption(selected_template['description'])

            # Show diagram
            with st.expander("📊 Visualizza diagramma"):
                render_mermaid_diagram(selected_template['mermaid'])

        st.session_state.answers[question_id] = selected

    # Mark if required and not answered
    if question.get("obbligatorio") and not st.session_state.answers.get(question_id):
        st.warning("⚠️ Questa domanda è obbligatoria")

def render_as_is_section():
    """Render AS-IS section"""
    questions = QUESTIONS["AS-IS"]

    # Get current question index within section
    current_q_idx = st.session_state.current_question_index

    if current_q_idx < len(questions):
        question = questions[current_q_idx]

        # Progress bar
        progress = (current_q_idx + 1) / len(questions)
        st.progress(progress)
        st.caption(f"Domanda {current_q_idx + 1} di {len(questions)}")

        # Render question
        render_question(question, "AS-IS")

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if current_q_idx > 0:
                if st.button("⬅️ Indietro"):
                    st.session_state.current_question_index -= 1
                    st.rerun()

        with col2:
            # Skip button for optional questions
            if not question.get("obbligatorio"):
                if st.button("⏭️ Salta"):
                    st.session_state.current_question_index += 1
                    st.rerun()

        with col3:
            # Next/Continue button
            # Check if answer exists and is not empty
            button_label = "Avanti ➡️" if current_q_idx < len(questions) - 1 else "Completa AS-IS ✅"

            if st.button(button_label, type="primary"):
                if current_q_idx < len(questions) - 1:
                    st.session_state.current_question_index += 1
                    st.rerun()
                else:
                    # Move to TO-BE section
                    st.session_state.current_section = "TO-BE"
                    st.session_state.current_question_index = 0
                    st.success("✅ Sezione AS-IS completata! Passa alla sezione TO-BE.")
                    st.rerun()

def render_to_be_section():
    """Render TO-BE section"""
    questions = QUESTIONS["TO-BE"]

    # Get current question index within section
    current_q_idx = st.session_state.current_question_index

    if current_q_idx < len(questions):
        question = questions[current_q_idx]

        # Progress bar
        progress = (current_q_idx + 1) / len(questions)
        st.progress(progress)
        st.caption(f"Domanda {current_q_idx + 1} di {len(questions)}")

        # Render question
        render_question(question, "TO-BE")

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if current_q_idx > 0:
                if st.button("⬅️ Indietro"):
                    st.session_state.current_question_index -= 1
                    st.rerun()
            elif st.button("⬅️ Torna a AS-IS"):
                st.session_state.current_section = "AS-IS"
                st.session_state.current_question_index = len(QUESTIONS["AS-IS"]) - 1
                st.rerun()

        with col2:
            # Skip button for optional questions
            if not question.get("obbligatorio"):
                if st.button("⏭️ Salta"):
                    st.session_state.current_question_index += 1
                    st.rerun()

        with col3:
            # Next/Continue button
            # Check if answer exists and is not empty
            button_label = "Avanti ➡️" if current_q_idx < len(questions) - 1 else "Completa TO-BE ✅"

            if st.button(button_label, type="primary"):
                if current_q_idx < len(questions) - 1:
                    st.session_state.current_question_index += 1
                    st.rerun()
                else:
                    # Move to Analysis section
                    st.session_state.current_section = "Analisi Finale"
                    st.success("✅ Sezione TO-BE completata! Passa all'Analisi Finale.")
                    st.rerun()

def render_analysis_section():
    """Render analysis section with AI insights"""

    st.markdown("## 📊 Analisi Finale del Progetto")

    # Check if we have enough data
    required_questions = ["as_is_processo", "as_is_problemi", "to_be_visione", "to_be_benefici"]
    missing = [q for q in required_questions if not st.session_state.answers.get(q)]

    if missing:
        st.warning("⚠️ Completa almeno le domande obbligatorie di AS-IS e TO-BE per generare l'analisi.")
        return

    # Generate analysis button
    if not st.session_state.analysis_results:
        if st.button("🚀 Genera Analisi con AI", type="primary"):
            analysis = analyze_with_claude(st.session_state.answers)
            if analysis:
                st.session_state.analysis_results = analysis
                st.rerun()
    else:
        # Display analysis results
        st.success("✅ Analisi completata!")

        # Overall score
        score = extract_score(st.session_state.analysis_results)
        if score:
            col1, col2 = st.columns([1, 2])
            with col1:
                fig = create_score_gauge(score)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.markdown(f"### Score: {score}/10")
                st.markdown(st.session_state.analysis_results.get("score_complessivo", ""))

        st.divider()

        # Display all sections (keys without accents to match ai_analysis.py)
        sections_display = {
            "fattibilita_tecnica": ("🔧 Fattibilita Tecnica", "info"),
            "analisi_impatto_sostituzione_vs_augmentation": ("⚖️ Sostituzione vs Augmentation", "warning"),
            "risparmio_di_tempo_stimato": ("⏱️ Risparmio di Tempo", "success"),
            "riduzione_costi": ("💰 Riduzione Costi", "success"),
            "attivita_eliminate_o_ottimizzate": ("✂️ Attivita Ottimizzate", "info"),
            "rischi_e_criticita": ("⚠️ Rischi e Criticita", "warning"),
            "formazione_necessaria": ("🎓 Formazione", "info"),
            "problemi_legali_e_privacy": ("⚖️ Aspetti Legali e Privacy", "warning"),
            "roadmap_implementazione": ("🗺️ Roadmap", "success"),
            "diagramma_flusso_agentico": ("📊 Diagramma Flusso Agentico", "diagram"),
            "raccomandazioni_finali": ("💡 Raccomandazioni", "info")
        }

        for key, (title, msg_type) in sections_display.items():
            content = st.session_state.analysis_results.get(key, "")
            if content:
                with st.expander(title, expanded=(key in ["raccomandazioni_finali", "roadmap_implementazione", "diagramma_flusso_agentico"])):
                    if msg_type == "diagram":
                        # Extract and render Mermaid diagram
                        render_mermaid_diagram(content)
                    elif msg_type == "info":
                        st.info(content)
                    elif msg_type == "warning":
                        st.warning(content)
                    elif msg_type == "success":
                        st.success(content)
                    else:
                        st.markdown(content)

        st.divider()

        # Visualizations
        st.markdown("### 📈 Dashboard Analisi")

        # Row 1: Radar chart and Impact matrix
        col1, col2 = st.columns(2)

        with col1:
            # Radar chart - multi-dimensional analysis
            fig_radar = create_feasibility_radar(st.session_state.analysis_results)
            st.plotly_chart(fig_radar, use_container_width=True)

        with col2:
            # Impact matrix (dynamic positioning based on analysis)
            fig = create_impact_matrix(
                analysis_results=st.session_state.analysis_results,
                answers=st.session_state.answers
            )
            st.plotly_chart(fig, use_container_width=True)

        # Row 2: Risk heatmap and Workflow comparison
        col3, col4 = st.columns(2)

        with col3:
            # Risk heatmap
            fig_risk = create_risk_heatmap(st.session_state.analysis_results)
            st.plotly_chart(fig_risk, use_container_width=True)

        with col4:
            # Workflow comparison
            as_is_steps = st.session_state.answers.get("as_is_step", "")
            to_be_vision = st.session_state.answers.get("to_be_visione", "")
            if as_is_steps and to_be_vision:
                create_workflow_comparison(as_is_steps, to_be_vision)

        st.divider()

        # Export options
        st.markdown("### 📤 Esporta Analisi")

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            render_pdf_download_button(st.session_state.answers, st.session_state.analysis_results)

        with col_btn2:
            if st.button("🔄 Rigenera Analisi", use_container_width=True):
                st.session_state.analysis_results = None
                st.rerun()

# Main routing logic
if section == "AS-IS":
    st.session_state.current_section = "AS-IS"
    render_as_is_section()

elif section == "TO-BE":
    st.session_state.current_section = "TO-BE"
    render_to_be_section()

elif section == "Analisi Finale":
    st.session_state.current_section = "Analisi Finale"
    render_analysis_section()

# Footer
st.markdown(f"""
<div class="footer">
    <p><strong>{config.IFAB_INFO['name']}</strong></p>
    <p>{config.IFAB_INFO['address']} | {config.IFAB_INFO['website']}</p>
    <p style="margin-top: 1rem;">Powered by Claude AI & Streamlit</p>
</div>
""", unsafe_allow_html=True)
