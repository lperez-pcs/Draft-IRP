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
        font-size: 20px;
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
    ]
})


hard_no_nacional = 32


# ============================================================
# NORMALIZAR NOMBRES
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
    texto = texto.replace("provincia de ", "")
    texto = texto.replace("comarca ", "")
    texto = texto.replace("-", " ")
    texto = " ".join(texto.split())

    # Unificar variantes de Ngäbe/Ngöbe Buglé
    if texto in [
        "ngabe bugle",
        "ngobe bugle"
    ]:
        texto = "ngabe bugle"

    return texto


# ============================================================
# CALCULAR CENTROIDE DE UN POLÍGONO
# ============================================================

def centroide_anillo(coordenadas):

    if not coordenadas or len(coordenadas) < 3:
        return None, None, 0

    area_doble = 0
    centro_x = 0
    centro_y = 0

    for i in range(len(coordenadas) - 1):

        x1 = coordenadas[i][0]
        y1 = coordenadas[i][1]

        x2 = coordenadas[i + 1][0]
        y2 = coordenadas[i + 1][1]

        producto_cruzado = (x1 * y2) - (x2 * y1)

        area_doble += producto_cruzado
        centro_x += (x1 + x2) * producto_cruzado
        centro_y += (y1 + y2) * producto_cruzado

    if abs(area_doble) < 1e-12:

        longitudes = [
            punto[0]
            for punto in coordenadas
        ]

        latitudes = [
            punto[1]
            for punto in coordenadas
        ]

        return (
            sum(longitudes) / len(longitudes),
            sum(latitudes) / len(latitudes),
            0
        )

    centro_x = centro_x / (3 * area_doble)
    centro_y = centro_y / (3 * area_doble)

    area = abs(area_doble / 2)

    return centro_x, centro_y, area


def centro_geometria(geometria):

    tipo = geometria.get("type")
    coordenadas = geometria.get("coordinates", [])

    candidatos = []

    if tipo == "Polygon":

        if coordenadas:

            resultado = centroide_anillo(
                coordenadas[0]
            )

            candidatos.append(resultado)

    elif tipo == "MultiPolygon":

        for poligono in coordenadas:

            if poligono:

                resultado = centroide_anillo(
                    poligono[0]
                )

                candidatos.append(resultado)

    candidatos = [
        resultado
        for resultado in candidatos
        if resultado[0] is not None
    ]

    if not candidatos:
        return None, None

    poligono_principal = max(
        candidatos,
        key=lambda resultado: resultado[2]
    )

    return (
        poligono_principal[0],
        poligono_principal[1]
    )


# ============================================================
# KPI
# ============================================================

territorio_mayor = data.loc[
    data["Hard No"].idxmax()
]

territorio_menor = data.loc[
    data["Hard No"].idxmin()
]

promedio_territorial = data[
    "Hard No"
].mean()


k1, k2, k3, k4 = st.columns(
    4,
    gap="medium"
)


with k1:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Hard No Nacional
            </div>

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

            <div class="kpi-label">
                Mayor porcentaje
            </div>

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

            <div class="kpi-label">
                Menor porcentaje
            </div>

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

            <div class="kpi-label">
                Promedio territorial
            </div>

            <p class="kpi-number">
                {promedio_territorial:.1f}%
            </p>

            <div class="kpi-unit">
                promedio simple territorial
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("")


# ============================================================
# CARGAR TEST.GEOJSON
# ============================================================

with open(
    "TEST.geojson",
    "r",
    encoding="utf-8"
) as archivo_geojson:

    panama = json.load(
        archivo_geojson
    )


# ============================================================
# CREAR IDENTIFICADORES
# ============================================================

data["map_key"] = data[
    "Territorio"
].apply(normalizar)


centros = []


for feature in panama["features"]:

    propiedades = feature.get(
        "properties",
        {}
    )

    # TEST.geojson utiliza el campo NOMBRE
    nombre = propiedades.get(
        "NOMBRE",
        ""
    )

    map_key = normalizar(
        nombre
    )

    propiedades["map_key"] = map_key

    centro_lon, centro_lat = centro_geometria(
        feature.get(
            "geometry",
            {}
        )
    )

    centros.append({
        "map_key": map_key,
        "Centro Longitud": centro_lon,
        "Centro Latitud": centro_lat
    })


centros_df = pd.DataFrame(
    centros
)


# ============================================================
# COMPROBAR COINCIDENCIAS
# ============================================================

claves_datos = set(
    data["map_key"]
)

claves_geojson = {
    feature["properties"]["map_key"]
    for feature in panama["features"]
}


faltantes_geojson = claves_datos - claves_geojson


if faltantes_geojson:

    st.error(
        "Estos territorios no coinciden con el GeoJSON: "
        + ", ".join(sorted(faltantes_geojson))
    )


# ============================================================
# FILTRAR SOLO TERRITORIOS CON DATOS
# ============================================================

panama["features"] = [
    feature
    for feature in panama["features"]
    if feature["properties"]["map_key"]
    in claves_datos
]


# ============================================================
# UNIR CENTROS CON LOS DATOS
# ============================================================

data = data.merge(
    centros_df,
    on="map_key",
    how="left"
)


# ============================================================
# AJUSTES VISUALES DE POSICIÓN
# ============================================================
# Son movimientos pequeños para evitar que algunos nombres
# queden sobre una frontera.

ajustes_labels = {

    "bocas del toro": {
        "lon": -0.02,
        "lat": 0.00
    },

    "ngabe bugle": {
        "lon": 0.00,
        "lat": 0.00
    },

    "chiriqui": {
        "lon": -0.03,
        "lat": -0.02
    },

    "veraguas": {
        "lon": 0.00,
        "lat": -0.02
    },

    "herrera": {
        "lon": 0.00,
        "lat": 0.00
    },

    "los santos": {
        "lon": 0.03,
        "lat": -0.03
    },

    "cocle": {
        "lon": 0.00,
        "lat": 0.00
    },

    "colon": {
        "lon": 0.00,
        "lat": 0.02
    },

    "panama oeste": {
        "lon": -0.02,
        "lat": -0.02
    },

    "panama": {
        "lon": 0.04,
        "lat": 0.00
    },

    "darien": {
        "lon": 0.00,
        "lat": 0.00
    }
}


for indice, fila in data.iterrows():

    ajuste = ajustes_labels.get(
        fila["map_key"],
        {
            "lon": 0,
            "lat": 0
        }
    )

    data.loc[
        indice,
        "Centro Longitud"
    ] += ajuste["lon"]

    data.loc[
        indice,
        "Centro Latitud"
    ] += ajuste["lat"]


# ============================================================
# TEXTO DE LAS ETIQUETAS
# ============================================================

data["Etiqueta"] = (
    "<b>"
    + data["Territorio"]
    + "</b>"
    + "<br>"
    + data["Hard No"].astype(str)
    + "%"
)


# ============================================================
# TAMAÑO DEL RESALTADO
# ============================================================
# El círculo aumenta ligeramente para nombres largos.

data["Tamaño Label"] = (
    data["Territorio"]
    .str.len()
    .apply(
        lambda longitud: max(
            38,
            min(62, longitud * 3.1)
        )
    )
)


# ============================================================
# MAPA
# ============================================================

fig_data = px.choropleth(
    data,

    geojson=panama,

    locations="map_key",

    featureidkey="properties.map_key",

    color="Hard No",

    color_continuous_scale=[
        [0.00, "#FDE3E1"],
        [0.20, "#F8B7B2"],
        [0.40, "#F17D74"],
        [0.60, "#E84A40"],
        [0.80, "#C92525"],
        [1.00, "#850B0B"]
    ],

    range_color=(
        data["Hard No"].min(),
        data["Hard No"].max()
    ),

    custom_data=[
        "Territorio",
        "Hard No",
        "N Entrevistas",
        "Base Ponderada"
    ]
)


# ============================================================
# RESALTADO GRIS TRANSLÚCIDO
# ============================================================
# Es circular y suave; no es un cuadro.

fig_data.add_trace(
    go.Scattergeo(

        lon=data["Centro Longitud"],

        lat=data["Centro Latitud"],

        mode="markers",

        marker={
            "size": data["Tamaño Label"],
            "color": "rgba(220, 220, 220, 0.68)",
            "line": {
                "color": "rgba(110, 110, 110, 0.25)",
                "width": 0.5
            },
            "symbol": "circle"
        },

        hoverinfo="skip",

        showlegend=False
    )
)


# ============================================================
# TEXTO CENTRADO SOBRE EL RESALTADO
# ============================================================

fig_data.add_trace(
    go.Scattergeo(

        lon=data["Centro Longitud"],

        lat=data["Centro Latitud"],

        text=data["Etiqueta"],

        mode="text",

        textposition="middle center",

        textfont={
            "size": 10,
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

    marker_line_width=1.4,

    hovertemplate=(
        "<b>%{customdata[0]}</b>"
        "<br>Hard No: %{customdata[1]:.0f}%"
        "<br>N entrevistas: %{customdata[2]}"
        "<br>Base ponderada: %{customdata[3]:.2f}"
        "<extra></extra>"
    )
)


# ============================================================
# DISEÑO DEL MAPA
# ============================================================

fig_data.update_layout(

    height=610,

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

        "thickness": 15,

        "len": 0.57,

        "y": 0.70,

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
            Los tonos más oscuros indican una mayor incidencia
            territorial de Hard No.

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
            "Territorio": "50%",
            "Hard No": "20%",
            "N Entrevistas": "30%"
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
