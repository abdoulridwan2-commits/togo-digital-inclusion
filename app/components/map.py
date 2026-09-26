"""
Composant cartographique interactif haute performance
Togo Digital & Financial Inclusion
Supporte Plotly Mapbox (OpenStreetMap) et Folium (Clusters & Heatmaps)
"""

import re
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Coordonnées du centre géographique du Togo
TOGO_CENTER = {"lat": 8.6195, "lon": 0.8248}
DEFAULT_ZOOM = 6.8


def parse_point(geom):
    """Extrait lon, lat depuis POINT (x y)."""
    if pd.isna(geom):
        return None, None
    match = re.search(r"POINT\s*\(\s*([-\d.]+)\s+([-\d.]+)\s*\)", str(geom))
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None


def add_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute colonnes lon, lat à partir de geometry si non présentes."""
    if df is None or df.empty:
        return df
    out = df.copy()
    if "lon" not in out.columns or "lat" not in out.columns:
        if "geometry" in out.columns:
            coords = out["geometry"].map(parse_point)
            out["lon"] = [c[0] for c in coords]
            out["lat"] = [c[1] for c in coords]
    out = out.dropna(subset=["lon", "lat"])
    return out


def render_interactive_map(
    df: pd.DataFrame,
    title: str = "Carte de couverture territoriale",
    color_col: str = None,
    max_points: int = 5000,
    point_type: str = "agent"
):
    """
    Affiche une carte géographique interactive avec tuiles OpenStreetMap / Carto.
    Propose un mode Vue Points et un mode Carte de Chaleur (Densité).
    """
    if df is None or df.empty:
        st.info("Aucun point géolocalisé disponible pour cette sélection.")
        return

    plot_df = add_coordinates(df)
    if plot_df.empty:
        st.info("Coordonnées GPS introuvables pour ces données.")
        return

    # Contrôles de visualisation
    map_col1, map_col2, map_col3 = st.columns([2, 2, 2])
    with map_col1:
        map_style = st.selectbox(
            "Style de carte",
            ["open-street-map", "carto-positron", "carto-darkmatter"],
            key=f"map_style_{title[:10]}"
        )
    with map_col2:
        view_type = st.radio(
            "Mode d'affichage",
            ["Points individuels", "Densité (Heatmap)"],
            horizontal=True,
            key=f"view_type_{title[:10]}"
        )
    with map_col3:
        if len(plot_df) > max_points:
            sample_size = st.slider(
                "Échantillon (performance)",
                min_value=1000,
                max_value=min(len(plot_df), 10000),
                value=max_points,
                step=1000,
                key=f"sample_{title[:10]}"
            )
            plot_df = plot_df.sample(sample_size, random_state=42)
            st.caption(f"Affichage de {sample_size:,} sur {len(df):,} points")

    hover_cols = [c for c in ["region", "prefecture", "commune", "canton", "operateur_clean", "categorie_clean", "etab_nom"] if c in plot_df.columns]

    # Compatibilité Plotly (v6+ utilise scatter_map/density_map avec map_style, v5- utilise scatter_mapbox/density_mapbox avec mapbox_style)
    use_new_map_api = hasattr(px, "scatter_map")
    style_kwarg = {"map_style": map_style} if use_new_map_api else {"mapbox_style": map_style}

    if view_type == "Densité (Heatmap)":
        density_func = px.density_map if use_new_map_api else px.density_mapbox
        fig = density_func(
            plot_df,
            lat="lat",
            lon="lon",
            radius=12,
            center=TOGO_CENTER,
            zoom=DEFAULT_ZOOM,
            title=f"{title} · Carte de chaleur de densité",
            color_continuous_scale="Viridis",
            **style_kwarg
        )
    else:
        color = color_col if (color_col and color_col in plot_df.columns) else None
        
        # Palette de couleurs personnalisée
        color_map = {
            "Togocom (T-Money)": "#0B3D5C",
            "Moov Africa (Flooz)": "#E05A47",
            "Multi-opérateur (Togocom + Moov)": "#136F63",
            "Non spécifié": "#8B95A5",
            "Banque Commerciale": "#0F2C59",
            "Microfinance / SFD": "#136F63",
            "Mutuelle d'Épargne": "#D4AF37",
            "Assurance": "#9C27B0",
            "Autre": "#78909C"
        }
        
        scatter_func = px.scatter_map if use_new_map_api else px.scatter_mapbox
        fig = scatter_func(
            plot_df,
            lat="lat",
            lon="lon",
            color=color,
            color_discrete_map=color_map if color else None,
            hover_name=hover_cols[0] if hover_cols else None,
            hover_data={c: True for c in hover_cols},
            center=TOGO_CENTER,
            zoom=DEFAULT_ZOOM,
            title=title,
            opacity=0.75,
            size_max=8,
            **style_kwarg
        )
        fig.update_traces(marker=dict(size=6))

    fig.update_layout(
        height=620,
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255,255,255,0.85)"
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def render_points_map(df: pd.DataFrame, title: str = "Carte des points", color_col: str = None, max_points: int = 4000):
    """Alias rétro-compatible qui redirige vers la carte interactive enrichie."""
    render_interactive_map(df, title=title, color_col=color_col, max_points=max_points)