import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Mi App de Mapas", layout="wide")

st.title("📍 Localizador y Mapa Interactivo")
st.markdown("Esta aplicación muestra un mapa estilo Google Maps usando Folium.")

# 1. Parámetros de ubicación inicial (Latitud, Longitud)
# Por defecto: Ciudad de México
lat_inicial = 19.4326
lon_inicial = -99.1332

st.sidebar.header("Configuración del Mapa")
zoom = st.sidebar.slider("Nivel de Zoom", 1, 20, 12)
estilo = st.sidebar.selectbox(
    "Estilo del mapa",
    ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "CartoDB positron"]
)

m = folium.Map(location=[lat_inicial, lon_inicial], zoom_start=zoom, tiles=estilo)

folium.Marker(
    [lat_inicial, lon_inicial], 
    popup="¡Estás aquí!", 
    tooltip="Ubicación Principal",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# 'st_folium' permite que el mapa sea interactivo y devuelva datos al hacer clic
output = st_folium(m, width=1200, height=600)

if output["last_clicked"]:
    st.write(f"**Coordenadas seleccionadas:** Lat: {output['last_clicked']['lat']}, Lon: {output['last_clicked']['lng']}")