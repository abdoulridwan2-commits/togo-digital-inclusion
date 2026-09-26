"""
Composants KPI stylisés et interactifs
Togo Digital & Financial Inclusion
"""

import streamlit as st
import pandas as pd


def format_number(value):
    if value is None:
        return "—"
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.0f}".replace(",", " ")
    except Exception:
        return str(value)


def format_decimal(value, decimals=1):
    if value is None:
        return "—"
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.{decimals}f}".replace(",", " ")
    except Exception:
        return str(value)


def render_kpi_row(items: list):
    """
    Affiche une ligne de KPI responsive.
    items = [("Label", value, optional_help_or_delta), ...]
    """
    cols = st.columns(len(items))
    for i, col in enumerate(cols):
        item = items[i]
        label = item[0]
        value = item[1]
        delta = item[2] if len(item) > 2 else None
        
        with col:
            val_str = (
                format_decimal(value)
                if isinstance(value, float) and value < 1000
                else format_number(value)
            )
            if delta:
                st.metric(label, val_str, delta=delta)
            else:
                st.metric(label, val_str)


def render_custom_card(title: str, value: str, subtitle: str = "", badge: str = None, color: str = "#0B3D5C"):
    """Rendu d'une carte métrique premium avec bordure thématique."""
    badge_html = f'<span style="background:{color}22; color:{color}; font-weight:700; font-size:0.75rem; padding:3px 8px; border-radius:12px; float:right;">{badge}</span>' if badge else ""
    st.markdown(f"""
    <div style="background:white; border-radius:14px; padding:1.2rem; border:1px solid #E2E8F0; border-top:4px solid {color}; box-shadow:0 3px 10px rgba(0,0,0,0.04); margin-bottom:10px;">
        {badge_html}
        <div style="font-size:0.82rem; font-weight:700; color:#526174; text-transform:uppercase; letter-spacing:0.04em;">{title}</div>
        <div style="font-size:1.85rem; font-weight:800; color:{color}; margin:0.3rem 0;">{value}</div>
        <div style="font-size:0.8rem; color:#78909C;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)