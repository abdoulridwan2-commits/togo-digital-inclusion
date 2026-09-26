"""
Page MÉTHODE — Rigueur Scientifique, Sources & Définitions
Togo Digital & Financial Inclusion
"""

import streamlit as st
import pandas as pd

from app.config.settings import DATA_PROCESSED, FILES


def render():
    st.markdown("## 📚 Méthodologie, Sources & Rigueur Analytique")
    st.caption("Traçabilité des données, clarification du cas Grand Lomé, formules de calcul et limites déclarées.")

    st.markdown("""
    <div class="card">
        <div class="card-title">L'Exigence de Transparence Scientifique</div>
        <div class="card-text">
            Un tableau de bord décisionnel ne se contente pas d'afficher des graphiques : il doit garantir 
            l'intégrité de ses sources, expliciter ses choix d'agrégation territoriale et documenter ses limites.
            Cette page assure la conformité du projet aux standards de l'INSEED, de l'ARCEP et de la BCEAO.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # 1. Traitement critique du District Autonome du Grand Lomé (DAGL)
    # --------------------------------------------------------
    st.markdown("### 1. Note Méthodologique Majeure : Traitement du Grand Lomé & Maritime")
    st.markdown("""
    <div class="observation">
        <strong>Clarification du découpage INSEED RGPH-5 (2022) :</strong><br>
        Le recensement général dénombre <strong>8 095 498 habitants</strong> au Togo répartis comme suit :<br>
        • Savanes (1 143 520) · Kara (985 512) · Centrale (795 529) · Plateaux (1 635 946)<br>
        • <strong>Maritime rurale / périurbaine :</strong> 1 346 615 hab. (Préfectures Zio, Vo, Lacs, Yoto, Avé, Bas-Mono).<br>
        • <strong>Grand Lomé (DAGL) :</strong> 2 188 376 hab. (Préfectures Golfe et Agoè-Nyivé).<br><br>
        <strong>Pourquoi notre approche est rigoureuse :</strong><br>
        Dans de nombreuses analyses hâtives, la population de Lomé (2,19M) est omise du dénominateur tout en conservant 
        ses 8 986 agents Mobile Money au numérateur, ce qui fausse artificiellement les ratios. Notre plateforme permet 
        soit d'analyser Lomé comme un pôle métropolitain distinct, soit de réunifier la Région Maritime à <strong>3 534 991 habitants</strong> 
        (43,7% de la population nationale).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 2. Formules des Indicateurs & Score Composite (IDNF)
    # --------------------------------------------------------
    st.markdown("### 2. Définition des Indicateurs & Indice Synthétique (IDNF)")

    formulas = pd.DataFrame({
        "Indicateur": [
            "Habitants / Agent Mobile Money",
            "Habitants / Point Financier",
            "Ratio Multiplicateur (MM / Point)",
            "Densité MM (/10 000 hab.)",
            "Densité Physique (/100 000 hab.)",
            "Score d'Inclusion Territoriale (IDNF / 100)"
        ],
        "Formule mathématique": [
            "Population ÷ Nombre d'agents MM",
            "Population ÷ Nombre de guichets fixes (Banques + SFD)",
            "Nombre d'agents MM ÷ Nombre de guichets fixes",
            "(Nombre agents MM ÷ Population) × 10 000",
            "(Nombre points fixes ÷ Population) × 100 000",
            "0.60 × Min(100, (Densité MM / 30) × 50) + 0.40 × Min(100, (Densité Fixe / 15) × 50)"
        ],
        "Interprétation & Norme": [
            "Charge de proximité (Optimal < 400 hab/agent)",
            "Pression d'accès bancaire (Critique si > 15 000 hab/point)",
            "Facteur de substitution numérique vs physique",
            "Maillage de proximité pour 10 000 habitants",
            "Capacité d'ancrage bancaire pour 100 000 habitants",
            "Indice composite d'inclusion financière (0 = désert absolu, 100 = inclusion optimale)"
        ]
    })
    st.dataframe(formulas, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 3. Sources Officielles et Fiabilité
    # --------------------------------------------------------
    st.markdown("### 3. Répertoire des Données Intégrées")
    sources = pd.DataFrame({
        "Jeu de données": [
            "Recensement Général (RGPH-5, 2022)",
            "Agents Mobile Money (2022-2024)",
            "Établissements Financiers (2022-2024)",
            "Indicateurs Marché Télécoms (2013-2022)",
            "Abonnements Internet & Technologies",
            "Taux de Pénétration Internet Global"
        ],
        "Source Institutionnelle": [
            "INSEED Togo (Institut National de la Statistique)",
            "Données géospatiales ouvertes / Opérateurs T-Money & Flooz",
            "Banque Centrale des États de l'Afrique de l'Ouest (BCEAO) / Cadastre",
            "ARCEP Togo (Autorité de Régulation des Communications)",
            "ARCEP Togo (Rapports annuels d'activité)",
            "Union Internationale des Télécommunications (UIT) / Banque Mondiale"
        ],
        "Périmètre / Volume": [
            "8 095 498 résidents · 5 régions · 39 préfectures · 117 communes",
            "19 790 agents marchands géolocalisés par GPS",
            "740 agences (Banques, Microfinances, Mutuelles)",
            "Séries chronologiques annuelles",
            "Répartition Fixe, Mobile 3G/4G, Fibre",
            "Historique d'adoption depuis 2000"
        ]
    })
    st.dataframe(sources, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --------------------------------------------------------
    # 4. Limites Déclarées & Éthique de la Donnée
    # --------------------------------------------------------
    st.markdown("### 4. Limites Déclarées & Déontologie de l'Analyse")
    limits = [
        "**Activité vs Présence :** Le recensement géolocalise les points déclarés, mais ne mesure pas leur chiffre d'affaires, leur disponibilité en liquidités (flotte cash) ni leur taux d'inactivité temporaire.",
        "**Hétérogénéité des guichets :** Une succursale de banque commerciale régionale n'a pas les mêmes attributions qu'un point de microfinance ou qu'un kiosque de rue Mobile Money.",
        "**Multi-SIM et multi-comptes :** Les abonnements télécoms et comptes Mobile Money peuvent dépasser la population adulte en raison du multi-équipement.",
        "**Causalité :** Une forte densité d'agents ne crée pas automatiquement la prospérité économique ; elle constitue une condition facilitatrice d'accès aux flux financiers."
    ]
    for lim in limits:
        st.markdown(f"- {lim}")

    st.markdown("""
    <div class="insight">
        <strong>Engagement Qualité :</strong><br>
        Aucune donnée n'a été extrapolée ou altérée. Tous les indicateurs sont calculés de manière déterministe 
        et reproductible par le moteur d'analyse du projet.
    </div>
    """, unsafe_allow_html=True)