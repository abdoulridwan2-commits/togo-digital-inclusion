"""
Page VUE NATIONALE — Synthèse Stratégique & Analyse Macro
"""

import streamlit as st
import plotly.express as px

from app.data.loader import (
    load_indicateurs,
    load_internet_penetration,
    load_telecoms,
)
from app.components.kpi import render_kpi_row, format_number, format_decimal, render_custom_card
from app.config.theme import COLORS


def render():
    st.markdown("## 📊 Vue Nationale & Diagnostic Macro")
    st.caption("Consolidation des indicateurs démographiques, numériques et financiers du Togo.")

    # Choix de la granularité
    col_c, col_v = st.columns([2, 5])
    with col_c:
        granularity = st.radio(
            "Vue d'agrégation",
            ["6 Pôles (Lomé distinct)", "5 Régions officielles"],
            horizontal=True,
            key="nat_granularity"
        )
    mode = "6_territoires" if "6 Pôles" in granularity else "5_regions"
    
    indicators = load_indicateurs(mode=mode)
    internet = load_internet_penetration()
    telecoms = load_telecoms()

    # --------------------------------------------------------
    # KPI Macro
    # --------------------------------------------------------
    if indicators is not None and not indicators.empty:
        total_pop = indicators["population"].sum()
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        latest_internet = f"{internet.iloc[-1]['value']:.1f}%" if (internet is not None and not internet.empty) else "—"

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_custom_card("Population Résidente (2022)", format_number(total_pop), "Source INSEED RGPH-5", badge="TOGO", color=COLORS["navy"])
        with k2:
            render_custom_card("Taux d'Usage Internet", latest_internet, "Part de la population connectée", badge="37.6%", color=COLORS["blue"])
        with k3:
            render_custom_card("Total Agents MM", format_number(total_agents), "Agents de proximité géolocalisés", badge="19 790", color=COLORS["green"])
        with k4:
            render_custom_card("Total Banques & SFD", format_number(total_points), "Agences physiques recensées", badge="740", color=COLORS["gold"])

    st.markdown("---")

    # --------------------------------------------------------
    # 1. Trajectoire d'Adoption Internet
    # --------------------------------------------------------
    st.markdown("### 1. Évolution historique de l'adoption numérique (2000-2022)")
    
    st.markdown("""
    **Observation clé :** Le Togo a connu une accélération majeure de l'usage d'Internet à partir de 2017, 
    passant de 12,4% à **37,6% en 2022**. Malgré ce bond, plus de 60% de la population n'utilise pas encore Internet au quotidien, 
    ce qui confère au canal SMS/USSD du Mobile Money un rôle d'inclusion irremplaçable.
    """)

    if internet is not None and not internet.empty:
        fig_net = px.area(
            internet,
            x="date",
            y="value",
            markers=True,
            labels={"date": "Année", "value": "% de la population"},
            title="Taux d'utilisation d'Internet au Togo (% population)"
        )
        fig_net.update_traces(line=dict(color=COLORS["navy"], width=3), fillcolor="rgba(11, 61, 92, 0.15)")
        fig_net.update_layout(height=380, plot_bgcolor="white", hovermode="x unified")
        st.plotly_chart(fig_net, use_container_width=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 2. Structure comparée des réseaux d'accès
    # --------------------------------------------------------
    st.markdown("### 2. Le fossé d'infrastructure : Réseau Physique vs Mobile Money")

    if indicators is not None and not indicators.empty:
        col_bar, col_radar = st.columns([3, 2])
        territory_col = "territoire" if "territoire" in indicators.columns else "region"

        with col_bar:
            finance_long = indicators.melt(
                id_vars=[territory_col],
                value_vars=["nb_agents_mm", "nb_points_financiers"],
                var_name="réseau",
                value_name="nombre"
            )
            finance_long["réseau"] = finance_long["réseau"].map({
                "nb_agents_mm": "Agents Mobile Money",
                "nb_points_financiers": "Points Financiers Physiques"
            })

            fig2 = px.bar(
                finance_long,
                x=territory_col,
                y="nombre",
                color="réseau",
                barmode="group",
                title="Agents Mobile Money vs Points physiques par territoire",
                labels={territory_col: "Territoire", "nombre": "Infrastructures", "réseau": "Réseau"},
                color_discrete_sequence=[COLORS["green"], COLORS["navy"]]
            )
            fig2.update_layout(height=400, plot_bgcolor="white", legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"))
            st.plotly_chart(fig2, use_container_width=True)

        with col_radar:
            if "score_inclusion" in indicators.columns:
                fig_score = px.bar(
                    indicators.sort_values("score_inclusion", ascending=True),
                    y=territory_col,
                    x="score_inclusion",
                    orientation="h",
                    title="Indice d'Inclusion Territoriale (IDNF / 100)",
                    labels={"score_inclusion": "Score", territory_col: ""},
                    color="score_inclusion",
                    color_continuous_scale="Tealgrn"
                )
                fig_score.update_layout(height=400, plot_bgcolor="white", coloraxis_showscale=False)
                st.plotly_chart(fig_score, use_container_width=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 3. Pression démographique relative sur les réseaux
    # --------------------------------------------------------
    st.markdown("### 3. Pression démographique : Charge par point de contact")

    if indicators is not None and not indicators.empty:
        col1, col2 = st.columns(2)
        territory_col = "territoire" if "territoire" in indicators.columns else "region"

        with col1:
            fig3 = px.bar(
                indicators,
                x=territory_col,
                y="habitants_par_point_financier",
                title="Habitants par guichet physique (Banque/IMF)",
                labels={territory_col: "Territoire", "habitants_par_point_financier": "Habitants / point"},
                color="habitants_par_point_financier",
                color_continuous_scale="Reds"
            )
            fig3.update_layout(height=380, plot_bgcolor="white", coloraxis_showscale=False)
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            fig4 = px.bar(
                indicators,
                x=territory_col,
                y="habitants_par_agent_mm",
                title="Habitants par agent Mobile Money",
                labels={territory_col: "Territoire", "habitants_par_agent_mm": "Habitants / agent"},
                color="habitants_par_agent_mm",
                color_continuous_scale="Greens_r"
            )
            fig4.update_layout(height=380, plot_bgcolor="white", coloraxis_showscale=False)
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown(f"""
        <div class="insight">
            <strong>Conclusion Stratégique pour les Décideurs :</strong><br>
            Dans les <strong>Savanes</strong> et les <strong>Plateaux</strong>, un guichet physique dessert en moyenne plus de 
            <strong>14 000 à 18 000 habitants</strong> (contre ~5 000 à Lomé). En revanche, le réseau d'agents Mobile Money garantit 
            un agent pour moins de <strong>400 à 530 habitants</strong> sur tout le territoire national.
        </div>
        """, unsafe_allow_html=True)