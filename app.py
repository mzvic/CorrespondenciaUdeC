import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuración básica de la página
st.set_page_config(
    page_title="Correspondencia UdeC",
    page_icon="📜",
    layout="wide"
)

# 2. Archivos y Carpetas
ARCHIVO_DATOS = "historial_correspondencia.csv"
CARPETA_ARCHIVOS = "archivos_adjuntos"

if not os.path.exists(CARPETA_ARCHIVOS):
    os.makedirs(CARPETA_ARCHIVOS)

# 3. Inicializar el estado de la sesión y asegurar compatibilidad de columnas
if "historial_correspondencia" not in st.session_state:
    if os.path.exists(ARCHIVO_DATOS):
        df_guardado = pd.read_csv(ARCHIVO_DATOS)
        # Compatibilidad si el CSV antiguo no tiene la columna Respuesta
        if "Respuesta" not in df_guardado.columns:
            df_guardado["Respuesta"] = ""
        st.session_state.historial_correspondencia = df_guardado.to_dict('records')
    else:
        st.session_state.historial_correspondencia = []

# 4. Inyección de CSS (Colores UdeC)
udec_css = """
<style>
    .stApp { background-color: #f4f6f9; }
    h1, h2, h3, h4 { color: #00386B !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    div.stButton > button:first-child, div.stFormSubmitButton > button:first-child, div.stDownloadButton > button:first-child {
        background-color: #EAAA00; color: #00386B; border: 2px solid #00386B; border-radius: 8px; font-weight: bold; transition: all 0.3s;
    }
    div.stButton > button:first-child:hover, div.stFormSubmitButton > button:first-child:hover, div.stDownloadButton > button:first-child:hover {
        background-color: #00386B; color: #EAAA00; border: 2px solid #EAAA00;
    }
</style>
"""
st.markdown(udec_css, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("<h1 style='text-align: center;'>Sistema de Gestión de Correspondencia</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Universidad de Concepción</h3>", unsafe_allow_html=True)
st.markdown("---")

# Distribución estricta de dos columnas
col_ingreso, col_tabla = st.columns([1, 2], gap="large")

# ==========================================
# COLUMNA 1: NUEVO REGISTRO
# ==========================================
with col_ingreso:
    st.subheader("📝 Nuevo Registro")
    
    with st.form("form_correspondencia", clear_on_submit=True):
        nombre = st.text_input("Remitente / Destinatario*", placeholder="Ej: Juan Pérez")
        num_correspondencia = st.text_input("N° de Correspondencia*", placeholder="Ej: UDEC-2026-001")
        fecha_documento = st.date_input("Fecha del Documento")
        descripcion = st.text_area("Descripción o Asunto", placeholder="Breve resumen...", height=80)
        
        # NUEVO: Campo opcional de respuesta manual
        respuesta_manual = st.text_area("Respuesta / Observación (Opcional)", placeholder="Detalle de la respuesta o gestión...", height=80)
        
        # NUEVO: Permitir múltiples archivos
        cartas_escaneadas = st.file_uploader(
            "Adjuntar Cartas (Puedes seleccionar varios)", 
            type=["pdf", "png", "jpg", "jpeg"], 
            accept_multiple_files=True
        )
        
        estado_inicial = st.selectbox("Estado Inicial", options=["Ingresada", "En Revisión", "Respondida", "Archivada"])
        
        submit_button = st.form_submit_button("Registrar Correspondencia")

    if submit_button:
        if not nombre or not num_correspondencia:
            st.error("⚠️ Los campos con asterisco (*) son obligatorios.")
        else:
            nombres_archivos = []
            if cartas_escaneadas:
                for archivo in cartas_escaneadas:
                    nombre_limpio = archivo.name.replace(" ", "_")
                    nombre_archivo_final = f"{num_correspondencia}_{nombre_limpio}"
                    ruta_guardado = os.path.join(CARPETA_ARCHIVOS, nombre_archivo_final)
                    with open(ruta_guardado, "wb") as f:
                        f.write(archivo.getbuffer())
                    nombres_archivos.append(nombre_archivo_final)
            
            # Guardamos los archivos separados por comas o "Sin archivo"
            str_archivos = ", ".join(nombres_archivos) if nombres_archivos else "Sin archivo"
            
            nuevo_registro = {
                "Fecha Ingreso": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "Fecha Documento": fecha_documento.strftime("%d-%m-%Y"),
                "N° Correspondencia": num_correspondencia,
                "Nombre": nombre,
                "Asunto": descripcion,
                "Respuesta": respuesta_manual,
                "Estado": estado_inicial,
                "Archivo Guardado": str_archivos
            }
            
            st.session_state.historial_correspondencia.append(nuevo_registro)
            pd.DataFrame(st.session_state.historial_correspondencia).to_csv(ARCHIVO_DATOS, index=False)
            st.success("✅ ¡Registro guardado exitosamente!")
            st.rerun()

# ==========================================
# COLUMNA 2: BASE DE DATOS Y GESTIÓN POR FILA
# ==========================================
with col_tabla:
    st.subheader("📋 Base de Datos de Correspondencia")
    st.caption("💡 *Busca por Nombre, N°, Asunto o Respuesta. Haz clic en una fila para gestionar su estado o descargar sus archivos.*")
    
    if st.session_state.historial_correspondencia:
        df_actual = pd.DataFrame(st.session_state.historial_correspondencia)
        if "Respuesta" not in df_actual.columns:
            df_actual["Respuesta"] = ""
            
        # NUEVO: Búsqueda avanzada ampliada (Nombre, N°, Asunto y Respuesta)
        busqueda = st.text_input("🔍 Buscar correspondencia", placeholder="Escribe nombre, número, asunto o respuesta...")
        if busqueda:
            df_actual.fillna("", inplace=True)
            df_filtrado = df_actual[
                df_actual["Nombre"].str.contains(busqueda, case=False, na=False) | 
                df_actual["N° Correspondencia"].str.contains(busqueda, case=False, na=False) |
                df_actual["Asunto"].str.contains(busqueda, case=False, na=False) |
                df_actual["Respuesta"].str.contains(busqueda, case=False, na=False)
            ]
        else:
            df_filtrado = df_actual

        # Tabla interactiva con selección de filas
        evento_tabla = st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            height=250,
            on_select="rerun",
            selection_mode="single-row",
            key="tabla_principal"
        )
        
        filas_seleccionadas = evento_tabla.selection.rows
        
        if filas_seleccionadas:
            idx_sel = filas_seleccionadas[0]
            if idx_sel < len(df_filtrado):
                reg_sel = df_filtrado.iloc[idx_sel]
                num_corr = reg_sel["N° Correspondencia"]
                
                # Encontrar índice global exacto
                idx_global = next(i for i, r in enumerate(st.session_state.historial_correspondencia) if r["N° Correspondencia"] == num_corr)
                
                st.markdown("<hr style='margin: 8px 0;'>", unsafe_allow_html=True)
                st.markdown(f"⚙️ **Gestionando Documento:** `{num_corr}` — *{reg_sel['Nombre']}*")
                
                col_est, col_desc = st.columns(2, gap="medium")
                
                # 1. Panel de cambio de estado y actualización de respuesta manual
                with col_est:
                    lista_estados = ["Ingresada", "En Revisión", "Respondida", "Archivada"]
                    est_actual = st.session_state.historial_correspondencia[idx_global]["Estado"]
                    idx_est = lista_estados.index(est_actual) if est_actual in lista_estados else 0
                    
                    nuevo_est = st.selectbox("Cambiar Estado:", options=lista_estados, index=idx_est, key=f"sel_est_{num_corr}")
                    
                    resp_actual = st.session_state.historial_correspondencia[idx_global]["Respuesta"]
                    nueva_resp = st.text_area("Actualizar Respuesta:", value=str(resp_actual), height=60, key=f"txt_resp_{num_corr}")
                    
                    if st.button("Guardar Cambios de Gestión", key=f"btn_guardar_{num_corr}"):
                        st.session_state.historial_correspondencia[idx_global]["Estado"] = nuevo_est
                        st.session_state.historial_correspondencia[idx_global]["Respuesta"] = nueva_resp
                        pd.DataFrame(st.session_state.historial_correspondencia).to_csv(ARCHIVO_DATOS, index=False)
                        st.success("✅ Cambios guardados con éxito.")
                        st.rerun()
                        
                # 2. Panel de descarga de múltiples archivos adjuntos
                with col_desc:
                    str_archs = reg_sel["Archivo Guardado"]
                    st.write("📁 **Archivos Adjuntos:**")
                    
                    if str_archs != "Sin archivo" and str_archs.strip() != "":
                        lista_archivos = [a.strip() for a in str_archs.split(",")]
                        for a_idx, arch in enumerate(lista_archivos):
                            ruta_arch = os.path.join(CARPETA_ARCHIVOS, arch)
                            if os.path.exists(ruta_arch):
                                with open(ruta_arch, "rb") as f:
                                    bytes_arch = f.read()
                                st.download_button(
                                    label=f"📥 Descargar: {arch.split('_', 1)[-1]}",
                                    data=bytes_arch,
                                    file_name=arch,
                                    key=f"dl_{num_corr}_{a_idx}"
                                )
                            else:
                                st.warning(f"⚠️ Archivo no encontrado: {arch}")
                    else:
                        st.info("ℹ️ Este registro no tiene archivos adjuntos.")
        else:
            st.caption("👆 *Haz clic en una fila de la tabla para cambiar estados, editar respuestas o descargar sus archivos.*")
            
    else:
        st.info("ℹ️ No hay correspondencia registrada todavía.")