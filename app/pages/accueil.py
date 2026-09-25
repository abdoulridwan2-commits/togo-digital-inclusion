"""
Page ACCUEIL
"""

import streamlit as st
from app.data.loader import load_indicateurs, load_internet_penetration
from app.components.kpi import render_kpi_row, format_number, format_decimal


def render():
    st.markdown("## Vue d'ensemble")

    indicators = load_indicateurs()
    internet = load_internet_penetration()

    # KPI principaux
    if indicators is not None and not indicators.empty:
        total_pop = indicators["population"].sum()
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        ratio = total_agents / total_points if total_points > 0 else None

        render_kpi_row([
            ("Population (2022)", total_pop),
            ("Agents Mobile Money", total_agents),
            ("Points financiers", total_points),
            ("Ratio Agents / Points", ratio),
        ])

    # Question centrale
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

    # 3 chiffres clés
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

    # Insight
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

    # Parcours
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