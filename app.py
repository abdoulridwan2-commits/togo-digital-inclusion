"""
Togo Digital & Financial Inclusion
Point d'entrée principal de l'application Streamlit
"""

import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Togo Digital & Financial Inclusion",
    page_icon="🇹🇬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    st.title("🇹🇬 Togo Digital & Financial Inclusion")
    st.subheader(
        "Mesurer l'accès au numérique. Comprendre le rôle du Mobile Money. "
        "Identifier les territoires sous-desservis."
    )

    st.info("""
    **Environnement de travail créé avec succès.**

    Prochaines étapes :
    1. Nettoyage et harmonisation des données (`analysis/cleaning.py`)
    2. Calcul des indicateurs (`analysis/indicators.py`)
    3. Construction des pages du dashboard
    """)

    st.markdown("---")
    st.markdown("### Structure des données sources")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Population 2022", "Disponible")
        st.metric("Agents Mobile Money", "Disponible")
    with col2:
        st.metric("Établissements financiers", "Disponible")
        st.metric("Télécoms (2013-2019)", "Disponible")
    with col3:
        st.metric("Internet abonnés", "Disponible")
        st.metric("Pénétration Internet", "Disponible")

if __name__ == "__main__":
    main()