"""
Filtres territoriaux en cascade
Région → Préfecture → Commune
"""

import streamlit as st
import pandas as pd


def render_geo_filters(df: pd.DataFrame, key_prefix: str = "geo"):
    """
    Affiche des filtres en cascade.
    Retourne le DataFrame filtré + les sélections.
    """
    if df is None or df.empty:
        return df, {}

    # Normaliser les noms de colonnes éventuels
    col_region = "region" if "region" in df.columns else None
    col_pref = "prefecture" if "prefecture" in df.columns else None
    col_com = "commune" if "commune" in df.columns else None

    if col_region is None:
        return df, {}

    regions = ["Toutes"] + sorted(df[col_region].dropna().unique().tolist())
    region = st.selectbox("Région", regions, key=f"{key_prefix}_region")

    filtered = df.copy()
    if region != "Toutes":
        filtered = filtered[filtered[col_region] == region]

    prefecture = "Toutes"
    if col_pref and not filtered.empty:
        prefs = ["Toutes"] + sorted(filtered[col_pref].dropna().unique().tolist())
        prefecture = st.selectbox("Préfecture", prefs, key=f"{key_prefix}_pref")
        if prefecture != "Toutes":
            filtered = filtered[filtered[col_pref] == prefecture]

    commune = "Toutes"
    if col_com and not filtered.empty:
        coms = ["Toutes"] + sorted(filtered[col_com].dropna().unique().tolist())
        commune = st.selectbox("Commune", coms, key=f"{key_prefix}_com")
        if commune != "Toutes":
            filtered = filtered[filtered[col_com] == commune]

    selections = {
        "region": region,
        "prefecture": prefecture,
        "commune": commune,
    }
    return filtered, selections