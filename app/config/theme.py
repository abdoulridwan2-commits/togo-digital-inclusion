"""
Thème et styles du dashboard Togo Digital & Financial Inclusion
Palette inspirée des couleurs nationales et du design Civic Tech
"""

COLORS = {
    "navy": "#0B3D5C",        # Bleu régal moderne
    "blue": "#1D70A2",        # Bleu technologique
    "gold": "#D99A00",        # Or togolais
    "green": "#16845B",       # Vert émeraude
    "red": "#C94C4C",         # Rouge alerte
    "light": "#F8FAFC",
    "border": "#E2E8F0",
    "text": "#0F172A",
}

def get_css() -> str:
    """Retourne le CSS global et enrichi du dashboard."""
    return f"""
    <style>
        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{
            padding-top: 0.8rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }}
        body {{ background: #F8FAFC; font-family: 'Inter', -apple-system, sans-serif; }}
        h1, h2, h3 {{ color: {COLORS['text']}; font-weight: 750; }}

        .togo-bar {{
            height: 4px;
            background: linear-gradient(to right, #006A4E 33%, #FFCE00 33%, #FFCE00 66%, #D21034 66%);
            border-radius: 4px;
            margin-bottom: 8px;
        }}

        .main-header {{
            background: linear-gradient(135deg, #07263D 0%, #0B3D5C 55%, #155E75 100%);
            padding: 1.8rem 2.2rem;
            border-radius: 16px;
            margin-bottom: 1.2rem;
            color: white;
            box-shadow: 0 10px 25px rgba(11,61,92,0.18);
            position: relative;
        }}
        .main-header h1 {{
            color: white !important;
            font-size: 2.1rem !important;
            margin: 0 !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em;
        }}
        .main-header p {{
            color: #E2E8F0 !important;
            font-size: 1.02rem !important;
            margin: 0.5rem 0 0 0 !important;
            max-width: 900px;
            line-height: 1.5;
        }}
        .header-badge {{
            display: inline-block;
            margin-top: 0.8rem;
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 999px;
            padding: 0.35rem 0.9rem;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            color: white;
        }}

        div[data-testid="stRadio"] > div {{
            background: white;
            padding: 0.5rem;
            border-radius: 14px;
            border: 1px solid {COLORS['border']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        div[data-testid="stRadio"] label {{ font-weight: 650; }}

        div[data-testid="stMetric"] {{
            background: white;
            padding: 1.1rem 1.1rem;
            border-radius: 14px;
            border: 1px solid {COLORS['border']};
            box-shadow: 0 3px 10px rgba(0,0,0,0.035);
            border-top: 3px solid {COLORS['blue']};
        }}
        div[data-testid="stMetricValue"] {{
            color: {COLORS['navy']} !important;
            font-weight: 800 !important;
            font-size: 1.9rem !important;
        }}

        .card {{
            background: white;
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 1.3rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 3px 12px rgba(0,0,0,0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .card:hover {{
            box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        }}
        .card-title {{ color: {COLORS['navy']}; font-weight: 750; font-size: 1.05rem; margin-bottom: 0.5rem; }}
        .card-text {{ color: #475569; line-height: 1.6; font-size: 0.93rem; }}

        .question-box {{
            background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
            border-left: 5px solid {COLORS['navy']};
            padding: 1.4rem 1.7rem;
            border-radius: 0 14px 14px 0;
            margin: 1.2rem 0;
            box-shadow: 0 2px 8px rgba(11,61,92,0.05);
        }}
        .question-title {{
            font-size: 0.78rem;
            font-weight: 800;
            color: {COLORS['navy']};
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .question-text {{
            font-size: 1.18rem;
            font-weight: 700;
            color: {COLORS['text']};
            margin-top: 0.4rem;
            line-height: 1.4;
        }}

        .insight {{
            background: #FEF9C3;
            border-left: 5px solid {COLORS['gold']};
            padding: 1rem 1.2rem;
            border-radius: 0 10px 10px 0;
            margin: 0.8rem 0;
            color: #713F12;
        }}
        .observation {{
            background: #EFF6FF;
            border-left: 5px solid {COLORS['blue']};
            padding: 1rem 1.2rem;
            border-radius: 0 10px 10px 0;
            margin: 0.8rem 0;
            color: #1E3A8A;
        }}
        .recommendation {{
            background: #ECFDF5;
            border-left: 5px solid {COLORS['green']};
            padding: 1.2rem 1.3rem;
            border-radius: 0 10px 10px 0;
            margin-bottom: 1rem;
            color: #064E3B;
            line-height: 1.6;
        }}
        .desert-badge {{
            background: #FEE2E2;
            color: #991B1B;
            padding: 4px 10px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.8rem;
            display: inline-block;
        }}
        .champion-badge {{
            background: #D1FAE5;
            color: #065F46;
            padding: 4px 10px;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.8rem;
            display: inline-block;
        }}
    </style>
    """