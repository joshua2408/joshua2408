import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Generador de Corazones Pro", page_icon="❤️", layout="centered")

# Estilos ocultos
st.markdown("""
    <style>
    .mensaje-fantasma {
        font-size: 0px !important;
        color: transparent !important;
        line-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        user-select: none;
    }
    </style>
""", unsafe_allow_html=True)

st.title("❤️ Silueta de Corazón Personalizada")
st.write("Crea un corazón con un contorno definido y relleno texturizado usando el nombre que quieras.")

# --- ENTRADAS DEL USUARIO ---
nombre = st.text_input("Introduce el nombre:", value="Ambar", max_chars=20)
color_elegido = st.color_picker("Selecciona el color:", "#FF1493")

# Controles separados para definir la silueta a gusto
st.sidebar.header("🎛️ Ajustes de Silueta")
densidad_contorno = st.sidebar.slider("Densidad del contorno (Silueta):", 100, 800, 400, step=50)
densidad_relleno = st.sidebar.slider("Densidad del relleno (Interior):", 200, 1500, 600, step=50)

if nombre:
    with st.spinner("Dibujando silueta..."):
        # Crear la figura de Matplotlib
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
        ax.set_facecolor('black')

        # --- 1. GENERAR EL CONTORNO (SILUETA PERFECTA) ---
        t_contorno = np.linspace(0, 2 * np.pi, densidad_contorno)
        x_contorno = 16 * np.sin(t_contorno) ** 3
        y_contorno = 13 * np.cos(t_contorno) - 5 * np.cos(2*t_contorno) - 2 * np.cos(3*t_contorno) - np.cos(4*t_contorno)

        # Dibujar contorno
        for i in range(densidad_contorno):
            ax.text(
                x_contorno[i], y_contorno[i], nombre,
                color=color_elegido,
                fontsize=8,
                fontweight='bold',
                ha='center', va='center',
                rotation=0, # Sin rotación en el contorno para que se lea la forma claramente
                alpha=0.9
            )

        # --- 2. GENERAR EL RELLENO INTERIOR ---
        t_relleno = np.linspace(0, 2 * np.pi, densidad_relleno)
        x_infinitesimal = 16 * np.sin(t_relleno) ** 3
        y_infinitesimal = 13 * np.cos(t_relleno) - 5 * np.cos(2*t_relleno) - 2 * np.cos(3*t_relleno) - np.cos(4*t_relleno)
        
        factor_adentro = np.random.uniform(0.0, 0.92, densidad_relleno) ** 0.6
        x_interior = x_infinitesimal * factor_adentro
        y_interior = y_infinitesimal * factor_adentro

        # Dibujar relleno (ajustado para mayor visibilidad sin saturar)
        for i in range(densidad_relleno):
            size = np.random.uniform(6.0, 8.5) # Un poco más grandes (antes 5 a 7.5)
            rotation = np.random.uniform(-15, 15) # Rotación ligeramente más sutil
            
            ax.text(
                x_interior[i], y_interior[i], nombre,
                color=color_elegido,
                fontsize=size,
                ha='center', va='center',
                rotation=rotation,
                alpha=0.55 # Opacidad intermedia perfecta (antes 0.4)
            )

        # Ajustes de límites y visualización
        ax.set_xlim(-19, 19)
        ax.set_ylim(-18, 15)
        ax.axis('off')

        # Mostrar en Streamlit
        st.pyplot(fig)
        st.success(f"¡Silueta generada para {nombre}!")

# --- MENSAJE INVISIBLE ---
st.markdown('<p class="mensaje-fantasma">te extraño sakura</p>', unsafe_allow_html=True)