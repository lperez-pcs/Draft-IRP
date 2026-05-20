import streamlit as st
import pandas as pd
import plotly.express as px
import json
import unicodedata

# Configuración general de la página
st.set_page_config(page_title="Strategic Risk Platform", layout="wide")

st.title("Termómetro Nacional")
st.subheader("Territorial Risk Monitor")
st.caption("Pilot version — conceptual prototype with simulated data")

# Datos de prueba del score por provincia
data = pd.DataFrame({
    "Provincia": [
        "Bocas del Toro",
        "Coclé",
        "Colón",
        "Chiriquí",
        "Darién",
        "Herrera",
        "Los Santos",
        "Panamá",
        "Panamá Oeste",
        "Veraguas"
    ],
    "Riesgo": [35, 78, 66, 52, 28, 41, 32, 57, 49, 61]
})

# Clasificación del nivel de riesgo
def categoria(score):
    if score >= 70:
        return "Alto"
    elif score >= 40:
        return "Medio"
    else:
        return "Bajo"

data["Categoria"] = data["Riesgo"].apply(categoria)

# Cargamos el mapa GeoJSON
with open("panama-provincias.geojson", "r", encoding="utf-8") as f:
    panama = json.load(f)

# Normalizamos nombres para evitar problemas con tildes o diferencias de texto
def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )
    texto = texto.lower()
    texto = texto.replace("provincia de ", "")
    texto = texto.strip()
    return texto

# Llave limpia para conectar datos con el mapa
data["map_key"] = data["Provincia"].apply(normalizar)

# Llave limpia dentro del GeoJSON
for feature in panama["features"]:
    props = feature["properties"]
    nombre = props.get("name", "")
    props["map_key"] = normalizar(nombre)

# Capa base gris para territorios sin data, como comarcas
base_map = pd.DataFrame({
    "map_key": [
        feature["properties"]["map_key"]
        for feature in panama["features"]
    ],
    "Base": ["Sin información"] * len(panama["features"])
})

# Primero pintamos todo el mapa en gris
fig = px.choropleth(
    base_map,
    geojson=panama,
    locations="map_key",
    featureidkey="properties.map_key",
    color="Base",
    color_discrete_map={
        "Sin información": "#D9D9D9"
    },
    hover_data={
        "Base": False,
        "map_key": False
    }
)

# Luego pintamos encima solo las provincias con datos
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

# Agregamos las provincias con data sobre la base gris
for trace in fig_data.data:
    fig.add_trace(trace)

# Ajustes visuales del mapa
fig.update_geos(
    fitbounds="locations",
    visible=False,
    showcountries=False,
    showcoastlines=False,
    showframe=False
)

# Bordes blancos para separación tipo Google Trends
fig.update_traces(
    marker_line_color="white",
    marker_line_width=1.1
)

# Hover más elegante para dar sensación de enfoque
fig.update_traces(
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_color="#333333",
        bordercolor="#7A7A7A"
    )
)

# Plantilla del tooltip al pasar el mouse
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Riesgo: %{customdata[0]}<br>Categoría: %{customdata[1]}<extra></extra>"
)

fig.update_layout(
    height=520,
    paper_bgcolor="white",
    plot_bgcolor="white",
    geo=dict(
        bgcolor="rgba(0,0,0,0)"
    ),
    margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    },
    legend_title_text="Categoría"
)

# Layout: mapa + ranking
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
