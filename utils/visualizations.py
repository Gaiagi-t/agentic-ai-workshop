import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import config

def render_mermaid_diagram(content):
    """Render a Mermaid diagram graphically using Mermaid.js"""

    import re

    # Extract mermaid code from markdown code block
    mermaid_match = re.search(r'```mermaid\s*(.*?)\s*```', content, re.DOTALL)

    if mermaid_match:
        mermaid_code = mermaid_match.group(1).strip()
    else:
        # If no code block found, assume entire content is mermaid code
        mermaid_code = content.strip()

    # Render using Mermaid.js via HTML component
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'default',
                flowchart: {{
                    useMaxWidth: true,
                    htmlLabels: true,
                    curve: 'basis'
                }}
            }});
        </script>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 20px;
                background-color: transparent;
            }}
            .mermaid {{
                width: 100%;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
{mermaid_code}
        </div>
    </body>
    </html>
    """

    # Render with appropriate height
    import streamlit.components.v1 as components
    components.html(html_code, height=600, scrolling=True)

def create_progress_chart(stats):
    """Create a progress chart showing completion percentage"""

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=stats["percentage"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Completamento", 'font': {'size': 24}},
        delta={'reference': 100, 'increasing': {'color': config.COLORS["success"]}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': config.COLORS["text_secondary"]},
            'bar': {'color': config.COLORS["primary"]},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': config.COLORS["border"],
            'steps': [
                {'range': [0, 33], 'color': config.COLORS["background"]},
                {'range': [33, 66], 'color': '#FEF3C7'},
                {'range': [66, 100], 'color': '#D1FAE5'}
            ],
            'threshold': {
                'line': {'color': config.COLORS["danger"], 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def create_time_comparison_chart(as_is_time, to_be_time):
    """Create a bar chart comparing AS-IS vs TO-BE time"""

    if not as_is_time or not to_be_time:
        return None

    fig = go.Figure(data=[
        go.Bar(
            name='AS-IS',
            x=['Tempo Processo'],
            y=[as_is_time],
            marker_color=config.COLORS["danger"]
        ),
        go.Bar(
            name='TO-BE',
            x=['Tempo Processo'],
            y=[to_be_time],
            marker_color=config.COLORS["success"]
        )
    ])

    # Calculate percentage improvement
    if as_is_time > 0:
        improvement = ((as_is_time - to_be_time) / as_is_time) * 100
        fig.add_annotation(
            x='Tempo Processo',
            y=max(as_is_time, to_be_time) * 1.1,
            text=f"Risparmio: {improvement:.1f}%",
            showarrow=False,
            font=dict(size=16, color=config.COLORS["success"])
        )

    fig.update_layout(
        title="Confronto Tempo: AS-IS vs TO-BE",
        yaxis_title="Tempo (unità)",
        barmode='group',
        height=400,
        showlegend=True
    )

    return fig

def create_feasibility_radar(analysis_results):
    """Create a radar chart for feasibility analysis - DYNAMIC based on AI analysis"""
    import re

    # Define dimensions
    categories = [
        'Fattibilita Tecnica',
        'Impatto Business',
        'Gestione Rischi',
        'ROI Previsto',
        'Facilita Implementazione'
    ]

    # Extract values from analysis results
    values = []

    # 1. Fattibilita Tecnica (from fattibilita_tecnica section, look for X/5 pattern)
    fatt_text = str(analysis_results.get("fattibilita_tecnica", ""))
    fatt_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*5', fatt_text)
    if fatt_match:
        values.append(float(fatt_match.group(1)))
    else:
        # Estimate based on keywords
        if any(kw in fatt_text.lower() for kw in ["alta", "elevata", "ottima"]):
            values.append(4.5)
        elif any(kw in fatt_text.lower() for kw in ["media", "moderata"]):
            values.append(3.0)
        elif any(kw in fatt_text.lower() for kw in ["bassa", "difficile"]):
            values.append(2.0)
        else:
            values.append(3.5)

    # 2. Impatto Business (from riduzione_costi and risparmio_di_tempo)
    costi_text = str(analysis_results.get("riduzione_costi", ""))
    tempo_text = str(analysis_results.get("risparmio_di_tempo_stimato", ""))
    combined = (costi_text + tempo_text).lower()
    if any(kw in combined for kw in ["significativ", "notevole", "alto", "50%", "60%", "70%"]):
        values.append(4.5)
    elif any(kw in combined for kw in ["moderat", "medio", "30%", "40%"]):
        values.append(3.5)
    else:
        values.append(3.0)

    # 3. Gestione Rischi (from rischi_e_criticita - inverse: more risks = lower score)
    rischi_text = str(analysis_results.get("rischi_e_criticita", ""))
    if any(kw in rischi_text.lower() for kw in ["alto rischio", "critico", "grave"]):
        values.append(2.0)
    elif any(kw in rischi_text.lower() for kw in ["medio", "moderato"]):
        values.append(3.0)
    elif any(kw in rischi_text.lower() for kw in ["basso", "minim", "gestibil"]):
        values.append(4.5)
    else:
        values.append(3.0)

    # 4. ROI Previsto (from overall score and benefits)
    score_text = str(analysis_results.get("score_complessivo", ""))
    score_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', score_text)
    if score_match:
        roi_value = float(score_match.group(1)) / 2  # Convert 10-scale to 5-scale
        values.append(min(5.0, roi_value))
    else:
        values.append(3.5)

    # 5. Facilita Implementazione (from roadmap and formazione)
    roadmap_text = str(analysis_results.get("roadmap_implementazione", ""))
    formazione_text = str(analysis_results.get("formazione_necessaria", ""))
    combined = (roadmap_text + formazione_text).lower()
    if any(kw in combined for kw in ["semplice", "facile", "rapida", "minima"]):
        values.append(4.5)
    elif any(kw in combined for kw in ["complessa", "lunga", "estesa"]):
        values.append(2.0)
    else:
        values.append(3.0)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=config.COLORS["primary"],
        opacity=0.4,
        line=dict(color=config.COLORS["primary"], width=2),
        name='Valutazione Progetto'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickmode='linear',
                tick0=0,
                dtick=1
            )
        ),
        showlegend=True,
        title="Analisi Multi-dimensionale",
        height=400,
        margin=dict(l=60, r=60, t=60, b=60)
    )

    return fig


def create_risk_heatmap(analysis_results):
    """Create a risk assessment heatmap"""
    import re

    # Define risk categories
    risk_categories = ['Tecnico', 'Privacy/GDPR', 'Organizzativo', 'Legale', 'Resistenza']

    # Extract risk levels from analysis
    rischi_text = str(analysis_results.get("rischi_e_criticita", "")).lower()
    privacy_text = str(analysis_results.get("problemi_legali_e_privacy", "")).lower()

    # Calculate risk scores (1=low, 5=high)
    risks = []

    # Tecnico
    if any(kw in rischi_text for kw in ["tecnico alto", "complessita elevata"]):
        risks.append(4)
    elif "tecnic" in rischi_text:
        risks.append(3)
    else:
        risks.append(2)

    # Privacy/GDPR
    if any(kw in privacy_text for kw in ["gdpr", "privacy", "dati personali"]):
        if any(kw in privacy_text for kw in ["critico", "alto"]):
            risks.append(4)
        else:
            risks.append(3)
    else:
        risks.append(2)

    # Organizzativo
    if any(kw in rischi_text for kw in ["cambiamento", "resistenza", "organizzativ"]):
        risks.append(3)
    else:
        risks.append(2)

    # Legale
    if any(kw in privacy_text for kw in ["responsabilita", "legal", "compliance"]):
        risks.append(3)
    else:
        risks.append(2)

    # Resistenza al cambiamento
    formazione = str(analysis_results.get("formazione_necessaria", "")).lower()
    if any(kw in rischi_text + formazione for kw in ["resistenza", "change management"]):
        risks.append(3)
    else:
        risks.append(2)

    # Create color scale based on risk level
    colors = []
    for r in risks:
        if r >= 4:
            colors.append('#EF4444')  # Red
        elif r >= 3:
            colors.append('#F59E0B')  # Orange
        else:
            colors.append('#10B981')  # Green

    fig = go.Figure(go.Bar(
        x=risks,
        y=risk_categories,
        orientation='h',
        marker=dict(color=colors),
        text=[f'{r}/5' for r in risks],
        textposition='outside'
    ))

    fig.update_layout(
        title="Valutazione Rischi per Area",
        xaxis=dict(title="Livello Rischio", range=[0, 5.5]),
        yaxis=dict(title=""),
        height=300,
        margin=dict(l=100, r=20, t=50, b=30)
    )

    return fig

def calculate_process_position(analysis_results=None, answers=None):
    """
    Calculate the position of the process in the impact matrix.
    Returns (x, y) coordinates in range 0-1.
    X = Process Complexity, Y = AI Autonomy
    """
    if not answers:
        return None, None

    # === Calculate X (Process Complexity) ===
    complexity_score = 0

    # Count steps in AS-IS process
    as_is_steps = answers.get("as_is_step", "")
    if as_is_steps:
        step_count = len([s for s in as_is_steps.strip().split("\n") if s.strip()])
        complexity_score += min(step_count, 10)  # Max 10 points from steps

    # Count systems/data sources
    dati_sistemi = answers.get("to_be_dati_sistemi", "")
    if dati_sistemi:
        # Count commas and newlines as separators
        system_count = len([s for s in dati_sistemi.replace(",", "\n").split("\n") if s.strip()])
        complexity_score += min(system_count, 5)  # Max 5 points

    # Count tools to integrate
    tools = answers.get("to_be_tool", "")
    if tools:
        tool_count = len([t for t in tools.replace(",", "\n").split("\n") if t.strip()])
        complexity_score += min(tool_count, 5)  # Max 5 points

    # Normalize to 0-1 (max possible = 20)
    x = min(1.0, complexity_score / 15)
    # Add small offset to avoid edge placement
    x = max(0.1, min(0.9, x))

    # === Calculate Y (AI Autonomy) ===
    autonomy_score = 0.5  # Start at middle

    if analysis_results:
        # Analyze substitution vs augmentation text
        impatto_text = str(analysis_results.get("analisi_impatto_sostituzione_vs_augmentation", "")).lower()

        # Keywords indicating high autonomy (substitution)
        high_autonomy_keywords = ["sostituzione", "automazione completa", "completamente automatizzato",
                                   "senza intervento", "autonomo", "sostituire"]
        # Keywords indicating low autonomy (augmentation)
        low_autonomy_keywords = ["augmentation", "supporto", "assistenza", "affiancamento",
                                  "supervisione", "approvazione", "revisione umana"]

        for kw in high_autonomy_keywords:
            if kw in impatto_text:
                autonomy_score += 0.1

        for kw in low_autonomy_keywords:
            if kw in impatto_text:
                autonomy_score -= 0.1

    # Also check user's description of actions and limits
    azioni_limiti = str(answers.get("to_be_azioni_limiti", "")).lower()
    if azioni_limiti:
        if any(kw in azioni_limiti for kw in ["senza supervisione", "autonomamente", "automatico"]):
            autonomy_score += 0.15
        if any(kw in azioni_limiti for kw in ["approvazione", "conferma", "supervisione", "controllo umano"]):
            autonomy_score -= 0.15

    # Normalize to 0-1
    y = max(0.1, min(0.9, autonomy_score))

    return x, y


def create_impact_matrix(analysis_results=None, answers=None):
    """Create a 2x2 matrix for Substitution vs Augmentation with dynamic positioning"""

    fig = go.Figure()

    # Add quadrants
    quadrants = [
        {"x": [0, 0.5, 0.5, 0], "y": [0, 0, 0.5, 0.5], "color": "#FEE2E2", "label": "Quick Wins"},
        {"x": [0.5, 1, 1, 0.5], "y": [0, 0, 0.5, 0.5], "color": "#FEF3C7", "label": "Augmentation"},
        {"x": [0, 0.5, 0.5, 0], "y": [0.5, 0.5, 1, 1], "color": "#DBEAFE", "label": "High Risk"},
        {"x": [0.5, 1, 1, 0.5], "y": [0.5, 0.5, 1, 1], "color": "#D1FAE5", "label": "Automation"}
    ]

    for quad in quadrants:
        fig.add_trace(go.Scatter(
            x=quad["x"],
            y=quad["y"],
            fill="toself",
            fillcolor=quad["color"],
            line=dict(width=0),
            showlegend=True,
            name=quad["label"],
            hoverinfo='name'
        ))

    # Calculate and add process marker if data available
    x, y = calculate_process_position(analysis_results, answers)
    if x is not None and y is not None:
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=25,
                color=config.COLORS["primary"],
                symbol='star',
                line=dict(width=2, color='white')
            ),
            text=[''],
            textposition='top center',
            name='Il tuo processo',
            hovertext=f'Complessita: {x:.0%}<br>Autonomia AI: {y:.0%}',
            hoverinfo='text+name'
        ))

    # Add labels
    annotations = [
        dict(x=0.25, y=0.25, text="Processi Semplici<br>Basso Rischio", showarrow=False, font=dict(size=10)),
        dict(x=0.75, y=0.25, text="Augmentation<br>Supporto Umano", showarrow=False, font=dict(size=10)),
        dict(x=0.25, y=0.75, text="Alto Rischio<br>Serve Giudizio", showarrow=False, font=dict(size=10)),
        dict(x=0.75, y=0.75, text="Automazione<br>Completa", showarrow=False, font=dict(size=10)),
    ]

    fig.update_layout(
        title="Matrice Impatto: Sostituzione vs Augmentation",
        xaxis=dict(title="Complessita Processo ->", showgrid=False, zeroline=False, range=[0, 1]),
        yaxis=dict(title="Autonomia AI ->", showgrid=False, zeroline=False, range=[0, 1]),
        height=500,
        annotations=annotations,
        hovermode='closest'
    )

    return fig

def create_score_gauge(score):
    """Create a gauge chart for overall project score"""

    if not score:
        score = 0

    # Determine color based on score
    if score >= 7:
        color = config.COLORS["success"]
    elif score >= 5:
        color = config.COLORS["warning"]
    else:
        color = config.COLORS["danger"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Score Complessivo Progetto", 'font': {'size': 20}},
        gauge={
            'axis': {'range': [0, 10], 'tickwidth': 1},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': config.COLORS["border"],
            'steps': [
                {'range': [0, 4], 'color': '#FEE2E2'},
                {'range': [4, 7], 'color': '#FEF3C7'},
                {'range': [7, 10], 'color': '#D1FAE5'}
            ],
        }
    ))

    fig.update_layout(height=350, margin=dict(l=20, r=20, t=60, b=20))

    return fig

def render_benefits_chart(benefits_text):
    """Create a visual representation of benefits"""

    # This is a simple implementation
    # In production, you might want to use NLP to extract and categorize benefits

    st.markdown("### 📈 Benefici Previsti")
    st.info(benefits_text)

def render_risks_chart(risks_text):
    """Create a visual representation of risks"""

    st.markdown("### ⚠️ Rischi Identificati")
    st.warning(risks_text)

def create_workflow_comparison(as_is_steps, to_be_description):
    """Create a side-by-side workflow comparison"""

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📋 Processo AS-IS")
        st.markdown(f"```\n{as_is_steps}\n```")

    with col2:
        st.markdown("#### 🤖 Processo TO-BE")
        st.markdown(f"```\n{to_be_description}\n```")
