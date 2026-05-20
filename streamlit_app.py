import streamlit as st
import pandas as pd
import plotly.express as px
import json
import unicodedata

st.set_page_config(page_title="Strategic Risk Platform", layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #061B33 0%, #082847 100%);
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.main-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #EEF0F4;
}
.kpi-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    border: 1px solid #EEF0F4;
    min-height: 120px;
}
.kpi-number {
    font-size: 38px;
    font-weight: 800;
    margin: 0;
}
.kpi-label {
    font-size: 15px;
    color: #334155;
}
.badge-alto {
    background:#F7B6C2;
    color:#7A1225;
    padding:5px 14px;
    border-radius:20px;
}
.badge-medio {
    background:#FFDFA8;
    color:#7A4A00;
    padding:5px 14px;
    border-radius:20px;
}
.badge-bajo {
    background:#BFE6C4;
    color:#145A24;
    padding:5px 14px;
    border-radius:20px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## SRP")
st.sidebar.markdown("### Strategic Risk Platform")
st.sidebar.markdown("---")
st.sidebar.markdown("🏠 **Dashboard**")
st.sidebar.markdown("🗺️ Mapa")
st.sidebar.markdown("📊 Ranking")
st.sidebar.markdown("📄 Reportes")
st.sidebar.markdown("🔔 Alertas")
st.sidebar.markdown("⚙️ Configuración")

# Header
col_title, col_date = st.columns([3, 1])

with col_title:
    st.title("Termómetro Nacional")
    st.subheader("Territorial Risk Monitor")
    st.caption("Pilot version — conceptual prototype with simulated data")

with col_date:
    st.markdown("**Actualizado:** 27 mayo 2025")
    vista = st.selectbox("Ver por:", ["Provincias"], label_visibility="collapsed")

# Data
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

# KPIs
alto = (data["Categoria"] == "Alto").sum()
medio = (data["Categoria"] == "Medio").sum()
bajo = (data["Categoria"] == "Bajo").sum()
total = len(data)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🛡️ Riesgo alto</div>
        <p class="kpi-number">{alto}</p>
        <div>provincias</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">📈 Riesgo medio</div>
        <p class="kpi-number">{medio}</p>
        <div>provincias</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">✅ Riesgo bajo</div>
        <p class="kpi-number">{bajo}</p>
        <div>provincias</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">🏛️ Total provincias</div>
        <p class="kpi-number">{total}</p>
        <div>provincias</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# GeoJSON
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

# Base gris para comarcas / territorios sin data
base = pd.DataFrame({
    "map_key": [feature["properties"]["map_key"] for feature in panama["features"]]
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
    category_orders={"Categoria": ["Alto", "Medio", "Bajo"]},
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
    marker_line_width=0.9
)

fig.update_layout(
    height=520,
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    legend_title_text="Categoría"
)

# Main layout
map_col, rank_col = st.columns([1.55, 1])

with map_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### Mapa de riesgo territorial")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("ⓘ Los colores representan el índice de riesgo país por provincia.")
    st.markdown('</div>', unsafe_allow_html=True)

with rank_col:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("### Ranking territorial")

    ranking = data.sort_values("Riesgo", ascending=False).copy()

    def badge(cat):
        if cat == "Alto":
            return '<span class="badge-alto">Alto</span>'
        elif cat == "Medio":
            return '<span class="badge-medio">Medio</span>'
        else:
            return '<span class="badge-bajo">Bajo</span>'

    ranking["Categoría"] = ranking["Categoria"].apply(badge)

    html = ranking[["Provincia", "Riesgo", "Categoría"]].to_html(
        escape=False,
        index=False
    )

    st.markdown(html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
