"""
Page SIMULATEUR — Outil d'Aide à la Décision & Scénarios d'Allocation ("What-If")
Togo Digital & Financial Inclusion
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app.data.loader import load_indicateurs, load_indicateurs_prefectures
from app.components.kpi import format_number, format_decimal, render_custom_card
from app.config.theme import COLORS


def render():
    st.markdown("## 🧮 Simulateur Décisionnel d'Inclusion Financière")
    st.caption("Module prospectif ('What-If') pour simuler l'impact de déploiements d'agents et de guichets financiers.")

    st.markdown("""
    <div class="question-box">
        <div class="question-title">AIDE À LA DÉCISION PUBLIQUE & PRIVÉE</div>
        <div class="question-text">
            Comment une politique ciblée d'incitations ou de déploiement de kiosques peut-elle 
            réduire la pression sur les territoires et éradiquer les déserts financiers ?
        </div>
        <p style="margin-top:0.5rem; color:#475569; font-size:0.92rem;">
            Sélectionnez un territoire cible, simulez l'ajout de nouveaux agents Mobile Money ou de points financiers physiques, 
            et visualisez instantanément le gain en termes de charge démographique et d'Indice d'Inclusion.
        </p>
    </div>
    """, unsafe_allow_html=True)

    indicators = load_indicateurs(mode="6_territoires")
    if indicators is None or indicators.empty:
        st.warning("Données territoriales indisponibles pour la simulation.")
        return

    territory_col = "territoire" if "territoire" in indicators.columns else "region"
    territories = indicators[territory_col].tolist()

    # --------------------------------------------------------
    # Paramètres de simulation
    # --------------------------------------------------------
    col_input1, col_input2, col_input3 = st.columns(3)

    with col_input1:
        selected_territory = st.selectbox("Territoire d'intervention", territories, index=territories.index("Savanes") if "Savanes" in territories else 0)
        curr_row = indicators[indicators[territory_col] == selected_territory].iloc[0]
        pop = curr_row["population"]
        st.caption(f"Population résidente : **{format_number(pop)} habitants**")

    with col_input2:
        new_agents = st.slider(
            "Agents Mobile Money à recruter / labelliser",
            min_value=0,
            max_value=2000,
            value=300,
            step=50,
            help="Subvention ou agrément pour l'installation de nouveaux points marchands MM."
        )

    with col_input3:
        new_points = st.slider(
            "Points financiers physiques à implanter",
            min_value=0,
            max_value=100,
            value=25,
            step=5,
            help="Agences de microfinance, guichets automatiques ou caisses mutualistes."
        )

    # --------------------------------------------------------
    # Calculs d'impact
    # --------------------------------------------------------
    current_agents = curr_row["nb_agents_mm"]
    current_points = curr_row["nb_points_financiers"]
    
    sim_agents = current_agents + new_agents
    sim_points = current_points + new_points

    curr_hab_agent = round(pop / current_agents) if current_agents > 0 else 0
    sim_hab_agent = round(pop / sim_agents) if sim_agents > 0 else 0

    curr_hab_point = round(pop / current_points) if current_points > 0 else 0
    sim_hab_point = round(pop / sim_points) if sim_points > 0 else 0

    # Calcul scores avant/après
    curr_agents_10k = (current_agents / pop) * 10000
    curr_points_100k = (current_points / pop) * 100000
    curr_score = min(100, round((min(100, (curr_agents_10k / 30.0) * 50) * 0.6) + (min(100, (curr_points_100k / 15.0) * 50) * 0.4), 1))

    sim_agents_10k = (sim_agents / pop) * 10000
    sim_points_100k = (sim_points / pop) * 100000
    sim_score = min(100, round((min(100, (sim_agents_10k / 30.0) * 50) * 0.6) + (min(100, (sim_points_100k / 15.0) * 50) * 0.4), 1))

    gain_score = round(sim_score - curr_score, 1)

    st.markdown("---")
    st.markdown("### 📈 Résultats prédictifs de la simulation")

    # 4 Cartes Avant / Après
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.metric(
            "Habitants / Agent MM",
            f"{sim_hab_agent:,} hab.".replace(",", " "),
            delta=f"{sim_hab_agent - curr_hab_agent:,} hab.".replace(",", " "),
            delta_color="inverse"
        )
    with r2:
        st.metric(
            "Habitants / Point Financier",
            f"{sim_hab_point:,} hab.".replace(",", " "),
            delta=f"{sim_hab_point - curr_hab_point:,} hab.".replace(",", " "),
            delta_color="inverse"
        )
    with r3:
        st.metric(
            "Score d'Inclusion IDNF",
            f"{sim_score:.1f} / 100",
            delta=f"+{gain_score} pts",
            delta_color="normal"
        )
    with r4:
        pop_couverte = round(new_points * 3000 + new_agents * 400)
        st.metric(
            "Bénéficiaires directs estimés",
            f"{format_number(min(pop, pop_couverte))} hab.",
            delta="Impact Territorial"
        )

    # Graphique Avant / Après
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        df_comp_points = pd.DataFrame({
            "Indicateur": ["Agents Mobile Money", "Points Financiers Physiques"],
            "Actuel": [current_agents, current_points],
            "Après Simulation": [sim_agents, sim_points]
        }).melt(id_vars=["Indicateur"], var_name="Scénario", value_name="Nombre")

        fig_comp = px.bar(
            df_comp_points,
            x="Indicateur",
            y="Nombre",
            color="Scénario",
            barmode="group",
            title=f"Évolution des infrastructures — {selected_territory}",
            color_discrete_map={"Actuel": COLORS["navy"], "Après Simulation": COLORS["green"]}
        )
        fig_comp.update_layout(height=360, plot_bgcolor="white")
        st.plotly_chart(fig_comp, use_container_width=True)

    with col_g2:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sim_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Progression Indice d'Inclusion — {selected_territory}"},
            delta={'reference': curr_score, 'increasing': {'color': COLORS["green"]}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': COLORS["navy"]},
                'steps': [
                    {'range': [0, 40], 'color': "#FEE2E2"},
                    {'range': [40, 70], 'color': "#FEF3C7"},
                    {'range': [70, 100], 'color': "#D1FAE5"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': sim_score
                }
            }
        ))
        fig_gauge.update_layout(height=360)
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Fiche de recommandation d'investissement
    st.markdown("### 📋 Feuille de Route d'Investissement Générée")
    st.markdown(f"""
    <div class="recommendation">
        <strong>Synthèse d'intervention pour la région {selected_territory} :</strong><br>
        • <strong>Objectif :</strong> Déploiement de <strong>+{new_points} guichets fixes</strong> et <strong>+{new_agents} agents marchands</strong>.<br>
        • <strong>Résultat :</strong> Réduction de la charge par guichet physique de <strong>{format_number(curr_hab_point)}</strong> à <strong>{format_number(sim_hab_point)}</strong> habitants par point.<br>
        • <strong>Indicateur clé :</strong> Le Score d'Inclusion Territoriale bondit de <strong>{curr_score}</strong> à <strong>{sim_score}/100</strong> (+{gain_score} points).<br>
        • <strong>Recommandation opérationnelle :</strong> Prioriser l'implantation des guichets dans les préfectures actuellement classées en <em>Désert bancaire</em> pour maximiser l'effet de désenclavement.
    </div>
    """, unsafe_allow_html=True)
