"""
Page ACTIONS
"""

import streamlit as st

from app.data.loader import load_indicateurs, load_internet_penetration
from app.components.kpi import format_number, format_decimal


def render():
    st.markdown("## 🎯 Actions")
    st.caption("Observations → Enjeux → Pistes d'action fondées sur les données disponibles.")

    indicators = load_indicateurs()
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
            La dernière valeur disponible de l'utilisation d'Internet est de
            <strong>{latest:.1f}%</strong> (moins de 4 personnes sur 10).<br><br>
            <b>Enjeu</b><br>
            L'accès mobile et l'usage effectif d'Internet ne sont pas équivalents.<br><br>
            <b>Piste d'action</b><br>
            • Réduction du coût de la data<br>
            • Points d'accès communautaires (Wi-Fi)<br>
            • Formation aux usages numériques de base<br><br>
            <b>Indicateur de suivi</b><br>
            Évolution de la part de la population utilisant Internet.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 02 · Renforcer les réseaux dans les territoires sous pression")

    pressure = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]
    st.markdown(f"""
    <div class="recommendation">
        <b>Observation</b><br>
        La région présentant la plus forte valeur d'habitants par point financier est
        <strong>{pressure['region']}</strong>
        ({format_number(pressure['habitants_par_point_financier'])} habitants par point).<br><br>
        <b>Enjeu</b><br>
        Accessibilité relative des services financiers physiques.<br><br>
        <b>Piste d'action</b><br>
        Examiner les préfectures et communes concernées afin d'identifier
        les territoires où l'ouverture ou le renforcement de points de service
        pourrait améliorer la couverture.<br><br>
        <b>Indicateur de suivi</b><br>
        Habitants par point financier.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 03 · Optimiser le rôle du Mobile Money comme relais")

    mm_dominant = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
    st.markdown(f"""
    <div class="recommendation">
        <b>Observation</b><br>
        La région où le ratio Agents Mobile Money / points financiers est le plus élevé est
        <strong>{mm_dominant['region']}</strong>
        (ratio {format_decimal(mm_dominant['ratio_agents_par_point'])}).<br><br>
        <b>Enjeu</b><br>
        Le Mobile Money apparaît comme un relais potentiel d'accès dans ce territoire.<br><br>
        <b>Piste d'action</b><br>
        • Professionnaliser et densifier le réseau d'agents dans les zones éloignées<br>
        • Développer des produits d'épargne et de crédit via Mobile Money<br>
        • Vérifier l'activité réelle des agents<br><br>
        <b>Indicateur de suivi</b><br>
        Nombre d'agents actifs + volume de transactions Mobile Money.
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "Ces recommandations sont des pistes fondées sur les données disponibles. "
        "La présence d'un point ou d'un agent ne mesure pas automatiquement son activité. "
        "Aucune causalité n'est affirmée."
    )