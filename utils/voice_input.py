import streamlit as st
from openai import OpenAI
import tempfile
import os
from io import BytesIO
import config

def setup_voice_input():
    """Initialize OpenAI client for Whisper API"""
    # Try session_state first, then config (lazy loading)
    api_key = st.session_state.get("openai_api_key") or config.get_api_key("OPENAI_API_KEY")

    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Errore nell'inizializzazione dell'API OpenAI: {str(e)}")
        return None

def transcribe_audio(audio_bytes, client):
    """
    Transcribe audio using OpenAI Whisper API

    Args:
        audio_bytes: Audio data in bytes
        client: OpenAI client instance

    Returns:
        str: Transcribed text or None if error
    """
    if not client:
        st.error("Client OpenAI non inizializzato. Verifica la tua API key.")
        return None

    try:
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            tmp_file_path = tmp_file.name

        # Transcribe using Whisper
        with open(tmp_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="it"  # Italian language
            )

        # Clean up temporary file
        os.unlink(tmp_file_path)

        return transcript.text

    except Exception as e:
        st.error(f"Errore nella trascrizione audio: {str(e)}")
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        return None

def voice_input_component(question_text, help_text=""):
    """
    Render voice input component with mic recorder and transcription

    Args:
        question_text: The question being asked
        help_text: Help text for the question

    Returns:
        str: Transcribed text or None
    """
    # Improved UI for voice input
    st.markdown("---")
    st.markdown("### 🎤 Registra la tua risposta")

    # Check if OpenAI API key is set (in session_state or config)
    has_api_key = st.session_state.get("openai_api_key") or config.get_api_key("OPENAI_API_KEY")

    if not has_api_key:
        st.error("⚠️ API Key OpenAI non configurata")
        with st.expander("⚙️ Configura API Key OpenAI"):
            api_key = st.text_input(
                "Inserisci la tua OpenAI API Key",
                type="password",
                help="Necessaria per la trascrizione vocale con Whisper"
            )
            if st.button("💾 Salva API Key"):
                st.session_state.openai_api_key = api_key
                st.success("✅ API Key salvata!")
                st.rerun()
        return None

    # Initialize OpenAI client
    client = setup_voice_input()

    if not client:
        st.error("❌ Impossibile inizializzare il client OpenAI. Verifica la tua API key.")
        return None

    # Instructions
    st.info("""
    **📝 Istruzioni:**
    1. Clicca sul pulsante del microfono per iniziare a registrare
    2. Clicca di nuovo sul microfono per fermare la registrazione
    """)

    try:
        from audio_recorder_streamlit import audio_recorder

        recorder_key = f"audio_recorder_{question_text[:20].replace(' ', '_')}"

        audio_bytes = audio_recorder(
            text="",
            recording_color="#DBCB4F",
            neutral_color="#1b98e0",
            icon_name="microphone",
            icon_size="3x",
            key=recorder_key,
            pause_threshold=300.0  # 5 minuti - disabilita stop automatico
        )

        if audio_bytes:
            st.success("✅ Audio registrato!")
            st.audio(audio_bytes, format="audio/wav")

            with st.spinner("🔄 Trascrizione in corso con Whisper AI..."):
                transcribed_text = transcribe_audio(audio_bytes, client)

            if transcribed_text:
                st.success("✅ Trascrizione completata!")
                st.markdown("**📝 Testo trascritto:**")
                st.info(transcribed_text)
                return transcribed_text
            else:
                st.error("❌ Errore nella trascrizione. Riprova.")

    except ImportError:
        st.error("⚠️ Componente audio_recorder_streamlit non installato.")
        st.caption("Installalo con: pip install audio-recorder-streamlit")

    except Exception as e:
        st.error(f"❌ Errore nella registrazione: {str(e)}")

    return None

def render_voice_or_text_input(question_id, question_text, placeholder="", help_text="", rows=3):
    """
    Render a combined voice + text input component

    Args:
        question_id: Unique question identifier
        question_text: The question text
        placeholder: Placeholder for text input
        help_text: Help text
        rows: Number of rows for text area

    Returns:
        str: User input (from voice or text)
    """
    # Initialize temp storage for transcribed text
    transcription_key = f"temp_transcription_{question_id}"
    if transcription_key not in st.session_state:
        st.session_state[transcription_key] = None

    # Create tabs for voice and text input
    tab1, tab2 = st.tabs(["✍️ Scrivi", "🎤 Parla"])

    user_input = None

    with tab1:
        # Check if there's a pending transcription from voice tab
        if st.session_state[transcription_key]:
            st.info(f"""
            **🎤 Trascrizione disponibile dalla tab Parla:**

            {st.session_state[transcription_key]}
            """)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Sostituisci con trascrizione", key=f"replace_in_text_{question_id}", type="primary"):
                    st.session_state.answers[question_id] = st.session_state[transcription_key]
                    st.session_state[transcription_key] = None  # Clear temp
                    st.success("✅ Risposta sostituita!")
                    st.rerun()

            with col2:
                if st.button("❌ Ignora trascrizione", key=f"ignore_{question_id}"):
                    st.session_state[transcription_key] = None  # Clear temp
                    st.rerun()

            st.markdown("---")

        # Text input
        current_value = st.session_state.answers.get(question_id, "")
        user_input = st.text_area(
            question_text,
            value=current_value,
            placeholder=placeholder,
            help=help_text,
            height=rows * 30,
            key=f"text_{question_id}"
        )

    with tab2:
        # Voice input
        transcribed = voice_input_component(question_text, help_text)

        if transcribed:
            # Save to temp storage
            st.session_state[transcription_key] = transcribed

            # Show action buttons
            st.markdown("---")
            st.markdown("**Cosa vuoi fare con questa trascrizione?**")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Usa come risposta", key=f"use_{question_id}", type="primary"):
                    st.session_state.answers[question_id] = transcribed
                    st.session_state[transcription_key] = None  # Clear temp
                    st.success("✅ Risposta salvata! Ora puoi cliccare 'Avanti' qui sotto.")
                    st.rerun()

            with col2:
                if st.button("✍️ Vai alla tab Scrivi", key=f"go_to_text_{question_id}"):
                    st.info("👉 Clicca sulla tab '✍️ Scrivi' qui sopra per vedere la trascrizione e usarla.")

        # Show current saved answer in voice tab
        elif question_id in st.session_state.answers and st.session_state.answers[question_id]:
            st.info(f"**💾 Risposta salvata:**\n\n{st.session_state.answers[question_id]}")

    # Return the text input value, but preserve existing answers
    # If user typed in text tab, use that. Otherwise keep what's in session_state
    if user_input and user_input.strip():
        return user_input
    else:
        # Return the current saved value to avoid overwriting with empty string
        return st.session_state.answers.get(question_id, "")
