"""
Agentic AI Workshop V2 - Executive Edition
Main application optimized for 30-45 minute workshop

Features:
- 8 strategic questions (vs 18 V1)
- Business-friendly language (no technical jargon)
- 4 distributed "aha!" moments
- Educational 4-layer analysis
- Concrete action plan with vendor suggestions

Target audience: Executive/Manager
Goal: Discover AI opportunities (not detailed design)
"""

import streamlit as st
import config
from utils_v2.questions_v2 import QUESTIONS_V2, get_total_questions_v2, get_progress_stats_v2
from utils_v2.onboarding import render_onboarding
from utils_v2.ai_analysis_v2 import analyze_with_claude_v2
from utils.data_manager import download_button, upload_button
from utils.voice_input import render_voice_or_text_input

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Agentic AI Workshop V2 - Executive Edition",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS (Executive-friendly, più clean di V1)
# ============================================================================

st.markdown(f"""
<style>
    /* IFAB Brand Colors */
    :root {{
        --primary-color: {config.COLORS['primary']};
        --secondary-color: {config.COLORS['secondary']};
        --background-color: {config.COLORS['background']};
        --text-color: {config.COLORS['text']};
    }}

    /* Main header */
    .main-header {{
        background: linear-gradient(135deg, #1b98e0 0%, #DBCB4F 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }}

    .ifab-logo {{
        font-size: 2rem;
        font-weight: bold;
        color: white;
    }}

    /* Question card V2 (più minimal) */
    .question-card-v2 {{
        background: white;
        padding: 2rem;
        border-radius: 8px;
        border-left: 3px solid #1b98e0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
    }}

    /* Insight card (animated) */
    .insight-card {{
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
        animation: slideIn 0.5s ease-out;
    }}

    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateY(-10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Phase indicator */
    .phase-indicator {{
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }}

    /* Progress bar custom */
    .stProgress > div > div > div > div {{
        background-color: #1b98e0;
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 6px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }}

    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem 0;
        color: #999;
        font-size: 0.9rem;
        border-top: 1px solid #eee;
        margin-top: 3rem;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state_v2():
    """Initialize session state for V2"""
    if 'answers_v2' not in st.session_state:
        st.session_state.answers_v2 = {}

    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    if 'analysis_v2' not in st.session_state:
        st.session_state.analysis_v2 = None

    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False

    if 'show_import' not in st.session_state:
        st.session_state.show_import = False

    # IMPORTANTE: Crea alias per compatibilità con utils V1
    # render_voice_or_text_input si aspetta 'answers' non 'answers_v2'
    st.session_state.answers = st.session_state.answers_v2

init_session_state_v2()

# ============================================================================
# ONBOARDING
# ============================================================================

if not st.session_state.onboarding_complete:
    if render_onboarding():
        st.rerun()
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"""
<div class="main-header">
    <div class="ifab-logo">{config.IFAB_INFO['name']}</div>
    <h1>🚀 Agentic AI Workshop - Executive Edition</h1>
    <p style="font-size: 1.1rem; margin-top: 0.5rem;">
        Scopri in 30-45 minuti se l'AI può trasformare il tuo processo
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - PROGRESS & KB
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 Progressi")

    stats = get_progress_stats_v2(st.session_state.answers_v2)

    st.progress(stats["percentage"] / 100)
    st.caption(f"{stats['answered']}/{stats['total']} domande completate")

    # Fase corrente
    current_q_idx = st.session_state.current_question
    if current_q_idx < len(QUESTIONS_V2):
        current_fase = QUESTIONS_V2[current_q_idx]["fase"]
        fase_emoji = {"Discovery": "🔍", "Design": "🎨", "ROI": "💰"}
        st.markdown(f"**Fase corrente:** {fase_emoji.get(current_fase, '📍')} {current_fase}")

    st.divider()

    # Knowledge Base compatta
    st.markdown("### 📋 Il Tuo Progetto")

    if st.session_state.answers_v2:
        # Q1 - Problema
        if 'q1_problem' in st.session_state.answers_v2:
            problem = st.session_state.answers_v2['q1_problem']
            if len(problem) > 80:
                problem = problem[:80] + "..."
            st.markdown(f"**🎯 Processo:**\n{problem}")

        # Q2 - Visione
        if 'q2_vision' in st.session_state.answers_v2:
            vision = st.session_state.answers_v2['q2_vision']
            if len(vision) > 80:
                vision = vision[:80] + "..."
            st.markdown(f"**✨ Visione:**\n{vision}")

        # Q5 - Flusso
        if 'q5_flow' in st.session_state.answers_v2:
            flow = st.session_state.answers_v2['q5_flow']
            flow_labels = {
                "single_agent": "🤖 Assistente Unico",
                "multi_agent": "🔄 Team Specialisti",
                "router": "🚦 Router Intelligente"
            }
            st.markdown(f"**Flusso:** {flow_labels.get(flow, flow)}")

    else:
        st.info("Inizia a rispondere alle domande per vedere il tuo progetto prendere forma!")

    st.divider()

    # Export/Import
    st.markdown("### 💾 Salva/Carica")

    # Export (solo se ci sono risposte)
    if st.session_state.answers_v2:
        import json
        from datetime import datetime

        export_data = {
            "version": "2.0",
            "timestamp": datetime.now().isoformat(),
            "answers": st.session_state.answers_v2,
            "current_question": st.session_state.current_question
        }

        st.download_button(
            label="📥 Esporta Progetto",
            data=json.dumps(export_data, indent=2, ensure_ascii=False),
            file_name=f"agentic_ai_workshop_v2_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )

    # Import
    uploaded_file = st.file_uploader("📤 Carica Progetto", type=['json'])
    if uploaded_file:
        import json
        try:
            data = json.load(uploaded_file)
            if data.get("version") == "2.0":
                st.session_state.answers_v2 = data.get("answers", {})
                st.session_state.current_question = data.get("current_question", 0)
                st.success("✅ Progetto caricato!")
                st.rerun()
            else:
                st.error("❌ File non compatibile con V2")
        except Exception as e:
            st.error(f"❌ Errore: {str(e)}")

# ============================================================================
# FUNCTION DEFINITIONS (MUST BE BEFORE MAIN FLOW)
# ============================================================================

def render_question_v2(question):
    """Render singola domanda con fase indicator e progress"""

    fase = question['fase']
    fase_colors = {
        "Discovery": "#4CAF50",
        "Design": "#FF9800",
        "ROI": "#2196F3"
    }

    # Phase indicator
    st.markdown(f"""
    <div class="phase-indicator" style="color: {fase_colors.get(fase, '#666')}">
        📍 Fase {fase} · Domanda {question['numero']}/8
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    progress = question['numero'] / 8
    st.progress(progress)

    # Question card
    st.markdown(f"""
    <div class="question-card-v2">
        <h2>{question['testo']}</h2>
    </div>
    """, unsafe_allow_html=True)

    # Help text
    if question.get("help"):
        st.info(f"💡 {question['help']}")

    # Input field (delegato a funzioni specifiche per tipo)
    answer = render_input_by_type_v2(question)

    # Salva risposta
    if answer is not None:
        st.session_state.answers_v2[question['id']] = answer

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Indietro"):
                st.session_state.current_question -= 1
                st.rerun()

    with col3:
        next_label = "Avanti ➡️" if question['numero'] < 8 else "🚀 Genera Analisi"

        if st.button(next_label, type="primary"):
            # Validazione
            if question.get("obbligatorio", False):
                if not answer or (isinstance(answer, str) and not answer.strip()):
                    st.error("⚠️ Questa domanda è obbligatoria")
                    st.stop()

            # Avanza
            st.session_state.current_question += 1
            st.rerun()


def render_input_by_type_v2(question):
    """
    Render input field basato sul tipo di domanda
    Supporta: text_area, two_column_input, checkbox_with_other, visual_selector, etc.

    Returns:
        Answer value (tipo dipende da question type)
    """
    q_type = question["tipo"]
    q_id = question["id"]

    # === TEXT AREA (standard) ===
    if q_type == "text_area":
        return render_voice_or_text_input(
            question_id=q_id,
            question_text="",  # Già mostrato sopra
            placeholder=question.get("placeholder", ""),
            help_text="",
            rows=question.get("rows", 3)
        )

    # === TWO COLUMN INPUT (Q3 - AI vs Human) ===
    elif q_type == "two_column_input":
        col1, col2 = st.columns(2)

        with col1:
            ai_label = question["columns"]["ai_decisions"]["label"]
            ai_placeholder = question["columns"]["ai_decisions"]["placeholder"]
            ai_rows = question["columns"]["ai_decisions"]["rows"]

            ai_decisions = st.text_area(
                ai_label,
                value=st.session_state.answers_v2.get(q_id, {}).get("ai_decisions", ""),
                placeholder=ai_placeholder,
                height=ai_rows * 30,
                key=f"{q_id}_ai"
            )

        with col2:
            human_label = question["columns"]["human_decisions"]["label"]
            human_placeholder = question["columns"]["human_decisions"]["placeholder"]
            human_rows = question["columns"]["human_decisions"]["rows"]

            human_decisions = st.text_area(
                human_label,
                value=st.session_state.answers_v2.get(q_id, {}).get("human_decisions", ""),
                placeholder=human_placeholder,
                height=human_rows * 30,
                key=f"{q_id}_human"
            )

        return {
            "ai_decisions": ai_decisions,
            "human_decisions": human_decisions
        }

    # === CHECKBOX WITH OTHER (Q4, Q6) ===
    elif q_type in ["checkbox_with_other", "checkbox_with_notes"]:
        st.markdown("**Seleziona tutte le opzioni che si applicano:**")

        selected = []
        for opt in question["options"]:
            if st.checkbox(opt["label"], key=f"{q_id}_{opt['value']}"):
                selected.append(opt)

        # Campo "other" o "notes"
        if q_type == "checkbox_with_other" and "other_field" in question:
            other_text = st.text_area(
                question["other_field"].get("placeholder", "Altro..."),
                height=question["other_field"].get("rows", 2) * 30,
                key=f"{q_id}_other_textarea"  # Diverso da checkbox key
            )
        elif q_type == "checkbox_with_notes" and "notes_field" in question:
            other_text = st.text_area(
                question["notes_field"].get("placeholder", "Note..."),
                height=question["notes_field"].get("rows", 3) * 30,
                key=f"{q_id}_notes_textarea"  # Diverso da checkbox key
            )
        else:
            other_text = ""

        return {
            "selected": selected,
            "other" if q_type == "checkbox_with_other" else "notes": other_text
        }

    # === VISUAL SELECTOR (Q5 - Flusso) ===
    elif q_type == "visual_selector":
        st.markdown("**Scegli l'approccio che meglio si adatta:**")

        # Render cards
        for opt in question["options"]:
            with st.container():
                col_icon, col_content = st.columns([1, 5])

                with col_icon:
                    st.markdown(f"<div style='font-size: 3rem; text-align: center;'>{opt['label'].split()[0]}</div>",
                                unsafe_allow_html=True)

                with col_content:
                    st.markdown(f"**{opt['title']}**")
                    st.caption(opt["description"])
                    st.caption(f"💡 {opt['use_cases']}")

                if st.button(f"Scegli {opt['label']}", key=f"{q_id}_{opt['value']}", use_container_width=True):
                    return opt['value']

        # Se già selezionato, mostra scelta
        current = st.session_state.answers_v2.get(q_id)
        if current:
            st.success(f"✅ Scelta attuale: {current}")
            return current

        return None

    # === METRIC SELECTOR (Q7) ===
    elif q_type == "metric_selector":
        st.markdown(f"**{question.get('subtitle', 'Seleziona le metriche')}**")

        selected_metrics = []
        for opt in question["options"]:
            if st.checkbox(f"{opt['label']} - {opt['description']}", key=f"{q_id}_{opt['value']}"):
                selected_metrics.append(opt)

        min_sel = question.get("min_selection", 1)
        max_sel = question.get("max_selection", 10)

        if len(selected_metrics) < min_sel:
            st.warning(f"⚠️ Seleziona almeno {min_sel} metrica/e")
        elif len(selected_metrics) > max_sel:
            st.warning(f"⚠️ Seleziona massimo {max_sel} metriche")

        return selected_metrics

    # === TIMELINE SELECTOR (Q8) ===
    elif q_type == "timeline_selector":
        st.markdown("**Scegli il tuo approccio:**")

        # Render approach cards
        selected_approach = None
        for approach in question["approaches"]:
            with st.expander(f"{approach['label']} - {approach['title']}", expanded=False):
                st.markdown(approach["description"])

                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.caption(f"**Budget:** {approach['typical_budget']}")
                    st.caption(f"**Timeline:** {approach['timeline']}")
                with col_info2:
                    st.caption(f"**Pro:** {', '.join(approach['pros'][:2])}")

                if st.button(f"Scegli {approach['label']}", key=f"{q_id}_{approach['value']}"):
                    selected_approach = approach['value']

        # Additional fields
        st.markdown("---")
        st.markdown("**Dettagli aggiuntivi:**")

        col_date, col_budget = st.columns(2)

        with col_date:
            start_date = st.date_input(
                "📅 Data target inizio",
                key=f"{q_id}_date"
            )

        with col_budget:
            budget_range = st.select_slider(
                "💰 Budget indicativo",
                options=["<€10k", "€10-50k", "€50-100k", ">€100k"],
                key=f"{q_id}_budget"
            )

        # Se già salvato, usa quello
        current = st.session_state.answers_v2.get(q_id, {})
        if not selected_approach:
            selected_approach = current.get("approach")

        return {
            "approach": selected_approach,
            "start_date": str(start_date) if start_date else current.get("start_date"),
            "budget_range": budget_range if budget_range else current.get("budget_range")
        }

    # Fallback - text input semplice
    else:
        return st.text_input("Risposta:", key=f"{q_id}_fallback")


# ============================================================================
# RENDER FINAL ANALYSIS
# ============================================================================

def render_final_analysis_v2():
    """Render analisi finale con 4 layer educativi"""

    st.markdown("## 🎯 La Tua Analisi Personalizzata")

    if not st.session_state.analysis_v2:
        if st.button("🚀 Genera Analisi Completa", type="primary", use_container_width=True):
            with st.spinner("Sto analizzando il tuo progetto... (30-45 secondi)"):
                analysis = analyze_with_claude_v2(st.session_state.answers_v2)
                if analysis:
                    st.session_state.analysis_v2 = analysis
                    st.rerun()
                else:
                    st.error("❌ Errore nella generazione dell'analisi. Verifica le API keys.")
        st.stop()

    analysis = st.session_state.analysis_v2

    # ========================================================================
    # LAYER 1: EXECUTIVE SUMMARY (sempre visibile)
    # ========================================================================

    st.markdown("### 📊 Executive Summary")

    # Score
    score = analysis.get("score", 0)
    if score:
        col_score, col_roi = st.columns([1, 2])

        with col_score:
            # Gauge semplificato (no plotly per ora in MVP)
            score_color = "#4CAF50" if score >= 7 else "#FF9800" if score >= 5 else "#F44336"
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: {score_color};
                        color: white; border-radius: 8px;">
                <h1 style="margin: 0; font-size: 3rem;">{score}/10</h1>
                <p style="margin: 0;">{'🟢 ALTA' if score >= 7 else '🟡 MEDIA' if score >= 5 else '🔴 BASSA'} FATTIBILITÀ</p>
            </div>
            """, unsafe_allow_html=True)

        with col_roi:
            roi_summary = analysis.get("roi_summary", {})
            st.markdown("**💰 ROI Stimato:**")
            st.metric("Risparmio anno 1", f"€{roi_summary.get('risparmio_anno1', 'N/A')}")
            st.metric("Break-even", f"{roi_summary.get('breakeven_mesi', 'N/A')} mesi")
            st.metric("ROI 12 mesi", f"{roi_summary.get('roi_12mesi', 'N/A')}%")

    # Strengths & Cautions
    col_str, col_cau = st.columns(2)

    with col_str:
        st.markdown("**✅ Punti di Forza:**")
        for strength in analysis.get("strengths", []):
            st.markdown(f"- {strength}")

    with col_cau:
        st.markdown("**⚠️ Attenzioni:**")
        for caution in analysis.get("cautions", []):
            st.markdown(f"- {caution}")

    # Next Step
    next_step = analysis.get("next_step", "")
    if next_step:
        st.info(f"🚀 **Prossimo Passo:** {next_step}")

    st.divider()

    # ========================================================================
    # LAYER 2: RAGIONAMENTO (expander)
    # ========================================================================

    with st.expander("🧠 Come Sono Arrivato a Queste Conclusioni", expanded=False):
        st.markdown(analysis.get("reasoning", ""))

    # ========================================================================
    # LAYER 3: ROADMAP (expander, default espanso)
    # ========================================================================

    with st.expander("🗺️ Roadmap Dettagliata", expanded=True):
        st.markdown(analysis.get("roadmap", ""))

    # ========================================================================
    # LAYER 4: ACTION PLAN (sempre visibile - CTA)
    # ========================================================================

    st.markdown("### ✅ I Tuoi Prossimi Passi")

    col_actions, col_vendors = st.columns([2, 1])

    with col_actions:
        st.markdown("**Questa Settimana:**")
        for action in analysis.get("actions_week", []):
            st.checkbox(action, key=f"action_week_{hash(action)}")

        st.markdown("**Prossime 2 Settimane:**")
        for action in analysis.get("actions_2weeks", []):
            st.checkbox(action, key=f"action_2w_{hash(action)}")

    with col_vendors:
        st.markdown("**💼 Vendor Suggeriti:**")
        vendors = analysis.get("vendors", [])
        for vendor in vendors:
            st.markdown(f"**{vendor.get('name', 'N/A')}**")
            st.caption(vendor.get("why", ""))

    st.divider()

    # Export options
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("📄 Scarica PDF", use_container_width=True):
            st.info("💡 Feature PDF in arrivo nella prossima versione")

    with col_btn2:
        if st.button("📧 Invia via Email", use_container_width=True):
            st.info("💡 Feature Email in arrivo")

    with col_btn3:
        if st.button("🔄 Ricomincia", use_container_width=True):
            st.session_state.answers_v2 = {}
            st.session_state.current_question = 0
            st.session_state.analysis_v2 = None
            st.rerun()


# ============================================================================
# MAIN FLOW - QUESTION OR ANALYSIS
# ============================================================================

# Get current question index
current_q_idx = st.session_state.current_question

# Check if all questions answered
if current_q_idx >= len(QUESTIONS_V2):
    # All questions answered - show analysis
    render_final_analysis_v2()
else:
    # Still answering questions - show current question
    current_question = QUESTIONS_V2[current_q_idx]
    render_question_v2(current_question)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div class="footer">
    <p>{config.IFAB_INFO['name']} | Agentic AI Workshop V2 - Executive Edition</p>
    <p style="font-size: 0.8rem; color: #ccc;">Powered by Claude AI | Versione 2.0.0</p>
</div>
""", unsafe_allow_html=True)
