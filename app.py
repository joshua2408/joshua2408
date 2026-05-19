import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from geopy.geocoders import Nominatim

st.set_page_config(
    page_title="GeoMap Pro",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

geolocator = Nominatim(user_agent="my_streamlit_maps_app")

st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📍 GeoMap Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tu mapa interactivo con GPS en tiempo real y buscador de direcciones.</p>', unsafe_allow_html=True)

if "lat" not in st.session_state:
    st.session_state.lat = 32.5149  
if "lon" not in st.session_state:
    st.session_state.lon = -117.0382
if "address_name" not in st.session_state:
    st.session_state.address_name = "Tijuana, Baja California (Defecto)"

with st.sidebar:
    st.header("⚙️ Panel de Control")
    
    st.subheader("🛰️ Mi Ubicación Actual")
    if st.button("🎯 Detectar mi GPS", use_container_width=True):
        with st.spinner("Obteniendo señal GPS..."):
            loc = streamlit_js_eval(data_of='gcl', want_objects=True)
            if loc:
                st.session_state.lat = loc['coords']['latitude']
                st.session_state.lon = loc['coords']['longitude']
                st.session_state.address_name = "Tu ubicación actual"
                st.success("¡Ubicación detectada!")
            else:
                st.warning("Por favor, permite el acceso a la ubicación en tu navegador.")

    st.write("---")

    st.subheader("🔍 Buscar Lugar")
    search_query = st.text_input("Escribe una ciudad, monumento o dirección:")
    if st.button("Buscar en el mapa", use_container_width=True) and search_query:
        with st.spinner("Buscando coordenadas..."):
            try:
                location = geolocator.geocode(search_query)
                if location:
                    st.session_state.lat = location.latitude
                    st.session_state.lon = location.longitude
                    st.session_state.address_name = location.address
                    st.success(f"Encontrado: {location.address[:40]}...")
                else:
                    st.error("No se encontró el lugar.")
            except Exception as e:
                st.error("Error en la búsqueda.")

    st.write("---")

    st.subheader("🎨 Personalización")
    map_style = st.selectbox(
        "Estilo visual:",
        ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark_Matter"]
    )
    zoom_level = st.slider("Zoom por defecto", 2, 20, 12)

col1, col2 = st.columns([3, 1])

with col1:
    tiles_dict = {
        "OpenStreetMap": ("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", '&copy; OpenStreetMap | te extraño sakura😔'),
        "CartoDB Positron": ("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", '&copy; CartoDB | te extraño sakura😔'),
        "CartoDB Dark_Matter": ("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", '&copy; CartoDB | te extraño sakura😔')
    }
    
    selected_tile, attribution_text = tiles_dict[map_style]

    m = folium.Map(
        location=[st.session_state.lat, st.session_state.lon],
        zoom_start=zoom_level,
        tiles=selected_tile,
        attr=attribution_text
    )

    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        popup=st.session_state.address_name,
        tooltip="Ubicación activa",
        icon=folium.Icon(color="red", icon="map-pin", prefix="fa")
    ).add_to(m)

    map_data = st_folium(m, width="100%", height=550)

with col2:
    st.markdown("### 📊 Datos de Ubicación")
    st.info(f"**Lugar:**\n{st.session_state.address_name}")
    
    st.metric(label="Latitud", value=f"{st.session_state.lat:.6f}")
    st.metric(label="Longitud", value=f"{st.session_state.lon:.6f}")

    if map_data and map_data.get("last_clicked"):
        click_lat = map_data["last_clicked"]["lat"]
        click_lon = map_data["last_clicked"]["lng"]
        
        st.write("---")
        st.markdown("**📍 Último punto seleccionado:**")
        st.code(f"Lat: {click_lat:.6f}\nLon: {click_lon:.6f}", language="text")
        
        if st.button("Centrar mapa aquí", use_container_width=True):
            st.session_state.lat = click_lat
            st.session_state.lon = click_lon
            st.session_state.address_name = "Punto seleccionado manualmente"
            st.rerun()