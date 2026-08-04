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
        padding: 12px 10px;
        border-bottom: 1px solid #F0F0F0;
    }

    tbody tr:hover {
        background: #FAFAFA;
    }

    .info-caption {
        font-size: 12px;
        color: #777;
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
        "Ngäbe Buglé",
        "Herrera",
        "Veraguas",
        "Chiriquí",
        "Los Santos",
        "Panamá",
        "Panamá Oeste",
        "Darién",
        "Coclé",
        "Colón"
    ],

    "N Entrevistas": [
        19,
        28,
        11,
        29,
        65,
        11,
        144,
        54,
        7,
        11,
        15
    ],

    "Base Ponderada": [
        18.70,
        28.72,
        9.89,
        27.87,
        68.27,
        9.09,
        142.25,
        52.67,
        6.10,
        12.88,
        13.60
    ],

    "Hard No": [
        46,
        45,
        43,
        42,
        39,
        37,
        32,
        26,
        25,
        22,
        18
    ],

    "Latitud": [
        9.34,
        8.82,
        7.96,
        8.10,
        8.43,
        7.77,
        8.98,
        8.88,
        8.42,
        8.52,
        9.35
    ],

    "Longitud": [
        -82.24,
        -81.75,
        -80.43,
        -80.98,
        -82.43,
        -80.28,
        -79.52,
        -79.78,
        -78.15,
        -80.36,
        -79.90
    ]
})


hard_no_nacional = 32


# ============================================================
# INDICADORES GENERALES
# ============================================================

territorio_mayor = data.loc[data["Hard No"].idxmax()]
territorio_menor = data.loc[data["Hard No"].idxmin()]

promedio_territorial = data["Hard No"].mean()


# ============================================================
# KPI DASHBOARD
# ============================================================

k1, k2, k3, k4 = st.columns(4, gap="medium")


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Hard No Nacional</div>

            <p class="kpi-number">
                {hard_no_nacional}%
            </p>

            <div class="kpi-unit">
                resultado nacional ponderado
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Mayor porcentaje</div>

            <p class="kpi-number">
                {territorio_mayor["Hard No"]}%
            </p>

            <div class="kpi-unit">
                {territorio_mayor["Territorio"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Menor porcentaje</div>

            <p class="kpi-number">
                {territorio_menor["Hard No"]}%
            </p>

            <div class="kpi-unit">
                {territorio_menor["Territorio"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Promedio territorial</div>

            <p class="kpi-number">
                {promedio_territorial:.1f}%
            </p>

            <div class="kpi-unit">
                promedio simple de los territorios
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("")


# ============================================================
# GEOJSON LOAD
# ============================================================

with open(
    "panama-provinciasV0.geojson",
    "r",
    encoding="utf-8"
) as f:

    panama = json.load(f)


# ============================================================
# NORMALIZACIÓN DE NOMBRES
# ============================================================

def normalizar(texto):

    texto = str(texto)

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    texto = texto.lower()

    texto = texto.replace(
        "provincia de ",
        ""
    )

    texto = texto.replace(
        "comarca ",
        ""
    )

    texto = texto.replace(
        "ngabe-bugle",
        "ngabe bugle"
    )

    texto = texto.replace(
        "ngabe bugle",
        "ngabe bugle"
    )

    texto = texto.strip()

    return texto


data["map_key"] = data["Territorio"].apply(
    normalizar
)


for feature in panama["features"]:

    propiedades = feature["properties"]

    nombre = propiedades.get(
        "NOMBRE",
        ""
    )

    propiedades["map_key"] = normalizar(
        nombre
    )


# ============================================================
# AJUSTES ESPECÍFICOS DE NOMBRES
# ============================================================

equivalencias = {
    "comarca ngabe-bugle": "ngabe bugle",
    "comarca ngabe bugle": "ngabe bugle",
    "ngabe-bugle": "ngabe bugle",
    "ngabe bugle": "ngabe bugle"
}


for feature in panama["features"]:

    map_key = feature["properties"]["map_key"]

    if map_key in equivalencias:

        feature["properties"]["map_key"] = equivalencias[
            map_key
        ]


# ============================================================
# FILTRAR SOLO TERRITORIOS CON DATOS
# ============================================================

territorios_validos = set(
    data["map_key"]
)


panama["features"] = [

    feature

    for feature in panama["features"]

    if feature["properties"]["map_key"]
    in territorios_validos
]


# ============================================================
# ETIQUETAS
# ============================================================

data["Etiqueta"] = (
    data["Territorio"]
    + "<br><b>"
    + data["Hard No"].astype(str)
    + "%</b>"
)


# ============================================================
# MAPA CHOROPLETH CONTINUO
# ============================================================

fig_data = px.choropleth(
    data,

    geojson=panama,

    locations="map_key",

    featureidkey="properties.map_key",

    color="Hard No",

    color_continuous_scale=[
        [0.00, "#FDE7E5"],
        [0.25, "#F8BBB6"],
        [0.50, "#F27A70"],
        [0.75, "#E7473C"],
        [1.00, "#B71C1C"]
    ],

    range_color=(
        data["Hard No"].min(),
        data["Hard No"].max()
    ),

    hover_name="Territorio",

    hover_data={
        "Hard No": ":.0f",
        "N Entrevistas": True,
        "Base Ponderada": ":.2f",
        "map_key": False,
        "Latitud": False,
        "Longitud": False
    }
)


# ============================================================
# LABELS SOBRE EL MAPA
# ============================================================

fig_data.add_trace(
    go.Scattergeo(

        lon=data["Longitud"],

        lat=data["Latitud"],

        text=data["Etiqueta"],

        mode="text",

        textfont={
            "size": 11,
            "color": "#111111",
            "family": "Arial"
        },

        hoverinfo="skip",

        showlegend=False
    )
)


# ============================================================
# CONFIGURACIÓN GEOGRÁFICA
# ============================================================

fig_data.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False,
    bgcolor="white"
)


# ============================================================
# BORDES Y HOVER
# ============================================================

fig_data.update_traces(
    selector={
        "type": "choropleth"
    },

    marker_line_color="white",

    marker_line_width=1.2,

    hovertemplate=(
        "<b>%{customdata[0]}</b>"
        "<br>Hard No: %{z:.0f}%"
        "<br>N entrevistas: %{customdata[2]}"
        "<br>Base ponderada: %{customdata[3]:.2f}"
        "<extra></extra>"
    )
)


# ============================================================
# DISEÑO GENERAL DEL MAPA
# ============================================================

fig_data.update_layout(

    height=600,

    paper_bgcolor="white",

    plot_bgcolor="white",

    margin={
        "r": 0,
        "t": 10,
        "l": 0,
        "b": 0
    },

    coloraxis_colorbar={

        "title": {
            "text": "Hard No (%)"
        },

        "thickness": 14,

        "len": 0.55,

        "y": 0.72,

        "x": 0.98,

        "tickvals": [
            data["Hard No"].min(),
            hard_no_nacional,
            data["Hard No"].max()
        ],

        "ticktext": [
            f'{data["Hard No"].min()}%',
            f'{hard_no_nacional}%',
            f'{data["Hard No"].max()}%'
        ]
    }
)


# ============================================================
# MAPA Y RANKING
# ============================================================

map_col, rank_col = st.columns(
    [2.15, 1],
    gap="medium"
)


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

            El porcentaje representa la proporción de personas
            clasificadas como Hard No en cada provincia o comarca.
            Los tonos más oscuros representan porcentajes más altos
            y los tonos más claros porcentajes más bajos.

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

    ranking["Hard No"] = (
        ranking["Hard No"]
        .astype(str)
        + "%"
    )

    ranking_html = ranking[
        [
            "Territorio",
            "Hard No",
            "N Entrevistas"
        ]
    ].to_html(
        escape=False,
        index=False,
        col_space={
            "Territorio": "55%",
            "Hard No": "25%",
            "N Entrevistas": "20%"
        }
    )

    st.markdown(
        f"""
        <div class="container-box">
            {ranking_html}
        </div>
        """,
        unsafe_allow_html=True
    )
