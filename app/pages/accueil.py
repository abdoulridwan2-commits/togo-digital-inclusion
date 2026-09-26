"""
Page ACCUEIL — Observatoire National de l'Inclusion Numérique & Financière au Togo
"""

import streamlit as st
import plotly.express as px
from app.data.loader import load_indicateurs, load_internet_penetration
from app.components.kpi import render_kpi_row, format_number, format_decimal, render_custom_card
from app.config.theme import COLORS


def render():
    st.markdown("## 🇹🇬 Vue d'ensemble stratégique")
    st.caption("Plateforme d'aide à la décision basée sur le RGPH-5 (INSEED 2022) et les données ARCEP.")

    # Choix du découpage analytique
    col_choice, col_info = st.columns([2, 4])
    with col_choice:
        mode = st.radio(
            "Granularité d'analyse territoriale",
            ["6 Pôles (Grand Lomé & Maritime séparés)", "5 Régions officielles (Maritime unifiée)"],
            index=0,
            horizontal=False,
            key="accueil_mode"
        )
    with col_info:
        if "6 Pôles" in mode:
            st.info("💡 **Focus Grand Lomé actif** : Le District Autonome de Lomé (2,19M hab.) est isolé de la Région Maritime rurale/périurbaine (1,35M hab.) pour révéler la véritable fracture urbain/rural.")
        else:
            st.info("💡 **Vue officielle unifiée** : Maritime regroupe Lomé et les préfectures du sud (3,53M hab., soit 43,7% de la population nationale).")

    mode_key = "6_territoires" if "6 Pôles" in mode else "5_regions"
    indicators = load_indicateurs(mode=mode_key)
    internet = load_internet_penetration()

    # KPI principaux consolidés
    if indicators is not None and not indicators.empty:
        total_pop = indicators["population"].sum()
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        ratio = total_agents / total_points if total_points > 0 else None

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_custom_card("Population Totale (RGPH-5)", format_number(total_pop), "Source officielle INSEED 2022", badge="100% TOGO", color=COLORS["navy"])
        with k2:
            render_custom_card("Réseau Mobile Money", format_number(total_agents), "Points d'agents géolocalisés", badge="T-Money / Flooz", color=COLORS["green"])
        with k3:
            render_custom_card("Points Financiers Physiques", format_number(total_points), "Banques, Microfinances & Mutuelles", badge="Réseau Fixe", color=COLORS["blue"])
        with k4:
            render_custom_card("Ratio Multiplicateur MM", f"x{format_decimal(ratio)}", "Agents MM pour 1 point physique", badge="Effet Levier", color=COLORS["gold"])

    # Question centrale
    st.markdown("""
    <div class="question-box">
        <div class="question-title">QUESTION CENTRALE & ENJEU STRATÉGIQUE</div>
        <div class="question-text">
            Là où les agences bancaires traditionnelles sont absentes, dans quelle mesure le Mobile Money 
            constitue-t-il l'infrastructure vitale de survie et d'inclusion financière au Togo ?
        </div>
        <p style="margin-top:0.6rem; color:#475569; font-size:0.95rem;">
            Alors que moins de 4 Togolais sur 10 utilisent activement l'Internet haut débit, le téléphone mobile de base (GSM/USSD) 
            a permis de déployer un maillage d'agents <strong>27 fois plus dense que l'ensemble des banques et microfinances réunies</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 3 piliers analytiques en graphiques rapides
    st.markdown("### 🔍 Les 3 dynamiques territoriales fondamentales")
    c_graph1, c_graph2 = st.columns([3, 2])

    if indicators is not None and not indicators.empty:
        with c_graph1:
            # Bar chart Agents vs Points
            fig_bar = px.bar(
                indicators,
                x="territoire" if "territoire" in indicators.columns else "region",
                y=["nb_agents_mm", "nb_points_financiers"],
                barmode="group",
                title="Maillage comparé : Agents Mobile Money vs Points Physiques",
                labels={"value": "Nombre d'infrastructures", "territoire": "Territoire", "variable": "Type"},
                color_discrete_map={"nb_agents_mm": COLORS["green"], "nb_points_financiers": COLORS["navy"]}
            )
            fig_bar.update_layout(height=350, plot_bgcolor="white", legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"))
            st.plotly_chart(fig_bar, use_container_width=True)

        with c_graph2:
            # Score d'Inclusion synthétique
            if "score_inclusion" in indicators.columns:
                fig_score = px.bar(
                    indicators.sort_values("score_inclusion", ascending=True),
                    y="territoire" if "territoire" in indicators.columns else "region",
                    x="score_inclusion",
                    orientation="h",
                    title="Indice Synthétique d'Inclusion (0-100)",
                    labels={"score_inclusion": "Score / 100", "y": ""},
                    color="score_inclusion",
                    color_continuous_scale="Tealgrn"
                )
                fig_score.update_layout(height=350, plot_bgcolor="white", coloraxis_showscale=False)
                st.plotly_chart(fig_score, use_container_width=True)

    # Synthèse d'alerte territoriale
    if indicators is not None and not indicators.empty:
        max_pressure = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]
        dominant_mm = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
        
        st.markdown(f"""
        <div class="observation">
            <strong>Observation stratégique majeure :</strong><br>
            • <strong>Pression bancaire maximale :</strong> La région <strong>{max_pressure.get('territoire', max_pressure.get('region'))}</strong> affiche la plus forte pression physique avec <strong>{format_number(max_pressure['habitants_par_point_financier'])} habitants par guichet</strong>.<br>
            • <strong>Relais Mobile Money le plus intensif :</strong> Le territoire <strong>{dominant_mm.get('territoire', dominant_mm.get('region'))}</strong> compense ce déficit par un ratio record de <strong>{format_decimal(dominant_mm['ratio_agents_par_point'])} agents Mobile Money pour chaque point financier</strong>.
        </div>
        """, unsafe_allow_html=True)

    # Parcours structuré du dashboard
    st.markdown("### 🧭 Parcours méthodologique & d'investigation")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        st.markdown("""
        <div class="card">
            <div class="card-title">01 · VUE NATIONALE</div>
            <div class="card-text">L'état des lieux macro : 8M d'habitants, courbe de pénétration Internet et télécoms.</div>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown("""
        <div class="card">
            <div class="card-title">02 · FINANCE & CARTOGRAPHIE</div>
            <div class="card-text">Carte OpenStreetMap interactive des 20 000 points, parts T-Money vs Flooz, banques vs IMF.</div>
        </div>
        """, unsafe_allow_html=True)
    with p3:
        st.markdown("""
        <div class="card">
            <div class="card-title">03 · TERRITOIRES & DÉSERTS</div>
            <div class="card-text">Drill-down préfectoral : identification des 39 préfectures et détection des zones blanches.</div>
        </div>
        """, unsafe_allow_html=True)
    with p4:
        st.markdown("""
        <div class="card">
            <div class="card-title">04 · SIMULATEUR & ACTIONS</div>
            <div class="card-text">Moteur d'aide à la décision : simuler des allocations d'agents pour réduire les fractures.</div>
        </div>
        """, unsafe_allow_html=True)