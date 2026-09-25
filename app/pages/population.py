"""
Page POPULATION
"""

import streamlit as st
import plotly.express as px
import pandas as pd

from app.data.loader import load_population, load_indicateurs
from app.components.kpi import format_number
from app.config.theme import COLORS


def render():
    st.markdown("## 👥 Population")
    st.caption("Répartition de la population selon le découpage administratif disponible.")

    pop = load_population()
    indicators = load_indicateurs()

    # --------------------------------------------------------
    # KPI nationaux (depuis indicateurs région pour éviter le double comptage)
    # --------------------------------------------------------
    st.markdown("### Vue nationale")

    if indicators is not None and not indicators.empty:
        total = indicators["population"].sum()
        st.metric("Population totale (somme des régions 2022)", format_number(total))
    else:
        st.warning("Indicateurs de population non disponibles.")
        return

    st.markdown("---")

    # --------------------------------------------------------
    # Population par région
    # --------------------------------------------------------
    st.markdown("### Population par région")

    st.markdown("""
    **Introduction**  
    Répartition de la population résidente par région administrative.
    Les totaux sont issus des indicateurs régionaux harmonisés 
    (évite le double comptage des niveaux hiérarchiques).
    """)

    fig = px.bar(
        indicators.sort_values("population", ascending=False),
        x="region",
        y="population",
        title="Population par région (2022)",
        labels={"region": "Région", "population": "Population"},
        color_discrete_sequence=[COLORS["navy"]]
    )
    fig.update_layout(height=400, plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        indicators[["region", "population"]].sort_values("population", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    max_region = indicators.loc[indicators["population"].idxmax()]
    min_region = indicators.loc[indicators["population"].idxmin()]

    st.markdown(f"""
    **Commentaire**  
    La région la plus peuplée est **{max_region['region']}** 
    ({format_number(max_region['population'])} habitants).  
    La région la moins peuplée est **{min_region['region']}** 
    ({format_number(min_region['population'])} habitants).

    **Conclusion**  
    La population est inégalement répartie entre les régions.

    **Piste d'action**  
    Croiser ces volumes de population avec la densité des points 
    d'accès financiers et numériques pour identifier les territoires 
    à forte pression.
    """)

    st.markdown("---")

    # --------------------------------------------------------
    # Détail du fichier population (si disponible)
    # --------------------------------------------------------
    if pop is not None and not pop.empty:
        st.markdown("### Détail du fichier population source")

        st.markdown("""
        **Introduction**  
        Aperçu des colonnes disponibles dans le fichier population nettoyé.
        Attention : ce fichier contient plusieurs niveaux administratifs.
        Il ne faut **jamais** additionner tous les niveaux ensemble 
        (risque de double comptage).
        """)

        st.write("Colonnes disponibles :", list(pop.columns))
        st.write(f"Nombre de lignes : {len(pop)}")

        # Afficher un échantillon
        st.markdown("#### Échantillon des données")
        st.dataframe(pop.head(20), use_container_width=True, hide_index=True)

        st.info(
            "Pour les analyses territoriales, on utilise les totaux régionaux "
            "déjà harmonisés dans `indicateurs_region.csv` afin d'éviter "
            "tout double comptage lié à la hiérarchie administrative."
        )
    else:
        st.info("Fichier population_clean.csv non trouvé. Les totaux régionaux restent disponibles via les indicateurs.")