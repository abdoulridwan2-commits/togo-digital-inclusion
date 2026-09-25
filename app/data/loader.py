"""
Chargement centralisé des données
"""

from pathlib import Path
import pandas as pd
import streamlit as st

from app.config.settings import DATA_PROCESSED, FILES


def _read_csv(filename: str) -> pd.DataFrame | None:
    path = DATA_PROCESSED / filename
    if not path.exists():
        return None
    return pd.read_csv(path)


@st.cache_data
def load_indicateurs() -> pd.DataFrame | None:
    df = _read_csv(FILES["indicateurs"])
    if df is None:
        return None
    for col in ["population", "nb_agents_mm", "nb_points_financiers",
                "habitants_par_agent_mm", "habitants_par_point_financier", "ratio_agents_par_point"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


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
    return _read_csv(FILES["etablissements"])


@st.cache_data
def load_agents() -> pd.DataFrame | None:
    return _read_csv(FILES["agents"])


@st.cache_data
def load_population() -> pd.DataFrame | None:
    return _read_csv(FILES["population"])