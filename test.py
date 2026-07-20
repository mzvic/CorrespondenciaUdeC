import os

print("--- Generando entorno de prueba para Correspondencia UdeC ---")

# 1. Crear carpeta de archivos adjuntos
CARPETA_ARCHIVOS = "archivos_adjuntos"
if not os.path.exists(CARPETA_ARCHIVOS):
    os.makedirs(CARPETA_ARCHIVOS)
    print(f"📁 Carpeta creada: '{CARPETA_ARCHIVOS}/'")

# 2. Crear el archivo CSV con los datos de prueba
csv_contenido = """Fecha Ingreso,Fecha Documento,N° Correspondencia,Nombre,Asunto,Respuesta,Estado,Archivo Guardado
15-06-2026 10:15,14-06-2026,UDEC-2026-001,Ministerio de Educación,Solicitud de acreditación institucional,Documentación enviada a rectoría para revisión final.,En Revisión,UDEC-2026-001_oficio_mineduc.pdf
18-06-2026 11:45,17-06-2026,UDEC-2026-002,Facultad de Ingeniería,Presupuesto anual laboratorios,Aprobado por el consejo de facultad.,Respondida,UDEC-2026-002_presupuesto.pdf
20-06-2026 09:30,19-06-2026,UDEC-2026-003,María González Soto,Invitación a seminario de innovación tecnológica,Pendiente de confirmación de asistencia.,Ingresada,Sin archivo
25-06-2026 16:20,24-06-2026,UDEC-2026-004,Dirección de Finanzas,Informe de ejecución presupuestaria Q1,Revisado y archivado correctamente.,Archivada,UDEC-2026-004_informe_q1.pdf
"""

with open("historial_correspondencia.csv", "w", encoding="utf-8") as f:
    f.write(csv_contenido)
print("📄 Archivo CSV generado: 'historial_correspondencia.csv'")

# 3. Función para generar PDFs válidos reales usando únicamente Python estándar (sin librerías externas)
def crear_pdf_valido(nombre_archivo, texto_interno):
    ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
    # Estructura binaria de un PDF válido mínimo
    contenido_pdf = b"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /Resources 4 0 R /MediaBox [0 0 612 792] /Contents 5 0 R >>
endobj
4 0 obj
<< /Font << /F1 6 0 R >> >>
endobj
5 0 obj
<< /Length 65 >>
stream
BT
/F1 14 Tf
50 720 Td
(UNIVERSIDAD DE CONCEPCION - DOCUMENTO DEMO) Tj
0 -30 Td
(""" + texto_interno.encode('latin-1', 'ignore') + b""") Tj
ET
endstream
endobj
6 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
xref
0 7
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000216 00000 n 
0000000257 00000 n 
0000000376 00000 n 
trailer
<< /Size 7 /Root 1 0 R >>
startxref
453
%%EOF
"""
    with open(ruta, "wb") as f:
        f.write(contenido_pdf)
    print(f"📥 PDF generado correctamente: {ruta}")

# Generar los 3 archivos PDF de ejemplo
crear_pdf_valido("UDEC-2026-001_oficio_mineduc.pdf", "Oficio Mineduc - Acreditacion Institucional")
crear_pdf_valido("UDEC-2026-002_presupuesto.pdf", "Presupuesto Anual Laboratorios Ingenieria")
crear_pdf_valido("UDEC-2026-004_informe_q1.pdf", "Informe Q1 - Direccion de Finanzas")

print("\n✨ ¡Todo listo! Ya puedes correr tu script de Streamlit habitual.")