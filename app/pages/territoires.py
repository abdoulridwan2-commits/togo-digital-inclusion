"""
Page TERRITOIRES — Drill-Down Préfectoral & Analyse des Déserts Financiers
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app.data.loader import load_indicateurs, load_indicateurs_prefectures
from app.components.kpi import format_number, format_decimal, render_custom_card
from app.config.theme import COLORS


def render():
    st.markdown("## 🗺️ Diagnostics Territoriaux & Déserts Financiers")
    st.caption("Exploration multi-niveaux (Régions & Préfectures), détection des zones d'exclusion et comparaison radar.")

    tab_regions, tab_prefectures, tab_deserts = st.tabs([
        "🏛️ Analyse Régionale",
        "📍 Drill-Down Préfectoral (39 Préfectures)",
        "⚠️ Observatoire des Déserts Bancaires"
    ])

    # ========================================================
    # TAB 1 : ANALYSE RÉGIONALE
    # ========================================================
    with tab_regions:
        mode = st.radio(
            "Vue territoriale",
            ["6 Pôles (Grand Lomé & Maritime séparés)", "5 Régions officielles"],
            horizontal=True,
            key="terr_reg_mode"
        )
        mode_key = "6_territoires" if "6 Pôles" in mode else "5_regions"
        indicators = load_indicateurs(mode=mode_key)

        if indicators is not None and not indicators.empty:
            territory_col = "territoire" if "territoire" in indicators.columns else "region"
            territories = sorted(indicators[territory_col].dropna().unique().tolist())

            selected = st.selectbox("Sélectionner un territoire", ["Tous les territoires"] + territories, key="terr_sel")

            if selected != "Tous les territoires":
                curr = indicators[indicators[territory_col] == selected].iloc[0]
                k1, k2, k3, k4 = st.columns(4)
                with k1:
                    render_custom_card("Population (2022)", format_number(curr["population"]), "Habitants résidents", badge="INSEED", color=COLORS["navy"])
                with k2:
                    render_custom_card("Agents Mobile Money", format_number(curr["nb_agents_mm"]), "Points de proximité", badge="MM", color=COLORS["green"])
                with k3:
                    render_custom_card("Points Financiers", format_number(curr["nb_points_financiers"]), "Banques & Microfinances", badge="Fixe", color=COLORS["blue"])
                with k4:
                    render_custom_card("Score Inclusion", f"{curr.get('score_inclusion', 0):.1f} / 100", "Indice IDNF", badge="Score", color=COLORS["gold"])

            st.markdown("---")

            # Comparateur Radar
            st.markdown("### 🕸️ Comparateur Radar de deux territoires")
            col_a, col_b = st.columns(2)
            with col_a:
                t_a = st.selectbox("Territoire A", territories, index=0, key="radar_a")
            with col_b:
                t_b = st.selectbox("Territoire B", territories, index=min(1, len(territories) - 1), key="radar_b")

            row_a = indicators[indicators[territory_col] == t_a].iloc[0]
            row_b = indicators[indicators[territory_col] == t_b].iloc[0]

            categories = ["Densité MM (/10k hab)", "Points Physiques (/100k hab)", "Score Inclusion (/100)", "Part Banques (%)"]
            
            val_a = [
                min(100, (row_a["nb_agents_mm"] / row_a["population"]) * 10000 * 2.5),
                min(100, (row_a["nb_points_financiers"] / row_a["population"]) * 100000 * 3),
                row_a.get("score_inclusion", 50),
                (row_a.get("nb_banques", 0) / max(1, row_a["nb_points_financiers"])) * 100
            ]
            val_b = [
                min(100, (row_b["nb_agents_mm"] / row_b["population"]) * 10000 * 2.5),
                min(100, (row_b["nb_points_financiers"] / row_b["population"]) * 100000 * 3),
                row_b.get("score_inclusion", 50),
                (row_b.get("nb_banques", 0) / max(1, row_b["nb_points_financiers"])) * 100
            ]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(r=val_a, theta=categories, fill='toself', name=t_a, line_color=COLORS["navy"]))
            fig_radar.add_trace(go.Scatterpolar(r=val_b, theta=categories, fill='toself', name=t_b, line_color=COLORS["gold"]))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                height=420,
                title=f"Profil comparé : {t_a} vs {t_b}"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    # ========================================================
    # TAB 2 : DRILL-DOWN PRÉFECTORAL
    # ========================================================
    with tab_prefectures:
        st.markdown("### 📍 Diagnostic au niveau des Préfectures")
        st.caption("Consultez la situation précise de chacune des préfectures togolaises.")
        
        pref_df = load_indicateurs_prefectures()
        if pref_df is not None and not pref_df.empty:
            # Filtre par région
            all_regs = ["Toutes"] + sorted(pref_df["region"].dropna().unique().tolist())
            sel_reg = st.selectbox("Filtrer les préfectures par région parente", all_regs, key="pref_filter_reg")
            
            p_display = pref_df.copy()
            if sel_reg != "Toutes":
                p_display = p_display[p_display["region"] == sel_reg]

            # Tri
            sort_by = st.selectbox("Trier par", ["Population", "Nombre d'agents MM", "Points financiers", "Habitants / point financier"], key="pref_sort")
            col_map = {
                "Population": "population",
                "Nombre d'agents MM": "nb_agents_mm",
                "Points financiers": "nb_points_financiers",
                "Habitants / point financier": "habitants_par_point_financier"
            }
            p_display = p_display.sort_values(by=col_map[sort_by], ascending=False)

            st.dataframe(
                p_display.rename(columns={
                    "prefecture": "Préfecture",
                    "region": "Région",
                    "population": "Population (2022)",
                    "nb_agents_mm": "Agents MM",
                    "nb_points_financiers": "Points Financiers",
                    "nb_banques": "Banques",
                    "nb_microfinances": "Microfinances",
                    "habitants_par_agent_mm": "Hab / Agent MM",
                    "habitants_par_point_financier": "Hab / Point",
                    "ratio_agents_par_point": "Agents / Point",
                    "statut_desert": "Statut de Couverture"
                }),
                use_container_width=True,
                hide_index=True
            )

    # ========================================================
    # TAB 3 : DÉSERTS BANCAIRES
    # ========================================================
    with tab_deserts:
        st.markdown("### ⚠️ Observatoire des Déserts Bancaires & Zones Vulnérables")
        st.markdown("""
        Un **désert bancaire** est défini comme une préfecture où il n'existe **aucune agence bancaire commerciale physique**. 
        Dans ces territoires, l'accès au compte bancaire conventionnel, aux crédits structurés et aux devises est inexistant 
        sans un déplacement long et coûteux vers la capitale régionale ou Lomé.
        """)

        pref_df = load_indicateurs_prefectures()
        if pref_df is not None and not pref_df.empty:
            deserts = pref_df[pref_df["nb_banques"] == 0].copy()
            
            c_d1, c_d2 = st.columns([2, 3])
            with c_d1:
                st.metric("Préfectures sans aucune banque", f"{len(deserts)} sur {len(pref_df)}")
                pop_desert = deserts["population"].sum()
                st.metric("Population en zone de désert bancaire", f"{pop_desert:,} hab.".replace(",", " "))
                st.warning("⚡ **Facteur de résilience :** Ces populations dépendent à 100% du réseau Mobile Money et de quelques caisses de microfinance pour leurs transactions quotidiennes.")

            with c_d2:
                fig_desert = px.bar(
                    deserts.sort_values("population", ascending=False).head(10),
                    x="population",
                    y="prefecture",
                    orientation="h",
                    title="Top 10 des préfectures les plus peuplées sans banque",
                    labels={"population": "Population résidente", "prefecture": "Préfecture"},
                    color="region",
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig_desert.update_layout(height=380, plot_bgcolor="white")
                st.plotly_chart(fig_desert, use_container_width=True)

            st.markdown("#### Liste exhaustive des préfectures en situation de désert bancaire")
            st.dataframe(
                deserts[["prefecture", "region", "population", "nb_agents_mm", "nb_points_financiers", "nb_microfinances", "statut_desert"]].rename(columns={
                    "prefecture": "Préfecture",
                    "region": "Région",
                    "population": "Population",
                    "nb_agents_mm": "Agents MM (Relais Vital)",
                    "nb_points_financiers": "Points Totaux",
                    "nb_microfinances": "Microfinances",
                    "statut_desert": "Diagnostic"
                }),
                use_container_width=True,
                hide_index=True
            )