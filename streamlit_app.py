import json
import unicodedata

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Strategic Risk Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.55rem;
    }

    .title-section {
        margin-bottom: 2rem;
        border-bottom: 2px solid #E8E8E8;
        padding-bottom: 1.5rem;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #F0F0F0;
        min-height: 110px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .kpi-label {
        font-size: 13px;
        color: #666;
        margin-bottom: 8px;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-number {
        font-size: 36px;
        font-weight: 700;
        color: #1A1A1A;
        margin: 0;
        line-height: 1;
    }

    .kpi-unit {
        font-size: 12px;
        color: #999;
        margin-top: 6px;
    }

    .badge-alto {
        background: #D32F2F;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }

    .badge-medio {
        background: #E74C3C;
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }

    .badge-bajo {
        background: #FADBD8;
        color: #8B4513;
        padding: 6px 14px;
        border-radius: 20px;
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        text-align: center;
    }

    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 1rem;
        margin-top: 0;
    }

    .container-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        border: 1px solid #F0F0F0;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 13px;
    }

    th {
        background: #FAFAFA;
        color: #666;
        padding: 12px 10px;
        text-align: left;
        border-bottom: 2px solid #E8E8E8;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
    }

    td {
        padding: 10px;
        border-bottom: 1px solid #F0F0F0;
    }

    tbody tr:hover {
        background: #FAFAFA;
    }

    .info-caption {
        font-size: 12px;
        color: #999;
        margin-top: 1rem;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    """
    <div class="title-section">
        <h1 style="margin: 0 0 0.5rem 0; font-size: 32px;">
            Termómetro Nacional
        </h1>
        <p style="margin: 0; font-size: 16px; color: #666;">
            Territorial Risk Monitor — Panamá
        </p>
        <p style="margin: 0.5rem 0 0 0; font-size: 12px; color: #999;">
            Perfilamiento territorial · Hard No
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATOS
# ============================================================

data = pd.DataFrame({
    "Territorio": [
        "Bocas del Toro",
        "Chiriquí",
        "Veraguas",
        "Herrera",
        "Los Santos",
        "Coclé",
        "Colón",
        "Panamá Oeste",
        "Panamá",
        "Darién",
        "Ngäbe Buglé"
    ],
    "Hard No": [
        46,
        39,
        42,
        43,
        37,
        22,
        18,
        26,
        32,
        25,
        45
    ],
    "Latitud": [
        9.34,
        8.43,
        8.10,
        7.96,
        7.77,
        8.52,
        9.35,
        8.88,
        8.98,
        8.42,
        8.75
    ],
    "Longitud": [
        -82.24,
        -82.43,
        -80.98,
        -80.43,
        -80.28,
        -80.36,
        -79.90,
        -79.78,
        -79.52,
        -78.15,
        -81.75
    ]
})

hard_no_nacional = 32


# ============================================================
# CLASIFICACIÓN
# ============================================================

def categoria(score):
    if score >= 40:
        return "Alto"
    elif score >= 25:
        return "Medio"
    else:
        return "Bajo"


data["Categoria"] = data["Hard No"].apply(categoria)


# ============================================================
# KPI DASHBOARD
# ============================================================

k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Hard No Nacional</div>
            <p class="kpi-number">{hard_no_nacional}%</p>
            <div class="kpi-unit">porcentaje nacional</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    alto = int((data["Categoria"] == "Alto").sum())

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Nivel Alto</div>
            <p class="kpi-number">{alto}</p>
            <div class="kpi-unit">territorios</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    medio = int((data["Categoria"] == "Medio").sum())

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Nivel Medio</div>
            <p class="kpi-number">{medio}</p>
            <div class="kpi-unit">territorios</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    bajo = int((data["Categoria"] == "Bajo").sum())

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Nivel Bajo</div>
            <p class="kpi-number">{bajo}</p>
            <div class="kpi-unit">territorios</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("")


# ============================================================
# GEOJSON LOAD
# ============================================================

with open(
    "panama-provincias.geojson",
    "r",
    encoding="utf-8"
) as f:
    panama = json.load(f)


def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = texto.lower()
    texto = texto.replace("provincia de ", "")
    texto = texto.replace("comarca ", "")
    texto = texto.strip()

    return texto


data["map_key"] = data["Territorio"].apply(normalizar)

for feature in panama["features"]:
    propiedades = feature["properties"]
    nombre = propiedades.get("NOMBRE", "")
    propiedades["map_key"] = normalizar(nombre)


territorios_validos = set(data["map_key"])

panama["features"] = [
    feature
    for feature in panama["features"]
    if feature["properties"]["map_key"] in territorios_validos
]


# ============================================================
# MAPA CHOROPLETH
# ============================================================

fig_data = px.choropleth(
    data,
    geojson=panama,
    locations="map_key",
    featureidkey="properties.map_key",
    color="Categoria",
    category_orders={
        "Categoria": ["Alto", "Medio", "Bajo"]
    },
    color_discrete_map={
        "Alto": "#D32F2F",
        "Medio": "#E74C3C",
        "Bajo": "#FADBD8"
    },
    hover_name="Territorio",
    hover_data={
        "Hard No": True,
        "Categoria": True,
        "map_key": False,
        "Latitud": False,
        "Longitud": False
    }
)


# ============================================================
# LABELS SOBRE EL MAPA
# ============================================================

data["Etiqueta"] = (
    data["Territorio"]
    + "<br><b>"
    + data["Hard No"].astype(str)
    + "%</b>"
)

fig_data.add_trace(
    go.Scattergeo(
        lon=data["Longitud"],
        lat=data["Latitud"],
        text=data["Etiqueta"],
        mode="text",
        textfont={
            "size": 11,
            "color": "#1A1A1A",
            "family": "Arial"
        },
        hoverinfo="skip",
        showlegend=False
    )
)


fig_data.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False
)

fig_data.update_traces(
    selector={"type": "choropleth"},
    marker_line_color="white",
    marker_line_width=1.2,
    hovertemplate=(
        "<b>%{customdata[0]}</b>"
        "<br>Hard No: %{customdata[1]}%"
        "<br>Nivel: %{customdata[2]}"
        "<extra></extra>"
    )
)

fig_data.update_layout(
    height=550,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={"r": 0, "t": 20, "l": 0, "b": 0},
    legend_title_text="Nivel Hard No",
    legend={
        "orientation": "v",
        "yanchor": "top",
        "y": 0.99,
        "xanchor": "right",
        "x": 0.99,
        "bgcolor": "rgba(255, 255, 255, 0.95)",
        "bordercolor": "#E8E8E8",
        "borderwidth": 1
    }
)


# ============================================================
# SECCIÓN: MAPA Y RANKING
# ============================================================

map_col, rank_col = st.columns([2, 1], gap="medium")

with map_col:
    st.markdown(
        '<h3 class="section-title">Hard No por territorio</h3>',
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig_data,
        use_container_width=True
    )

    st.markdown(
        """
        <p class="info-caption">
            El porcentaje representa la proporción de personas clasificadas
            como Hard No en cada provincia o comarca.
        </p>
        """,
        unsafe_allow_html=True
    )

with rank_col:
    st.markdown(
        '<h3 class="section-title">Ranking Territorial</h3>',
        unsafe_allow_html=True
    )

    ranking = data.sort_values(
        "Hard No",
        ascending=False
    ).copy()

    def badge(cat):
        if cat == "Alto":
            return '<span class="badge-alto">Alto</span>'

        elif cat == "Medio":
            return '<span class="badge-medio">Medio</span>'

        return '<span class="badge-bajo">Bajo</span>'

    ranking["Nivel"] = ranking["Categoria"].apply(badge)
    ranking["Hard No"] = ranking["Hard No"].astype(str) + "%"

    ranking_html = ranking[
        ["Territorio", "Hard No", "Nivel"]
    ].to_html(
        escape=False,
        index=False,
        col_space={
            "Territorio": "55%",
            "Hard No": "20%",
            "Nivel": "25%"
        }
    )

    st.markdown(
        f'<div class="container-box">{ranking_html}</div>',
        unsafe_allow_html=True
    )
