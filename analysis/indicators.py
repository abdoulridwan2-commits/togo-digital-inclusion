"""
Module de calcul des indicateurs
Togo Digital & Financial Inclusion
"""

import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path("data/processed")


def load_clean_data():
    """Charge les données nettoyées."""
    population = pd.read_csv(PROCESSED_DIR / "population_clean.csv")
    agents = pd.read_csv(PROCESSED_DIR / "agents_mobile_money_clean.csv")
    etabs = pd.read_csv(PROCESSED_DIR / "etablissements_financiers_clean.csv")
    return population, agents, etabs


def get_population_by_region(population: pd.DataFrame) -> pd.DataFrame:
    """
    Extrait la population au niveau région.
    On garde uniquement les lignes qui correspondent aux 5 régions.
    """
    # Liste officielle des régions
    regions = ["SAVANES", "KARA", "CENTRALE", "PLATEAUX", "MARITIME"]
    
    # Filtrer les lignes qui sont des régions
    pop = population[
        population["découpage_administratif"].str.upper().isin(regions)
    ].copy()
    
    # Harmoniser le nom de la colonne
    pop = pop.rename(columns={
        "découpage_administratif": "region",
        "value": "population"
    })
    
    # Mettre en forme standard (première lettre majuscule)
    pop["region"] = pop["region"].str.title()
    
    # Garder uniquement les colonnes utiles
    pop = pop[["region", "population"]].drop_duplicates()
    
    return pop


def count_points_by_territory(df: pd.DataFrame, level: str = "region") -> pd.DataFrame:
    """Compte le nombre de points par territoire."""
    counts = df.groupby(level).size().reset_index(name="nb_points")
    return counts


def build_territorial_indicators():
    """
    Construit les indicateurs territoriaux :
    - Population
    - Nombre d'agents Mobile Money
    - Nombre de points financiers
    - Habitants / agent Mobile Money
    - Habitants / point financier
    - Ratio agents MM / points financiers
    """
    population, agents, etabs = load_clean_data()
    
    # 1. Population par région
    pop_region = get_population_by_region(population)
    
    # 2. Agents par région
    agents_by_region = count_points_by_territory(agents, level="region")
    agents_by_region = agents_by_region.rename(columns={"nb_points": "nb_agents_mm"})
    agents_by_region["region"] = agents_by_region["region"].str.title()
    
    # 3. Établissements financiers par région
    etabs_by_region = count_points_by_territory(etabs, level="region")
    etabs_by_region = etabs_by_region.rename(columns={"nb_points": "nb_points_financiers"})
    etabs_by_region["region"] = etabs_by_region["region"].str.title()
    
    # 4. Fusion de tout
    indicators = pop_region.merge(agents_by_region, on="region", how="outer")
    indicators = indicators.merge(etabs_by_region, on="region", how="outer")
    
    # Remplir les valeurs manquantes
    indicators["nb_agents_mm"] = indicators["nb_agents_mm"].fillna(0).astype(int)
    indicators["nb_points_financiers"] = indicators["nb_points_financiers"].fillna(0).astype(int)
    indicators["population"] = indicators["population"].fillna(0).astype(int)
    
    # 5. Calcul des ratios
    indicators["habitants_par_agent_mm"] = indicators.apply(
        lambda row: round(row["population"] / row["nb_agents_mm"])
        if row["nb_agents_mm"] > 0 else None,
        axis=1
    )
    
    indicators["habitants_par_point_financier"] = indicators.apply(
        lambda row: round(row["population"] / row["nb_points_financiers"])
        if row["nb_points_financiers"] > 0 else None,
        axis=1
    )
    
    indicators["ratio_agents_par_point"] = indicators.apply(
        lambda row: round(row["nb_agents_mm"] / row["nb_points_financiers"], 2)
        if row["nb_points_financiers"] > 0 else None,
        axis=1
    )
    
    # Ordre des colonnes
    indicators = indicators[[
        "region",
        "population",
        "nb_agents_mm",
        "nb_points_financiers",
        "habitants_par_agent_mm",
        "habitants_par_point_financier",
        "ratio_agents_par_point"
    ]]
    
    return indicators


def run_indicators():
    """Affiche et sauvegarde les indicateurs."""
    print("=" * 70)
    print("INDICATEURS TERRITORIAUX (avec population)")
    print("=" * 70)
    
    indicators = build_territorial_indicators()
    
    print("\n")
    print(indicators.to_string(index=False))
    
    # Sauvegarde
    indicators.to_csv(PROCESSED_DIR / "indicateurs_region.csv", index=False)
    print("\n✓ Fichier sauvegardé : data/processed/indicateurs_region.csv")
    
    return indicators


if __name__ == "__main__":
    run_indicators()