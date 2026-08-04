import json
import textwrap
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
        gap: 0.65rem;
    }

    .title-section {
        margin-bottom: 1.6rem;
        border-bottom: 2px solid #E8E8E8;
        padding-bottom: 1.2rem;
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
        margin-top: 7px;
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 0.8rem;
        margin-top: 0;
    }

    .container-box {
        background: white;
        border-radius: 12px;
        padding: 16px;
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
        padding: 11px 8px;
        text-align: left;
        border-bottom: 2px solid #E8E8E8;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: 0.4px;
    }

    td {
        padding: 11px 8px;
        border-bottom: 1px solid #F0F0F0;
    }

    tbody tr:hover {
        background: #FAFAFA;
    }

    .info-caption {
        font-size: 12px;
        color: #777;
        margin-top: 0.8rem;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIÓN PARA MOSTRAR HTML
# ============================================================

def mostrar_html(contenido):

    st.markdown(
        textwrap.dedent(contenido).strip(),
        unsafe_allow_html=True
    )


# ============================================================
# ENCABEZADO
# ============================================================

mostrar_html(
    """
    <div class="title-section">

        <h1 style="margin:0 0 0.5rem 0; font-size:32px;">
            Termómetro Nacional
        </h1>

        <p style="margin:0; font-size:16px; color:#666;">
            Territorial Risk Monitor — Panamá
        </p>

        <p style="margin:0.5rem 0 0 0; font-size:12px; color:#999;">
            Perfilamiento territorial · Hard No
        </p>

    </div>
    """
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
        "-",
        " "
    )

    texto = " ".join(
        texto.split()
    )

    # Igualar Ngäbe y Ngöbe
    if texto in {
        "ngabe bugle",
        "ngobe bugle"
    }:
        texto = "ngabe bugle"

    return texto


# ============================================================
# CORREGIR ORIENTACIÓN DE LOS POLÍGONOS
# ============================================================

def area_firmada(anillo):

    if not anillo or len(anillo) < 3:
        return 0

    puntos = list(anillo)

    if puntos[0] != puntos[-1]:
        puntos.append(puntos[0])

    area = 0.0

    for i in range(len(puntos) - 1):

        x1, y1 = puntos[i][0], puntos[i][1]
        x2, y2 = puntos[i + 1][0], puntos[i + 1][1]

        area += (
            x1 * y2
            -
            x2 * y1
        )

    return area / 2.0


def corregir_anillo_exterior(anillo):

    puntos = list(anillo)

    if not puntos:
        return puntos

    if puntos[0] != puntos[-1]:
        puntos.append(puntos[0])

    # El anillo exterior debe quedar antihorario
    if area_firmada(puntos) < 0:
        puntos = list(reversed(puntos))

    return puntos


def corregir_anillo_interior(anillo):

    puntos = list(anillo)

    if not puntos:
        return puntos

    if puntos[0] != puntos[-1]:
        puntos.append(puntos[0])

    # Los agujeros deben quedar en sentido contrario
    if area_firmada(puntos) > 0:
        puntos = list(reversed(puntos))

    return puntos


def corregir_orientacion_geojson(geojson):

    for feature in geojson.get(
        "features",
        []
    ):

        geometria = feature.get(
            "geometry",
            {}
        )

        tipo = geometria.get(
            "type"
        )

        coordenadas = geometria.get(
            "coordinates",
            []
        )

        if tipo == "Polygon":

            if not coordenadas:
                continue

            coordenadas[0] = corregir_anillo_exterior(
                coordenadas[0]
            )

            for i in range(
                1,
                len(coordenadas)
            ):

                coordenadas[i] = corregir_anillo_interior(
                    coordenadas[i]
                )

        elif tipo == "MultiPolygon":

            for poligono in coordenadas:

                if not poligono:
                    continue

                poligono[0] = corregir_anillo_exterior(
                    poligono[0]
                )

                for i in range(
                    1,
                    len(poligono)
                ):

                    poligono[i] = corregir_anillo_interior(
                        poligono[i]
                    )

    return geojson


# ============================================================
# CALCULAR CENTROIDE DEL POLÍGONO
# ============================================================

def centroide_anillo(coordenadas):

    if not coordenadas or len(coordenadas) < 3:
        return None, None, 0

    puntos = list(coordenadas)

    if puntos[0] != puntos[-1]:
        puntos.append(puntos[0])

    area_doble = 0
    centro_x = 0
    centro_y = 0

    for i in range(len(puntos) - 1):

        x1, y1 = puntos[i][0], puntos[i][1]
        x2, y2 = puntos[i + 1][0], puntos[i + 1][1]

        cruzado = (
            x1 * y2
            -
            x2 * y1
        )

        area_doble += cruzado

        centro_x += (
            x1 + x2
        ) * cruzado

        centro_y += (
            y1 + y2
        ) * cruzado

    if abs(area_doble) < 1e-12:

        longitudes = [
            punto[0]
            for punto in puntos
        ]

        latitudes = [
            punto[1]
            for punto in puntos
        ]

        return (
            sum(longitudes) / len(longitudes),
            sum(latitudes) / len(latitudes),
            0
        )

    centro_x = centro_x / (
        3 * area_doble
    )

    centro_y = centro_y / (
        3 * area_doble
    )

    area = abs(
        area_doble / 2
    )

    return (
        centro_x,
        centro_y,
        area
    )


def centro_geometria(geometria):

    tipo = geometria.get(
        "type"
    )

    coordenadas = geometria.get(
        "coordinates",
        []
    )

    candidatos = []

    if tipo == "Polygon":

        if coordenadas:

            resultado = centroide_anillo(
                coordenadas[0]
            )

            if resultado[0] is not None:
                candidatos.append(resultado)

    elif tipo == "MultiPolygon":

        for poligono in coordenadas:

            if not poligono:
                continue

            resultado = centroide_anillo(
                poligono[0]
            )

            if resultado[0] is not None:
                candidatos.append(resultado)

    if not candidatos:
        return None, None

    # Usa la parte más grande del territorio
    principal = max(
        candidatos,
        key=lambda elemento: elemento[2]
    )

    return (
        principal[0],
        principal[1]
    )


# ============================================================
# KPI GENERALES
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


# ============================================================
# KPI DASHBOARD
# ============================================================

k1, k2, k3, k4 = st.columns(
    4,
    gap="medium"
)


with k1:

    mostrar_html(
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
        """
    )


with k2:

    mostrar_html(
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
        """
    )


with k3:

    mostrar_html(
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
        """
    )


with k4:

    mostrar_html(
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
        """
    )


st.markdown("")


# ============================================================
# CARGAR GEOJSON
# ============================================================

with open(
    "TEST.geojson",
    "r",
    encoding="utf-8"
) as archivo_geojson:

    panama = json.load(
        archivo_geojson
    )


# Corregir automáticamente la orientación
panama = corregir_orientacion_geojson(
    panama
)


# ============================================================
# CREAR IDENTIFICADORES
# ============================================================

data["map_key"] = data[
    "Territorio"
].apply(normalizar)


centros = []


for feature in panama.get(
    "features",
    []
):

    propiedades = feature.get(
        "properties",
        {}
    )

    nombre_geojson = propiedades.get(
        "NOMBRE",
        ""
    )

    map_key = normalizar(
        nombre_geojson
    )

    # Identificador directo para Plotly
    feature["id"] = map_key

    propiedades[
        "map_key"
    ] = map_key

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
# VERIFICAR COINCIDENCIAS
# ============================================================

claves_datos = set(
    data["map_key"]
)


claves_geojson = {

    feature["id"]

    for feature in panama.get(
        "features",
        []
    )
}


faltan_en_geojson = (
    claves_datos
    -
    claves_geojson
)


if faltan_en_geojson:

    st.error(
        "No se encontraron en TEST.geojson: "
        + ", ".join(
            sorted(faltan_en_geojson)
        )
    )


# ============================================================
# CONSERVAR SOLO LOS TERRITORIOS CON DATOS
# ============================================================

panama["features"] = [

    feature

    for feature in panama.get(
        "features",
        []
    )

    if feature["id"]
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
# AJUSTES VISUALES DE LOS LABELS
# ============================================================

ajustes_labels = {

    "bocas del toro": {
        "lon": 0.02,
        "lat": 0.02
    },

    "ngabe bugle": {
        "lon": 0.00,
        "lat": 0.00
    },

    "chiriqui": {
        "lon": -0.01,
        "lat": -0.02
    },

    "veraguas": {
        "lon": 0.00,
        "lat": -0.03
    },

    "herrera": {
        "lon": 0.00,
        "lat": 0.02
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
        "lat": 0.03
    },

    "panama oeste": {
        "lon": -0.02,
        "lat": -0.02
    },

    "panama": {
        "lon": 0.08,
        "lat": -0.02
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

    if pd.notna(
        fila["Centro Longitud"]
    ):

        data.loc[
            indice,
            "Centro Longitud"
        ] += ajuste["lon"]

    if pd.notna(
        fila["Centro Latitud"]
    ):

        data.loc[
            indice,
            "Centro Latitud"
        ] += ajuste["lat"]


# ============================================================
# ETIQUETAS
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
# MAPA CHOROPLETH
# ============================================================

fig_data = px.choropleth(

    data,

    geojson=panama,

    locations="map_key",

    featureidkey="id",

    color="Hard No",

    color_continuous_scale=[
        [0.00, "#FCE1DF"],
        [0.20, "#F7B7B2"],
        [0.40, "#F08078"],
        [0.60, "#DE4A43"],
        [0.80, "#B92525"],
        [1.00, "#850A0A"]
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
# RESALTADO DETRÁS DEL TEXTO
# ============================================================

fig_data.add_trace(
    go.Scattergeo(

        lon=data["Centro Longitud"],

        lat=data["Centro Latitud"],

        mode="markers",

        marker={
            "size": 39,
            "color": "rgba(225, 225, 225, 0.63)",
            "line": {
                "color": "rgba(130, 130, 130, 0.15)",
                "width": 0.3
            },
            "symbol": "circle"
        },

        hoverinfo="skip",

        showlegend=False
    )
)


# ============================================================
# TEXTO CENTRADO
# ============================================================

fig_data.add_trace(
    go.Scattergeo(

        lon=data["Centro Longitud"],

        lat=data["Centro Latitud"],

        text=data["Etiqueta"],

        mode="text",

        textposition="middle center",

        textfont={
            "size": 9,
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

        "thickness": 15,

        "len": 0.58,

        "y": 0.70,

        "x": 0.99,

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

    mostrar_html(
        """
        <h3 class="section-title">
            Hard No por territorio
        </h3>
        """
    )

    st.plotly_chart(
        fig_data,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    mostrar_html(
        """
        <p class="info-caption">

            El porcentaje representa la proporción de personas
            clasificadas como Hard No en cada provincia o comarca.
            Los tonos más oscuros indican una mayor incidencia
            territorial de Hard No.

        </p>
        """
    )


with rank_col:

    mostrar_html(
        """
        <h3 class="section-title">
            Ranking Territorial
        </h3>
        """
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

    mostrar_html(
        f"""
        <div class="container-box">
            {ranking_html}
        </div>
        """
    )
