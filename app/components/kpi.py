"""
Composants KPI
"""

import streamlit as st


def format_number(value):
    if value is None:
        return "—"
    try:
        import pandas as pd
        if pd.isna(value):
            return "—"
        return f"{float(value):,.0f}".replace(",", " ")
    except Exception:
        return str(value)


def format_decimal(value, decimals=1):
    if value is None:
        return "—"
    try:
        import pandas as pd
        if pd.isna(value):
            return "—"
        return f"{float(value):,.{decimals}f}".replace(",", " ")
    except Exception:
        return str(value)


def render_kpi_row(items: list):
    """
    Affiche une ligne de KPI.
    items = [("Label", value), ...]
    """
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        with col:
            if isinstance(value, float) and value < 1000:
                st.metric(label, format_decimal(value))
            else:
                st.metric(label, format_number(value))