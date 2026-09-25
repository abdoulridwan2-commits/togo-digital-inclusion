"""
Page VUE NATIONALE — vue exécutive
"""

import streamlit as st
import plotly.express as px

from app.data.loader import (
    load_indicateurs,
    load_internet_penetration,
    load_telecoms,
)
from app.components.kpi import render_kpi_row, format_number, format_decimal
from app.config.theme import COLORS


def render():
    st.markdown("## 📊 Vue nationale")
    st.caption("Synthèse exécutive des principaux indicateurs.")

    indicators = load_indicateurs()
    internet = load_internet_penetration()
    telecoms = load_telecoms()

    # --------------------------------------------------------
    # KPI principaux
    # --------------------------------------------------------
    st.markdown("### Indicateurs clés")

    kpi_items = []

    if indicators is not None and not indicators.empty:
        kpi_items.append(("Population (2022)", indicators["population"].sum()))
        kpi_items.append(("Agents Mobile Money", indicators["nb_agents_mm"].sum()))
        kpi_items.append(("Points financiers", indicators["nb_points_financiers"].sum()))

    if internet is not None and not internet.empty:
        latest_internet = internet.iloc[-1]["value"]
        kpi_items.append(("Usage Internet", f"{latest_internet:.1f}%"))

    if kpi_items:
        # Affichage manuel pour gérer le % 
        cols = st.columns(len(kpi_items))
        for col, (label, value) in zip(cols, kpi_items):
            with col:
                if isinstance(value, str):
                    st.metric(label, value)
                else:
                    st.metric(label, format_number(value))

    st.markdown("---")

    # --------------------------------------------------------
    # Analyse 1 — Internet
    # --------------------------------------------------------
    st.markdown("### 1. Adoption d'Internet")

    st.markdown("""
    **Introduction**  
    Cet indicateur mesure la part de la population utilisant Internet.
    Il permet de suivre l'évolution de l'adoption numérique au niveau national.
    """)

    if internet is not None and not internet.empty:
        fig = px.line(
            internet,
            x="date",
            y="value",
            markers=True,
            labels={"date": "Année", "value": "% de la population"},
            title="Évolution de la part de la population utilisant Internet"
        )
        fig.update_traces(line=dict(color=COLORS["navy"], width=3))
        fig.update_layout(height=400, plot_bgcolor="white", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        latest = internet.iloc[-1]
        first = internet.iloc[0]
        progress = latest["value"] - first["value"]

        st.markdown(f"""
        **Commentaire**  
        Entre {int(first['date'])} et {int(latest['date'])}, la part de la population 
        utilisant Internet est passée de {first['value']:.1f}% à {latest['value']:.1f}% 
        (progression de +{progress:.1f} points).

        **Conclusion**  
        L'usage d'Internet progresse, mais reste en dessous de 40 % de la population 
        dans la dernière année disponible.

        **Piste d'action**  
        Accélérer l'accès à la data et les usages numériques de base, 
        notamment dans les territoires où la pénétration reste faible.
        """)
    else:
        st.warning("Données de pénétration Internet non disponibles.")

    st.markdown("---")

    # --------------------------------------------------------
    # Analyse 2 — Réseaux financiers
    # --------------------------------------------------------
    st.markdown("### 2. Présence des réseaux financiers")

    st.markdown("""
    **Introduction**  
    Comparaison entre le réseau physique (établissements financiers) 
    et le réseau Mobile Money au niveau régional.
    """)

    if indicators is not None and not indicators.empty:
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

        fig2 = px.bar(
            finance_long,
            x="region",
            y="nombre",
            color="réseau",
            barmode="group",
            title="Agents Mobile Money vs Points financiers par région",
            labels={"region": "Région", "nombre": "Nombre", "réseau": "Type de réseau"},
            color_discrete_sequence=[COLORS["navy"], COLORS["gold"]]
        )
        fig2.update_layout(height=420, plot_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

        dominant = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
        pressure = indicators.loc[indicators["habitants_par_point_financier"].idxmax()]

        st.markdown(f"""
        **Commentaire**  
        La région **{dominant['region']}** présente le ratio le plus élevé 
        d'agents Mobile Money par point financier 
        ({format_decimal(dominant['ratio_agents_par_point'])}).  
        La région **{pressure['region']}** présente la plus forte pression 
        sur le réseau physique ({format_number(pressure['habitants_par_point_financier'])} habitants par point).

        **Conclusion**  
        Le réseau Mobile Money est nettement plus dense que le réseau 
        d'établissements financiers dans toutes les régions. 
        Certains territoires s'appuient particulièrement sur le Mobile Money.

        **Piste d'action**  
        Examiner les territoires à forte population et faible densité 
        de points financiers pour évaluer le rôle potentiel du Mobile Money 
        comme relais d'accès.
        """)
    else:
        st.warning("Indicateurs territoriaux non disponibles.")

    st.markdown("---")

    # --------------------------------------------------------
    # Analyse 3 — Densité relative
    # --------------------------------------------------------
    st.markdown("### 3. Densité relative d'accès")

    st.markdown("""
    **Introduction**  
    Les ratios habitants/point et habitants/agent permettent de mesurer 
    la pression relative sur chaque type de réseau.
    """)

    if indicators is not None and not indicators.empty:
        col1, col2 = st.columns(2)

        with col1:
            fig3 = px.bar(
                indicators,
                x="region",
                y="habitants_par_point_financier",
                title="Habitants par point financier",
                labels={"region": "Région", "habitants_par_point_financier": "Habitants / point"},
                color_discrete_sequence=[COLORS["red"]]
            )
            fig3.update_layout(height=380, plot_bgcolor="white", showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

        with col2:
            fig4 = px.bar(
                indicators,
                x="region",
                y="habitants_par_agent_mm",
                title="Habitants par agent Mobile Money",
                labels={"region": "Région", "habitants_par_agent_mm": "Habitants / agent"},
                color_discrete_sequence=[COLORS["green"]]
            )
            fig4.update_layout(height=380, plot_bgcolor="white", showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("""
        **Commentaire**  
        Le nombre d'habitants par point financier est systématiquement 
        plus élevé que le nombre d'habitants par agent Mobile Money, 
        ce qui illustre la plus grande densification du réseau d'agents.

        **Conclusion**  
        La densité relative d'accès via Mobile Money est plus favorable 
        que celle des établissements financiers physiques.

        **Piste d'action**  
        Dans les territoires à forte pression sur le réseau physique, 
        évaluer le renforcement du réseau d'agents et des services numériques associés.
        """)