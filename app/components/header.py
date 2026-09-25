"""
Header du dashboard
"""

import streamlit as st
from app.config.theme import get_css


def render_header():
    st.markdown(get_css(), unsafe_allow_html=True)

    st.markdown("""
    <div class="main-header">
        <h1>🇹🇬 Togo Digital & Financial Inclusion</h1>
        <p>Mesurer l'accès au numérique · analyser les réseaux d'accès · comprendre le rôle du Mobile Money · explorer les territoires</p>
        <div class="header-badge">DATA PRODUCT · TOGO · 2026</div>
    </div>
    """, unsafe_allow_html=True)