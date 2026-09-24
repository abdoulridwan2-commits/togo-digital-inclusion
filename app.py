"""
Togo Digital & Financial Inclusion
Dashboard professionnel — Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Togo Digital & Financial Inclusion",
    page_icon="🇹🇬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main-header {
        background-color: #0B3D5C;
        padding: 1.2rem 2rem;
        border-radius: 0 0 8px 8px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 {
        color: white !important;
        font-size: 1.6rem !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .main-header p {
        color: #B8D4E8 !important;
        font-size: 0.95rem !important;
        margin: 0.3rem 0 0 0 !important;
    }
    
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    .question-box {
        background-color: #E8F4FC;
        border-left: 5px solid #0B3D5C;
        padding: 1.2rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1.5rem 0;
        font-size: 1.05rem;
    }
    
    .reco-box {
        background-color: #f0fdf4;
        border-left: 5px solid #16a34a;
        padding: 1rem 1.3rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

PROCESSED_DIR = Path("data/processed")


# =========================================================
# CHARGEMENT DES DONNÉES
# =========================================================
@st.cache_data
def load_indicators():
    path = PROCESSED_DIR / "indicateurs_region.csv"
    if path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_internet_penetration():
    path = PROCESSED_DIR / "internet_penetration_clean.csv"
    if path.exists():
        df = pd.read_csv(path)
        return df.dropna(subset=["value"]).sort_values("date")
    return None

@st.cache_data
def load_internet_abonnes():
    path = PROCESSED_DIR / "internet_abonnes_clean.csv"
    if path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_telecoms():
    path = PROCESSED_DIR / "telecoms_clean.csv"
    if path.exists():
        return pd.read_csv(path)
    return None

@st.cache_data
def load_etablissements():
    path = PROCESSED_DIR / "etablissements_financiers_clean.csv"
    if path.exists():
        return pd.read_csv(path)
    return None


# =========================================================
# HEADER
# =========================================================
def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🇹🇬 Togo Digital & Financial Inclusion</h1>
        <p>Mesurer l'accès au numérique · Comprendre le rôle du Mobile Money · Identifier les territoires sous-desservis</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PAGES
# =========================================================
def render_intro():
    st.markdown("### Vue d'ensemble")
    
    indicators = load_indicators()
    if indicators is not None:
        total_pop = indicators["population"].sum()
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        ratio = round(total_agents / total_points, 1) if total_points > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Population (2022)", f"{total_pop:,.0f}".replace(",", " "))
        with col2:
            st.metric("Agents Mobile Money", f"{total_agents:,.0f}".replace(",", " "))
        with col3:
            st.metric("Points financiers", f"{total_points:,.0f}".replace(",", " "))
        with col4:
            st.metric("Ratio Agents / Points", f"{ratio}")

    st.markdown("""
    <div class="question-box">
        <strong>Question centrale</strong><br><br>
        Là où les services financiers physiques sont peu présents,<br>
        dans quelle mesure le réseau Mobile Money constitue-t-il un relais<br>
        d'accès aux services financiers numériques ?
    </div>
    """, unsafe_allow_html=True)

    if indicators is not None:
        st.markdown("#### Aperçu des territoires")
        st.dataframe(indicators, use_container_width=True, hide_index=True)


def render_internet():
    st.markdown("### Adoption d'Internet au Togo")
    st.caption("Évolution de l'usage d'Internet dans la population (1996–2022)")

    df_pen = load_internet_penetration()
    if df_pen is not None and len(df_pen) > 0:
        fig = px.line(df_pen, x="date", y="value", markers=True,
                      labels={"date": "Année", "value": "% de la population"})
        fig.update_layout(title="Part de la population utilisant Internet", height=420,
                          xaxis_title="Année", yaxis_title="% de la population", hovermode="x unified")
        fig.update_traces(line_color="#0B3D5C")
        st.plotly_chart(fig, use_container_width=True)

        latest = df_pen.iloc[-1]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dernière valeur", f"{latest['value']:.1f}%", help=f"Année {int(latest['date'])}")
        with col2:
            st.metric("Maximum atteint", f"{df_pen['value'].max():.1f}%")
        with col3:
            first = df_pen[df_pen["value"] > 0].iloc[0]
            st.metric("Première valeur", f"{first['value']:.2f}%", help=f"Année {int(first['date'])}")

        st.info(f"En **{int(latest['date'])}**, environ **{latest['value']:.1f}%** de la population togolaise utilisait Internet.")

    df_abo = load_internet_abonnes()
    if df_abo is not None:
        st.markdown("#### Abonnés Internet (données ARCEP)")
        indicateurs_cles = [
            "T abonnés Internet Fixe et Mobile (Toutes technologies)",
            "T abonnés Internet haut débit Fixe et Mobile",
            "Taux de pénétration Internet (Toutes technologies) (%)",
            "Taux de pénétration Internet haut débit (%)"
        ]
        df_filtre = df_abo[df_abo["indicateur"].isin(indicateurs_cles)].copy()
        if len(df_filtre) > 0:
            fig2 = px.line(df_filtre, x="date", y="value", color="indicateur", markers=True,
                           labels={"date": "Année", "value": "Valeur", "indicateur": "Indicateur"})
            fig2.update_layout(height=420, legend_title_text="")
            st.plotly_chart(fig2, use_container_width=True)


def render_telecoms():
    st.markdown("### Marché des télécommunications")
    st.caption("Abonnés, télédensité, chiffre d'affaires et parts de marché")

    df = load_telecoms()
    if df is None:
        st.warning("Données télécoms non disponibles.")
        return

    abonnes = df[df["indicateur"].str.contains("nombre total d'abonnés fixe et mobile", case=False, na=False)].copy()
    if len(abonnes) > 0:
        fig = px.line(abonnes, x="date", y="value", markers=True, labels={"date": "Année", "value": "Abonnés"})
        fig.update_layout(title="Nombre total d'abonnés (fixe + mobile)", height=400)
        fig.update_traces(line_color="#0B3D5C")
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    teledensite = df[df["indicateur"].str.contains("télédensité mobile", case=False, na=False)].copy()
    with col1:
        if len(teledensite) > 0:
            fig2 = px.line(teledensite, x="date", y="value", markers=True,
                           labels={"date": "Année", "value": "Télédensité (%)"})
            fig2.update_layout(title="Télédensité mobile GSM (%)", height=350)
            st.plotly_chart(fig2, use_container_width=True)

    ca = df[df["indicateur"].str.contains("chiffres d'affaires", case=False, na=False)].copy()
    with col2:
        if len(ca) > 0:
            fig3 = px.bar(ca, x="date", y="value", labels={"date": "Année", "value": "FCFA"})
            fig3.update_layout(title="Chiffre d'affaires (FCFA)", height=350)
            st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Parts de marché (en abonnés)")
    parts = df[df["indicateur"].str.contains("part de marché", case=False, na=False)].copy()
    if len(parts) > 0:
        fig4 = px.line(parts, x="date", y="value", color="indicateur", markers=True,
                       labels={"date": "Année", "value": "Part de marché (%)", "indicateur": "Opérateur"})
        fig4.update_layout(height=400, legend_title_text="")
        st.plotly_chart(fig4, use_container_width=True)


def render_finance():
    st.markdown("### Réseaux d'accès financiers")
    st.caption("Comparaison entre établissements physiques et agents Mobile Money")

    indicators = load_indicators()
    if indicators is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Agents Mobile Money", f"{indicators['nb_agents_mm'].sum():,.0f}".replace(",", " "))
        with col2:
            st.metric("Total Points financiers", f"{indicators['nb_points_financiers'].sum():,.0f}".replace(",", " "))
        with col3:
            ratio = round(indicators['nb_agents_mm'].sum() / indicators['nb_points_financiers'].sum(), 1)
            st.metric("Ratio national Agents / Points", f"{ratio}")

        st.markdown("#### Répartition par région")
        fig = px.bar(indicators, x="region", y=["nb_agents_mm", "nb_points_financiers"], barmode="group",
                     labels={"value": "Nombre", "region": "Région", "variable": "Type"},
                     title="Agents Mobile Money vs Points financiers par région")
        fig.update_layout(height=420, legend_title_text="")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Indicateurs de densité")
        st.dataframe(
            indicators[["region", "population", "nb_agents_mm", "nb_points_financiers",
                        "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point"]],
            use_container_width=True, hide_index=True
        )

        st.info(
            "La région **Savanes** présente le ratio le plus élevé d'agents Mobile Money "
            "par point financier, ce qui suggère un rôle de relais plus important du Mobile Money "
            "dans les territoires où les services physiques sont moins présents."
        )

    etabs = load_etablissements()
    if etabs is not None and "categorie" in etabs.columns:
        st.markdown("#### Répartition des établissements par catégorie")
        cat_counts = etabs["categorie"].value_counts().reset_index()
        cat_counts.columns = ["Catégorie", "Nombre"]
        fig2 = px.pie(cat_counts, names="Catégorie", values="Nombre",
                      title="Répartition des établissements financiers")
        st.plotly_chart(fig2, use_container_width=True)


def render_territoires():
    st.markdown("### Analyse territoriale")
    st.caption("Densité d'accès et fracture territoriale")

    indicators = load_indicators()
    if indicators is None:
        st.warning("Indicateurs non disponibles.")
        return

    # Filtres
    regions = indicators["region"].tolist()
    selected_region = st.selectbox("Filtrer par région", ["Toutes"] + regions)

    df = indicators.copy()
    if selected_region != "Toutes":
        df = df[df["region"] == selected_region]

    # KPI
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Population", f"{df['population'].sum():,.0f}".replace(",", " "))
    with col2:
        st.metric("Agents MM", f"{df['nb_agents_mm'].sum():,.0f}".replace(",", " "))
    with col3:
        st.metric("Points financiers", f"{df['nb_points_financiers'].sum():,.0f}".replace(",", " "))
    with col4:
        if df["nb_points_financiers"].sum() > 0:
            ratio = round(df["nb_agents_mm"].sum() / df["nb_points_financiers"].sum(), 1)
            st.metric("Ratio Agents/Points", f"{ratio}")

    st.markdown("---")

    # Graphiques de densité
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(indicators, x="region", y="habitants_par_point_financier",
                      title="Habitants par point financier",
                      labels={"habitants_par_point_financier": "Habitants / point", "region": "Région"},
                      color="habitants_par_point_financier", color_continuous_scale="Blues")
        fig1.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(indicators, x="region", y="habitants_par_agent_mm",
                      title="Habitants par agent Mobile Money",
                      labels={"habitants_par_agent_mm": "Habitants / agent", "region": "Région"},
                      color="habitants_par_agent_mm", color_continuous_scale="Greens")
        fig2.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Ratio
    fig3 = px.bar(indicators, x="region", y="ratio_agents_par_point",
                  title="Ratio Agents Mobile Money / Points financiers",
                  labels={"ratio_agents_par_point": "Ratio", "region": "Région"},
                  color="ratio_agents_par_point", color_continuous_scale="Oranges")
    fig3.update_layout(height=380, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("#### Tableau détaillé")
    st.dataframe(indicators, use_container_width=True, hide_index=True)

    # Lecture
    max_ratio = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
    max_pression = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]
    
    st.info(
        f"**Lecture** : La région **{max_ratio['region']}** a le ratio Agents/Points le plus élevé "
        f"({max_ratio['ratio_agents_par_point']}). "
        f"La région **{max_pression['region']}** subit la plus forte pression sur le réseau physique "
        f"({max_pression['habitants_par_point_financier']:,.0f} habitants par point financier)."
    )


def render_actions():
    st.markdown("### De la donnée à l'action")
    st.caption("Recommandations ciblées basées sur les observations")

    indicators = load_indicators()
    if indicators is None:
        st.warning("Indicateurs non disponibles.")
        return

    # Identifier les territoires prioritaires
    savanes = indicators[indicators["region"] == "Savanes"].iloc[0]
    plateaux = indicators[indicators["region"] == "Plateaux"].iloc[0]
    maritime = indicators[indicators["region"] == "Maritime"].iloc[0]

    st.markdown("#### Recommandations")

    # Recommandation 1
    st.markdown(f"""
    <div class="reco-box">
        <strong>Observation</strong> : La région Savanes compte seulement {int(savanes['nb_points_financiers'])} points financiers 
        pour {savanes['population']:,.0f} habitants ({int(savanes['habitants_par_point_financier'])} hab/point), 
        mais dispose de {int(savanes['nb_agents_mm'])} agents Mobile Money (ratio {savanes['ratio_agents_par_point']}).<br><br>
        <strong>Enjeu</strong> : Fort potentiel de relais du Mobile Money là où le réseau physique est faible.<br><br>
        <strong>Territoires concernés</strong> : Savanes<br><br>
        <strong>Action possible</strong> : Renforcer la formation et le maillage des agents Mobile Money dans les zones 
        les plus éloignées des points physiques.<br><br>
        <strong>Indicateur de suivi</strong> : Évolution du ratio Agents MM / Points financiers et du nombre d'agents actifs.
    </div>
    """, unsafe_allow_html=True)

    # Recommandation 2
    st.markdown(f"""
    <div class="reco-box">
        <strong>Observation</strong> : La région Plateaux a {int(plateaux['habitants_par_point_financier'])} habitants 
        par point financier, l'un des ratios les plus élevés, avec un réseau d'agents encore perfectible.<br><br>
        <strong>Enjeu</strong> : Pression importante sur le réseau physique existant.<br><br>
        <strong>Territoires concernés</strong> : Plateaux<br><br>
        <strong>Action possible</strong> : Encourager l'ouverture de points de microfinance ou d'agences légères 
        dans les préfectures les moins desservies.<br><br>
        <strong>Indicateur de suivi</strong> : Nombre de nouveaux points financiers ouverts par an.
    </div>
    """, unsafe_allow_html=True)

    # Recommandation 3
    st.markdown(f"""
    <div class="reco-box">
        <strong>Observation</strong> : La région Maritime concentre {int(maritime['nb_points_financiers'])} points financiers 
        et {int(maritime['nb_agents_mm'])} agents, avec la meilleure densité d'accès ({int(maritime['habitants_par_point_financier'])} hab/point).<br><br>
        <strong>Enjeu</strong> : Capitaliser sur cette densité pour expérimenter des services innovants.<br><br>
        <strong>Territoires concernés</strong> : Maritime<br><br>
        <strong>Action possible</strong> : Tester des services financiers numériques avancés (crédit digital, épargne) 
        en s'appuyant sur le dense réseau d'agents existant.<br><br>
        <strong>Indicateur de suivi</strong> : Taux d'adoption de nouveaux services digitaux.
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "**Limite importante** : Ces recommandations sont des pistes fondées sur la présence recensée des points d'accès. "
        "Elles ne mesurent pas le niveau d'activité réel des agents ni l'impact causal des interventions."
    )


def render_apropos():
    st.markdown("### À propos du projet")
    
    st.markdown("""
    #### Objectif
    Transformer six sources de données ouvertes en une expérience analytique claire, interactive et reproductible 
    permettant de mesurer l'adoption du numérique et de comprendre le rôle du Mobile Money dans l'inclusion financière au Togo.
    
    #### Question centrale
    > *Là où les services financiers physiques sont peu présents, dans quelle mesure le réseau Mobile Money 
    constitue-t-il un relais d'accès aux services financiers numériques ?*
    
    #### Sources de données
    | Source | Contenu |
    |--------|---------|
    | Population 2022 | Découpage administratif |
    | Agents Mobile Money | Points géolocalisés |
    | Établissements financiers | Banques, microfinance, assurances, mutuelles |
    | Télécoms (ARCEP) | Abonnés, télédensité, CA, investissements |
    | Internet abonnés (ARCEP) | Abonnés par technologie |
    | Pénétration Internet | % population (série longue) |
    
    #### Méthodologie
    - Conservation des sources originales dans `data/raw/`
    - Nettoyage et harmonisation dans `data/processed/`
    - Calcul d'indicateurs transparents (pas de score composite arbitraire)
    - Ratios : Habitants/point, Habitants/agent, Agents/point
    
    #### Limites
    - Les données couvrent des périodes différentes
    - Un agent Mobile Money n'est pas équivalent à une agence bancaire
    - La présence géographique ne prouve pas le niveau d'activité
    - Les conclusions portent sur l'**accessibilité recensée**, pas sur l'impact causal
    
    #### Règle d'or
    > Aucune donnée inventée, aucun chiffre reconstruit sans méthode, aucune causalité affirmée sans preuve.
    
    #### Stack technique
    Python · Streamlit · Pandas · Plotly
    """)


# =========================================================
# MAIN
# =========================================================
def main():
    render_header()

    pages = ["INTRO", "INTERNET", "TÉLÉCOMS", "FINANCE", "TERRITOIRES", "ACTIONS", "À PROPOS"]
    
    selected = st.radio("Navigation", pages, horizontal=True, label_visibility="collapsed")
    st.markdown("---")

    if selected == "INTRO":
        render_intro()
    elif selected == "INTERNET":
        render_internet()
    elif selected == "TÉLÉCOMS":
        render_telecoms()
    elif selected == "FINANCE":
        render_finance()
    elif selected == "TERRITOIRES":
        render_territoires()
    elif selected == "ACTIONS":
        render_actions()
    elif selected == "À PROPOS":
        render_apropos()


if __name__ == "__main__":
    main()