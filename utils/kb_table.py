import streamlit as st
import pandas as pd
import config
import re

# Version: 2.0 - Fixed None handling in tables

def render_kb_table(section_name, current_question_id, answers):
    """
    Render progressive knowledge base table showing all collected answers

    Args:
        section_name: "AS-IS" or "TO-BE"
        current_question_id: ID of the current question being answered
        answers: Dictionary of all user answers
    """

    if section_name == "AS-IS":
        render_as_is_kb_table_step_based(current_question_id, answers)
    elif section_name == "TO-BE":
        render_to_be_kb_table(current_question_id, answers)

def parse_steps(step_text):
    """
    Parse step text into a list of steps
    Handles both manual input (newlines) and voice input (commas, periods)
    """
    if not step_text:
        return []

    # First, try to detect if it's voice input (contains commas but few newlines)
    newline_count = step_text.count('\n')
    comma_count = step_text.count(',')

    # If there are many commas and few newlines, it's likely voice input
    # Split by both commas and periods
    if comma_count > newline_count:
        # Voice input mode: split by commas, semicolons, and periods (but keep decimal points)
        # Replace common separators with a special marker
        normalized = step_text
        normalized = normalized.replace(';', '|||')
        normalized = normalized.replace(',', '|||')
        # Split by period only if followed by space (to avoid breaking decimals)
        normalized = re.sub(r'\.\s+', '|||', normalized)
        # Also split by newlines
        normalized = normalized.replace('\n', '|||')

        lines = normalized.split('|||')
    else:
        # Manual input mode: split by newlines (original behavior)
        lines = step_text.strip().split('\n')

    steps = []
    for line in lines:
        line = line.strip()
        if line:
            # Remove numbering if present (1., 2., etc.)
            cleaned = re.sub(r'^\d+[\.\)\-\:]?\s*', '', line)
            # Remove trailing punctuation
            cleaned = cleaned.rstrip('.,;:!?')
            cleaned = cleaned.strip()

            # Only add if not empty and has at least 2 characters
            if cleaned and len(cleaned) >= 2:
                steps.append(cleaned)

    return steps

def update_answers_from_table(edited_df, answers):
    """
    Update session state answers from edited table
    Converts table data back to text format for storage
    Also syncs text widget keys for proper UI reflection
    """
    # Extract steps - filter out None/empty and convert to string
    steps = edited_df["Attività"].tolist()
    steps_clean = [str(s) if s is not None else "" for s in steps]
    steps_text = "\n".join([s for s in steps_clean if s.strip()])
    if steps_text.strip():
        st.session_state.answers["as_is_step"] = steps_text
        # Sync text widget
        if "text_as_is_step" in st.session_state:
            st.session_state["text_as_is_step"] = steps_text

    # Extract roles - filter out None/empty and convert to string
    ruoli = edited_df["Chi la svolge"].tolist()
    ruoli_clean = [str(r) if r is not None else "" for r in ruoli]
    ruoli_text = "\n".join(ruoli_clean)
    if ruoli_text.strip():
        st.session_state.answers["as_is_ruoli"] = ruoli_text
        # Sync text widget
        if "text_as_is_ruoli" in st.session_state:
            st.session_state["text_as_is_ruoli"] = ruoli_text

    # Extract time - filter out None/empty and convert to string
    tempo = edited_df["Tempo"].tolist()
    tempo_clean = [str(t) if t is not None else "" for t in tempo]
    tempo_text = "\n".join(tempo_clean)
    if tempo_text.strip():
        st.session_state.answers["as_is_tempo"] = tempo_text
        # Sync text widget
        if "text_as_is_tempo" in st.session_state:
            st.session_state["text_as_is_tempo"] = tempo_text

    # Note: Strumenti and Problemi are general (not per-step), so we don't update them here

def parse_list_items(text):
    """
    Parse text into list items (for roles, time, etc.)
    Similar to parse_steps but without step-specific cleaning
    """
    if not text:
        return []

    # Detect if voice input (commas) or manual (newlines)
    newline_count = text.count('\n')
    comma_count = text.count(',')

    if comma_count > newline_count:
        # Voice input: split by commas and semicolons
        normalized = text
        normalized = normalized.replace(';', '|||')
        normalized = normalized.replace(',', '|||')
        normalized = normalized.replace('\n', '|||')
        lines = normalized.split('|||')
    else:
        # Manual input: split by newlines
        lines = text.strip().split('\n')

    items = []
    for line in lines:
        line = line.strip()
        # Remove trailing punctuation
        line = line.rstrip('.,;:!?')
        line = line.strip()

        if line and len(line) >= 1:
            items.append(line)

    return items

def render_as_is_summary_table(current_question_id, answers):
    """Render AS-IS summary table - EDITABLE version"""

    st.caption("💡 Clicca su una cella nella colonna 'Contenuto' per modificarla direttamente")

    # Map field keys to display names
    field_keys = ["as_is_processo", "as_is_step", "as_is_ruoli", "as_is_strumenti", "as_is_tempo", "as_is_problemi"]
    field_names = [
        "🎯 Processo",
        "📝 Step del processo",
        "👥 Chi lo esegue",
        "🛠️ Strumenti utilizzati",
        "⏱️ Tempo richiesto",
        "⚠️ Problemi e criticità"
    ]

    # Define the KB structure for AS-IS
    kb_data = {
        "Campo": field_names,
        "Contenuto": [
            answers.get("as_is_processo", ""),
            answers.get("as_is_step", ""),
            answers.get("as_is_ruoli", ""),
            answers.get("as_is_strumenti", ""),
            answers.get("as_is_tempo", ""),
            answers.get("as_is_problemi", "")
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(kb_data)

    # Store original state for comparison
    original_state = df.to_dict('records')

    # Display editable table
    edited_df = st.data_editor(
        df,
        key="as_is_summary_editor",
        hide_index=True,
        use_container_width=True,
        height=280,
        disabled=["Campo"],  # Lock the field names column
        column_config={
            "Campo": st.column_config.TextColumn("Campo", width="medium"),
            "Contenuto": st.column_config.TextColumn("Contenuto", width="large")
        }
    )

    # Check if table was edited and update answers
    edited_state = edited_df.to_dict('records')
    if edited_state != original_state:
        # Update session state answers from edited table
        for i, key in enumerate(field_keys):
            new_value = edited_df.iloc[i]["Contenuto"]
            # Handle None values - convert to string safely
            if new_value is not None and str(new_value).strip():
                st.session_state.answers[key] = str(new_value)
                # Also update the text widget key so it reflects the change
                widget_key = f"text_{key}"
                if widget_key in st.session_state:
                    st.session_state[widget_key] = str(new_value)
        # Note: Don't call st.rerun() here as it interferes with navigation buttons

    st.divider()

def render_as_is_kb_table_step_based(current_question_id, answers):
    """Render AS-IS knowledge base table with steps as rows (like in slides)"""

    st.markdown("### 📋 Mappatura AS-IS")
    st.markdown("*Questa tabella si compila progressivamente con le tue risposte*")

    # Parse steps
    step_text = answers.get("as_is_step", "")
    steps = parse_steps(step_text)

    # Show ONLY ONE table: summary table if no steps, step-based table if steps exist
    if not steps:
        # No steps yet - show the summary table
        render_as_is_summary_table(current_question_id, answers)
        st.info("""
        👉 **Inserisci gli step del processo** (Domanda 2) per vedere la tabella dettagliata editabile!
        """)
        return

    # Show process name if available
    processo = answers.get("as_is_processo", "")
    if processo:
        st.markdown(f"**🎯 Processo:** {processo}")
        st.markdown("---")

    # Determine current question stage
    question_map = {
        "as_is_processo": 0,
        "as_is_step": 1,
        "as_is_ruoli": 2,
        "as_is_strumenti": 3,
        "as_is_tempo": 4,
        "as_is_problemi": 5
    }
    current_stage = question_map.get(current_question_id, -1)

    # Build table data
    table_data = []

    for i, step in enumerate(steps, 1):
        row = {
            "#": i,
            "Attività": step,
            "Chi la svolge": "",
            "Strumenti": "",
            "Tempo": "",
            "Problemi/Criticità": ""
        }

        # Try to extract info from other answers
        # Who (as_is_ruoli)
        if current_stage >= 2:
            ruoli_text = answers.get("as_is_ruoli", "")
            if ruoli_text:
                # Parse roles (handles both voice and manual input)
                ruoli_list = parse_list_items(ruoli_text)
                if i <= len(ruoli_list):
                    row["Chi la svolge"] = ruoli_list[i-1]

        # Tools (as_is_strumenti)
        if current_stage >= 3:
            strumenti = answers.get("as_is_strumenti", "")
            if strumenti:
                # Show tools for all steps
                row["Strumenti"] = truncate_text(strumenti, 30)

        # Time (as_is_tempo)
        if current_stage >= 4:
            tempo_text = answers.get("as_is_tempo", "")
            if tempo_text:
                # Parse time (handles both voice and manual input)
                tempo_list = parse_list_items(tempo_text)
                if i <= len(tempo_list):
                    row["Tempo"] = tempo_list[i-1]

        # Problems (as_is_problemi)
        if current_stage >= 5:
            problemi = answers.get("as_is_problemi", "")
            if problemi:
                row["Problemi/Criticità"] = truncate_text(problemi, 40)

        table_data.append(row)

    # Create DataFrame
    df = pd.DataFrame(table_data)

    # Style based on completion
    def style_table(row):
        # Color rows based on completion
        if current_stage >= 5:
            return [f'background-color: #E8F5E9'] * len(row)  # Green - complete
        elif current_stage >= 2:
            return [f'background-color: #FFF9C4'] * len(row)  # Yellow - in progress
        else:
            return [f'background-color: #E3F2FD'] * len(row)  # Blue - just steps

    # Display table (editable)
    st.markdown("**📊 Tabella Processo (Modificabile):**")
    st.caption("💡 Clicca su una cella per modificarla direttamente")

    # Use a unique key for the data editor to properly track changes
    table_key = "as_is_table_editor"

    # Store the current df state before editing (for comparison)
    current_state = df.to_dict('records')

    edited_df = st.data_editor(
        df,
        key=table_key,
        hide_index=True,
        use_container_width=True,
        height=min(len(steps) * 50 + 100, 400),
        disabled=["#"],  # Lock the step number column
        num_rows="fixed",  # Fixed rows - add steps in text input
        column_config={
            "#": st.column_config.NumberColumn("Step", width="small"),
            "Attività": st.column_config.TextColumn("Attività", width="large"),
            "Chi la svolge": st.column_config.TextColumn("Chi la svolge", width="medium"),
            "Strumenti": st.column_config.TextColumn("Strumenti", width="medium"),
            "Tempo": st.column_config.TextColumn("Tempo", width="small"),
            "Problemi/Criticità": st.column_config.TextColumn("Problemi/Criticità", width="medium")
        }
    )

    # Compare edited_df with original df to detect changes
    edited_state = edited_df.to_dict('records')

    # Check if there are actual edits (compare with what we built from answers)
    if edited_state != current_state:
        # User made edits in the table - update answers
        update_answers_from_table(edited_df, answers)
        # Note: Don't call st.rerun() here as it interferes with navigation buttons

    # Progress indicator
    col1, col2, col3 = st.columns(3)
    with col1:
        status = "✅" if current_stage >= 2 else "⏳"
        st.caption(f"{status} Step definiti")
    with col2:
        status = "✅" if current_stage >= 4 else "⏳"
        st.caption(f"{status} Ruoli e tempo")
    with col3:
        status = "✅" if current_stage >= 5 else "⏳"
        st.caption(f"{status} Problemi identificati")

    st.divider()

def render_as_is_kb_table(current_question_id, answers):
    """Render AS-IS knowledge base table (OLD VERSION - DEPRECATED)"""

    st.markdown("### 📋 Mappatura AS-IS")
    st.markdown("*Questa tabella si riempie progressivamente con le tue risposte*")

    # Define the KB structure for AS-IS
    kb_data = {
        "Campo": [
            "🎯 Processo",
            "📝 Step del processo",
            "👥 Chi lo esegue",
            "🛠️ Strumenti utilizzati",
            "⏱️ Tempo richiesto",
            "⚠️ Problemi e criticità"
        ],
        "Contenuto": [
            answers.get("as_is_processo", ""),
            answers.get("as_is_step", ""),
            answers.get("as_is_ruoli", ""),
            answers.get("as_is_strumenti", ""),
            answers.get("as_is_tempo", ""),
            answers.get("as_is_problemi", "")
        ],
        "Status": []
    }

    # Determine status for each field
    question_map = {
        "as_is_processo": 0,
        "as_is_step": 1,
        "as_is_ruoli": 2,
        "as_is_strumenti": 3,
        "as_is_tempo": 4,
        "as_is_problemi": 5
    }

    current_index = question_map.get(current_question_id, -1)

    for i, question_id in enumerate(question_map.keys()):
        if i < current_index:
            kb_data["Status"].append("✅")
        elif i == current_index:
            kb_data["Status"].append("✏️")
        else:
            kb_data["Status"].append("⏳")

    # Create DataFrame
    df = pd.DataFrame(kb_data)

    # Style the table
    def style_row(row):
        if row["Status"] == "✏️":
            return [f'background-color: {config.COLORS["accent"]}; font-weight: bold'] * len(row)
        elif row["Status"] == "✅":
            return [f'background-color: #E8F5E9'] * len(row)
        else:
            return ['background-color: #F5F5F5; opacity: 0.6'] * len(row)

    # Display table
    styled_df = df.style.apply(style_row, axis=1)
    st.dataframe(
        styled_df,
        hide_index=True,
        use_container_width=True,
        height=280
    )

    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("✅ Completato")
    with col2:
        st.caption("✏️ In compilazione")
    with col3:
        st.caption("⏳ Da completare")

    st.divider()

def render_to_be_kb_table(current_question_id, answers):
    """Render TO-BE knowledge base table - EDITABLE version"""

    st.markdown("### 📋 Mappatura TO-BE")
    st.caption("💡 Clicca su una cella nella colonna 'Contenuto' per modificarla direttamente")

    # Map field keys to display names
    field_keys = [
        "to_be_visione", "to_be_agenti", "to_be_input_output", "to_be_azioni_limiti",
        "to_be_dati_sistemi", "to_be_tool", "to_be_flusso", "to_be_soluzioni",
        "to_be_tempo", "to_be_benefici", "to_be_rischi", "to_be_system_prompt"
    ]
    field_names = [
        "🎯 Visione",
        "🤖 Agenti AI",
        "📥📤 Input/Output",
        "⚡ Azioni e Limiti",
        "💾 Dati e Sistemi",
        "🔧 Tool da integrare",
        "🔄 Flusso Agentico",
        "🛒 Soluzioni esistenti",
        "⏱️ Tempo TO-BE",
        "✨ Benefici",
        "⚠️ Rischi",
        "📜 System Prompt"
    ]

    # Define the KB structure for TO-BE
    kb_data = {
        "Campo": field_names,
        "Contenuto": [answers.get(key, "") for key in field_keys]
    }

    # Create DataFrame
    df = pd.DataFrame(kb_data)

    # Store original state for comparison
    original_state = df.to_dict('records')

    # Display editable table
    edited_df = st.data_editor(
        df,
        key="to_be_summary_editor",
        hide_index=True,
        use_container_width=True,
        height=450,
        disabled=["Campo"],  # Lock the field names column
        column_config={
            "Campo": st.column_config.TextColumn("Campo", width="medium"),
            "Contenuto": st.column_config.TextColumn("Contenuto", width="large")
        }
    )

    # Check if table was edited and update answers
    edited_state = edited_df.to_dict('records')
    if edited_state != original_state:
        # Update session state answers from edited table
        for i, key in enumerate(field_keys):
            new_value = edited_df.iloc[i]["Contenuto"]
            # Handle None values - convert to string safely
            if new_value is not None and str(new_value).strip():
                st.session_state.answers[key] = str(new_value)
                # Also update the text widget key so it reflects the change
                widget_key = f"text_{key}"
                if widget_key in st.session_state:
                    st.session_state[widget_key] = str(new_value)
        # Note: Don't call st.rerun() here as it interferes with navigation buttons

    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("✅ Completato")
    with col2:
        st.caption("✏️ In compilazione")
    with col3:
        st.caption("⏳ Da completare")

    st.divider()

def truncate_text(text, max_length=100):
    """Truncate text for display in table"""
    if not text:
        return ""
    text_str = str(text)
    if len(text_str) > max_length:
        return text_str[:max_length] + "..."
    return text_str
