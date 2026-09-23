"""
Module de nettoyage et d'harmonisation des sources de données
Togo Digital & Financial Inclusion
"""

import pandas as pd
from pathlib import Path

# Chemins
RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_population() -> pd.DataFrame:
    """Charge et nettoie le fichier population 2022."""
    df = pd.read_csv(RAW_DIR / "population_2022.csv")
    
    # Nettoyage basique
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    
    # On garde uniquement les lignes Total
    if "sexe" in df.columns:
        df = df[df["sexe"].str.lower() == "total"].copy()
    
    # Conversion de la valeur en numérique
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    
    return df


def load_telecoms() -> pd.DataFrame:
    """Charge les données télécoms."""
    df = pd.read_csv(RAW_DIR / "telecoms_abonnes.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    
    return df


def load_internet_abonnes() -> pd.DataFrame:
    """Charge les abonnés Internet par technologie."""
    df = pd.read_csv(RAW_DIR / "internet_abonnes.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    
    return df


def load_internet_penetration() -> pd.DataFrame:
    """Charge le taux de pénétration Internet (% population)."""
    df = pd.read_csv(RAW_DIR / "internet_penetration.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    
    df = df.dropna(subset=["value"])
    
    return df


def load_agents_mobile_money() -> pd.DataFrame:
    """Charge les agents Mobile Money."""
    df = pd.read_csv(RAW_DIR / "agents_mobile_money.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    
    rename_map = {
        "region_nom_bdd": "region",
        "prefecture_nom_bdd": "prefecture",
        "commune_nom_bdd": "commune",
        "canton_nom_bdd": "canton",
    }
    df = df.rename(columns=rename_map)
    
    return df


def load_etablissements_financiers() -> pd.DataFrame:
    """Charge les établissements financiers."""
    df = pd.read_csv(RAW_DIR / "etablissements_financiers.csv")
    df.columns = [c.strip().lower() for c in df.columns]
    
    rename_map = {
        "region_nom_bdd": "region",
        "prefecture_nom_bdd": "prefecture",
        "commune_nom_bdd": "commune",
        "canton_nom_bdd": "canton",
        "activite_categorie": "categorie",
    }
    df = df.rename(columns=rename_map)
    
    return df


def run_audit():
    """Lance un audit rapide de toutes les sources."""
    print("=" * 60)
    print("AUDIT DES SOURCES DE DONNÉES")
    print("=" * 60)
    
    sources = {
        "Population 2022": load_population,
        "Télécoms": load_telecoms,
        "Internet abonnés": load_internet_abonnes,
        "Pénétration Internet": load_internet_penetration,
        "Agents Mobile Money": load_agents_mobile_money,
        "Établissements financiers": load_etablissements_financiers,
    }
    
    for name, loader in sources.items():
        print(f"\n>>> {name}")
        try:
            df = loader()
            print(f"    Lignes     : {len(df)}")
            print(f"    Colonnes   : {list(df.columns)}")
            print(f"    Valeurs manquantes : {df.isna().sum().sum()}")
        except Exception as e:
            print(f"    ERREUR : {e}")
    
    print("\n" + "=" * 60)
    print("Audit terminé.")
    print("=" * 60)


def save_processed_data():
    """Sauvegarde les données nettoyées dans data/processed/."""
    
    print("\nSauvegarde des données nettoyées...")
    
    pop = load_population()
    pop.to_csv(PROCESSED_DIR / "population_clean.csv", index=False)
    print("  ✓ population_clean.csv")
    
    telecoms = load_telecoms()
    telecoms.to_csv(PROCESSED_DIR / "telecoms_clean.csv", index=False)
    print("  ✓ telecoms_clean.csv")
    
    internet = load_internet_abonnes()
    internet.to_csv(PROCESSED_DIR / "internet_abonnes_clean.csv", index=False)
    print("  ✓ internet_abonnes_clean.csv")
    
    penetration = load_internet_penetration()
    penetration.to_csv(PROCESSED_DIR / "internet_penetration_clean.csv", index=False)
    print("  ✓ internet_penetration_clean.csv")
    
    agents = load_agents_mobile_money()
    agents.to_csv(PROCESSED_DIR / "agents_mobile_money_clean.csv", index=False)
    print("  ✓ agents_mobile_money_clean.csv")
    
    etabs = load_etablissements_financiers()
    etabs.to_csv(PROCESSED_DIR / "etablissements_financiers_clean.csv", index=False)
    print("  ✓ etablissements_financiers_clean.csv")
    
    print("\nToutes les données nettoyées ont été sauvegardées dans data/processed/")


if __name__ == "__main__":
    run_audit()
    save_processed_data()