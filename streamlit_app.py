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

st.markdown("""
<div class="title-section">
    <h1 style="margin: 0 0 0.5rem 0; font-size: 32px;">Termómetro Nacional</h1>
    <p style="margin: 0; font-size: 16px; color: #666;">Territorial Risk Monitor — Panama</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 12px; color: #999;">Pilot version with simulated data · Updated May 2025</p>
</div>
""", unsafe_allow_html=True)


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
# KPI DASHBOARD
# ============================================================

k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Índice Nacional</div>
            <p class="kpi-number">{indice_nacional_desempleo}</p>
            <div class="kpi-unit">desempleo normalizado</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    alto = int((data["Categoria"] == "Alto").sum())
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Riesgo Alto</div>
            <p class="kpi-number">{alto}</p>
            <div class="kpi-unit">provincias/comarcas</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    medio = int((data["Categoria"] == "Medio").sum())
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Riesgo Medio</div>
            <p class="kpi-number">{medio}</p>
            <div class="kpi-unit">provincias/comarcas</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    bajo = int((data["Categoria"] == "Bajo").sum())
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">Riesgo Bajo</div>
            <p class="kpi-number">{bajo}</p>
            <div class="kpi-unit">provincias/comarcas</div>
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
    nombre = propiedades.get("Provincia", "")
    propiedades["map_key"] = normalizar(nombre)


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
        "Desempleo": ":.0f",
        "Categoria": True,
        "map_key": False
    }
)

fig_data.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False
)

fig_data.update_traces(
    marker_line_color="white",
    marker_line_width=1.2,
    hovertemplate="<b>%{customdata[1]}</b><br>Desempleo: %{customdata[0]:.0f}<br>Nivel: %{customdata[2]}<extra></extra>"
)

fig_data.update_layout(
    height=550,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={"r": 0, "t": 20, "l": 0, "b": 0},
    legend_title_text="Nivel de Riesgo",
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
    st.markdown('<h3 class="section-title">Mapa </h3>', unsafe_allow_html=True)
    st.plotly_chart(fig_data, use_container_width=True)
    st.markdown(
        '<p class="info-caption">Los tonos más intensos representan mayores niveles de desempleo normalizado. Escala: Rojo claro (Bajo) → Rojo coral (Medio) → Rojo intenso (Alto).</p>',
        unsafe_allow_html=True
    )

with rank_col:
    st.markdown('<h3 class="section-title">Ranking Territorial</h3>', unsafe_allow_html=True)
    
    ranking = data.sort_values("Desempleo", ascending=False).copy()
    
    def badge(cat):
        if cat == "Alto":
            return '<span class="badge-alto">Alto</span>'
        elif cat == "Medio":
            return '<span class="badge-medio">Medio</span>'
        return '<span class="badge-bajo">Bajo</span>'
    
    ranking["Nivel"] = ranking["Categoria"].apply(badge)
    
    ranking_html = ranking[["Territorio", "Desempleo", "Nivel"]].to_html(
        escape=False,
        index=False,
        col_space={"Territorio": "60%", "Desempleo": "20%", "Nivel": "20%"}
    )
    
    st.markdown(
        f'<div class="container-box">{ranking_html}</div>',
        unsafe_allow_html=True
    )


# ============================================================
# SECCIÓN: ÍNDICE DE MISERIA
# ============================================================

st.markdown("")
st.markdown('<h2 style="font-size: 24px; font-weight: 700; margin-top: 2rem;">Índice de Miseria</h2>', unsafe_allow_html=True)

col_miseria, col_referencia = st.columns([2.2, 1], gap="medium")

with col_miseria:
    st.markdown('<h3 class="section-title">Resultado Territorial</h3>', unsafe_allow_html=True)
    
    tabla_miseria = data[["Territorio", "Indice de Miseria"]].sort_values(
        "Indice de Miseria",
        ascending=False
    )
    
    tabla_html = tabla_miseria.to_html(
        escape=False,
        index=False
    )
    
    st.markdown(
        f'<div class="container-box">{tabla_html}</div>',
        unsafe_allow_html=True
    )

with col_referencia:
    st.markdown('<h3 class="section-title">Referencia Nacional</h3>', unsafe_allow_html=True)
    
    referencia = pd.DataFrame({
        "Indicador": ["Índice de Miseria", "Desempleo"],
        "Valor Nacional": [indice_nacional_miseria, indice_nacional_desempleo]
    })
    
    ref_html = referencia.to_html(
        escape=False,
        index=False
    )
    
    st.markdown(
        f'<div class="container-box">{ref_html}</div>',
        unsafe_allow_html=True
    )
