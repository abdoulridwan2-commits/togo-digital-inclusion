"""
Togo Digital & Financial Inclusion
Point d'entrée principal de l'application Streamlit
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Configuration de la page
st.set_page_config(
    page_title="Togo Digital & Financial Inclusion",
    page_icon="🇹🇬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Chemins
PROCESSED_DIR = Path("data/processed")


@st.cache_data
def load_indicators():
    """Charge les indicateurs régionaux."""
    path = PROCESSED_DIR / "indicateurs_region.csv"
    if path.exists():
        return pd.read_csv(path)
    return None


def render_intro():
    """Page INTRO — porte d'entrée du dashboard."""
    
    # Hero
    st.title("🇹🇬 Togo Digital & Financial Inclusion")
    st.subheader(
        "Mesurer l'accès au numérique. Comprendre le rôle du Mobile Money. "
        "Identifier les territoires sous-desservis."
    )
    
    st.markdown("---")
    
    # KPI de contexte
    indicators = load_indicators()
    
    if indicators is not None:
        total_pop = indicators["population"].sum()
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Population (2022)", f"{total_pop:,.0f}".replace(",", " "))
        with col2:
            st.metric("Agents Mobile Money", f"{total_agents:,.0f}".replace(",", " "))
        with col3:
            st.metric("Points financiers", f"{total_points:,.0f}".replace(",", " "))
        with col4:
            ratio = round(total_agents / total_points, 1) if total_points > 0 else 0
            st.metric("Ratio Agents / Points", f"{ratio}")
    
    st.markdown("---")
    
    # Question centrale
    st.markdown("### Question centrale")
    st.info(
        """
        **Là où les services financiers physiques sont peu présents,  
        dans quelle mesure le réseau Mobile Money constitue-t-il un relais  
        d'accès aux services financiers numériques ?**
        """
    )
    
    st.markdown("")
    
    # Bouton Explorer (pour l'instant juste informatif)
    st.success("Utilisez la navigation en bas pour explorer les différentes sections du dashboard.")
    
    # Aperçu rapide des régions
    if indicators is not None:
        st.markdown("### Aperçu des territoires")
        st.dataframe(
            indicators.style.format({
                "population": "{:,.0f}",
                "nb_agents_mm": "{:,.0f}",
                "nb_points_financiers": "{:,.0f}",
                "habitants_par_agent_mm": "{:,.0f}",
                "habitants_par_point_financier": "{:,.0f}",
                "ratio_agents_par_point": "{:.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )


def main():
    # Navigation simple (on améliorera plus tard)
    pages = ["INTRO", "INTERNET", "TÉLÉCOMS", "FINANCE", "TERRITOIRES", "ACTIONS", "À PROPOS"]
    
    # Menu horizontal basique
    selected = st.radio(
        "Navigation",
        pages,
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if selected == "INTRO":
        render_intro()
    else:
        st.title(selected)
        st.info(f"La page **{selected}** sera développée prochainement.")


if __name__ == "__main__":
    main()