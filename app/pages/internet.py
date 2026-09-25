"""
Page INTERNET
"""

import streamlit as st
import plotly.express as px

from app.data.loader import load_internet_penetration, load_internet_abonnes
from app.config.theme import COLORS


def render():
    st.markdown("## 🌐 Internet")
    st.caption("Évolution de l'usage d'Internet, abonnements et technologies.")

    df_pen = load_internet_penetration()
    df_abo = load_internet_abonnes()

    # --------------------------------------------------------
    # 1. PÉNÉTRATION
    # --------------------------------------------------------
    st.markdown("### 1. Pénétration Internet")

    st.markdown("""
    **Introduction**  
    Cet indicateur mesure la part de la population utilisant Internet.
    Il permet d'observer les périodes d'accélération et de stagnation.
    """)

    if df_pen is not None and not df_pen.empty:
        df = df_pen.copy()
        df["variation"] = df["value"].diff()

        latest = df.iloc[-1]
        first = df.iloc[0]
        progress = latest["value"] - first["value"]

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Dernière valeur", f"{latest['value']:.1f}%", f"{int(latest['date'])}")
        c2.metric("Première valeur", f"{first['value']:.1f}%", f"{int(first['date'])}")
        c3.metric("Progression totale", f"+{progress:.1f} points")

        if df["variation"].notna().any():
            max_year = int(df.loc[df["variation"].idxmax(), "date"])
            c4.metric("Plus forte progression", f"{max_year}")

        fig = px.line(
            df, x="date", y="value", markers=True,
            labels={"date": "Année", "value": "% de la population"},
            title="Évolution de la part de la population utilisant Internet"
        )
        fig.update_traces(line=dict(color=COLORS["navy"], width=3), marker=dict(size=7))
        fig.update_layout(height=450, plot_bgcolor="white", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # Variation annuelle
        st.markdown("#### Rythme de progression annuel")
        var_df = df.dropna(subset=["variation"])
        if not var_df.empty:
            fig_var = px.bar(
                var_df, x="date", y="variation",
                labels={"date": "Année", "variation": "Variation (points)"},
                title="Variation annuelle de l'usage d'Internet"
            )
            fig_var.update_layout(height=360, plot_bgcolor="white")
            st.plotly_chart(fig_var, use_container_width=True)

            strongest = df.loc[df["variation"].idxmax()]
            weakest = df.loc[df["variation"].idxmin()]

            st.markdown(f"""
            **Commentaire**  
            La plus forte progression annuelle observée intervient autour de 
            **{int(strongest['date'])}** (+{strongest['variation']:.1f} point(s)).  
            La variation la plus faible est observée autour de **{int(weakest['date'])}**.

            **Conclusion**  
            L'usage d'Internet progresse sur la période disponible, 
            mais reste en dessous de 40 % de la population dans la dernière année.

            **Piste d'action**  
            Accélérer l'accès à la data et les compétences numériques de base, 
            particulièrement dans les zones où la pénétration reste faible.
            """)
    else:
        st.warning("Données de pénétration Internet non disponibles.")

    st.markdown("---")

    # --------------------------------------------------------
    # 2. ABONNÉS & TECHNOLOGIES
    # --------------------------------------------------------
    st.markdown("### 2. Abonnés Internet et technologies")

    st.markdown("""
    **Introduction**  
    Analyse des abonnements Internet et des technologies d'accès 
    présentes dans les données (3G, 4G, FTTH, haut débit, etc.).
    """)

    if df_abo is not None and not df_abo.empty and "indicateur" in df_abo.columns:
        tech_keywords = ["3G", "4G", "FTTH", "fibre", "haut débit", "GPRS", "EDGE", "ADSL", "Wimax"]
        pattern = "|".join(tech_keywords)
        tech = df_abo[df_abo["indicateur"].astype(str).str.contains(pattern, case=False, na=False)].copy()

        if not tech.empty:
            fig_tech = px.line(
                tech, x="date", y="value", color="indicateur", markers=True,
                labels={"date": "Année", "value": "Abonnements", "indicateur": "Technologie"},
                title="Évolution des abonnements par technologie"
            )
            fig_tech.update_layout(height=450, plot_bgcolor="white", legend_title_text="")
            st.plotly_chart(fig_tech, use_container_width=True)

            st.markdown("""
            **Commentaire**  
            Les données disponibles permettent d'observer l'évolution 
            des abonnements selon les technologies recensées.

            **Conclusion**  
            L'analyse des technologies doit rester strictement limitée 
            aux indicateurs présents dans les sources.

            **Piste d'action**  
            Suivre le développement des technologies haut débit 
            (4G, FTTH) comme levier d'accélération de l'usage d'Internet.
            """)
        else:
            st.info("Aucune technologie correspondante n'a été détectée automatiquement dans les données.")

        # Taux de pénétration si disponible
        taux = df_abo[df_abo["indicateur"].astype(str).str.contains("Taux de pénétration", case=False, na=False)].copy()
        if not taux.empty:
            st.markdown("#### Taux de pénétration Internet (données ARCEP)")
            fig_taux = px.line(
                taux, x="date", y="value", color="indicateur", markers=True,
                labels={"date": "Année", "value": "Taux (%)", "indicateur": "Indicateur"}
            )
            fig_taux.update_layout(height=400, plot_bgcolor="white", legend_title_text="")
            st.plotly_chart(fig_taux, use_container_width=True)
    else:
        st.warning("Données d'abonnés Internet non disponibles.")