"""
Page ACTIONS — Feuille de Route Stratégique & Matrice de Priorisation
Togo Digital & Financial Inclusion
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.data.loader import load_indicateurs, load_internet_penetration, load_indicateurs_prefectures
from app.components.kpi import format_number, format_decimal
from app.config.theme import COLORS


def render():
    st.markdown("## 🎯 Matrice d'Actions & Recommandations 2026-2030")
    st.caption("Traduire les données probantes en plans d'intervention ciblés et mesurables.")

    indicators = load_indicateurs(mode="6_territoires")
    internet = load_internet_penetration()
    prefectures = load_indicateurs_prefectures()

    if indicators is None or indicators.empty:
        st.warning("Indicateurs territoriaux requis pour afficher cette section.")
        return

    # --------------------------------------------------------
    # 1. Matrice de Priorisation Territoriale
    # --------------------------------------------------------
    st.markdown("### 1. Matrice de Priorité d'Intervention")
    
    st.markdown("""
    En croisant le **volume de population résidente**, la **pression par point financier** et l'**indice d'inclusion IDNF**, 
    nous classons les territoires togolais selon leur niveau d'urgence :
    """)

    priority_rows = []
    territory_col = "territoire" if "territoire" in indicators.columns else "region"
    
    for _, row in indicators.iterrows():
        t = row[territory_col]
        score = row.get("score_inclusion", 50)
        hab_pt = row["habitants_par_point_financier"]
        
        if score < 45 or hab_pt > 15000:
            niveau = "🔴 Priorité 1 : Urgence Haute"
            action_cle = "Déploiement d'urgence de points physiques fixes et kiosques bancaires"
        elif score < 65 or hab_pt > 10000:
            niveau = "🟡 Priorité 2 : Vigilance / Consolidation"
            action_cle = "Densification des agents MM et encouragement de la microfinance"
        else:
            niveau = "🟢 Priorité 3 : Territoire Avancé"
            action_cle = "Diversification vers les services financiers numériques complexes (crédit, épargne)"
            
        priority_rows.append({
            "Territoire": t,
            "Population": format_number(row["population"]),
            "Charge / Point": f"{format_number(hab_pt)} hab.",
            "Score IDNF": f"{score:.1f} / 100",
            "Niveau d'Urgence": niveau,
            "Axe d'Intervention Prioritaire": action_cle
        })

    st.dataframe(pd.DataFrame(priority_rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 2. Les 4 Axes Stratégiques Fondés sur les Données
    # --------------------------------------------------------
    st.markdown("### 2. Piliers d'intervention opérationnelle")

    c1, c2 = st.columns(2)

    with c1:
        latest_net = internet.iloc[-1]["value"] if (internet is not None and not internet.empty) else 37.6
        st.markdown(f"""
        <div class="recommendation">
            <h4 style="color:#065F46; margin-top:0;">AXE 1 · Démocratiser l'Accès Internet & la Data</h4>
            <b>Donnée probante :</b> Taux d'usage Internet à <strong>{latest_net:.1f}%</strong> (62% de non-utilisateurs).<br><br>
            <b>Objectifs opérationnels :</b><br>
            • Inciter à la baisse des tarifs de connectivité data mobile par l'ARCEP.<br>
            • Déployer des points Wi-Fi communautaires gratuits autour des mairies et marchés ruraux.<br>
            • Généraliser les terminaux 4G low-cost par des partenariats public-privé.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="recommendation">
            <h4 style="color:#065F46; margin-top:0;">AXE 3 · Résorption des Déserts Bancaires</h4>
            <b>Donnée probante :</b> Plus de 15 préfectures togolaises sans aucune banque commerciale.<br><br>
            <b>Objectifs opérationnels :</b><br>
            • Incitations fiscales pour l'installation d'agences bancaires et de GAB dans les chefs-lieux délaissés.<br>
            • Soutien au réseau des Systèmes Financiers Décentralisés (SFD / Microfinances) pour combler le vide bancaire.<br>
            • Création d'agences bancaires mobiles itinérantes sur les grands marchés forains.
        </div>
        """, unsafe_allow_html=True)

    with c2:
        dominant = indicators.loc[indicators["ratio_agents_par_point"].idxmax()]
        t_dom = dominant.get("territoire", dominant.get("region"))
        st.markdown(f"""
        <div class="recommendation">
            <h4 style="color:#065F46; margin-top:0;">AXE 2 · Professionnalisation & Liquidité du Mobile Money</h4>
            <b>Donnée probante :</b> Ratio de <strong>{format_decimal(dominant['ratio_agents_par_point'])} agents MM</strong> par point fixe dans les <strong>{t_dom}</strong>.<br><br>
            <b>Objectifs opérationnels :</b><br>
            • Résoudre le goulot d'étranglement de la liquidité (cash-in / cash-out) dans les zones enclavées.<br>
            • Accélérer l'interopérabilité totale et sans frais entre T-Money et Moov Flooz.<br>
            • Sécuriser le statut et les marges des agents ruraux pour éviter la cessation d'activité.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="recommendation">
            <h4 style="color:#065F46; margin-top:0;">AXE 4 · Éducation Financière & Confiance Numérique</h4>
            <b>Donnée probante :</b> Forte utilisation du cash persistant malgré 19 790 agents MM.<br><br>
            <b>Objectifs opérationnels :</b><br>
            • Campagnes d'alphabétisation financière en langues nationales (Éwé, Kabyè, Kotokoli, Moba).<br>
            • Renforcement de la lutte contre les arnaques et fraudes téléphoniques ciblant les usagers vulnérables.<br>
            • Numérisation des aides sociales et des paiements agricoles bord-champ.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 3. Export des Recommandations
    # --------------------------------------------------------
    st.markdown("### 📥 Télécharger le Plan d'Action")
    df_export = pd.DataFrame(priority_rows)
    csv_data = df_export.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📄 Télécharger la Matrice de Priorités (CSV)",
        data=csv_data,
        file_name="togo_matrice_priorites_inclusion_2026.csv",
        mime="text/csv"
    )