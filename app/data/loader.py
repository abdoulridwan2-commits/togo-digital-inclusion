"""
Chargement centralisé et enrichi des données
Togo Digital & Financial Inclusion
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from app.config.settings import DATA_PROCESSED, FILES
from app.analytics.engine import (
    get_clean_geodata,
    get_indicators_table,
    get_prefecture_indicators,
    get_population_hierarchy,
)


def _read_csv(filename: str) -> pd.DataFrame | None:
    path = DATA_PROCESSED / filename
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data
def load_indicateurs(mode="5_regions") -> pd.DataFrame | None:
    """Charge les indicateurs consolidés (5_regions ou 6_territoires avec Grand Lomé)."""
    try:
        df = get_indicators_table(mode=mode)
        if df is not None and not df.empty:
            # Compatibilité : s'assurer que la colonne 'region' existe
            if "region" not in df.columns and "territoire" in df.columns:
                df["region"] = df["territoire"]
            return df
    except Exception as e:
        pass
    
    # Fallback vers fichier CSV existant
    df = _read_csv(FILES["indicateurs"])
    if df is None:
        return None
    for col in ["population", "nb_agents_mm", "nb_points_financiers",
                "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


@st.cache_data
def load_indicateurs_prefectures() -> pd.DataFrame:
    """Charge les indicateurs détaillés au niveau préfectoral."""
    return get_prefecture_indicators()


@st.cache_data
def load_internet_penetration() -> pd.DataFrame | None:
    df = _read_csv(FILES["internet_penetration"])
    if df is None:
        return None
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    df = df.dropna(subset=[c for c in ["date", "value"] if c in df.columns])
    if "date" in df.columns:
        df = df.sort_values("date")
    return df


@st.cache_data
def load_internet_abonnes() -> pd.DataFrame | None:
    df = _read_csv(FILES["internet_abonnes"])
    if df is None:
        return None
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    return df


@st.cache_data
def load_telecoms() -> pd.DataFrame | None:
    df = _read_csv(FILES["telecoms"])
    if df is None:
        return None
    if "value" in df.columns:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "date" in df.columns:
        df["date"] = pd.to_numeric(df["date"], errors="coerce")
    return df


@st.cache_data
def load_etablissements() -> pd.DataFrame | None:
    _, etabs = get_clean_geodata()
    if not etabs.empty:
        return etabs
    return _read_csv(FILES["etablissements"])


@st.cache_data
def load_agents() -> pd.DataFrame | None:
    agents, _ = get_clean_geodata()
    if not agents.empty:
        return agents
    return _read_csv(FILES["agents"])


@st.cache_data
def load_population() -> pd.DataFrame | None:
    return _read_csv(FILES["population"])