import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
from geopy.geocoders import Nominatim

# Configuración avanzada de la página
st.set_page_config(
    page_title="GeoMap Pro",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar el buscador de direcciones (User_agent es requerido por Nominatim)
geolocator = Nominatim(user_agent="my_streamlit_maps_app")

# --- ESTILOS CSS PERSONALIZADOS ---
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

# --- ESTADO DE LA SESIÓN (Para recordar ubicaciones) ---
if "lat" not in st.session_state:
    st.session_state.lat = 19.4326  # CDMX por defecto
if "lon" not in st.session_state:
    st.session_state.lon = -99.1332
if "address_name" not in st.session_state:
    st.session_state.address_name = "Ciudad de México (Defecto)"

# --- BARRA LATERAL (CONTROLES) ---
with st.sidebar:
    st.header("⚙️ Panel de Control")
    
    # 1. BOTÓN DE GPS REAL
    st.subheader("🛰️ Mi Ubicación Actual")
    if st.button("🎯 Detectar mi GPS", use_container_width=True):
        with st.spinner("Obteniendo señal GPS del navegador..."):
            # Obtiene la ubicación del navegador del usuario vía JS
            loc = streamlit_js_eval(data_of='gcl', want_objects=True)
            if loc:
                st.session_state.lat = loc['coords']['latitude']
                st.session_state.lon = loc['coords']['longitude']
                st.session_state.address_name = "Tu ubicación actual"
                st.success("¡Ubicación detectada con éxito!")
            else:
                st.warning("Por favor, permite el acceso a la ubicación en tu navegador.")

    st.write("---")

    # 2. BUSCADOR DE DIRECCIONES
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
                    st.error("No se encontró el lugar. Intenta ser más específico.")
            except Exception as e:
                st.error("Error en la búsqueda. Intenta de nuevo.")

    st.write("---")

    # 3. PERSONALIZACIÓN DEL MAPA
    st.subheader("🎨 Personalización")
    map_style = st.selectbox(
        "Estilo visual:",
        ["OpenStreetMap", "CartoDB Positron", "CartoDB Dark_Matter"]
    )
    zoom_level = st.slider("Zoom por defecto", 2, 20, 14)

# --- CUERPO PRINCIPAL ---
col1, col2 = st.columns([3, 1])

with col1:
    # Crear el mapa interactivo de Folium
    m = folium.Map(
        location=[st.session_state.lat, st.session_state.lon],
        zoom_start=zoom_level,
        tiles=map_style
    )

    # Añadir marcador de la ubicación actual
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        popup=st.session_state.address_name,
        tooltip="Ubicación activa",
        icon=folium.Icon(color="red", icon="map-pin", prefix="fa")
    ).add_to(m)

    # Renderizar el mapa de manera responsiva
    map_data = st_folium(m, width="100%", height=550)

with col2:
    st.markdown("### 📊 Datos de Ubicación")
    st.info(f"**Lugar:**\n{st.session_state.address_name}")
    
    # Mostrar coordenadas actuales en cajitas limpias
    st.metric(label="Latitud", value=f"{st.session_state.lat:.6f}")
    st.metric(label="Longitud", value=f"{st.session_state.lon:.6f}")

    # Capturar clics nuevos en el mapa
    if map_data and map_data.get("last_clicked"):
        click_lat = map_data["last_clicked"]["lat"]
        click_lon = map_data["last_clicked"]["lng"]
        
        st.write("---")
        st.markdown("**📍 Último punto seleccionado:**")
        st.code(f"Lat: {click_lat:.6f}\nLon: {click_lon:.6f}", language="text")
        
        # Botón para mover el marcador allí
        if st.button("Centrar mapa aquí", use_container_width=True):
            st.session_state.lat = click_lat
            st.session_state.lon = click_lon
            st.session_state.address_name = "Punto seleccionado manualmente"
            st.rerun()