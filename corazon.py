import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Generador de Corazones", page_icon="❤️", layout="centered")

# Ocultar menús visuales innecesarios y estilos limpios
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

st.title("❤️ Generador de Corazón Personalizado")
st.write("Escribe un nombre para diseñar un corazón formado por miles de repeticiones.")

# --- ENTRADAS DEL USUARIO ---
nombre = st.text_input("Introduce el nombre que quieras:", value="Sakura", max_chars=20)
color_elegido = st.color_picker("Selecciona el color del corazón:", "#FF1493")
cantidad_nombres = st.slider("Densidad del corazón (Cantidad de nombres):", 500, 3000, 1500, step=100)

if nombre:
    with st.spinner("Creando tu corazón..."):
        # 1. Definir la ecuación matemática del corazón
        t = np.linspace(0, 2 * np.pi, cantidad_nombres)
        
        # Coordenadas base del contorno del corazón
        x_base = 16 * np.sin(t) ** 3
        y_base = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        
        # Generar un factor aleatorio para rellenar el interior del corazón
        # Usamos una distribución que empuje los puntos hacia adentro
        factor_relleno = np.random.uniform(0, 1, cantidad_nombres) ** 0.5
        
        x = x_base * factor_relleno
        y = y_base * factor_relleno

        # 2. Crear la figura con Matplotlib
        fig, ax = plt.subplots(figsize=(8, 8), facecolor='black')
        ax.set_facecolor('black')

        # 3. Dibujar cada nombre en sus coordenadas correspondientes
        for i in range(cantidad_nombres):
            # Variar ligeramente el tamaño y la rotación para darle textura visual
            size = np.random.uniform(6, 10)
            rotation = np.random.uniform(-15, 15)
            
            ax.text(
                x[i], y[i], nombre,
                color=color_elegido,
                fontsize=size,
                fontweight='bold',
                family='sans-serif',
                ha='center', va='center',
                rotation=rotation,
                alpha=np.random.uniform(0.6, 1.0) # Opacidad variable para dar profundidad
            )

        # Ajustes de los límites del gráfico para que no se corte
        ax.set_xlim(-18, 18)
        ax.set_ylim(-18, 15)
        ax.axis('off') # Ocultar los ejes numéricos

        # 4. Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        
        st.success(f"¡Corazón creado con éxito usando el nombre '{nombre}'!")

# --- MENSAJE INVISIBLE (Manteniendo la opción 2 del paso anterior) ---
st.markdown('<p class="mensaje-fantasma">te extraño sakura</p>', unsafe_allow_html=True)