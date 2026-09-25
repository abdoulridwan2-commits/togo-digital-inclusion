"""
Page MÉTHODE
"""

import streamlit as st
import pandas as pd

from app.config.settings import DATA_PROCESSED, FILES


def render():
    st.markdown("## 📚 Méthode")
    st.caption("Sources, définitions, formules et limites.")

    st.markdown("""
    <div class="card">
        <div class="card-title">Pourquoi cette page est importante ?</div>
        <div class="card-text">
            Un dashboard professionnel ne présente pas seulement des graphiques.
            Il doit permettre de comprendre d'où viennent les chiffres,
            comment ils sont calculés et quelles sont leurs limites.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Sources intégrées")
    sources = pd.DataFrame({
        "Jeu de données": [
            "Population 2022",
            "Agents Mobile Money",
            "Établissements financiers",
            "Télécommunications (ARCEP)",
            "Abonnés Internet (ARCEP)",
            "Utilisation d'Internet",
        ],
        "Rôle": [
            "Population des territoires",
            "Réseau d'agents géolocalisés",
            "Réseau financier physique",
            "Marché télécom",
            "Technologies et abonnements Internet",
            "Adoption d'Internet (% population)",
        ],
    })
    st.dataframe(sources, use_container_width=True, hide_index=True)

    st.markdown("### Indicateurs calculés")
    formulas = pd.DataFrame({
        "Indicateur": [
            "Habitants / agent Mobile Money",
            "Habitants / point financier",
            "Agents Mobile Money / point financier",
        ],
        "Formule": [
            "Population ÷ nombre d'agents MM",
            "Population ÷ nombre de points financiers",
            "Nombre d'agents MM ÷ nombre de points financiers",
        ],
        "Interprétation": [
            "Densité relative du réseau d'agents",
            "Pression relative sur le réseau physique",
            "Rapport entre les deux types de réseau",
        ],
    })
    st.dataframe(formulas, use_container_width=True, hide_index=True)

    st.info(
        "Ces indicateurs mesurent la présence et la densité relative. "
        "Ils ne constituent pas un score d'inclusion financière."
    )

    st.markdown("### Limites déclarées")
    for limit in [
        "Les périodes de référence peuvent varier selon les sources.",
        "Un agent Mobile Money n'est pas équivalent à une agence bancaire.",
        "La présence géographique ne mesure pas l'activité réelle.",
        "Les ratios ne constituent pas un score global d'inclusion.",
        "Une corrélation ne prouve pas une causalité.",
        "Les recommandations doivent être complétées par des données locales.",
    ]:
        st.markdown(f"- {limit}")

    st.markdown("### Disponibilité des fichiers")
    status_rows = []
    for key, filename in FILES.items():
        path = DATA_PROCESSED / filename
        status_rows.append({
            "Fichier": filename,
            "Statut": "✅ Disponible" if path.exists() else "❌ Manquant",
        })
    st.dataframe(pd.DataFrame(status_rows), use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="observation">
        <strong>Règle de qualité</strong><br><br>
        Aucun chiffre n'est inventé. Lorsqu'une donnée n'est pas disponible,
        le dashboard l'indique clairement.
    </div>
    """, unsafe_allow_html=True)