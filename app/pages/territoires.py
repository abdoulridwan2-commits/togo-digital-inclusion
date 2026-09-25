"""
Page TERRITOIRES — Explorateur territorial
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app.data.loader import load_indicateurs
from app.components.kpi import format_number, format_decimal
from app.config.theme import COLORS


def territory_profile(row):
    """Affiche le profil d'un territoire."""
    st.markdown(f"""
    <div style="background:white; border:1px solid #E2E8F0; border-radius:18px; padding:1.4rem; box-shadow:0 5px 16px rgba(0,0,0,0.04);">
        <div style="font-size:1.4rem; font-weight:800; color:#0B3D5C;">{row['region']}</div>
        <div style="color:#64748B; font-size:0.9rem;">Profil territorial d'accès</div>
        <hr>
        <b>Population :</b> {format_number(row.get('population'))}<br><br>
        <b>Agents Mobile Money :</b> {format_number(row.get('nb_agents_mm'))}<br><br>
        <b>Points financiers :</b> {format_number(row.get('nb_points_financiers'))}<br><br>
        <b>Habitants / agent :</b> {format_number(row.get('habitants_par_agent_mm'))}<br><br>
        <b>Habitants / point financier :</b> {format_number(row.get('habitants_par_point_financier'))}<br><br>
        <b>Agents MM / point financier :</b> {format_decimal(row.get('ratio_agents_par_point'))}
    </div>
    """, unsafe_allow_html=True)


def render():
    st.markdown("## 🗺️ Territoires")
    st.caption("Explorer et comparer les profils d'accès des territoires.")

    indicators = load_indicateurs()
    if indicators is None or indicators.empty:
        st.warning("Indicateurs territoriaux non disponibles.")
        return

    regions = sorted(indicators["region"].dropna().unique().tolist())

    # --------------------------------------------------------
    # FILTRE RÉGION
    # --------------------------------------------------------
    selected = st.selectbox("Sélectionner une région", ["Toutes les régions"] + regions)
    current = indicators if selected == "Toutes les régions" else indicators[indicators["region"] == selected].copy()

    # KPI
    population = current["population"].sum()
    agents = current["nb_agents_mm"].sum()
    points = current["nb_points_financiers"].sum()
    ratio = agents / points if points > 0 else None

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Population", format_number(population))
    c2.metric("Agents MM", format_number(agents))
    c3.metric("Points financiers", format_number(points))
    c4.metric("Agents / point", format_decimal(ratio))

    st.markdown("---")

    # --------------------------------------------------------
    # PROFIL D'UN TERRITOIRE
    # --------------------------------------------------------
    if selected != "Toutes les régions":
        st.markdown("### Profil du territoire")

        row = current.iloc[0]
        p1, p2 = st.columns([1, 2])

        with p1:
            territory_profile(row)

        with p2:
            # Radar relatif (normalisation simple, pas de score)
            categories = ["Agents MM", "Points financiers", "Population"]
            values = [row["nb_agents_mm"], row["nb_points_financiers"], row["population"]]
            max_vals = [
                indicators["nb_agents_mm"].max(),
                indicators["nb_points_financiers"].max(),
                indicators["population"].max()
            ]
            normalized = [(v / m * 100) if m else 0 for v, m in zip(values, max_vals)]

            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=normalized + [normalized[0]],
                theta=categories + [categories[0]],
                fill="toself",
                name=selected,
                line_color=COLORS["navy"]
            ))
            radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                height=400,
                title="Profil relatif du territoire"
            )
            st.plotly_chart(radar, use_container_width=True)

        st.markdown(f"""
        **Commentaire**  
        Le profil de **{selected}** est présenté à partir des indicateurs de présence 
        et de densité relative disponibles.

        **Conclusion**  
        Ces mesures décrivent la structure d'accès du territoire. 
        Elles ne mesurent pas l'activité réelle des points ou des agents.

        **Piste d'action**  
        Compléter par une analyse locale (préfectures / communes) 
        lorsque des données plus fines sont disponibles.
        """)

        st.markdown("---")

    # --------------------------------------------------------
    # COMPARAISON DE DEUX TERRITOIRES
    # --------------------------------------------------------
    st.markdown("### Comparer deux territoires")

    col_a, col_b = st.columns(2)
    with col_a:
        region_a = st.selectbox("Territoire A", regions, key="terr_a")
    with col_b:
        region_b = st.selectbox("Territoire B", regions, index=min(1, len(regions)-1), key="terr_b")

    row_a = indicators[indicators["region"] == region_a]
    row_b = indicators[indicators["region"] == region_b]

    if not row_a.empty and not row_b.empty:
        a, b = row_a.iloc[0], row_b.iloc[0]

        comparison = pd.DataFrame({
            "Indicateur": [
                "Population",
                "Agents Mobile Money",
                "Points financiers",
                "Habitants / agent MM",
                "Habitants / point financier",
                "Agents MM / point financier",
            ],
            region_a: [
                a["population"], a["nb_agents_mm"], a["nb_points_financiers"],
                a["habitants_par_agent_mm"], a["habitants_par_point_financier"],
                a["ratio_agents_par_point"],
            ],
            region_b: [
                b["population"], b["nb_agents_mm"], b["nb_points_financiers"],
                b["habitants_par_agent_mm"], b["habitants_par_point_financier"],
                b["ratio_agents_par_point"],
            ],
        })

        st.dataframe(comparison, use_container_width=True, hide_index=True)

        st.markdown("""
        **Commentaire**  
        La comparaison présente les valeurs côte à côte.  
        Aucun classement « gagnant / perdant » n'est produit automatiquement.

        **Conclusion**  
        Les écarts observés portent sur la présence et la densité relative des réseaux.

        **Piste d'action**  
        Approfondir l'analyse sur les territoires présentant 
        une forte population et une densité relative faible de points financiers.
        """)

    st.markdown("---")

    # --------------------------------------------------------
    # VUE COMPARATIVE NATIONALE
    # --------------------------------------------------------
    st.markdown("### Vue comparative nationale")

    metric = st.selectbox(
        "Indicateur à comparer",
        [
            "habitants_par_point_financier",
            "habitants_par_agent_mm",
            "ratio_agents_par_point",
            "nb_agents_mm",
            "nb_points_financiers",
        ],
        format_func=lambda x: {
            "habitants_par_point_financier": "Habitants par point financier",
            "habitants_par_agent_mm": "Habitants par agent Mobile Money",
            "ratio_agents_par_point": "Agents Mobile Money / point financier",
            "nb_agents_mm": "Nombre d'agents Mobile Money",
            "nb_points_financiers": "Nombre de points financiers",
        }.get(x, x)
    )

    fig = px.bar(
        indicators.sort_values(metric, ascending=False),
        x="region",
        y=metric,
        title=f"Comparaison — {metric}",
        labels={"region": "Région", metric: metric},
        color_discrete_sequence=[COLORS["navy"]]
    )
    fig.update_layout(height=420, plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Données territoriales")
    st.dataframe(current, use_container_width=True, hide_index=True)