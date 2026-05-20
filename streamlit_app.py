import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Strategic Risk Platform", layout="wide")

st.title("Strategic Risk Intelligence Platform")
st.subheader("Territorial Risk Monitor")
st.caption("Pilot version — conceptual prototype with simulated data")

data = pd.DataFrame({
    "Provincia":[
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

    "Riesgo":[35,78,66,52,28,41,32,57,49,61]
})

def categoria(score):
    if score>=70:
        return "Alto"
    elif score>=40:
        return "Medio"
    else:
        return "Bajo"

data["Categoria"]=data["Riesgo"].apply(categoria)

with open("panama.geojson","r",encoding="utf-8") as f:
    panama=json.load(f)

fig=px.choropleth_mapbox(
    data,
    geojson=panama,
    locations="Provincia",
    featureidkey="properties.name",
    color="Categoria",

    color_discrete_map={
        "Bajo":"#2ECC71",
        "Medio":"#F1C40F",
        "Alto":"#E74C3C"
    },

    hover_name="Provincia",

    hover_data={
        "Riesgo":True
    },

    center={"lat":8.5,"lon":-80},
    zoom=6,
    opacity=.75
)

fig.update_layout(
    mapbox_style="open-street-map"
)

col1,col2=st.columns([2,1])

with col1:
    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    st.subheader("Ranking territorial")

    ranking=data.sort_values(
        "Riesgo",
        ascending=False
    )

    st.dataframe(
        ranking[
            ["Provincia","Riesgo","Categoria"]
        ],
        hide_index=True
    )
