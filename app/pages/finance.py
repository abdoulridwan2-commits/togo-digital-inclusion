"""
Page FINANCE
"""

import streamlit as st
import plotly.express as px

from app.data.loader import load_indicateurs, load_etablissements
from app.components.kpi import format_number, format_decimal
from app.config.theme import COLORS


def render():
    st.markdown("## 🏦 Finance")
    st.caption("Établissements financiers et comparaison avec le réseau Mobile Money.")

    indicators = load_indicateurs()
    etabs = load_etablissements()

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------
    st.markdown("### Indicateurs clés")

    if indicators is not None and not indicators.empty:
        total_agents = indicators["nb_agents_mm"].sum()
        total_points = indicators["nb_points_financiers"].sum()
        ratio = total_agents / total_points if total_points > 0 else None

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Agents Mobile Money", format_number(total_agents))
        c2.metric("Total Points financiers", format_number(total_points))
        c3.metric("Ratio Agents / Points", format_decimal(ratio))
    else:
        st.warning("Indicateurs territoriaux non disponibles.")
        return

    st.markdown("---")

    # --------------------------------------------------------
    # 1. COMPARAISON DES DEUX RÉSEAUX
    # --------------------------------------------------------
    st.markdown("### 1. Deux réseaux d'accès")

    st.markdown("""
    **Introduction**  
    Comparaison entre le réseau d'établissements financiers physiques 
    et le réseau d'agents Mobile Money par région.
    """)

    finance_long = indicators.melt(
        id_vars=["region"],
        value_vars=["nb_agents_mm", "nb_points_financiers"],
        var_name="réseau",
        value_name="nombre"
    )
    finance_long["réseau"] = finance_long["réseau"].map({
        "nb_agents_mm": "Agents Mobile Money",
        "nb_points_financiers": "Points financiers"
    })

    fig = px.bar(
        finance_long, x="region", y="nombre", color="réseau", barmode="group",
        title="Agents Mobile Money vs Points financiers par région",
        labels={"region": "Région", "nombre": "Nombre", "réseau": "Type de réseau"},
        color_discrete_sequence=[COLORS["navy"], COLORS["gold"]]
    )
    fig.update_layout(height=420, plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    dominant = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
    pressure = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]

    st.markdown(f"""
    **Commentaire**  
    La région **{dominant['region']}** présente le ratio le plus élevé 
    d'agents Mobile Money par point financier 
    ({format_decimal(dominant['ratio_agents_par_point'])}).  
    La région **{pressure['region']}** présente la plus forte pression 
    sur le réseau physique ({format_number(pressure['habitants_par_point_financier'])} habitants/point).

    **Conclusion**  
    Le réseau Mobile Money est nettement plus dense que le réseau 
    d'établissements financiers dans toutes les régions observées.

    **Piste d'action**  
    Dans les territoires à forte population et faible densité de points financiers, 
    examiner le rôle potentiel du Mobile Money comme relais d'accès.
    """)

    st.markdown("---")

    # --------------------------------------------------------
    # 2. DENSITÉ RELATIVE
    # --------------------------------------------------------
    st.markdown("### 2. Densité relative d'accès")

    st.markdown("""
    **Introduction**  
    Les ratios habitants/point et habitants/agent mesurent la pression 
    relative sur chaque type de réseau.
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            indicators, x="region", y="habitants_par_point_financier",
            title="Habitants par point financier",
            labels={"region": "Région", "habitants_par_point_financier": "Habitants / point"},
            color_discrete_sequence=[COLORS["red"]]
        )
        fig1.update_layout(height=380, plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            indicators, x="region", y="habitants_par_agent_mm",
            title="Habitants par agent Mobile Money",
            labels={"region": "Région", "habitants_par_agent_mm": "Habitants / agent"},
            color_discrete_sequence=[COLORS["green"]]
        )
        fig2.update_layout(height=380, plot_bgcolor="white", showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Commentaire**  
    Le nombre d'habitants par point financier est systématiquement plus élevé 
    que le nombre d'habitants par agent Mobile Money.

    **Conclusion**  
    La densité relative d'accès via Mobile Money est plus favorable 
    que celle des établissements physiques.

    **Piste d'action**  
    Évaluer le renforcement du réseau d'agents et des services numériques 
    dans les territoires à forte pression sur le réseau physique.
    """)

    st.markdown("---")

    # --------------------------------------------------------
    # 3. TABLEAU + CATÉGORIES
    # --------------------------------------------------------
    st.markdown("### 3. Tableau de comparaison")

    display_cols = [
        "region", "population", "nb_agents_mm", "nb_points_financiers",
        "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point"
    ]
    available = [c for c in display_cols if c in indicators.columns]
    table = indicators[available].copy()
    table = table.rename(columns={
        "region": "Région",
        "population": "Population",
        "nb_agents_mm": "Agents MM",
        "nb_points_financiers": "Points financiers",
        "habitants_par_agent_mm": "Hab. / agent MM",
        "habitants_par_point_financier": "Hab. / point financier",
        "ratio_agents_par_point": "Agents MM / point"
    })
    st.dataframe(table, use_container_width=True, hide_index=True)

    if etabs is not None and not etabs.empty and "categorie" in etabs.columns:
        st.markdown("### 4. Structure des établissements financiers")

        st.markdown("""
        **Introduction**  
        Répartition des établissements selon les catégories présentes dans les données.
        """)

        categories = etabs["categorie"].value_counts().reset_index()
        categories.columns = ["Catégorie", "Nombre"]

        fig_cat = px.bar(
            categories, x="Catégorie", y="Nombre",
            title="Nombre d'établissements par catégorie",
            color_discrete_sequence=[COLORS["blue"]]
        )
        fig_cat.update_layout(height=400, plot_bgcolor="white")
        st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("""
        **Commentaire**  
        Les catégories affichées correspondent strictement à celles présentes dans les sources.

        **Conclusion**  
        La structure du réseau financier physique est diversifiée 
        (banques, microfinance, assurances, mutuelles, etc.).

        **Piste d'action**  
        Croiser cette répartition avec la densité territoriale 
        pour identifier d'éventuels déséquilibres de couverture.
        """)