import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(
    page_title="Levantamiento Etapa 2 - ERGOSOLAR",
    page_icon="Ergogo.png",
    layout="wide"
)

st.title("Levantamiento Preventa - Etapa 2")
st.write("Captura los datos del levantamiento preventa en campo y exporta la información en formato Excel.")

# Pestañas para organizar la captura de datos
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 1. Fotos de Drone",
    "🪜 2. Acceso y Seguridad",
    "🏠 3. Tipo de Techo y Naves",
    "🏗️ 4. Requisitos Adicionales y Estructural"
])

# ---------------------------------------------------------
# PESTAÑA 1: FOTOGRAFÍAS DE DRONE
# ---------------------------------------------------------
with tab1:
    st.header("📸 Checklist de Fotografías de Drone")
    st.info("Marca las vistas que hayan sido capturadas correctamente en sitio (mínimo 3 fotos por vista).")

    col1, col2 = st.columns(2)
    with col1:
        drone_techumbre = st.checkbox("Techumbre", value=True)
        drone_aguila = st.checkbox("Vistas aéreas (Vista de águila)", value=True)
        drone_frontales = st.checkbox("Vistas frontales", value=True)
        drone_laterales = st.checkbox("Vistas laterales", value=True)
        drone_traseras = st.checkbox("Vistas traseras", value=True)

    with col2:
        drone_lamina = st.checkbox("Fotos de la lámina (Identificación de tipo y medidas)", value=True)
        drone_obstaculos = st.checkbox("Fotos de obstáculos", value=True)
        drone_video = st.checkbox("Video de drone (Recorrido de techo)", value=False)
        drone_terreno = st.checkbox("Terreno y periferia de la propiedad", value=True)

# ---------------------------------------------------------
# PESTAÑA 2: ACCESO Y SEGURIDAD EN TECHUMBRE
# ---------------------------------------------------------
with tab2:
    st.header("🪜 Acceso y Revisión de Seguridad en Techumbre")
    
    col1, col2 = st.columns(2)
    with col1:
        facil_acceso = st.radio("¿Existe un acceso a techumbre de fácil acceso?", ["Si", "No"], index=0)
        obs_acceso = st.text_input("Observaciones de acceso")

        equipo_adic = st.radio("¿Se requiere equipo adicional para acceso? (Escalera, arnés, anclaje móvil)", ["No", "Si"], index=0)
        obs_equipo = st.text_input("Observaciones equipo adicional")

        lineas_energ = st.radio("¿Existen líneas energizadas en el área a instalar?", ["No", "Si"], index=0)
        obs_lineas = st.text_input("Observaciones líneas energizadas")

    with col2:
        estado_techo = st.radio("¿El estado físico del techo/losa/terreno es bueno?", ["Si", "No"], index=0)
        obs_estado = st.text_input("Observaciones estado del techo")

        pasos_gato = st.radio("¿Existen pasos de gato?", ["No", "Si"], index=0)
        obs_pasos = st.text_input("Observaciones pasos de gato")

        lineas_vida = st.radio("¿Existen líneas de vida?", ["No", "Si"], index=0)
        obs_vida = st.text_input("Observaciones líneas de vida")

# ---------------------------------------------------------
# PESTAÑA 3: TIPO DE TECHO Y DIMENSIONES DE NAVES
# ---------------------------------------------------------
with tab3:
    st.header("🏠 Identificación de Techo y Dimensiones de Naves")

    st.subheader("Tipo de Techo")
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        tipo_techo_sel = st.selectbox(
            "Tipo de Techo Principal",
            ["Lámina engargolada", "Losa de concreto", "Lámina trapezoidal", "Lámina galvateja", "Lámina multipanel", "Otro"]
        )
    with col_t2:
        cantidad_techo = st.text_input("Cantidad / N° de secciones", value="1")
    with col_t3:
        calibre_espesor = st.text_input("Calibre o Espesor", value="Cal 24")

    st.markdown("---")
    st.subheader("Dimensiones por Nave")
    
    nave_tab1, nave_tab2, nave_tab3, nave_tab4 = st.tabs(["Nave 1", "Nave 2", "Nave 3", "Nave 4"])
    
    naves_data = {}
    for i, tab in enumerate([nave_tab1, nave_tab2, nave_tab3, nave_tab4], start=1):
        with tab:
            c1, c2, c3 = st.columns(3)
            with c1:
                alt_menor = st.number_input(f"Altura menor B (m) - Nave {i}", value=8.66 if i==1 else 0.0)
                alt_mayor = st.number_input(f"Altura mayor A (m) - Nave {i}", value=10.70 if i==1 else 0.0)
                ancho_nave = st.number_input(f"Ancho D (m) - Nave {i}", value=33.60 if i==1 else 0.0)
            with c2:
                largo_nave = st.number_input(f"Largo C (m) - Nave {i}", value=46.20 if i==1 else 0.0)
                inclinacion = st.number_input(f"Inclinación ° (α) - Nave {i}", value=2.40 if i==1 else 0.0)
            with c3:
                orientacion = st.text_input(f"Orientación - Nave {i}", value="Este-Oeste" if i==1 else "N/A")
                num_aguas = st.number_input(f"N° de aguas - Nave {i}", value=1 if i==1 else 1, step=1)
            
            naves_data[f"Nave {i}"] = {
                "Altura menor (B)": alt_menor,
                "Altura mayor (A)": alt_mayor,
                "Ancho (D)": ancho_nave,
                "Largo (C)": largo_nave,
                "Inclinación (α)": inclinacion,
                "Orientación": orientacion,
                "N° de aguas": num_aguas
            }

# ---------------------------------------------------------
# PESTAÑA 4: REQUISITOS ADICIONALES Y EVALUACIÓN ESTRUCTURAL
# ---------------------------------------------------------
with tab4:
    st.header("🏗️ Requisitos Adicionales de Instalaciones")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        esc_marina = st.radio("Escalera marina", ["Si", "No"], index=0)
        obs_esc = st.text_input("Observaciones Escalera Marina", value="Está de fácil acceso")

        toma_agua = st.radio("Toma de agua cercana", ["Si", "No"], index=0)
        obs_agua = st.text_input("Observaciones Toma de Agua", value="Se requiere obra hidráulica")

    with col_r2:
        pararrayos = st.radio("Sistema de pararrayos", ["Si", "No"], index=0)
        obs_pararrayos = st.text_input("Observaciones Pararrayos", value="Medidas en retensores")

    st.markdown("---")
    st.subheader("Evaluación Estructural General")
    eval_estructural = st.text_area("Comentarios sobre evaluación estructural (requiere DRO / refuerzos):")

    st.markdown("---")
    st.subheader("📄 Generar y Descargar Archivo Excel de Etapa 2")

    def generar_excel_etapa2():
        output = io.BytesIO()
        
        # 1. Datos de Drone
        df_drone = pd.DataFrame({
            "Vista / Fotografía": [
                "Techumbre", "Vistas aéreas (Vista de águila)", "Vistas frontales", 
                "Vistas laterales", "Vistas traseras", "Fotos de lámina", 
                "Fotos de obstáculos", "Video de drone", "Terreno y periferia"
            ],
            "Estatus": [
                "✔" if drone_techumbre else "X",
                "✔" if drone_aguila else "X",
                "✔" if drone_frontales else "X",
                "✔" if drone_laterales else "X",
                "✔" if drone_traseras else "X",
                "✔" if drone_lamina else "X",
                "✔" if drone_obstaculos else "X",
                "✔" if drone_video else "X",
                "✔" if drone_terreno else "X"
            ]
        })

        # 2. Seguridad y Acceso
        df_seguridad = pd.DataFrame({
            "Concepto": [
                "Acceso a techumbre de fácil acceso",
                "Requiere equipo adicional para acceso",
                "Líneas energizadas en área a instalar",
                "Estado físico de techo/losa/terreno bueno",
                "Pasos de gato existentes",
                "Líneas de vida existentes"
            ],
            "Respuesta": [facil_acceso, equipo_adic, lineas_energ, estado_techo, pasos_gato, lineas_vida],
            "Observaciones": [obs_acceso, obs_equipo, obs_lineas, obs_estado, obs_pasos, obs_vida]
        })

        # 3. Tipo de Techo y Naves
        df_techo = pd.DataFrame({
            "Tipo de Techo": [tipo_techo_sel],
            "Cantidad": [cantidad_techo],
            "Calibre / Espesor": [calibre_espesor]
        })

        df_naves = pd.DataFrame(naves_data).T.reset_index().rename(columns={"index": "Nave"})

        # 4. Requisitos Adicionales
        df_adicionales = pd.DataFrame({
            "Elemento": ["Escalera marina", "Toma de agua cercana", "Sistema de pararrayos"],
            "Aplica": [esc_marina, toma_agua, pararrayos],
            "Observaciones": [obs_esc, obs_agua, obs_pararrayos]
        })

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_drone.to_excel(writer, sheet_name='Drone', index=False)
            df_seguridad.to_excel(writer, sheet_name='Acceso y Seguridad', index=False)
            df_techo.to_excel(writer, sheet_name='Tipo Techo', index=False)
            df_naves.to_excel(writer, sheet_name='Dimensiones Naves', index=False)
            df_adicionales.to_excel(writer, sheet_name='Requisitos Adicionales', index=False)

        output.seek(0)
        return output

    excel_file = generar_excel_etapa2()

    st.download_button(
        label="📥 Descargar Reporte Etapa 2 en Excel (.xlsx)",
        data=excel_file,
        file_name="Levantamiento_Etapa2_Completado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )
