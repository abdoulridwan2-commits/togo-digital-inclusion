"""
Configuration globale du projet
Togo Digital & Financial Inclusion
"""

from pathlib import Path

# Chemins
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT_DIR / "data" / "raw"
DATA_PROCESSED = ROOT_DIR / "data" / "processed"
ASSETS_DIR = ROOT_DIR / "assets"

# Noms des fichiers processed
FILES = {
    "indicateurs": "indicateurs_region.csv",
    "internet_penetration": "internet_penetration_clean.csv",
    "internet_abonnes": "internet_abonnes_clean.csv",
    "telecoms": "telecoms_clean.csv",
    "etablissements": "etablissements_financiers_clean.csv",
    "agents": "agents_mobile_money_clean.csv",
    "population": "population_clean.csv",
}

# Navigation
PAGES = [
    "🏠 ACCUEIL",
    "📊 VUE NATIONALE",
    "🌐 INTERNET",
    "📡 TÉLÉCOMS",
    "🏦 FINANCE",
    "👥 POPULATION",
    "🗺️ TERRITOIRES",
    "🎯 ACTIONS",
    "📚 MÉTHODE",
]

# Hiérarchie territoriale
GEO_LEVELS = ["National", "Région", "Préfecture", "Commune", "Canton"]