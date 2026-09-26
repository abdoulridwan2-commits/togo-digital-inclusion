"""
Page FINANCE — Établissements Financiers, Mobile Money & Cartographie Spatiale
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from app.data.loader import load_indicateurs, load_etablissements, load_agents
from app.components.kpi import format_number, format_decimal, render_custom_card
from app.components.filters import render_geo_filters
from app.components.map import add_coordinates, render_interactive_map
from app.config.theme import COLORS


def render():
    st.markdown("## 🏦 Réseaux Financiers & Inclusion Spatiale")
    st.caption("Cartographie géospatiale, comparaison des opérateurs Mobile Money et maillage bancaire.")

    # Choix de la granularité
    granularity = st.radio(
        "Découpage territorial",
        ["6 Pôles (Grand Lomé & Maritime distincts)", "5 Régions officielles"],
        horizontal=True,
        key="fin_granularity"
    )
    mode = "6_territoires" if "6 Pôles" in granularity else "5_regions"

    indicators = load_indicateurs(mode=mode)
    etabs = load_etablissements()
    agents = load_agents()

    if indicators is None or indicators.empty:
        st.warning("Indicateurs territoriaux non disponibles.")
        return

    # --------------------------------------------------------
    # KPI Supérieurs
    # --------------------------------------------------------
    total_agents = len(agents) if agents is not None else indicators["nb_agents_mm"].sum()
    total_points = len(etabs) if etabs is not None else indicators["nb_points_financiers"].sum()
    ratio = total_agents / total_points if total_points > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_custom_card("Points d'Agents MM", format_number(total_agents), "Agents de proximité", badge="Mobile Money", color=COLORS["green"])
    with c2:
        render_custom_card("Points Physiques Fixes", format_number(total_points), "Banques & Microfinances", badge="Réseau Fixe", color=COLORS["navy"])
    with c3:
        render_custom_card("Ratio de Densification", f"{ratio:.1f} : 1", "Agents MM pour 1 agence fixe", badge="Multiplicateur", color=COLORS["gold"])
    with c4:
        nb_banques = len(etabs[etabs["categorie_clean"] == "Banque Commerciale"]) if (etabs is not None and "categorie_clean" in etabs.columns) else 0
        render_custom_card("Banques Commerciales", format_number(nb_banques), "Agences bancaires pures", badge="Banques", color=COLORS["blue"])

    st.markdown("---")

    # --------------------------------------------------------
    # 1. Analyse des Opérateurs & Structure Financière
    # --------------------------------------------------------
    st.markdown("### 1. Structure de marché & Typologie des points")
    col_op, col_cat = st.columns(2)

    with col_op:
        if agents is not None and not agents.empty and "operateur_clean" in agents.columns:
            op_counts = agents["operateur_clean"].value_counts().reset_index()
            op_counts.columns = ["Opérateur", "Nombre"]
            fig_op = px.pie(
                op_counts,
                names="Opérateur",
                values="Nombre",
                hole=0.45,
                title="Répartition des Agents Mobile Money par Opérateur",
                color_discrete_sequence=[COLORS["navy"], COLORS["red"], COLORS["green"], "#94A3B8"]
            )
            fig_op.update_layout(height=350, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_op, use_container_width=True)
            
            st.caption("ℹ️ **Observation clé :** La présence massive d'agents multi-opérateurs (Togocom + Moov) démontre une forte interpénétration commerciale et une volonté de mutualisation des coûts par les marchands.")

    with col_cat:
        if etabs is not None and not etabs.empty and "categorie_clean" in etabs.columns:
            cat_counts = etabs["categorie_clean"].value_counts().reset_index()
            cat_counts.columns = ["Catégorie", "Nombre"]
            fig_cat = px.bar(
                cat_counts,
                x="Nombre",
                y="Catégorie",
                orientation="h",
                title="Établissements Financiers par Catégorie",
                color="Catégorie",
                color_discrete_sequence=[COLORS["blue"], COLORS["green"], COLORS["gold"], COLORS["navy"], "#94A3B8"]
            )
            fig_cat.update_layout(height=350, showlegend=False, plot_bgcolor="white", margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_cat, use_container_width=True)
            
            st.caption("ℹ️ **Rôle des Microfinances & Mutuelles :** Les institutions de microfinance (FUCEC, WAGES, etc.) dépassent largement les banques commerciales dans les villes secondaires et zones rurales.")

    st.markdown("---")

    # --------------------------------------------------------
    # 2. Carte Interactive des 20 000 Points Géolocalisés
    # --------------------------------------------------------
    st.markdown("### 2. Cartographie interactive des points d'accès (OpenStreetMap)")
    st.caption("Zoomez sur n'importe quelle ville ou canton togolais pour observer le maillage réel.")

    tab_map_agents, tab_map_etabs = st.tabs(["🗺️ Agents Mobile Money (19 790 points)", "🏦 Établissements Financiers (740 agences)"])

    with tab_map_agents:
        if agents is not None and not agents.empty:
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                agents_filtered, _ = render_geo_filters(agents, key_prefix="map_agents")
            with f_col2:
                all_ops = ["Tous"] + sorted(agents["operateur_clean"].dropna().unique().tolist())
                selected_op = st.selectbox("Filtrer par opérateur", all_ops, key="filter_op")
                if selected_op != "Tous":
                    agents_filtered = agents_filtered[agents_filtered["operateur_clean"] == selected_op]

            st.metric("Agents sélectionnés", f"{len(agents_filtered):,}".replace(",", " "))
            render_interactive_map(
                agents_filtered,
                title="Agents Mobile Money au Togo",
                color_col="operateur_clean",
                max_points=5000,
                point_type="agent"
            )

    with tab_map_etabs:
        if etabs is not None and not etabs.empty:
            fe_col1, fe_col2 = st.columns(2)
            with fe_col1:
                etabs_filtered, _ = render_geo_filters(etabs, key_prefix="map_etabs")
            with fe_col2:
                all_cats = ["Toutes"] + sorted(etabs["categorie_clean"].dropna().unique().tolist())
                selected_cat = st.selectbox("Filtrer par type d'établissement", all_cats, key="filter_cat")
                if selected_cat != "Toutes":
                    etabs_filtered = etabs_filtered[etabs_filtered["categorie_clean"] == selected_cat]

            st.metric("Établissements sélectionnés", f"{len(etabs_filtered):,}".replace(",", " "))
            render_interactive_map(
                etabs_filtered,
                title="Établissements Financiers au Togo",
                color_col="categorie_clean",
                max_points=2000,
                point_type="etab"
            )

    st.markdown("---")

    # --------------------------------------------------------
    # 3. Tableau Comparatif Synthétique
    # --------------------------------------------------------
    st.markdown("### 3. Matrice de densité financière territoriale")
    territory_col = "territoire" if "territoire" in indicators.columns else "region"
    cols_to_show = [territory_col, "population", "nb_agents_mm", "nb_points_financiers", "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point", "score_inclusion"]
    table_df = indicators[[c for c in cols_to_show if c in indicators.columns]].copy()
    
    st.dataframe(
        table_df.rename(columns={
            territory_col: "Territoire",
            "population": "Population",
            "nb_agents_mm": "Agents MM",
            "nb_points_financiers": "Points Financiers",
            "habitants_par_agent_mm": "Habitants / Agent MM",
            "habitants_par_point_financier": "Habitants / Point",
            "ratio_agents_par_point": "Agents / Point",
            "score_inclusion": "Score Inclusion (0-100)"
        }),
        use_container_width=True,
        hide_index=True
    )