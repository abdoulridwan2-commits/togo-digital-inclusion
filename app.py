"""
TOGO DIGITAL & FINANCIAL INCLUSION
Dashboard analytique territorial
Version stabilisée et complète
"""

from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Togo Digital & Financial Inclusion",
    page_icon="🇹🇬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROCESSED_DIR = Path("data/processed")

COLOR_NAVY = "#0B3D5C"
COLOR_BLUE = "#1D70A2"
COLOR_GOLD = "#D99A00"
COLOR_GREEN = "#16845B"
COLOR_BORDER = "#E2E8F0"
COLOR_TEXT = "#172033"

# ============================================================
# STYLE
# ============================================================

st.markdown(f"""
<style>
    #MainMenu, footer, header {{ visibility: hidden; }}
    .block-container {{ padding-top: 1rem; padding-bottom: 3rem; max-width: 1450px; }}
    body {{ background: #F7F9FC; }}
    h1, h2, h3 {{ color: {COLOR_TEXT}; }}

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
        border: 1px solid {COLOR_BORDER};
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    div[data-testid="stRadio"] label {{ font-weight: 600; }}

    div[data-testid="stMetric"] {{
        background: white;
        padding: 1.1rem 1rem;
        border-radius: 14px;
        border: 1px solid {COLOR_BORDER};
        box-shadow: 0 3px 10px rgba(0,0,0,0.04);
    }}
    div[data-testid="stMetricValue"] {{
        color: {COLOR_NAVY} !important;
        font-weight: 750 !important;
    }}

    .card {{
        background: white;
        border: 1px solid {COLOR_BORDER};
        border-radius: 16px;
        padding: 1.2rem 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.035);
    }}
    .card-title {{ color: {COLOR_NAVY}; font-weight: 750; font-size: 1rem; margin-bottom: 0.5rem; }}
    .card-text {{ color: #526174; line-height: 1.6; }}

    .question-box {{
        background: linear-gradient(100deg, #E8F4FC, #F7FBFE);
        border-left: 5px solid {COLOR_NAVY};
        padding: 1.5rem 1.7rem;
        border-radius: 0 14px 14px 0;
        margin: 1.4rem 0;
    }}
    .question-title {{
        font-size: 0.78rem;
        font-weight: 800;
        color: {COLOR_NAVY};
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}
    .question-text {{
        font-size: 1.15rem;
        font-weight: 650;
        color: {COLOR_TEXT};
        margin-top: 0.5rem;
    }}

    .insight {{
        background: #FFF9E8;
        border-left: 5px solid {COLOR_GOLD};
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin: 0.8rem 0;
    }}
    .observation {{
        background: #EFF7FB;
        border-left: 5px solid {COLOR_BLUE};
        padding: 1rem 1.2rem;
        border-radius: 0 10px 10px 0;
        margin: 0.8rem 0;
    }}
    .recommendation {{
        background: #EEF9F4;
        border-left: 5px solid {COLOR_GREEN};
        padding: 1.1rem 1.3rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1rem;
    }}
    .territory-profile {{
        background: white;
        border: 1px solid {COLOR_BORDER};
        border-radius: 18px;
        padding: 1.4rem;
        box-shadow: 0 5px 16px rgba(0,0,0,0.04);
    }}
    .territory-title {{ font-size: 1.4rem; font-weight: 800; color: {COLOR_NAVY}; }}
    .territory-subtitle {{ color: #64748B; font-size: 0.9rem; }}
    .footer {{ text-align: center; color: #94A3B8; font-size: 0.8rem; padding: 2rem 0 0 0; }}
</style>
""", unsafe_allow_html=True)


# ============================================================
# UTILITAIRES
# ============================================================

def format_number(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    try:
        return f"{float(value):,.0f}".replace(",", " ")
    except Exception:
        return str(value)

def format_decimal(value, decimals=1):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    try:
        return f"{float(value):,.{decimals}f}".replace(",", " ")
    except Exception:
        return str(value)

def show_missing_dataset(filename, description):
    st.warning(f"Le fichier **{filename}** n'a pas été trouvé dans `data/processed/`.\n\n**Donnée concernée :** {description}")

def dataframe_download(df, filename="donnees.csv"):
    if df is None or df.empty:
        return
    csv_data = df.to_csv(index=False, encoding="utf-8-sig")
    st.download_button("⬇️ Télécharger les données", data=csv_data, file_name=filename, mime="text/csv")


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data
def load_indicators():
    path = PROCESSED_DIR / "indicateurs_region.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    for col in ["population", "nb_agents_mm", "nb_points_financiers",
                "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

@st.cache_data
def load_internet_penetration():
    path = PROCESSED_DIR / "internet_penetration_clean.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    df = df.dropna(subset=[c for c in ["date", "value"] if c in df.columns])
    if "date" in df.columns:
        df = df.sort_values("date")
    return df

@st.cache_data
def load_internet_abonnes():
    path = PROCESSED_DIR / "internet_abonnes_clean.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    return df

@st.cache_data
def load_telecoms():
    path = PROCESSED_DIR / "telecoms_clean.csv"
    if not path.exists():
        return None
    df = pd.read_csv(path)
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    return df

@st.cache_data
def load_etablissements():
    path = PROCESSED_DIR / "etablissements_financiers_clean.csv"
    if not path.exists():
        return None
    return pd.read_csv(path)


# ============================================================
# HEADER + NAV
# ============================================================

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🇹🇬 Togo Digital & Financial Inclusion</h1>
        <p>Mesurer l'accès au numérique · analyser les réseaux d'accès · comprendre le rôle du Mobile Money · explorer les territoires</p>
        <div class="header-badge">DATA PRODUCT · TOGO · 2026</div>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    pages = ["🏠 INTRO", "🌐 INTERNET", "📡 TÉLÉCOMS", "🏦 FINANCE", "🗺️ TERRITOIRES", "🎯 ACTIONS", "📚 MÉTHODE"]
    return st.radio("Navigation", pages, horizontal=True, label_visibility="collapsed")


# ============================================================
# INTRO
# ============================================================

def render_intro():
    st.markdown("## Vue d'ensemble")
    indicators = load_indicators()
    internet = load_internet_penetration()

    if indicators is not None and not indicators.empty:
        total_pop = indicators["population"].sum()
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        ratio = total_agents / total_points if total_points > 0 else None

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Population couverte", format_number(total_pop))
        c2.metric("Agents Mobile Money", format_number(total_agents))
        c3.metric("Points financiers", format_number(total_points))
        c4.metric("Agents / point financier", format_decimal(ratio))

    st.markdown("""
    <div class="question-box">
        <div class="question-title">QUESTION CENTRALE</div>
        <div class="question-text">
            Là où les services financiers physiques sont peu présents,
            dans quelle mesure le Mobile Money constitue-t-il un relais
            d'accès aux services financiers numériques ?
        </div>
        <p style="margin-top:0.8rem; color:#526174;">
            Le mobile s'est imposé au Togo, mais moins de 4 personnes sur 10 utilisent Internet
            et les banques restent concentrées dans les villes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Le problème en 3 chiffres")
    a, b, c = st.columns(3)

    if internet is not None and not internet.empty:
        latest = internet.iloc[-1]["value"]
        with a:
            st.metric("Usage Internet — dernière année", f"{latest:.1f}%")

    if indicators is not None and not indicators.empty:
        max_pressure = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]
        with b:
            st.metric("Plus forte pression réseau physique", max_pressure["region"])
        max_mm = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
        with c:
            st.metric("Mobile Money le plus dominant", max_mm["region"])

    if indicators is not None and not indicators.empty:
        ratio_region = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
        st.markdown(f"""
        <div class="observation">
            <strong>Lecture rapide</strong><br>
            La région <strong>{ratio_region['region']}</strong> présente le ratio le plus élevé
            d'agents Mobile Money par point financier
            ({format_decimal(ratio_region['ratio_agents_par_point'])}).
            Ce ratio décrit une structure de réseau ; il ne mesure pas l'activité réelle des agents.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Parcours d'analyse")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown('<div class="card"><div class="card-title">01 · INTERNET</div><div class="card-text">Évolution de l\'usage d\'Internet et périodes d\'accélération.</div></div>', unsafe_allow_html=True)
    with p2:
        st.markdown('<div class="card"><div class="card-title">02 · TÉLÉCOMS</div><div class="card-text">Marché, abonnements, investissements et technologies.</div></div>', unsafe_allow_html=True)
    with p3:
        st.markdown('<div class="card"><div class="card-title">03 · TERRITOIRES</div><div class="card-text">Comparer les niveaux d\'accès selon les régions.</div></div>', unsafe_allow_html=True)
    with p4:
        st.markdown('<div class="card"><div class="card-title">04 · ACTIONS</div><div class="card-text">Transformer les observations en pistes d\'intervention.</div></div>', unsafe_allow_html=True)


# ============================================================
# INTERNET
# ============================================================

def render_internet():
    st.markdown("## 🌐 Adoption d'Internet")
    st.caption("Évolution temporelle, rythme de progression et technologies d'accès.")

    df = load_internet_penetration()
    if df is None or df.empty:
        show_missing_dataset("internet_penetration_clean.csv", "Évolution de l'utilisation d'Internet.")
        return

    df = df.copy()
    df["variation"] = df["value"].diff()
    latest = df.iloc[-1]
    first = df.iloc[0]
    total_progress = latest["value"] - first["value"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Dernière valeur", f"{latest['value']:.1f}%", f"{int(latest['date'])}")
    c2.metric("Première valeur", f"{first['value']:.1f}%", f"{int(first['date'])}")
    c3.metric("Progression totale", f"+{total_progress:.1f} points")
    if df["variation"].notna().any():
        max_year = df.loc[df["variation"].idxmax(), "date"]
        c4.metric("Plus forte progression annuelle", f"{int(max_year)}")

    fig = px.line(df, x="date", y="value", markers=True,
                  labels={"date": "Année", "value": "Population utilisant Internet (%)"},
                  title="Évolution de l'utilisation d'Internet")
    fig.update_traces(line=dict(color=COLOR_NAVY, width=4), marker=dict(size=7))
    fig.update_layout(height=470, hovermode="x unified", plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Rythme de progression")
    variation_df = df.dropna(subset=["variation"]).copy()
    if not variation_df.empty:
        fig_var = px.bar(variation_df, x="date", y="variation",
                         labels={"date": "Année", "variation": "Variation en points"},
                         title="Variation annuelle de la part de population utilisant Internet")
        fig_var.update_layout(height=360, plot_bgcolor="white")
        st.plotly_chart(fig_var, use_container_width=True)

        strongest = df.loc[df["variation"].idxmax()]
        weakest = df.loc[df["variation"].idxmin()]
        st.markdown(f"""
        <div class="insight">
            <strong>Lecture des données</strong><br><br>
            • Plus forte progression annuelle autour de <strong>{int(strongest['date'])}</strong>
            (+{strongest['variation']:.1f} point(s)).<br>
            • Variation la plus faible autour de <strong>{int(weakest['date'])}</strong>.<br><br>
            Malgré la progression, moins de 4 personnes sur 10 utilisent Internet.
        </div>
        """, unsafe_allow_html=True)

    df_abo = load_internet_abonnes()
    if df_abo is not None and not df_abo.empty and "indicateur" in df_abo.columns:
        st.markdown("### Technologies et abonnements Internet")
        tech_keywords = ["3G", "4G", "FTTH", "fibre", "haut débit", "GPRS", "EDGE"]
        pattern = "|".join(tech_keywords)
        tech = df_abo[df_abo["indicateur"].astype(str).str.contains(pattern, case=False, na=False)].copy()
        if not tech.empty:
            fig_tech = px.line(tech, x="date", y="value", color="indicateur", markers=True,
                               labels={"date": "Année", "value": "Abonnements", "indicateur": "Technologie"},
                               title="Évolution des abonnements par technologie")
            fig_tech.update_layout(height=440, plot_bgcolor="white")
            st.plotly_chart(fig_tech, use_container_width=True)


# ============================================================
# TÉLÉCOMS
# ============================================================

def render_telecoms():
    st.markdown("## 📡 Télécommunications")
    st.caption("Évolution du marché, abonnements, télédensité, revenus et investissements.")

    df = load_telecoms()
    if df is None or df.empty:
        show_missing_dataset("telecoms_clean.csv", "Indicateurs du marché des télécommunications.")
        return

    if "indicateur" not in df.columns:
        st.error("La colonne `indicateur` est absente du fichier télécoms.")
        return

    # Abonnés totaux
    abonnes = df[df["indicateur"].str.contains("nombre total d'abonnés fixe et mobile", case=False, na=False)].copy()
    if not abonnes.empty:
        fig = px.line(abonnes, x="date", y="value", markers=True,
                      labels={"date": "Année", "value": "Abonnés"},
                      title="Nombre total d'abonnés (fixe + mobile)")
        fig.update_traces(line=dict(color=COLOR_NAVY, width=3))
        fig.update_layout(height=400, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    teledensite = df[df["indicateur"].str.contains("télédensité mobile", case=False, na=False)].copy()
    with col1:
        if not teledensite.empty:
            fig2 = px.line(teledensite, x="date", y="value", markers=True,
                           labels={"date": "Année", "value": "Télédensité (%)"},
                           title="Télédensité mobile GSM (%)")
            fig2.update_layout(height=350, plot_bgcolor="white")
            st.plotly_chart(fig2, use_container_width=True)

    ca = df[df["indicateur"].str.contains("chiffres d'affaires", case=False, na=False)].copy()
    with col2:
        if not ca.empty:
            fig3 = px.bar(ca, x="date", y="value",
                          labels={"date": "Année", "value": "FCFA"},
                          title="Chiffre d'affaires (FCFA)")
            fig3.update_layout(height=350, plot_bgcolor="white")
            st.plotly_chart(fig3, use_container_width=True)

    inv = df[df["indicateur"].str.contains("investissement", case=False, na=False)].copy()
    if not inv.empty:
        fig_inv = px.bar(inv, x="date", y="value",
                         labels={"date": "Année", "value": "FCFA"},
                         title="Investissements (FCFA)")
        fig_inv.update_layout(height=350, plot_bgcolor="white")
        st.plotly_chart(fig_inv, use_container_width=True)

    st.markdown("#### Parts de marché des opérateurs")
    parts = df[df["indicateur"].str.contains("part de marché", case=False, na=False)].copy()
    if not parts.empty:
        fig4 = px.line(parts, x="date", y="value", color="indicateur", markers=True,
                       labels={"date": "Année", "value": "Part de marché (%)", "indicateur": "Opérateur"})
        fig4.update_layout(height=400, plot_bgcolor="white", legend_title_text="")
        st.plotly_chart(fig4, use_container_width=True)

    st.info("Le marché mobile est mature (télédensité élevée). L'enjeu n'est plus l'accès au mobile, mais le passage vers Internet et les services numériques.")


# ============================================================
# FINANCE
# ============================================================

def render_finance():
    st.markdown("## 🏦 Réseaux d'accès financiers")
    st.caption("Comparaison entre établissements physiques et agents Mobile Money")

    indicators = load_indicators()
    etabs = load_etablissements()

    if indicators is None or indicators.empty:
        show_missing_dataset("indicateurs_region.csv", "Indicateurs territoriaux.")
        return

    total_agents = indicators["nb_agents_mm"].sum()
    total_points = indicators["nb_points_financiers"].sum()
    ratio = total_agents / total_points if total_points > 0 else None

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Agents Mobile Money", format_number(total_agents))
    c2.metric("Total Points financiers", format_number(total_points))
    c3.metric("Ratio national Agents / Points", format_decimal(ratio))

    finance_long = indicators.melt(
        id_vars=["region"],
        value_vars=["nb_agents_mm", "nb_points_financiers"],
        var_name="réseau",
        value_name="nombre"
    )
    finance_long["réseau"] = finance_long["réseau"].map({
        "nb_agents_mm": "Agents Mobile Money",
        "nb_points_financiers": "Points financiers"
    })

    fig = px.bar(finance_long, x="region", y="nombre", color="réseau", barmode="group",
                 title="Deux réseaux d'accès aux services financiers",
                 labels={"region": "Région", "nombre": "Nombre de points", "réseau": "Réseau"},
                 color_discrete_sequence=[COLOR_NAVY, COLOR_GOLD])
    fig.update_layout(height=450, plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Pression sur les réseaux")
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.bar(indicators, x="region", y="habitants_par_point_financier",
                      title="Habitants par point financier",
                      labels={"region": "Région", "habitants_par_point_financier": "Habitants / point"})
        fig1.update_layout(height=390, plot_bgcolor="white")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.bar(indicators, x="region", y="habitants_par_agent_mm",
                      title="Habitants par agent Mobile Money",
                      labels={"region": "Région", "habitants_par_agent_mm": "Habitants / agent"})
        fig2.update_layout(height=390, plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Tableau de comparaison")
    display_columns = ["region", "population", "nb_agents_mm", "nb_points_financiers",
                       "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point"]
    available = [c for c in display_columns if c in indicators.columns]
    table = indicators[available].copy()
    table = table.rename(columns={
        "region": "Région", "population": "Population", "nb_agents_mm": "Agents MM",
        "nb_points_financiers": "Points financiers", "habitants_par_agent_mm": "Hab./agent MM",
        "habitants_par_point_financier": "Hab./point financier", "ratio_agents_par_point": "Agents MM / point"
    })
    st.dataframe(table, use_container_width=True, hide_index=True)
    dataframe_download(table, "comparaison_financiere_togo.csv")

    dominant = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
    st.success(
        f"**Mobile Money dominant** — En **{dominant['region']}**, "
        f"**{format_decimal(dominant['ratio_agents_par_point'])}** agents MM pour 1 point financier. "
        f"C’est le territoire où le réseau numérique compense le plus clairement la faiblesse du réseau physique."
    )

    if etabs is not None and not etabs.empty and "categorie" in etabs.columns:
        st.markdown("### Structure des établissements financiers")
        categories = etabs["categorie"].value_counts().reset_index()
        categories.columns = ["Catégorie", "Nombre"]
        fig_cat = px.bar(categories, x="Catégorie", y="Nombre", title="Nombre d'établissements par catégorie")
        fig_cat.update_layout(height=400, plot_bgcolor="white")
        st.plotly_chart(fig_cat, use_container_width=True)


# ============================================================
# TERRITOIRES
# ============================================================

def territory_profile(row):
    st.markdown(f"""
    <div class="territory-profile">
        <div class="territory-title">{row['region']}</div>
        <div class="territory-subtitle">Profil territorial d'accès</div>
        <hr>
        <b>Population :</b> {format_number(row.get('population'))}<br><br>
        <b>Agents Mobile Money :</b> {format_number(row.get('nb_agents_mm'))}<br><br>
        <b>Points financiers :</b> {format_number(row.get('nb_points_financiers'))}<br><br>
        <b>Habitants / agent :</b> {format_number(row.get('habitants_par_agent_mm'))}<br><br>
        <b>Habitants / point financier :</b> {format_number(row.get('habitants_par_point_financier'))}<br><br>
        <b>Agents MM / point financier :</b> {format_decimal(row.get('ratio_agents_par_point'))}
    </div>
    """, unsafe_allow_html=True)

def render_territoires():
    st.markdown("## 🗺️ Intelligence territoriale")
    st.caption("Comparer les profils d'accès des territoires à partir des données disponibles.")

    indicators = load_indicators()
    if indicators is None or indicators.empty:
        show_missing_dataset("indicateurs_region.csv", "Indicateurs territoriaux.")
        return

    regions = sorted(indicators["region"].dropna().unique().tolist())
    selected = st.selectbox("Sélectionner une région", ["Toutes les régions"] + regions)
    current = indicators if selected == "Toutes les régions" else indicators[indicators["region"] == selected].copy()

    population = current["population"].sum()
    agents = current["nb_agents_mm"].sum()
    points = current["nb_points_financiers"].sum()
    ratio = agents / points if points > 0 else None

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Population", format_number(population))
    c2.metric("Agents MM", format_number(agents))
    c3.metric("Points financiers", format_number(points))
    c4.metric("Agents / point", format_decimal(ratio))

    if selected != "Toutes les régions":
        st.markdown("### Profil du territoire")
        row = current.iloc[0]
        p1, p2 = st.columns([1, 2])
        with p1:
            territory_profile(row)
        with p2:
            radar_categories = ["Agents MM", "Points financiers", "Population"]
            values = [row["nb_agents_mm"], row["nb_points_financiers"], row["population"]]
            max_values = [indicators["nb_agents_mm"].max(), indicators["nb_points_financiers"].max(), indicators["population"].max()]
            normalized = [(v / m * 100) if m else 0 for v, m in zip(values, max_values)]
            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(r=normalized + [normalized[0]], theta=radar_categories + [radar_categories[0]], fill="toself", name=selected))
            radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=430, title="Profil relatif du territoire")
            st.plotly_chart(radar, use_container_width=True)

    st.markdown("### Comparer deux territoires")
    compare1, compare2 = st.columns(2)
    with compare1:
        region_a = st.selectbox("Territoire A", regions, key="territory_a")
    with compare2:
        region_b = st.selectbox("Territoire B", regions, index=min(1, len(regions)-1), key="territory_b")

    row_a = indicators[indicators["region"] == region_a]
    row_b = indicators[indicators["region"] == region_b]
    if not row_a.empty and not row_b.empty:
        a, b = row_a.iloc[0], row_b.iloc[0]
        comparison = pd.DataFrame({
            "Indicateur": ["Population", "Agents Mobile Money", "Points financiers",
                           "Habitants / agent", "Habitants / point financier", "Agents MM / point"],
            region_a: [a["population"], a["nb_agents_mm"], a["nb_points_financiers"],
                       a["habitants_par_agent_mm"], a["habitants_par_point_financier"], a["ratio_agents_par_point"]],
            region_b: [b["population"], b["nb_agents_mm"], b["nb_points_financiers"],
                       b["habitants_par_agent_mm"], b["habitants_par_point_financier"], b["ratio_agents_par_point"]],
        })
        st.dataframe(comparison, use_container_width=True, hide_index=True)

    st.markdown("### Vue comparative nationale")
    metric = st.selectbox(
        "Indicateur à comparer",
        ["habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point", "nb_agents_mm", "nb_points_financiers"],
        format_func=lambda x: {
            "habitants_par_agent_mm": "Habitants par agent Mobile Money",
            "habitants_par_point_financier": "Habitants par point financier",
            "ratio_agents_par_point": "Agents Mobile Money / point financier",
            "nb_agents_mm": "Nombre d'agents Mobile Money",
            "nb_points_financiers": "Nombre de points financiers",
        }.get(x, x)
    )
    fig = px.bar(indicators.sort_values(metric, ascending=False), x="region", y=metric,
                 title=f"Comparaison — {metric}", labels={"region": "Région", metric: metric})
    fig.update_layout(height=430, plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Données territoriales")
    st.dataframe(current, use_container_width=True, hide_index=True)
    dataframe_download(current, "donnees_territoriales_filtrees.csv")


# ============================================================
# ACTIONS
# ============================================================

def render_actions():
    st.markdown("## 🎯 De la donnée à l'action")
    st.caption("Recommandations formulées à partir des indicateurs observés.")

    indicators = load_indicators()
    internet = load_internet_penetration()

    if indicators is None or indicators.empty:
        st.warning("Les indicateurs territoriaux sont nécessaires pour cette section.")
        return

    st.markdown("### 01 · Accélérer l'usage d'Internet")
    if internet is not None and not internet.empty:
        latest = internet.iloc[-1]["value"]
        st.markdown(f"""
        <div class="recommendation">
            <b>Observation</b><br>
            La dernière valeur disponible de l'utilisation d'Internet est de <strong>{latest:.1f}%</strong>
            (moins de 4 personnes sur 10).<br><br>
            <b>Enjeu</b><br>
            L'accès mobile et l'usage effectif d'Internet ne sont pas équivalents.<br><br>
            <b>Pistes à tester</b><br>
            • Réduction du coût de la data<br>
            • Points d'accès communautaires (Wi-Fi)<br>
            • Formation aux usages numériques de base<br><br>
            <b>Indicateur de suivi</b><br>
            Évolution de la part de la population utilisant Internet.
        </div>
        """, unsafe_allow_html=True)

    pressure = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]
    st.markdown("### 02 · Renforcer les réseaux dans les territoires sous pression")
    st.markdown(f"""
    <div class="recommendation">
        <b>Observation</b><br>
        La région avec la plus forte pression sur le réseau physique est
        <strong>{pressure['region']}</strong>
        ({format_number(pressure['habitants_par_point_financier'])} habitants par point financier).<br><br>
        <b>Piste d'action</b><br>
        Examiner les préfectures les moins desservies pour identifier où ouvrir
        ou renforcer des points de microfinance / agences légères.<br><br>
        <b>Indicateur de suivi</b><br>
        Habitants par point financier.
    </div>
    """, unsafe_allow_html=True)

    mm_dominant = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
    st.markdown("### 03 · Optimiser le rôle du Mobile Money comme relais")
    st.markdown(f"""
    <div class="recommendation">
        <b>Observation</b><br>
        La région où le Mobile Money est le plus dominant (ratio agents/points le plus élevé) est
        <strong>{mm_dominant['region']}</strong>
        (ratio {format_decimal(mm_dominant['ratio_agents_par_point'])}).<br><br>
        <b>Pistes d'action</b><br>
        • Professionnaliser et densifier le réseau d'agents dans les zones éloignées<br>
        • Développer des produits d'épargne et de crédit via Mobile Money<br>
        • Vérifier l'activité réelle des agents<br><br>
        <b>Indicateur de suivi</b><br>
        Nombre d'agents actifs + volume de transactions MM.
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "**Important :** ces recommandations sont des pistes fondées sur les données disponibles. "
        "La présence d'un point ou d'un agent ne mesure pas automatiquement son activité, "
        "sa qualité de service ou son impact économique."
    )


# ============================================================
# MÉTHODE
# ============================================================

def render_method():
    st.markdown("## 📚 Méthodologie & qualité des données")

    st.markdown("""
    <div class="card">
        <div class="card-title">Pourquoi cette page est importante ?</div>
        <div class="card-text">
            Un dashboard professionnel ne présente pas seulement des graphiques.
            Il doit permettre de comprendre d'où viennent les chiffres, comment ils sont calculés
            et quelles sont leurs limites.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Sources intégrées")
    sources = pd.DataFrame({
        "Jeu de données": ["Population", "Agents Mobile Money", "Établissements financiers",
                           "Télécommunications", "Abonnés Internet", "Utilisation d'Internet"],
        "Rôle": ["Population des territoires", "Réseau d'agents", "Réseau financier physique",
                 "Marché télécom", "Technologies Internet", "Adoption d'Internet"]
    })
    st.dataframe(sources, use_container_width=True, hide_index=True)

    st.markdown("### Indicateurs calculés")
    formulas = pd.DataFrame({
        "Indicateur": ["Habitants / agent MM", "Habitants / point financier", "Agents MM / point financier"],
        "Formule": ["Population ÷ agents MM", "Population ÷ points financiers", "Agents MM ÷ points financiers"],
        "Interprétation": ["Densité relative du réseau d'agents", "Pression sur le réseau physique", "Rapport entre les deux réseaux"]
    })
    st.dataframe(formulas, use_container_width=True, hide_index=True)

    st.markdown("### Limites")
    for limit in [
        "Les périodes de référence peuvent varier selon les sources.",
        "Un agent Mobile Money n'est pas équivalent à une agence bancaire.",
        "La présence géographique ne mesure pas l'activité réelle.",
        "Les ratios ne constituent pas un score global d'inclusion.",
        "Une corrélation ne prouve pas une causalité.",
        "Les recommandations doivent être complétées par des données locales.",
    ]:
        st.markdown(f"- {limit}")

    st.markdown("### Contrôle des fichiers")
    expected = ["indicateurs_region.csv", "internet_penetration_clean.csv", "internet_abonnes_clean.csv",
                "telecoms_clean.csv", "etablissements_financiers_clean.csv"]
    status = [{"Fichier": f, "Statut": "✅ Disponible" if (PROCESSED_DIR / f).exists() else "❌ Manquant"} for f in expected]
    st.dataframe(pd.DataFrame(status), use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="observation">
        <strong>Règle de qualité</strong><br><br>
        Aucun chiffre ne doit être inventé. Lorsqu'une donnée n'est pas disponible,
        le dashboard l'indique clairement.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FOOTER + MAIN
# ============================================================

def render_footer():
    st.markdown("""
    <div class="footer">
        Togo Digital & Financial Inclusion · Dashboard analytique territorial ·
        Python · Streamlit · Pandas · Plotly
    </div>
    """, unsafe_allow_html=True)

def main():
    render_header()
    selected = render_navigation()
    st.markdown("---")

    if selected == "🏠 INTRO":
        render_intro()
    elif selected == "🌐 INTERNET":
        render_internet()
    elif selected == "📡 TÉLÉCOMS":
        render_telecoms()
    elif selected == "🏦 FINANCE":
        render_finance()
    elif selected == "🗺️ TERRITOIRES":
        render_territoires()
    elif selected == "🎯 ACTIONS":
        render_actions()
    elif selected == "📚 MÉTHODE":
        render_method()

    render_footer()

if __name__ == "__main__":
    main()