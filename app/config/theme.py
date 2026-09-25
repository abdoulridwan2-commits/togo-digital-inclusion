"""
Thème et couleurs du dashboard
"""

COLORS = {
    "navy": "#0B3D5C",
    "blue": "#1D70A2",
    "gold": "#D99A00",
    "green": "#16845B",
    "red": "#C94C4C",
    "light": "#F5F7FA",
    "border": "#E2E8F0",
    "text": "#172033",
}

def get_css() -> str:
    """Retourne le CSS global du dashboard."""
    return f"""
    <style>
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{
            padding-top: 1rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}
        body {{ background: #F7F9FC; }}
        h1, h2, h3 {{ color: {COLORS['text']}; }}

        .main-header {{
            background: linear-gradient(135deg, #082F49 0%, #0B3D5C 50%, #155E75 100%);
            padding: 1.8rem 2rem;
            border-radius: 0 0 18px 18px;
            margin-bottom: 1rem;
            color: white;
            box-shadow: 0 8px 24px rgba(11,61,92,0.20);
        }}
        .main-header h1 {{
            color: white !important;
            font-size: 2rem !important;
            margin: 0 !important;
            font-weight: 750 !important;
        }}
        .main-header p {{
            color: #D5E7F3 !important;
            font-size: 1rem !important;
            margin: 0.5rem 0 0 0 !important;
        }}
        .header-badge {{
            display: inline-block;
            margin-top: 0.8rem;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 999px;
            padding: 0.35rem 0.8rem;
            font-size: 0.78rem;
            color: white;
        }}

        div[data-testid="stRadio"] > div {{
            background: white;
            padding: 0.45rem;
            border-radius: 14px;
            border: 1px solid {COLORS['border']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        div[data-testid="stRadio"] label {{ font-weight: 600; }}

        div[data-testid="stMetric"] {{
            background: white;
            padding: 1.1rem 1rem;
            border-radius: 14px;
            border: 1px solid {COLORS['border']};
            box-shadow: 0 3px 10px rgba(0,0,0,0.04);
        }}
        div[data-testid="stMetricValue"] {{
            color: {COLORS['navy']} !important;
            font-weight: 750 !important;
        }}

        .card {{
            background: white;
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 1.2rem 1.3rem;
            margin-bottom: 1rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.035);
        }}
        .card-title {{ color: {COLORS['navy']}; font-weight: 750; font-size: 1rem; margin-bottom: 0.5rem; }}
        .card-text {{ color: #526174; line-height: 1.6; }}

        .question-box {{
            background: linear-gradient(100deg, #E8F4FC, #F7FBFE);
            border-left: 5px solid {COLORS['navy']};
            padding: 1.5rem 1.7rem;
            border-radius: 0 14px 14px 0;
            margin: 1.4rem 0;
        }}
        .question-title {{
            font-size: 0.78rem;
            font-weight: 800;
            color: {COLORS['navy']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .question-text {{
            font-size: 1.15rem;
            font-weight: 650;
            color: {COLORS['text']};
            margin-top: 0.5rem;
        }}

        .insight {{
            background: #FFF9E8;
            border-left: 5px solid {COLORS['gold']};
            padding: 1rem 1.2rem;
            border-radius: 0 10px 10px 0;
            margin: 0.8rem 0;
        }}
        .observation {{
            background: #EFF7FB;
            border-left: 5px solid {COLORS['blue']};
            padding: 1rem 1.2rem;
            border-radius: 0 10px 10px 0;
            margin: 0.8rem 0;
        }}
        .recommendation {{
            background: #EEF9F4;
            border-left: 5px solid {COLORS['green']};
            padding: 1.1rem 1.3rem;
            border-radius: 0 10px 10px 0;
            margin-bottom: 1rem;
        }}
        .footer {{
            text-align: center;
            color: #94A3B8;
            font-size: 0.8rem;
            padding: 2rem 0 0 0;
        }}
    </style>
    """