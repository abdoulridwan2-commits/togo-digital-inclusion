"""
Point d'entrée principal du dashboard
Togo Digital & Financial Inclusion
"""

import sys
from pathlib import Path

# Fix du chemin Python (obligatoire pour Streamlit)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from app.components.header import render_header
from app.components.navigation import render_navigation

from app.pages import (
    accueil,
    nationale,
    internet,
    telecoms,
    finance,
    population,
    territoires,
    simulateur,
    actions,
    methode,
)


st.set_page_config(
    page_title="Togo Digital & Financial Inclusion",
    page_icon="🇹🇬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main():
    render_header()
    selected = render_navigation()
    st.markdown("---")

    if selected == "🏠 ACCUEIL":
        accueil.render()
    elif selected == "📊 VUE NATIONALE":
        nationale.render()
    elif selected == "🌐 INTERNET":
        internet.render()
    elif selected == "📡 TÉLÉCOMS":
        telecoms.render()
    elif selected == "🏦 FINANCE":
        finance.render()
    elif selected == "👥 POPULATION":
        population.render()
    elif selected == "🗺️ TERRITOIRES":
        territoires.render()
    elif selected == "🧮 SIMULATEUR":
        simulateur.render()
    elif selected == "🎯 ACTIONS":
        actions.render()
    elif selected == "📚 MÉTHODE":
        methode.render()


if __name__ == "__main__":
    main()