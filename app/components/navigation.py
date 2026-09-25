"""
Navigation principale
"""

import streamlit as st
from app.config.settings import PAGES


def render_navigation():
    return st.radio(
        "Navigation",
        PAGES,
        horizontal=True,
        label_visibility="collapsed"
    )