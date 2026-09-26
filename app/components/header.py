"""
Header du dashboard avec identité visuelle togolaise
"""

import streamlit as st
from app.config.theme import get_css


def render_header():
    st.markdown(get_css(), unsafe_allow_html=True)
    st.markdown('<div class="togo-bar"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="main-header">
        <h1>🇹🇬 Togo Digital & Financial Inclusion</h1>
        <p>Observatoire territorial de l'accès au numérique et de l'inclusion financière · Analyse spatiale du Mobile Money et des réseaux bancaires · Recensement RGPH-5 & Séries ARCEP</p>
        <div class="header-badge">PLATEFORME DÉCISIONNELLE · TOGO 2026</div>
    </div>
    """, unsafe_allow_html=True)