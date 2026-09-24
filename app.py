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

# Style CSS personnalisé
st.markdown("""
<style>
    /* Masquer le menu Streamlit par défaut */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Header */
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
    
    /* Navigation */
    .stRadio > div {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .stRadio label {
        background-color: #f0f4f8;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    /* KPI cards */
    div[data-testid="stMetric"] {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    
    /* Question centrale */
    .question-box {
        background-color: #E8F4FC;
        border-left: 5px solid #0B3D5C;
        padding: 1.2rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1.5rem 0;
        font-size: 1.05rem;
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
        df = df.dropna(subset=["value"]).sort_values("date")
        return df
    return None


@st.cache_data
def load_internet_abonnes():
    path = PROCESSED_DIR / "internet_abonnes_clean.csv"
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

    # Question centrale
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
        st.dataframe(
            indicators,
            use_container_width=True,
            hide_index=True
        )


def render_internet():
    st.markdown("### Adoption d'Internet au Togo")
    st.caption("Évolution de l'usage d'Internet dans la population (1996–2022)")

    df_pen = load_internet_penetration()
    
    if df_pen is not None and len(df_pen) > 0:
        fig = px.line(
            df_pen,
            x="date",
            y="value",
            markers=True,
            labels={"date": "Année", "value": "% de la population"},
        )
        fig.update_layout(
            title="Part de la population utilisant Internet",
            xaxis_title="Année",
            yaxis_title="% de la population",
            hovermode="x unified",
            height=420
        )
        fig.update_traces(line_color="#0B3D5C")
        st.plotly_chart(fig, use_container_width=True)

        latest = df_pen.iloc[-1]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dernière valeur", f"{latest['value']:.1f}%", help=f"Année {int(latest['date'])}")
        with col2:
            max_val = df_pen["value"].max()
            st.metric("Maximum atteint", f"{max_val:.1f}%")
        with col3:
            first_nonzero = df_pen[df_pen["value"] > 0].iloc[0]
            st.metric("Première valeur", f"{first_nonzero['value']:.2f}%", help=f"Année {int(first_nonzero['date'])}")

        st.info(
            f"En **{int(latest['date'])}**, environ **{latest['value']:.1f}%** de la population togolaise "
            f"utilisait Internet. La progression s'accélère nettement à partir des années 2010."
        )
    else:
        st.warning("Données de pénétration Internet non disponibles.")

    # Abonnés
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
            fig2 = px.line(
                df_filtre,
                x="date",
                y="value",
                color="indicateur",
                markers=True,
                labels={"date": "Année", "value": "Valeur", "indicateur": "Indicateur"}
            )
            fig2.update_layout(height=420, legend_title_text="")
            st.plotly_chart(fig2, use_container_width=True)


def render_placeholder(title: str):
    st.markdown(f"### {title}")
    st.info(f"La page **{title}** sera développée prochainement.")


# =========================================================
# MAIN
# =========================================================
def main():
    render_header()

    pages = ["INTRO", "INTERNET", "TÉLÉCOMS", "FINANCE", "TERRITOIRES", "ACTIONS", "À PROPOS"]
    
    selected = st.radio(
        "Navigation",
        pages,
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    if selected == "INTRO":
        render_intro()
    elif selected == "INTERNET":
        render_internet()
    elif selected == "TÉLÉCOMS":
        render_placeholder("Télécoms")
    elif selected == "FINANCE":
        render_placeholder("Finance")
    elif selected == "TERRITOIRES":
        render_placeholder("Territoires")
    elif selected == "ACTIONS":
        render_placeholder("Actions")
    elif selected == "À PROPOS":
        render_placeholder("À propos")


if __name__ == "__main__":
    main()