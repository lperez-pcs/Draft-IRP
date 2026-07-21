import json
import unicodedata

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Strategic Risk Platform",
    layout="wide"
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

    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.07);
        border: 1px solid #E9EDF2;
        min-height: 115px;
    }

    .kpi-label {
        font-size: 14px;
        color: #475569;
        margin-bottom: 4px;
    }

    .kpi-number {
        font-size: 34px;
        font-weight: 800;
        color: #0F172A;
        margin: 0;
        line-height: 1.1;
    }

    .kpi-unit {
        font-size: 13px;
        color: #64748B;
        margin-top: 5px;
    }

    .badge-alto {
        background: #E7B1B7;
        color: #771824;
        padding: 5px 13px;
        border-radius: 20px;
        display: inline-block;
        min-width: 62px;
        text-align: center;
    }

    .badge-medio {
        background: #F3D8DB;
        color: #9A3E47;
        padding: 5px 13px;
        border-radius: 20px;
        display: inline-block;
        min-width: 62px;
        text-align: center;
    }

    .badge-bajo {
        background: #FAECEE;
        color: #A45D64;
        padding: 5px 13px;
        border-radius: 20px;
        display: inline-block;
        min-width: 62px;
        text-align: center;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }

    th {
        background: #F7F8FA;
        color: #334155;
        padding: 10px;
        text-align: left;
        border: 1px solid #E5E7EB;
    }

    td {
        padding: 9px 10px;
        border: 1px solid #E5E7EB;
    }

    tbody tr:hover {
        background: #FAFAFA;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ENCABEZADO
# ============================================================

col_title, col_update = st.columns([4, 1])

with col_title:
    st.title("Termómetro Nacional")
    st.subheader("Territorial Risk Monitor")
    st.caption(
        "Pilot version — conceptual prototype with simulated data"
    )

with col_update:
    st.markdown("**Actualizado:** mayo 2025")


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
    "Indice de Miseria": [
        100,
        93,
        100,
        54,
        100,
        69,
        33,
        48,
        56,
        66,
        15
    ],
    "Desempleo": [
        100,
        100,
        100,
        74,
        100,
        100,
        70,
        55,
        74,
        95,
        48
    ]
})

indice_nacional_desempleo = 85
indice_nacional_miseria = 65


# ============================================================
# CLASIFICACIÓN
# ============================================================

def categoria(score):
    if score >= 70:
        return "Alto"
    elif score >= 40:
        return "Medio"
    else:
        return "Bajo"


data["Categoria"] = data["Desempleo"].apply(categoria)


# ============================================================
# KPI
# ============================================================

alto = int((data["Categoria"] == "Alto").sum())
medio = int((data["Categoria"] == "Medio").sum())
bajo = int((data["Categoria"] == "Bajo").sum())

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Índice nacional</div>
            <p class="kpi-number">{indice_nacional_desempleo}</p>
            <div class="kpi-unit">desempleo normalizado</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Riesgo alto</div>
            <p class="kpi-number">{alto}</p>
            <div class="kpi-unit">territorios</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Riesgo medio</div>
            <p class="kpi-number">{medio}</p>
            <div class="kpi-unit">territorios</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Riesgo bajo</div>
            <p class="kpi-number">{bajo}</p>
            <div class="kpi-unit">territorios</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GEOJSON
# ============================================================

with open(
    "panama-provincias.geojson",
    "r",
    encoding="utf-8"
) as f:
    panama = json.load(f)


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
    texto = texto.strip()

    return texto


data["map_key"] = data["Territorio"].apply(normalizar)

for feature in panama["features"]:
    propiedades = feature["properties"]
    nombre = propiedades.get("NOMBRE", "")
    propiedades["map_key"] = normalizar(nombre)


# ============================================================
# CAPA BASE GRIS
# ============================================================

base = pd.DataFrame({
    "map_key": [
        feature["properties"]["map_key"]
        for feature in panama["features"]
    ]
})

fig = px.choropleth(
    base,
    geojson=panama,
    locations="map_key",
    featureidkey="properties.map_key",
    color_discrete_sequence=["#D9D9D9"]
)

fig.data[0].showlegend = False
fig.data[0].hoverinfo = "skip"
fig.data[0].hovertemplate = None


# ============================================================
# CAPA DE DESEMPLEO
# ============================================================

fig_data = px.choropleth(
    data,
    geojson=panama,
    locations="map_key",
    featureidkey="properties.map_key",
    color="Categoria",

    category_orders={
        "Categoria": [
            "Alto",
            "Medio",
            "Bajo"
        ]
    },

    color_discrete_map={
        "Alto": "#8F1724",
        "Medio": "#C95F69",
        "Bajo": "#EEC4C8"
    },

    hover_name="Territorio",

    hover_data={
        "Desempleo": True,
        "Categoria": True,
        "map_key": False
    }
)

for trace in fig_data.data:
    fig.add_trace(trace)


# ============================================================
# FORMATO DEL MAPA
# ============================================================

fig.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False
)

fig.update_traces(
    marker_line_color="white",
    marker_line_width=0.9
)

fig.update_layout(
    height=500,
    paper_bgcolor="white",
    plot_bgcolor="white",

    margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    },

    legend_title_text="Nivel de riesgo",

    legend={
        "orientation": "v",
        "yanchor": "top",
        "y": 1,
        "xanchor": "right",
        "x": 1
    }
)


# ============================================================
# MAPA Y RANKING
# ============================================================

map_col, rank_col = st.columns([1.6, 1])

with map_col:
    with st.container(border=True):
        st.markdown("### Mapa de desempleo normalizado")

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption(
            "Los tonos más oscuros representan mayores niveles "
            "de desempleo normalizado."
        )

with rank_col:
    with st.container(border=True):
        st.markdown("### Ranking territorial")

        ranking = data.sort_values(
            "Desempleo",
            ascending=False
        ).copy()

        def badge(cat):
            if cat == "Alto":
                return (
                    '<span class="badge-alto">'
                    'Alto'
                    '</span>'
                )

            elif cat == "Medio":
                return (
                    '<span class="badge-medio">'
                    'Medio'
                    '</span>'
                )

            return (
                '<span class="badge-bajo">'
                'Bajo'
                '</span>'
            )

        ranking["Nivel"] = ranking["Categoria"].apply(badge)

        ranking_html = ranking[
            [
                "Territorio",
                "Desempleo",
                "Nivel"
            ]
        ].to_html(
            escape=False,
            index=False
        )

        st.markdown(
            ranking_html,
            unsafe_allow_html=True
        )


# ============================================================
# ÍNDICE DE MISERIA
# ============================================================

st.markdown("## Índice de Miseria")

col_miseria, col_referencia = st.columns([2.2, 1])

with col_miseria:
    with st.container(border=True):
        st.markdown("### Resultado territorial")

        tabla_miseria = data[
            [
                "Territorio",
                "Indice de Miseria"
            ]
        ].sort_values(
            "Indice de Miseria",
            ascending=False
        )

        st.dataframe(
            tabla_miseria,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Territorio": "Territorio",
                "Indice de Miseria":
                    st.column_config.NumberColumn(
                        "Índice de Miseria",
                        format="%d"
                    )
            }
        )

with col_referencia:
    with st.container(border=True):
        st.markdown("### Referencia nacional")

        referencia = pd.DataFrame({
            "Indicador": [
                "Índice de Miseria",
                "Desempleo"
            ],
            "Valor nacional": [
                indice_nacional_miseria,
                indice_nacional_desempleo
            ]
        })

        st.dataframe(
            referencia,
            hide_index=True,
            use_container_width=True
        )
