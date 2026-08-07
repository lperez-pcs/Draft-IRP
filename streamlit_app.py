# ============================================================
# 1. IMPORTAMOS LAS LIBRERÍAS
# ============================================================

# json:
# Nos permite trabajar con el GeoJSON que devuelve ArcGIS.
import json

# unicodedata:
# Lo usamos para normalizar nombres.
# Ejemplo: "Colón" -> "colon"
import unicodedata

# requests:
# Permite que Python consulte directamente la URL de ArcGIS.
import requests

# pandas:
# Para trabajar con nuestra tabla de datos.
import pandas as pd

# plotly.graph_objects:
# Lo usaremos para construir el mapa por capas.
import plotly.graph_objects as go

# streamlit:
# Construye toda nuestra aplicación web.
import streamlit as st


# ============================================================
# 2. CONFIGURACIÓN GENERAL DE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Strategic Risk Platform",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 3. TÍTULO DE LA APLICACIÓN
# ============================================================

st.title("Termómetro Nacional")

st.caption(
    "Territorial Risk Monitor — Panamá · "
    "Perfilamiento territorial · Hard No"
)


# ============================================================
# 4. DATOS DE HARD NO
# ============================================================

# Esta tabla representa nuestros datos.
#
# IMPORTANTE:
# Las 10 provincias tienen información.
# Ngäbe Buglé también tiene información.
#
# Las demás comarcas NO están aquí porque queremos que
# aparezcan en gris, sin valor de Hard No.

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


# Resultado nacional
hard_no_nacional = 32


# ============================================================
# 5. DEFINIMOS LAS 10 PROVINCIAS DE PANAMÁ
# ============================================================

# Esta lista es importante porque nos permite distinguir
# automáticamente una provincia de una comarca.

PROVINCIAS = {
    "bocas del toro",
    "cocle",
    "colon",
    "chiriqui",
    "darien",
    "herrera",
    "los santos",
    "panama",
    "panama oeste",
    "veraguas"
}


# ============================================================
# 6. FUNCIÓN PARA NORMALIZAR NOMBRES
# ============================================================

def normalizar(texto):
    """
    Convierte distintos formatos de nombres en una misma clave.

    Ejemplos:

    Panamá          -> panama
    Colón           -> colon
    Chiriquí        -> chiriqui
    Comarca Ngäbe Buglé -> ngabe bugle

    Esto evita problemas cuando ArcGIS y nuestra tabla
    escriben un territorio ligeramente diferente.
    """

    texto = str(texto)

    # Separar letras de sus tildes
    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    # Eliminar las tildes
    texto = "".join(
        caracter
        for caracter in texto
        if not unicodedata.combining(caracter)
    )

    # Todo en minúscula
    texto = texto.lower()

    # Si ArcGIS escribe "Provincia de Panamá",
    # eliminamos "provincia de".
    texto = texto.replace(
        "provincia de ",
        ""
    )

    # Si ArcGIS escribe "Comarca Ngäbe Buglé",
    # eliminamos "comarca".
    texto = texto.replace(
        "comarca ",
        ""
    )

    # Convertimos guiones en espacios
    texto = texto.replace(
        "-",
        " "
    )

    # Eliminamos espacios duplicados
    texto = " ".join(
        texto.split()
    )

    # Ngäbe también puede aparecer escrito como Ngöbe.
    # Para nosotros ambos significarán lo mismo.
    if texto in {
        "ngabe bugle",
        "ngobe bugle"
    }:
        texto = "ngabe bugle"

    return texto


# ============================================================
# 7. DESCARGAR LA CAPA DIRECTAMENTE DESDE ARCGIS
# ============================================================

# Esta es la URL que tú encontraste.
#
# No descargamos el archivo manualmente.
# Python consulta directamente el FeatureServer.

ARCGIS_URL = (
    "https://services2.arcgis.com/"
    "HRY6x8qt5qjGnAA9/"
    "arcgis/rest/services/"
    "Panama_Province_Boundaries_2024/"
    "FeatureServer/0/query"
)


# @st.cache_data significa:
#
# "No vuelvas a descargar 73 MB cada vez que alguien toca algo
# en Streamlit".
#
# Streamlit guarda el resultado temporalmente.
#
# ttl=86400 = 24 horas.

@st.cache_data(
    ttl=86400,
    show_spinner=False
)
def cargar_mapa_arcgis():

    # Parámetros enviados al servidor ArcGIS.
    parametros = {

        # 1=1 significa:
        # tráeme todos los territorios.
        "where": "1=1",

        # Solo necesitamos estos dos atributos.
        # No traemos columnas innecesarias.
        "outFields": "ID_PROV,Provincia",

        # Queremos las geometrías.
        "returnGeometry": "true",

        # EPSG 4326 = longitud/latitud.
        # Es el sistema que Plotly necesita.
        "outSR": "4326",

        # Queremos GeoJSON.
        "f": "geojson"
    }

    respuesta = requests.get(
        ARCGIS_URL,
        params=parametros,
        timeout=120
    )

    # Si ArcGIS devuelve un error,
    # Streamlit nos mostrará el problema.
    respuesta.raise_for_status()

    geojson = respuesta.json()

    return geojson


# Mientras descarga la primera vez,
# mostramos un mensaje.

with st.spinner(
    "Cargando límites territoriales..."
):
    panama = cargar_mapa_arcgis()


# ============================================================
# 8. PREPARAR LOS NOMBRES DEL GEOJSON
# ============================================================

# Nuestra tabla también necesita la clave normalizada.

data["map_key"] = (
    data["Territorio"]
    .apply(normalizar)
)


# Ahora recorremos cada territorio que vino de ArcGIS.

for feature in panama["features"]:

    propiedades = feature.get(
        "properties",
        {}
    )

    # La capa de ArcGIS utiliza la columna "Provincia".
    nombre_arcgis = propiedades.get(
        "Provincia",
        ""
    )

    # Creamos una versión normalizada.
    map_key = normalizar(
        nombre_arcgis
    )

    # Guardamos esa clave dentro de la geometría.
    propiedades["map_key"] = map_key

    # También la ponemos como ID.
    # Plotly utilizará este ID para hacer el match.
    feature["id"] = map_key


# ============================================================
# 9. IDENTIFICAR PROVINCIAS Y COMARCAS
# ============================================================

# Creamos una tabla únicamente para entender qué
# territorios llegaron desde ArcGIS.

territorios_arcgis = []

for feature in panama["features"]:

    propiedades = feature["properties"]

    nombre = propiedades.get(
        "Provincia",
        ""
    )

    clave = propiedades.get(
        "map_key",
        ""
    )

    # Si la clave está dentro de las 10 provincias:
    if clave in PROVINCIAS:
        tipo = "Provincia"

    # Todo lo demás es tratado como comarca.
    else:
        tipo = "Comarca"

    territorios_arcgis.append({
        "Territorio ArcGIS": nombre,
        "map_key": clave,
        "Tipo": tipo
    })


territorios_arcgis = pd.DataFrame(
    territorios_arcgis
)


# ============================================================
# 10. SEPARAR COMARCAS SIN DATOS
# ============================================================

# Los territorios que tienen Hard No están aquí:

territorios_con_datos = set(
    data["map_key"]
)


# Todo territorio del ArcGIS que:
#
# 1. no es una de las 10 provincias
# 2. no está dentro de nuestros datos
#
# será una comarca que debe aparecer gris.

comarcas_grises = territorios_arcgis[

    (territorios_arcgis["Tipo"] == "Comarca")

    &

    (~territorios_arcgis["map_key"].isin(
        territorios_con_datos
    ))

].copy()


# Ngäbe Buglé NO aparecerá aquí porque sí está
# en territorios_con_datos.


# ============================================================
# 11. KPI
# ============================================================

territorio_mayor = data.loc[
    data["Hard No"].idxmax()
]

territorio_menor = data.loc[
    data["Hard No"].idxmin()
]


# Creamos cuatro columnas.

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        label="Hard No Nacional",
        value=f"{hard_no_nacional}%"
    )


with k2:

    st.metric(
        label="Mayor porcentaje",
        value=f'{territorio_mayor["Hard No"]}%',
        help=territorio_mayor["Territorio"]
    )

    st.caption(
        territorio_mayor["Territorio"]
    )


with k3:

    st.metric(
        label="Menor porcentaje",
        value=f'{territorio_menor["Hard No"]}%',
        help=territorio_menor["Territorio"]
    )

    st.caption(
        territorio_menor["Territorio"]
    )


with k4:

    st.metric(
        label="Territorios analizados",
        value=len(data)
    )


st.divider()


# ============================================================
# 12. FUNCIÓN PARA CALCULAR EL CENTRO DEL POLÍGONO
# ============================================================

def centroide_anillo(coordenadas):
    """
    Calcula aproximadamente el centro geométrico
    de un polígono.

    Lo necesitamos para colocar:

        Panamá
        32%

    en el centro de la provincia.
    """

    if not coordenadas:
        return None

    puntos = list(coordenadas)

    # Cerramos el polígono si fuese necesario.
    if puntos[0] != puntos[-1]:
        puntos.append(
            puntos[0]
        )

    area = 0
    centro_x = 0
    centro_y = 0

    for i in range(
        len(puntos) - 1
    ):

        x1, y1 = puntos[i][0], puntos[i][1]
        x2, y2 = puntos[i + 1][0], puntos[i + 1][1]

        cruzado = (
            x1 * y2
            -
            x2 * y1
        )

        area += cruzado

        centro_x += (
            x1 + x2
        ) * cruzado

        centro_y += (
            y1 + y2
        ) * cruzado

    if abs(area) < 0.0000001:
        return None

    centro_x /= (
        3 * area
    )

    centro_y /= (
        3 * area
    )

    return {
        "lon": centro_x,
        "lat": centro_y,
        "area": abs(area)
    }


def obtener_centro(geometry):
    """
    ArcGIS puede devolver:

    Polygon
    o
    MultiPolygon.

    Si hay varias islas/polígonos,
    utilizamos el polígono principal,
    es decir, el de mayor superficie.
    """

    tipo = geometry.get(
        "type"
    )

    coordenadas = geometry.get(
        "coordinates",
        []
    )

    candidatos = []


    # ----------------------------
    # POLYGON
    # ----------------------------

    if tipo == "Polygon":

        if coordenadas:

            resultado = centroide_anillo(
                coordenadas[0]
            )

            if resultado:
                candidatos.append(
                    resultado
                )


    # ----------------------------
    # MULTIPOLYGON
    # ----------------------------

    elif tipo == "MultiPolygon":

        for poligono in coordenadas:

            if not poligono:
                continue

            resultado = centroide_anillo(
                poligono[0]
            )

            if resultado:
                candidatos.append(
                    resultado
                )


    if not candidatos:
        return None, None


    # Elegimos la masa terrestre principal.
    principal = max(
        candidatos,
        key=lambda x: x["area"]
    )


    return (
        principal["lon"],
        principal["lat"]
    )


# ============================================================
# 13. OBTENER CENTRO DE CADA TERRITORIO
# ============================================================

centros = []


for feature in panama["features"]:

    clave = feature["properties"][
        "map_key"
    ]

    lon, lat = obtener_centro(
        feature["geometry"]
    )

    centros.append({
        "map_key": clave,
        "lon": lon,
        "lat": lat
    })


centros = pd.DataFrame(
    centros
)


# Agregamos longitud y latitud a nuestros datos.

data = data.merge(
    centros,
    on="map_key",
    how="left"
)


# ============================================================
# 14. CREAR EL MAPA
# ============================================================

fig = go.Figure()


# ============================================================
# 15. CAPA BASE GRIS
# ============================================================

# PRIMERA CAPA:
#
# Pintamos TODOS los territorios de gris.
#
# Después colocaremos encima los territorios
# que tienen Hard No.
#
# Por eso las comarcas sin datos permanecerán grises.

todos_los_ids = [
    feature["id"]
    for feature in panama["features"]
]


fig.add_trace(

    go.Choropleth(

        geojson=panama,

        locations=todos_los_ids,

        featureidkey="id",

        # Todos reciben el mismo valor.
        z=[1] * len(
            todos_los_ids
        ),

        # Un solo gris.
        colorscale=[
            [0, "#D9D9D9"],
            [1, "#D9D9D9"]
        ],

        showscale=False,

        marker_line_color="white",

        marker_line_width=1.1,

        hoverinfo="skip"
    )
)


# ============================================================
# 16. CAPA HARD NO
# ============================================================

# SEGUNDA CAPA:
#
# Solo colocamos encima las 10 provincias +
# Ngäbe Buglé.
#
# Cuanto mayor el porcentaje,
# más oscuro será el rojo.

fig.add_trace(

    go.Choropleth(

        geojson=panama,

        locations=data["map_key"],

        featureidkey="id",

        z=data["Hard No"],


        # ESCALA CONTINUA
        #
        # NO HAY:
        # Alto
        # Medio
        # Bajo
        #
        # Es simplemente de menor a mayor.

        colorscale=[

            [0.00, "#FCE8E6"],

            [0.20, "#F9C5C1"],

            [0.40, "#F28B82"],

            [0.60, "#E85D55"],

            [0.80, "#C9342F"],

            [1.00, "#8B0D0D"]

        ],


        zmin=data["Hard No"].min(),

        zmax=data["Hard No"].max(),


        colorbar=dict(

            title="Hard No (%)",

            thickness=14,

            len=0.60,

            tickvals=[
                data["Hard No"].min(),
                hard_no_nacional,
                data["Hard No"].max()
            ],

            ticktext=[
                f'{data["Hard No"].min()}%',
                f'{hard_no_nacional}%',
                f'{data["Hard No"].max()}%'
            ]
        ),


        customdata=data[
            [
                "Territorio",
                "N Entrevistas",
                "Base Ponderada"
            ]
        ],


        hovertemplate=(

            "<b>%{customdata[0]}</b>"

            "<br>Hard No: %{z:.0f}%"

            "<br>N entrevistas: %{customdata[1]}"

            "<br>Base ponderada: %{customdata[2]:.2f}"

            "<extra></extra>"
        ),


        marker_line_color="white",

        marker_line_width=1.3
    )
)


# ============================================================
# 17. LABELS DE PROVINCIAS
# ============================================================

# Creamos el texto:

data["Label"] = (

    "<b>"
    + data["Territorio"]
    + "</b>"

    + "<br>"

    + data["Hard No"].astype(str)

    + "%"
)


fig.add_trace(

    go.Scattergeo(

        lon=data["lon"],

        lat=data["lat"],

        text=data["Label"],

        mode="text",

        textposition="middle center",

        textfont=dict(
            size=10,
            color="#222222",
            family="Arial"
        ),

        hoverinfo="skip",

        showlegend=False
    )
)


# ============================================================
# 18. CONFIGURACIÓN GEOGRÁFICA
# ============================================================

fig.update_geos(

    # Zoom automático usando las geometrías.
    fitbounds="locations",

    # Quitamos mapa mundial, océanos, etc.
    visible=False,

    showcountries=False,

    showcoastlines=False,

    showframe=False,

    bgcolor="white"
)


# ============================================================
# 19. DISEÑO
# ============================================================

fig.update_layout(

    height=610,

    margin=dict(
        l=0,
        r=0,
        t=10,
        b=0
    ),

    paper_bgcolor="white"
)


# ============================================================
# 20. MAPA + RANKING
# ============================================================

col_mapa, col_ranking = st.columns(
    [2.2, 1]
)


# ----------------------------
# MAPA
# ----------------------------

with col_mapa:

    st.subheader(
        "Hard No por territorio"
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )

    st.caption(
        "Los tonos más oscuros representan una mayor "
        "incidencia de Hard No. Las comarcas sin información "
        "se muestran en gris."
    )


# ----------------------------
# RANKING
# ----------------------------

with col_ranking:

    st.subheader(
        "Ranking Territorial"
    )

    ranking = (
        data[
            [
                "Territorio",
                "Hard No",
                "N Entrevistas"
            ]
        ]
        .sort_values(
            "Hard No",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )


    # Creamos una columna visual con %.
    ranking["Hard No"] = (
        ranking["Hard No"]
        .astype(str)
        + "%"
    )


    st.dataframe(

        ranking,

        hide_index=True,

        use_container_width=True,

        column_config={

            "Territorio":
                st.column_config.TextColumn(
                    "Territorio"
                ),

            "Hard No":
                st.column_config.TextColumn(
                    "Hard No"
                ),

            "N Entrevistas":
                st.column_config.NumberColumn(
                    "N Entrevistas",
                    format="%d"
                )
        }
    )


# ============================================================
# 21. INFORMACIÓN OPCIONAL PARA APRENDER / DEBUG
# ============================================================

# Este expander te permite ver qué está llegando de ArcGIS.
#
# Lo puedes dejar mientras desarrollamos la aplicación
# y eliminarlo cuando terminemos.

with st.expander(
    "Ver territorios recibidos desde ArcGIS"
):

    st.dataframe(
        territorios_arcgis,
        hide_index=True,
        use_container_width=True
    )
