"""
Agentic AI Workshop V2 - Onboarding
Schermata introduttiva (2 minuti) per contestualizzare il workshop

Obiettivi:
- Spiegare cosa aspettarsi (30-45 min, 8 domande)
- Preparare mentalmente all'approccio discovery
- Dare tips per massimizzare valore
"""

import streamlit as st


def render_onboarding():
    """
    Render schermata onboarding

    Returns:
        bool: True se utente ha completato onboarding e può procedere
    """

    # Logo e header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="font-size: 4rem; color: #1b98e0;">🚀</div>
        <h1 style="color: #1b98e0; margin-top: 1rem;">
            Agentic AI Workshop
        </h1>
        <h3 style="color: #666; font-weight: 300;">
            Executive Edition - Discovery Rapida
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Cosa scoprirai
    st.markdown("### 🎯 Cosa Scoprirai in 30-45 Minuti")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                    padding: 1.5rem; border-radius: 8px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem;">💡</div>
            <h4 style="color: #1976D2; margin: 0.5rem 0;">L'Opportunità</h4>
            <p style="color: #555; font-size: 0.9rem;">
                Se l'AI può trasformare il tuo processo
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                    padding: 1.5rem; border-radius: 8px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem;">🎬</div>
            <h4 style="color: #388E3C; margin: 0.5rem 0;">La Demo Live</h4>
            <p style="color: #555; font-size: 0.9rem;">
                Come funzionerebbe nella pratica
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9C4 0%, #FFF59D 100%);
                    padding: 1.5rem; border-radius: 8px; text-align: center; height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 2.5rem;">📊</div>
            <h4 style="color: #F57C00; margin: 0.5rem 0;">Il ROI</h4>
            <p style="color: #555; font-size: 0.9rem;">
                Stima di risparmio e prossimi passi
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Come funziona
    st.markdown("### 📋 Come Funziona")

    st.markdown("""
    <div style="background: white; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #1b98e0;">
        <p style="margin: 0; line-height: 1.8;">
            Risponderai a <strong>8 domande strategiche</strong> (non tecniche!) sul tuo processo:
        </p>
        <ul style="margin: 1rem 0; padding-left: 1.5rem; line-height: 1.8;">
            <li><strong>FASE 1 - Discovery:</strong> Quale problema, quale risultato ideale, dove serve l'AI</li>
            <li><strong>FASE 2 - Design:</strong> Dati disponibili, flusso di lavoro, rischi</li>
            <li><strong>FASE 3 - ROI:</strong> Metriche di successo, timeline e budget</li>
        </ul>
        <p style="margin: 0; color: #666; font-size: 0.95rem;">
            💡 L'AI ti darà <strong>4 momenti "aha!"</strong> lungo il percorso + un'analisi finale completa
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tips per massimizzare valore
    st.markdown("### ✨ Tips per Massimizzare il Valore")

    tip1, tip2, tip3 = st.columns(3)

    with tip1:
        st.info("""
        **1️⃣ Pensa a UN processo**

        Scegli un processo specifico che ti fa perdere tempo o soldi oggi.

        ✅ Buono: "Gestione reclami clienti"
        ❌ Troppo vago: "Customer service"
        """)

    with tip2:
        st.info("""
        **2️⃣ Sii concreto**

        Numeri concreti anche se stimati.

        ✅ Buono: "2 giorni di attesa"
        ❌ Generico: "Molto tempo"
        """)

    with tip3:
        st.info("""
        **3️⃣ Usa il microfono 🎤**

        Puoi parlare invece di scrivere. Più veloce e naturale!

        (Funziona su desktop e mobile)
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Opzioni per iniziare
    st.markdown("### 🚀 Sei Pronto?")

    col_start, col_load, col_skip = st.columns([2, 2, 1])

    with col_start:
        if st.button("✨ Inizia il Workshop", type="primary", use_container_width=True):
            st.session_state.onboarding_complete = True
            return True

    with col_load:
        if st.button("📁 Carica Progetto Esistente", use_container_width=True):
            st.session_state.show_import = True
            st.session_state.onboarding_complete = True
            return True

    with col_skip:
        if st.button("⏭️ Skip", use_container_width=True):
            st.session_state.onboarding_complete = True
            return True

    # Info aggiuntive (collapsible)
    with st.expander("ℹ️ Altre Informazioni"):
        st.markdown("""
        **Quanto tempo ci vuole?**
        - Tipicamente 30-45 minuti
        - Dipende da quanto sei dettagliato nelle risposte
        - Puoi salvare e riprendere in qualsiasi momento

        **Cosa succede dopo?**
        - Ricevi un'analisi completa con score, ROI stimato e prossimi passi
        - Puoi scaricare PDF per condividere con il team
        - Hai suggerimenti di vendor/piattaforme specifici per il tuo caso

        **È sicuro?**
        - I tuoi dati restano confidenziali
        - Niente è condiviso esternamente
        - Puoi esportare e cancellare tutto quando vuoi

        **Supporto tecnico:**
        - Se hai problemi, verifica le API keys in config.py
        - Input vocale richiede OpenAI API key (Whisper)
        - Analisi AI richiede Anthropic API key (Claude)
        """)

    return False
