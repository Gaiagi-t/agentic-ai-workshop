import json
import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

# Key for localStorage
STORAGE_KEY = "agentic_workshop_data"

def save_to_storage():
    """Save current session data to browser localStorage"""
    try:
        data = {
            "answers": st.session_state.get("answers", {}),
            "current_question": st.session_state.get("current_question_index", 0),
            "section": st.session_state.get("current_section", "AS-IS"),
            "saved_at": datetime.now().isoformat()
        }
        json_data = json.dumps(data, ensure_ascii=False)
        # Escape quotes for JavaScript
        json_escaped = json_data.replace("\\", "\\\\").replace("'", "\\'")
        streamlit_js_eval(js_expressions=f"localStorage.setItem('{STORAGE_KEY}', '{json_escaped}')")
    except Exception:
        pass

def load_from_storage():
    """Load data from browser localStorage and restore session state"""
    try:
        # Check if we already tried to load (to avoid infinite loops)
        if st.session_state.get("_storage_loaded"):
            return False

        # Get data from localStorage
        saved_data = streamlit_js_eval(js_expressions=f"localStorage.getItem('{STORAGE_KEY}')", key="load_storage")

        if saved_data and isinstance(saved_data, str):
            data = json.loads(saved_data)

            # Only restore if we don't already have data
            if data.get("answers") and not st.session_state.get("answers"):
                st.session_state.answers = data.get("answers", {})
                st.session_state.current_question_index = data.get("current_question", 0)
                st.session_state.current_section = data.get("section", "AS-IS")
                st.session_state._storage_loaded = True
                return True
    except Exception:
        pass

    st.session_state._storage_loaded = True
    return False

def clear_storage():
    """Clear saved data from localStorage"""
    try:
        streamlit_js_eval(js_expressions=f"localStorage.removeItem('{STORAGE_KEY}')")
    except Exception:
        pass

def reset_project():
    """Reset all session state and start a new project"""
    # Clear session state
    st.session_state.answers = {}
    st.session_state.current_question_index = 0
    st.session_state.current_section = "AS-IS"
    st.session_state.analysis_results = None
    st.session_state._storage_loaded = False

    # Clear any widget keys that might have cached values
    keys_to_clear = [k for k in st.session_state.keys() if k.startswith("text_") or k.startswith("temp_")]
    for key in keys_to_clear:
        del st.session_state[key]

    # Clear localStorage
    clear_storage()

def render_new_project_button():
    """Render button to start a new project"""
    if st.button("🆕 Nuova Mappatura", help="Inizia un nuovo progetto da zero", type="secondary"):
        reset_project()
        st.success("✅ Nuovo progetto iniziato!")
        st.rerun()

def auto_save():
    """Auto-save current state to localStorage (call periodically)"""
    if st.session_state.get("answers"):
        save_to_storage()

def export_to_json():
    """Export current session data to JSON format"""

    export_data = {
        "metadata": {
            "export_date": datetime.now().isoformat(),
            "app_version": "1.0.0",
            "workshop": "Agentic AI Workshop - iFAB"
        },
        "answers": st.session_state.answers,
        "current_question": st.session_state.current_question_index,
        "section": st.session_state.current_section,
        "analysis": st.session_state.get("analysis_results", None)
    }

    json_string = json.dumps(export_data, indent=2, ensure_ascii=False)
    return json_string

def import_from_json(json_string):
    """Import session data from JSON string"""

    try:
        data = json.loads(json_string)

        # Validate data structure
        if "answers" not in data:
            return False, "File JSON non valido: manca la sezione 'answers'"

        # Load data into session state
        st.session_state.answers = data.get("answers", {})
        st.session_state.current_question_index = data.get("current_question", 0)
        st.session_state.current_section = data.get("section", "AS-IS")

        # Load analysis if present
        if "analysis" in data and data["analysis"]:
            st.session_state.analysis_results = data["analysis"]

        # Don't set show_analysis here - let the user navigate freely
        # The analysis section will check if data is sufficient

        return True, "Dati importati con successo!"

    except json.JSONDecodeError as e:
        return False, f"Errore nel parsing del JSON: {str(e)}"
    except Exception as e:
        return False, f"Errore nell'importazione: {str(e)}"

def download_button():
    """Render download button for exporting data"""

    json_data = export_to_json()

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"agentic_ai_project_{timestamp}.json"

    st.download_button(
        label="📥 Esporta Progetto (JSON)",
        data=json_data,
        file_name=filename,
        mime="application/json",
        help="Scarica il tuo progetto per salvarlo o condividerlo"
    )

def upload_button():
    """Render upload button for importing data"""

    # Initialize upload counter if not exists
    if 'upload_counter' not in st.session_state:
        st.session_state.upload_counter = 0

    uploaded_file = st.file_uploader(
        "📤 Importa Progetto",
        type=["json"],
        help="Carica un file JSON precedentemente esportato",
        key=f"file_uploader_{st.session_state.upload_counter}"
    )

    if uploaded_file is not None:
        # Read and import the file
        try:
            json_string = uploaded_file.read().decode("utf-8")
            success, message = import_from_json(json_string)

            if success:
                st.success(message)
                # Increment counter to reset the file uploader on next render
                st.session_state.upload_counter += 1
                # Small delay to show success message
                import time
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Errore durante la lettura del file: {str(e)}")

def get_progress_stats():
    """Calculate progress statistics"""

    from utils.questions import QUESTIONS

    total_as_is = len(QUESTIONS["AS-IS"])
    total_to_be = len(QUESTIONS["TO-BE"])
    total_questions = total_as_is + total_to_be

    answered_as_is = sum(
        1 for q in QUESTIONS["AS-IS"]
        if q["id"] in st.session_state.answers and st.session_state.answers[q["id"]]
    )

    answered_to_be = sum(
        1 for q in QUESTIONS["TO-BE"]
        if q["id"] in st.session_state.answers and st.session_state.answers[q["id"]]
    )

    total_answered = answered_as_is + answered_to_be

    return {
        "total": total_questions,
        "answered": total_answered,
        "percentage": (total_answered / total_questions * 100) if total_questions > 0 else 0,
        "as_is": {"answered": answered_as_is, "total": total_as_is},
        "to_be": {"answered": answered_to_be, "total": total_to_be}
    }

def get_answers_summary():
    """Get a summary of all answers for display"""

    from utils.questions import QUESTIONS

    summary = {
        "AS-IS": [],
        "TO-BE": []
    }

    for section_name, questions in QUESTIONS.items():
        if section_name == "CONFRONTO":
            continue

        for q in questions:
            answer = st.session_state.answers.get(q["id"], "")
            if answer:
                summary[section_name].append({
                    "numero": q.get("numero", ""),
                    "domanda": q["testo"],
                    "risposta": answer,
                    "obbligatorio": q.get("obbligatorio", False)
                })

    return summary

def render_answers_sidebar():
    """Render answers summary in sidebar"""

    stats = get_progress_stats()

    st.sidebar.markdown("### 📊 Progresso")

    # Overall progress bar
    st.sidebar.progress(stats["percentage"] / 100)
    st.sidebar.caption(f"{stats['answered']}/{stats['total']} domande completate")

    # Section progress
    st.sidebar.markdown("#### Sezioni")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric(
            "AS-IS",
            f"{stats['as_is']['answered']}/{stats['as_is']['total']}"
        )
    with col2:
        st.metric(
            "TO-BE",
            f"{stats['to_be']['answered']}/{stats['to_be']['total']}"
        )

    # Summary expander
    with st.sidebar.expander("📝 Riepilogo Risposte"):
        summary = get_answers_summary()

        for section_name, answers in summary.items():
            if answers:
                st.markdown(f"**{section_name}**")
                for item in answers:
                    with st.container():
                        st.caption(f"Q{item['numero']}: {item['domanda'][:50]}...")
                        # Truncate long answers
                        short_answer = item['risposta'][:100] + "..." if len(item['risposta']) > 100 else item['risposta']
                        st.text(short_answer)
                        st.divider()
