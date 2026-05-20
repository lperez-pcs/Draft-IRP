import streamlit as st
import pandas as pd
import plotly.express as px
import json
import unicodedata

st.set_page_config(page_title="Strategic Risk Platform", layout="wide")

st.title("Termómetro Nacional")
st.subheader("Territorial Risk Monitor")
st.caption("Pilot version — conceptual prototype with simulated data")

data = pd.DataFrame({
    "Provincia": [
        "Bocas del Toro", "Coclé", "Colón", "Chiriquí", "Darién",
        "Herrera", "Los Santos", "Panamá", "Panamá Oeste", "Veraguas"
    ],
    "Riesgo": [35, 78, 66, 52, 28, 41, 32, 57, 49, 61]
})

def categoria(score):
    if score >= 70:
        return "Alto"
    elif score >= 40:
        return "Medio"
    else:
        return "Bajo"

data["Categoria"] = data["Riesgo"].apply(categoria)

with open("panama-provincias.geojson", "r", encoding="utf-8") as f:
    panama = json.load(f)

def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = texto.lower()
    texto = texto.replace("provincia de ", "")
    texto = texto.strip()
    return texto

data["map_key"] = data["Provincia"].apply(normalizar)

for feature in panama["features"]:
    props = feature["properties"]
    nombre = props.get("NOMBRE", "")
    props["map_key"] = normalizar(nombre)

# Base gris: pinta todo el mapa primero.
# Como no se usa una categoría llamada "Sin data", no aparece en la leyenda.
base = pd.DataFrame({
    "map_key": [
        feature["properties"]["map_key"]
        for feature in panama["features"]
    ],
    "color_base": ["#D9D9D9"] * len(panama["features"])
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
        "Alto": "#D94B67",
        "Medio": "#F2A93B",
        "Bajo": "#74C476"
    },
    hover_name="Provincia",
    hover_data={
        "Riesgo": True,
        "Categoria": True,
        "map_key": False
    }
)

for trace in fig_data.data:
    fig.add_trace(trace)

fig.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False
)

fig.update_traces(
    marker_line_color="white",
    marker_line_width=0.8
)

fig.update_traces(
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="#222222",
        bordercolor="#777777"
    )
)

fig.update_layout(
    height=520,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    },
    legend_title_text="Categoría"
)

col1, col2 = st.columns([2, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Ranking territorial")

    ranking = data.sort_values("Riesgo", ascending=False)

    st.dataframe(
        ranking[["Provincia", "Riesgo", "Categoria"]],
        hide_index=True,
        use_container_width=True
    )
