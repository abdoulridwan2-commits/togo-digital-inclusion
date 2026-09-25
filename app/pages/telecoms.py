"""
Page TÉLÉCOMS
"""

import streamlit as st
import plotly.express as px

from app.data.loader import load_telecoms
from app.config.theme import COLORS


def render():
    st.markdown("## 📡 Télécommunications")
    st.caption("Abonnés, télédensité, chiffre d'affaires, investissements et parts de marché.")

    df = load_telecoms()

    if df is None or df.empty:
        st.warning("Données télécoms non disponibles.")
        return

    if "indicateur" not in df.columns:
        st.error("La colonne `indicateur` est absente du fichier télécoms.")
        return

    # --------------------------------------------------------
    # 1. ABONNÉS
    # --------------------------------------------------------
    st.markdown("### 1. Abonnés")

    st.markdown("""
    **Introduction**  
    Évolution du nombre total d'abonnés (fixe + mobile).
    """)

    abonnes = df[df["indicateur"].str.contains("nombre total d'abonnés fixe et mobile", case=False, na=False)].copy()

    if not abonnes.empty:
        fig = px.line(
            abonnes, x="date", y="value", markers=True,
            labels={"date": "Année", "value": "Abonnés"},
            title="Nombre total d'abonnés (fixe + mobile)"
        )
        fig.update_traces(line=dict(color=COLORS["navy"], width=3))
        fig.update_layout(height=400, plot_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Commentaire**  
        La courbe montre l'évolution du parc total d'abonnés sur la période disponible.

        **Conclusion**  
        Le marché de la téléphonie mobile est mature.

        **Piste d'action**  
        L'enjeu n'est plus l'accès au mobile, mais le passage vers Internet et les services numériques.
        """)
    else:
        st.info("Indicateur d'abonnés totaux non trouvé dans les données.")

    st.markdown("---")

    # --------------------------------------------------------
    # 2. TÉLÉDENSITÉ + CA
    # --------------------------------------------------------
    st.markdown("### 2. Télédensité et chiffre d'affaires")

    col1, col2 = st.columns(2)

    teledensite = df[df["indicateur"].str.contains("télédensité mobile", case=False, na=False)].copy()
    with col1:
        st.markdown("**Télédensité mobile**")
        if not teledensite.empty:
            fig2 = px.line(
                teledensite, x="date", y="value", markers=True,
                labels={"date": "Année", "value": "Télédensité (%)"},
                title="Télédensité mobile GSM (%)"
            )
            fig2.update_layout(height=350, plot_bgcolor="white")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Donnée de télédensité non trouvée.")

    ca = df[df["indicateur"].str.contains("chiffres d'affaires", case=False, na=False)].copy()
    with col2:
        st.markdown("**Chiffre d'affaires**")
        if not ca.empty:
            fig3 = px.bar(
                ca, x="date", y="value",
                labels={"date": "Année", "value": "FCFA"},
                title="Chiffre d'affaires (FCFA)"
            )
            fig3.update_layout(height=350, plot_bgcolor="white")
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Donnée de chiffre d'affaires non trouvée.")

    st.markdown("---")

    # --------------------------------------------------------
    # 3. INVESTISSEMENTS
    # --------------------------------------------------------
    st.markdown("### 3. Investissements")

    inv = df[df["indicateur"].str.contains("investissement", case=False, na=False)].copy()
    if not inv.empty:
        fig_inv = px.bar(
            inv, x="date", y="value",
            labels={"date": "Année", "value": "FCFA"},
            title="Investissements (FCFA)"
        )
        fig_inv.update_layout(height=350, plot_bgcolor="white")
        st.plotly_chart(fig_inv, use_container_width=True)

        st.markdown("""
        **Commentaire**  
        Les investissements recensés dans les données sont présentés tels quels.

        **Conclusion**  
        L'interprétation doit rester prudente faute de détail sur la nature exacte des investissements.

        **Piste d'action**  
        Croiser ces données avec le déploiement des technologies (3G, 4G, fibre) lorsque disponibles.
        """)
    else:
        st.info("Donnée d'investissements non trouvée.")

    st.markdown("---")

    # --------------------------------------------------------
    # 4. PARTS DE MARCHÉ
    # --------------------------------------------------------
    st.markdown("### 4. Parts de marché des opérateurs")

    st.markdown("""
    **Introduction**  
    Répartition des parts de marché en abonnés entre les opérateurs présents dans les données.
    """)

    parts = df[df["indicateur"].str.contains("part de marché", case=False, na=False)].copy()
    if not parts.empty:
        fig4 = px.line(
            parts, x="date", y="value", color="indicateur", markers=True,
            labels={"date": "Année", "value": "Part de marché (%)", "indicateur": "Opérateur"}
        )
        fig4.update_layout(height=400, plot_bgcolor="white", legend_title_text="")
        st.plotly_chart(fig4, use_container_width=True)

        st.markdown("""
        **Commentaire**  
        Les parts de marché sont affichées telles que recensées dans les sources.

        **Conclusion**  
        Le marché mobile est structuré autour des opérateurs présents dans les données.

        **Piste d'action**  
        Suivre l'évolution des parts de marché en lien avec le déploiement des services numériques.
        """)
    else:
        st.info("Données de parts de marché non trouvées.")