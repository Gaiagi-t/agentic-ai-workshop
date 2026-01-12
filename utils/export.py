"""
Export utilities for Agentic AI Workshop
Generates PDF reports with visualizations
"""

import streamlit as st
from fpdf import FPDF
from datetime import datetime
import config
import tempfile
import os
import re

# Try to import matplotlib for chart generation
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class AnalysisPDF(FPDF):
    """Custom PDF class for analysis reports"""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Logo/Title
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(27, 152, 224)  # IFAB blue
        self.cell(0, 10, 'Agentic AI Workshop - Report Analisi', 0, 1, 'C')
        self.set_font('Helvetica', '', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, config.IFAB_INFO['name'], 0, 1, 'C')
        self.ln(5)
        # Line
        self.set_draw_color(27, 152, 224)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generato il {date_str} | Pagina {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(27, 152, 224)
        self.cell(0, 10, self._clean_text(title), 0, 1)
        self.ln(2)

    def section_content(self, content):
        self.set_font('Helvetica', '', 11)
        self.set_text_color(50, 50, 50)
        clean_content = self._clean_text(content)
        self.multi_cell(0, 6, clean_content)
        self.ln(5)

    def _clean_text(self, text):
        """Clean text for PDF - remove problematic characters"""
        if not text:
            return ""

        # Convert to string if needed
        text = str(text)

        # Character replacements for latin-1 compatibility
        replacements = {
            # Quotes
            '\u2019': "'",   # Right single quote
            '\u2018': "'",   # Left single quote
            '\u201c': '"',   # Left double quote
            '\u201d': '"',   # Right double quote
            '\u00ab': '"',   # Left guillemet
            '\u00bb': '"',   # Right guillemet
            '\u0060': "'",   # Grave accent
            '\u00b4': "'",   # Acute accent
            # Dashes
            '\u2013': '-',   # En dash
            '\u2014': '-',   # Em dash
            '\u2212': '-',   # Minus sign
            '\u2010': '-',   # Hyphen
            '\u2011': '-',   # Non-breaking hyphen
            # Ellipsis
            '\u2026': '...',
            # Bullets and list markers
            '\u2022': '-',   # Bullet
            '\u2023': '>',   # Triangular bullet
            '\u25aa': '-',   # Small square
            '\u25cf': '-',   # Black circle
            '\u25cb': 'o',   # White circle
            '\u25a0': '-',   # Black square
            '\u25a1': '-',   # White square
            '\u2043': '-',   # Hyphen bullet
            '\u27a2': '>',   # Arrow bullet
            # Italian accented vowels - use plain ASCII for maximum compatibility
            '\u00e0': 'a',   # a grave
            '\u00c0': 'A',   # A grave
            '\u00e8': 'e',   # e grave
            '\u00c8': 'E',   # E grave
            '\u00e9': 'e',   # e acute
            '\u00c9': 'E',   # E acute
            '\u00ec': 'i',   # i grave
            '\u00cc': 'I',   # I grave
            '\u00f2': 'o',   # o grave
            '\u00d2': 'O',   # O grave
            '\u00f9': 'u',   # u grave
            '\u00d9': 'U',   # U grave
            '\u00e1': 'a',   # a acute
            '\u00ed': 'i',   # i acute
            '\u00f3': 'o',   # o acute
            '\u00fa': 'u',   # u acute
            # Other accented chars
            '\u00e2': 'a',   # a circumflex
            '\u00ea': 'e',   # e circumflex
            '\u00ee': 'i',   # i circumflex
            '\u00f4': 'o',   # o circumflex
            '\u00fb': 'u',   # u circumflex
            '\u00e4': 'a',   # a umlaut
            '\u00eb': 'e',   # e umlaut
            '\u00ef': 'i',   # i umlaut
            '\u00f6': 'o',   # o umlaut
            '\u00fc': 'u',   # u umlaut
            '\u00f1': 'n',   # n tilde
            '\u00e7': 'c',   # c cedilla
            # Symbols
            '\u00b0': ' gradi',  # Degree symbol
            '\u20ac': 'EUR',     # Euro sign
            '\u00a3': 'GBP',     # Pound sign
            '\u00a9': '(c)',     # Copyright
            '\u00ae': '(R)',     # Registered
            '\u2122': '(TM)',    # Trademark
            '\u00b7': '-',       # Middle dot
            '\u2027': '-',       # Hyphenation point
            # Arrows
            '\u2192': '->',      # Right arrow
            '\u2190': '<-',      # Left arrow
            '\u2194': '<->',     # Left right arrow
            '\u21d2': '=>',      # Double right arrow
            '\u21d0': '<=',      # Double left arrow
            # Math
            '\u00d7': 'x',       # Multiplication
            '\u00f7': '/',       # Division
            '\u2264': '<=',      # Less than or equal
            '\u2265': '>=',      # Greater than or equal
            '\u2260': '!=',      # Not equal
            '\u2248': '~',       # Approximately equal
            '\u00b1': '+/-',     # Plus-minus
            '\u221e': 'inf',     # Infinity
            # Spaces
            '\u00a0': ' ',       # Non-breaking space
            '\u2002': ' ',       # En space
            '\u2003': ' ',       # Em space
            '\u2009': ' ',       # Thin space
            '\u200b': '',        # Zero-width space
            '\u200c': '',        # Zero-width non-joiner
            '\u200d': '',        # Zero-width joiner
            '\ufeff': '',        # BOM
            # Line breaks
            '\r\n': '\n',        # Windows line break
            '\r': '\n',          # Old Mac line break
            '\n': '\n',          # Keep newlines
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # Remove any remaining non-ASCII characters
        result = []
        for char in text:
            if ord(char) < 128:  # Pure ASCII
                result.append(char)
            else:
                try:
                    char.encode('latin-1')
                    result.append(char)
                except UnicodeEncodeError:
                    # Replace with space for readability
                    pass  # Skip character entirely

        # Clean up result
        cleaned = ''.join(result)

        # Remove trailing/leading whitespace from each line but preserve structure
        lines = cleaned.split('\n')
        lines = [line.rstrip() for line in lines]
        cleaned = '\n'.join(lines)

        return cleaned.strip()

    def add_score(self, score):
        self.set_font('Helvetica', 'B', 24)
        if score >= 7:
            self.set_text_color(76, 175, 80)  # Green
        elif score >= 5:
            self.set_text_color(255, 152, 0)  # Orange
        else:
            self.set_text_color(244, 67, 54)  # Red
        self.cell(0, 15, f'Score: {score}/10', 0, 1, 'C')
        self.ln(5)

    def add_image_file(self, image_path, width=170):
        """Add image from file path to PDF"""
        try:
            x = (210 - width) / 2  # Center horizontally (A4 width = 210mm)
            self.image(image_path, x=x, w=width)
            self.ln(5)
        except Exception as e:
            pass


def calculate_radar_values(analysis_results):
    """Calculate values for radar chart from analysis results"""
    values = []

    # 1. Fattibilita Tecnica
    fatt_text = str(analysis_results.get("fattibilita_tecnica", ""))
    fatt_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*5', fatt_text)
    if fatt_match:
        values.append(float(fatt_match.group(1)))
    else:
        if any(kw in fatt_text.lower() for kw in ["alta", "elevata", "ottima"]):
            values.append(4.5)
        elif any(kw in fatt_text.lower() for kw in ["media", "moderata"]):
            values.append(3.0)
        elif any(kw in fatt_text.lower() for kw in ["bassa", "difficile"]):
            values.append(2.0)
        else:
            values.append(3.5)

    # 2. Impatto Business
    costi_text = str(analysis_results.get("riduzione_costi", ""))
    tempo_text = str(analysis_results.get("risparmio_di_tempo_stimato", ""))
    combined = (costi_text + tempo_text).lower()
    if any(kw in combined for kw in ["significativ", "notevole", "alto", "50%", "60%", "70%"]):
        values.append(4.5)
    elif any(kw in combined for kw in ["moderat", "medio", "30%", "40%"]):
        values.append(3.5)
    else:
        values.append(3.0)

    # 3. Gestione Rischi
    rischi_text = str(analysis_results.get("rischi_e_criticita", ""))
    if any(kw in rischi_text.lower() for kw in ["alto rischio", "critico", "grave"]):
        values.append(2.0)
    elif any(kw in rischi_text.lower() for kw in ["medio", "moderato"]):
        values.append(3.0)
    elif any(kw in rischi_text.lower() for kw in ["basso", "minim", "gestibil"]):
        values.append(4.5)
    else:
        values.append(3.0)

    # 4. ROI Previsto
    score_text = str(analysis_results.get("score_complessivo", ""))
    score_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', score_text)
    if score_match:
        roi_value = float(score_match.group(1)) / 2
        values.append(min(5.0, roi_value))
    else:
        values.append(3.5)

    # 5. Facilita Implementazione
    roadmap_text = str(analysis_results.get("roadmap_implementazione", ""))
    formazione_text = str(analysis_results.get("formazione_necessaria", ""))
    combined = (roadmap_text + formazione_text).lower()
    if any(kw in combined for kw in ["semplice", "facile", "rapida", "minima"]):
        values.append(4.5)
    elif any(kw in combined for kw in ["complessa", "lunga", "estesa"]):
        values.append(2.0)
    else:
        values.append(3.0)

    return values


def calculate_risk_values(analysis_results):
    """Calculate risk values for bar chart"""
    rischi_text = str(analysis_results.get("rischi_e_criticita", "")).lower()
    privacy_text = str(analysis_results.get("problemi_legali_e_privacy", "")).lower()
    formazione = str(analysis_results.get("formazione_necessaria", "")).lower()

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

    # Resistenza
    if any(kw in rischi_text + formazione for kw in ["resistenza", "change management"]):
        risks.append(3)
    else:
        risks.append(2)

    return risks


def create_radar_chart_image(analysis_results):
    """Create radar chart image using matplotlib"""
    if not MATPLOTLIB_AVAILABLE:
        return None

    try:
        categories = ['Fattibilita\nTecnica', 'Impatto\nBusiness', 'Gestione\nRischi',
                      'ROI\nPrevisto', 'Facilita\nImplementazione']
        values = calculate_radar_values(analysis_results)

        # Close the polygon
        values_closed = values + [values[0]]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles_closed = angles + [angles[0]]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles_closed, values_closed, color='#1b98e0', alpha=0.3)
        ax.plot(angles_closed, values_closed, color='#1b98e0', linewidth=2)

        ax.set_xticks(angles)
        ax.set_xticklabels(categories, size=9)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_title('Analisi Multi-dimensionale', size=12, fontweight='bold', pad=20)
        ax.grid(True)

        # Save to temp file
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        return tmp_file.name
    except Exception as e:
        return None


def create_risk_chart_image(analysis_results):
    """Create horizontal bar chart for risks using matplotlib"""
    if not MATPLOTLIB_AVAILABLE:
        return None

    try:
        categories = ['Tecnico', 'Privacy/GDPR', 'Organizzativo', 'Legale', 'Resistenza']
        risks = calculate_risk_values(analysis_results)

        # Define colors based on risk level
        colors = []
        for r in risks:
            if r >= 4:
                colors.append('#EF4444')
            elif r >= 3:
                colors.append('#F59E0B')
            else:
                colors.append('#10B981')

        fig, ax = plt.subplots(figsize=(7, 3.5))
        bars = ax.barh(categories, risks, color=colors)

        ax.set_xlim(0, 5.5)
        ax.set_xlabel('Livello Rischio (1-5)')
        ax.set_title('Valutazione Rischi per Area', size=12, fontweight='bold')

        # Add value labels
        for bar, risk in zip(bars, risks):
            ax.text(risk + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{risk}/5', va='center', fontsize=10)

        plt.tight_layout()

        # Save to temp file
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        return tmp_file.name
    except Exception as e:
        return None


def create_matrix_chart_image(answers, analysis_results):
    """Create impact matrix chart using matplotlib"""
    if not MATPLOTLIB_AVAILABLE:
        return None

    try:
        # Calculate position (simplified version)
        complexity_score = 0
        as_is_steps = answers.get("as_is_step", "")
        if as_is_steps:
            step_count = len([s for s in as_is_steps.strip().split("\n") if s.strip()])
            complexity_score += min(step_count, 10)

        dati_sistemi = answers.get("to_be_dati_sistemi", "")
        if dati_sistemi:
            system_count = len([s for s in dati_sistemi.replace(",", "\n").split("\n") if s.strip()])
            complexity_score += min(system_count, 5)

        x = max(0.1, min(0.9, complexity_score / 15))

        # Calculate autonomy
        autonomy_score = 0.5
        impatto_text = str(analysis_results.get("analisi_impatto_sostituzione_vs_augmentation", "")).lower()
        for kw in ["sostituzione", "automazione completa", "autonomo"]:
            if kw in impatto_text:
                autonomy_score += 0.1
        for kw in ["augmentation", "supporto", "supervisione"]:
            if kw in impatto_text:
                autonomy_score -= 0.1
        y = max(0.1, min(0.9, autonomy_score))

        fig, ax = plt.subplots(figsize=(6, 5))

        # Draw quadrants
        ax.fill([0, 0.5, 0.5, 0], [0, 0, 0.5, 0.5], color='#FEE2E2', alpha=0.7, label='Quick Wins')
        ax.fill([0.5, 1, 1, 0.5], [0, 0, 0.5, 0.5], color='#FEF3C7', alpha=0.7, label='Augmentation')
        ax.fill([0, 0.5, 0.5, 0], [0.5, 0.5, 1, 1], color='#DBEAFE', alpha=0.7, label='High Risk')
        ax.fill([0.5, 1, 1, 0.5], [0.5, 0.5, 1, 1], color='#D1FAE5', alpha=0.7, label='Automation')

        # Add labels
        ax.text(0.25, 0.25, 'Processi\nSemplici', ha='center', va='center', fontsize=9)
        ax.text(0.75, 0.25, 'Augmentation\nSupporto', ha='center', va='center', fontsize=9)
        ax.text(0.25, 0.75, 'Alto Rischio\nGiudizio', ha='center', va='center', fontsize=9)
        ax.text(0.75, 0.75, 'Automazione\nCompleta', ha='center', va='center', fontsize=9)

        # Plot process position
        ax.scatter([x], [y], s=300, c='#1b98e0', marker='*', zorder=5, edgecolors='white', linewidths=2)
        ax.annotate('Il tuo\nprocesso', (x, y), textcoords="offset points", xytext=(15, 10),
                    fontsize=9, fontweight='bold', color='#1b98e0')

        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Complessita Processo ->', fontsize=10)
        ax.set_ylabel('Autonomia AI ->', fontsize=10)
        ax.set_title('Matrice Impatto: Sostituzione vs Augmentation', size=12, fontweight='bold')
        ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5)

        plt.tight_layout()

        # Save to temp file
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(tmp_file.name, dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        return tmp_file.name
    except Exception as e:
        return None


def generate_analysis_pdf(answers, analysis_results):
    """
    Generate PDF report from analysis results
    """
    pdf = AnalysisPDF()
    pdf.add_page()

    # Date
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(100, 100, 100)
    date_str = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 5, f'Data: {date_str}', 0, 1, 'R')
    pdf.ln(5)

    # Score if available
    score_text = analysis_results.get("score_complessivo", "")
    extracted_score = None
    if score_text:
        try:
            import re
            score_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*10', str(score_text))
            if score_match:
                extracted_score = float(score_match.group(1))
                pdf.add_score(extracted_score)
        except:
            pass

    # === SEZIONE AS-IS ===
    pdf.section_title("1. ANALISI AS-IS (Situazione Attuale)")

    if answers.get("as_is_processo"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Processo:", 0, 1)
        pdf.section_content(answers.get("as_is_processo", ""))

    if answers.get("as_is_step"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Step del processo:", 0, 1)
        pdf.section_content(answers.get("as_is_step", ""))

    if answers.get("as_is_ruoli"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Ruoli coinvolti:", 0, 1)
        pdf.section_content(answers.get("as_is_ruoli", ""))

    if answers.get("as_is_strumenti"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Strumenti utilizzati:", 0, 1)
        pdf.section_content(answers.get("as_is_strumenti", ""))

    if answers.get("as_is_tempo"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Tempi:", 0, 1)
        pdf.section_content(answers.get("as_is_tempo", ""))

    if answers.get("as_is_problemi"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Problemi identificati:", 0, 1)
        pdf.section_content(answers.get("as_is_problemi", ""))

    # === SEZIONE TO-BE ===
    pdf.add_page()
    pdf.section_title("2. VISIONE TO-BE (Stato Futuro)")

    if answers.get("to_be_visione"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Visione:", 0, 1)
        pdf.section_content(answers.get("to_be_visione", ""))

    if answers.get("to_be_agenti"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Agenti AI previsti:", 0, 1)
        pdf.section_content(answers.get("to_be_agenti", ""))

    if answers.get("to_be_azioni_limiti"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Azioni e limiti:", 0, 1)
        pdf.section_content(answers.get("to_be_azioni_limiti", ""))

    if answers.get("to_be_benefici"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Benefici attesi:", 0, 1)
        pdf.section_content(answers.get("to_be_benefici", ""))

    if answers.get("to_be_rischi"):
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 6, "Rischi identificati:", 0, 1)
        pdf.section_content(answers.get("to_be_rischi", ""))

    # === ANALISI AI ===
    pdf.add_page()
    pdf.section_title("3. ANALISI AI")

    sections = [
        ("fattibilita_tecnica", "Fattibilita Tecnica"),
        ("analisi_impatto_sostituzione_vs_augmentation", "Sostituzione vs Augmentation"),
        ("risparmio_di_tempo_stimato", "Risparmio di Tempo"),
        ("riduzione_costi", "Riduzione Costi"),
        ("attivita_eliminate_o_ottimizzate", "Attivita Ottimizzate"),
        ("rischi_e_criticita", "Rischi e Criticita"),
        ("formazione_necessaria", "Formazione Necessaria"),
        ("problemi_legali_e_privacy", "Aspetti Legali e Privacy"),
        ("roadmap_implementazione", "Roadmap Implementazione"),
        ("raccomandazioni_finali", "Raccomandazioni Finali")
    ]

    for key, title in sections:
        content = analysis_results.get(key, "")
        if content:
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(27, 152, 224)
            pdf.cell(0, 8, pdf._clean_text(title), 0, 1)
            pdf.section_content(content)

    # === DASHBOARD VISUALIZZAZIONI ===
    pdf.add_page()
    pdf.section_title("4. DASHBOARD ANALISI")

    temp_files = []  # Track temp files for cleanup

    # Radar Chart
    radar_path = create_radar_chart_image(analysis_results)
    if radar_path:
        temp_files.append(radar_path)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, "Analisi Multi-dimensionale del Progetto", 0, 1, 'C')
        pdf.add_image_file(radar_path, width=120)
        pdf.ln(5)

    # Risk Chart
    risk_path = create_risk_chart_image(analysis_results)
    if risk_path:
        temp_files.append(risk_path)
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, "Valutazione Rischi", 0, 1, 'C')
        pdf.add_image_file(risk_path, width=150)
        pdf.ln(5)

    # Impact Matrix
    matrix_path = create_matrix_chart_image(answers, analysis_results)
    if matrix_path:
        temp_files.append(matrix_path)
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(50, 50, 50)
        pdf.cell(0, 8, "Matrice di Impatto", 0, 1, 'C')
        pdf.add_image_file(matrix_path, width=140)

    # If no charts were generated, add a note
    if not any([radar_path, risk_path, matrix_path]):
        pdf.set_font('Helvetica', 'I', 10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "[Dashboard non disponibili - matplotlib non installato]", 0, 1, 'C')
        pdf.ln(5)
        # Add text summary instead
        pdf.section_title("Riepilogo Valutazioni")
        radar_values = calculate_radar_values(analysis_results)
        categories = ['Fattibilita Tecnica', 'Impatto Business', 'Gestione Rischi', 'ROI Previsto', 'Facilita Implementazione']
        summary = ""
        for cat, val in zip(categories, radar_values):
            summary += f"- {cat}: {val}/5\n"
        pdf.section_content(summary)

    # Cleanup temp files
    for tmp_path in temp_files:
        try:
            os.unlink(tmp_path)
        except:
            pass

    # Return PDF as bytes
    pdf_output = pdf.output()
    return bytes(pdf_output)


def render_pdf_download_button(answers, analysis_results):
    """
    Render PDF download button in Streamlit
    """
    try:
        pdf_bytes = generate_analysis_pdf(answers, analysis_results)
        filename = f"analisi_agentic_ai_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

        st.download_button(
            label="📄 Scarica PDF",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Errore nella generazione del PDF: {str(e)}")
        st.caption("Assicurati di aver installato: pip install fpdf2")
