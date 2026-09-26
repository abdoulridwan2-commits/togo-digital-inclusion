# 🇹🇬 Togo Digital & Financial Inclusion — Observatoire Décisionnel

[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B.svg)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data](https://img.shields.io/badge/Data-INSEED%20|%20ARCEP%20|%20BCEAO-0B3D5C.svg)]()

> **Plateforme analytique et décisionnelle sur l'inclusion numérique et financière au Togo**, exploitant les données géospatiales de **19 790 agents Mobile Money**, **740 établissements financiers**, le **recensement général RGPH-5 (2022)** et les séries chronologiques de l'**ARCEP Togo**.

---

## 🎯 Question Centrale & Problématique

> *Là où les services financiers physiques sont rares ou absents, dans quelle mesure le Mobile Money constitue-t-il l'infrastructure vitale de relais d'accès aux services financiers au Togo ?*

Bien que moins de **4 personnes sur 10 (37,6%)** utilisent l'Internet haut débit au Togo, le téléphone mobile de base a permis le déploiement d'un réseau de proximité **27 fois plus dense** que l'ensemble des banques et microfinances réunies.

---

## 🌟 Points Forts & Valeur Ajoutée du Projet

1. **Rigueur Démographique & Traitement Scientifique du Grand Lomé (DAGL) :**
   - Intégration de la population officielle exhaustive (**8 095 498 habitants**, RGPH-5 INSEED 2022).
   - Double niveau d'agrégation :
     - **5 Régions officielles unifiées** (avec la Région Maritime à 3,53M hab.).
     - **6 Pôles territoriaux** isolant le District Autonome du Grand Lomé (2,19M hab.) de la Maritime rurale (1,35M hab.) pour révéler la véritable fracture urbain/rural.
2. **Cartographie Interactive Haute Précision :**
   - Cartes dynamiques avec fond **OpenStreetMap** et **CartoDB**.
   - Mode d'affichage par **points individuels** ou par **carte de chaleur (Heatmap)**.
   - Filtres en temps réel par opérateur (*Togocom T-Money vs Moov Africa Flooz*) et par catégorie d'établissement (*Banques Commerciales, Microfinances/SFD, Mutuelles*).
3. **Indice Synthétique d'Inclusion Territoriale (IDNF / 100) :**
   - Un score composite de 0 à 100 benchmarkant objectivement chaque territoire.
4. **Observatoire des Déserts Bancaires :**
   - Identification algorithmique des préfectures sans aucune agence bancaire physique, dépendantes à 100% du Mobile Money.
5. **Simulateur d'Aide à la Décision ("What-If") :**
   - Outil prospectif pour simuler l'impact de nouveaux déploiements d'agents ou de kiosques sur la réduction des charges par habitant et le gain en score d'inclusion.

---

## 🚀 Installation & Lancement

### 1. Prérequis
- Python 3.10 ou supérieur
- Environnement virtuel recommandé

### 2. Installation des dépendances
```bash
# Cloner le dépôt ou se placer dans le dossier du projet
cd togo-digital-inclusion

# Créer et activer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sous Linux/Mac
# ou sous Windows PowerShell :
# .venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
streamlit run app/main.py
```
L'application sera accessible dans votre navigateur à l'adresse : `http://localhost:8501`.

---

## 📁 Architecture du Projet

```
togo-digital-inclusion/
│
├── app/
│   ├── main.py                  # Point d'entrée principal Streamlit
│   ├── analytics/
│   │   └── engine.py            # Moteur analytique central (RGPH-5, IDNF, préfectures)
│   ├── components/
│   │   ├── header.py            # Bannière et identité visuelle togolaise
│   │   ├── navigation.py        # Barre de navigation interactive
│   │   ├── kpi.py               # Cartes KPI stylisées et badges métriques
│   │   ├── map.py               # Cartographie OpenStreetMap & Heatmaps
│   │   └── filters.py           # Filtres territoriaux en cascade
│   ├── config/
│   │   ├── settings.py          # Configuration globale et constantes
│   │   └── theme.py             # Palette de couleurs et styles CSS
│   ├── data/
│   │   └── loader.py            # Chargement centralisé et mise en cache
│   └── pages/
│       ├── accueil.py           # Synthèse exécutive & 3 chiffres clés
│       ├── nationale.py         # Vue macroéconomique et historique
│       ├── internet.py          # Pénétration et technologies Internet
│       ├── telecoms.py          # Abonnements et marché télécom
│       ├── finance.py           # Analyse spatiale banques vs Mobile Money
│       ├── population.py        # Structure démographique RGPH-5
│       ├── territoires.py       # Drill-down préfectoral & déserts bancaires
│       ├── simulateur.py        # Outil décisionnel de simulation d'impact
│       ├── actions.py           # Matrice d'actions prioritaires 2026-2030
│       └── methode.py           # Rigueur méthodologique, sources et formules
│
├── data/
│   ├── raw/                     # Jeux de données sources bruts
│   └── processed/               # Données nettoyées et harmonisées
│
├── analysis/                    # Scripts d'audit et de préparation des données
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation complète
```

---

## 📊 Sources Officielles

| Source | Données | Usage |
| :--- | :--- | :--- |
| **INSEED Togo** | Recensement Général RGPH-5 (2022) | Démographie officielle (8,095M hab.) |
| **ARCEP Togo** | Rapports annuels de régulation | Séries temporelles Internet et Télécoms |
| **BCEAO / Open Data** | Cadastre financier national | 740 établissements financiers géocodés |
| **Opérateurs Télécoms** | Réseaux T-Money et Flooz | 19 790 agents marchands géoréférencés |

---

## 🏆 Équipe & Contribution
Projet développé dans le cadre de l'analyse territoriale pour l'inclusion numérique et financière au Togo (2026).
