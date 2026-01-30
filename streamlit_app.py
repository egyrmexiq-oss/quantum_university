#Quantum University 
import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

from fpdf import FPDF
import os
from datetime import datetime

def generar_pdf_sesion(nombre_archivo="sesion_quantum_university.pdf"):
    mensajes = st.session_state.get("mensajes", [])

    # Crear PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cargar fuente Unicode
    pdf.add_font("DejaVu", "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=14)

    # ================================
    # 📄 PORTADA
    # ================================
    pdf.add_page()

    # Título principal
    pdf.set_font("DejaVu", size=26)
    pdf.cell(0, 15, "Quantum University", ln=True, align="C")

    # Subtítulo
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, "Sesión educativa personalizada", ln=True, align="C")
    pdf.ln(10)

    # Logo (texto por ahora)
    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 10, "Logo Quantum", ln=True, align="C")
    pdf.ln(10)

    # Datos del usuario
    usuario = st.session_state.get("usuario_activo", "Desconocido")
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    pdf.set_font("DejaVu", size=12)
    pdf.cell(0, 8, f"👤 Usuario: {usuario}", ln=True)
    pdf.cell(0, 8, f"📘 Materia: {materia}", ln=True)
    pdf.cell(0, 8, f"🎓 Nivel educativo: {nivel_educativo}", ln=True)
    pdf.cell(0, 8, f"🧭 Modo de ayuda: {modo}", ln=True)
    pdf.cell(0, 8, f"📅 Fecha: {fecha}", ln=True)

    pdf.ln(15)
    pdf.set_font("DejaVu", size=12)
    pdf.multi_cell(0, 8, "A continuación se muestra el registro completo de la sesión con el tutor Quantum.")
    pdf.ln(10)

    # ================================
    # 💬 CONTENIDO DEL CHAT
    # ================================
    pdf.add_page()
    pdf.set_font("DejaVu", size=12)

    pdf.cell(0, 10, "📄 Registro de la sesión", ln=True)
    pdf.ln(5)

    for msg in mensajes:
        rol = "Usuario" if msg["role"] == "user" else "Asistente"
        contenido = msg["content"].strip()

        # Limpiar caracteres no soportados
        contenido_limpio = contenido.encode("latin-1", "ignore").decode("latin-1")

        pdf.set_font("DejaVu", size=12)
        pdf.multi_cell(0, 8, f"{rol}: {contenido_limpio}")
        pdf.ln(2)

    # Guardar PDF
    ruta = nombre_archivo
    pdf.output(ruta)

    return ruta




# ==========================================
# ⚙️ CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Quantum University", page_icon="🎓", layout="wide")

if "usuario_activo" not in st.session_state:
    st.session_state.usuario_activo = None

# ==========================================
# 🔐 1. LOGIN / LANDING QUANTUM UNIVERSITY
# ==========================================
if not st.session_state.usuario_activo:
    st.markdown("## 🔐 Quantum – University")

    # Animación 3D (puedes cambiar la URL por otra de Spline)
    try:
        components.iframe(
            "https://my.spline.design/claritystream-Vcf5uaN9MQgIR4VGFA5iU6Es/",
            height=400
        )
    except:
        pass

    # Música de fondo suave
    st.audio(
        "https://cdn.pixabay.com/audio/2022/05/27/audio_1808fbf07a.mp3",
        loop=True,
        autoplay=True
    )

    st.markdown(
        """
        <div style="text-align:center; margin-top: 10px;">
            <h1 style="color:#00C2FF; margin-bottom:0;">Quantum University</h1>
            <p style="color:#cccccc; font-size: 0.95rem;">
                Tu tutor inteligente para comprender desde primaria hasta posgrado.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )



    
    st.info("🔑 Para ingresar, usa la clave: **DEMO**")

    clave = st.text_input("Clave de Acceso:", type="password")
    if st.button("Entrar"):
        if clave.strip() == "DEMO" or (
            "access_keys" in st.secrets
            and clave.strip() in st.secrets["access_keys"]
        ):
            nombre = (
                "Visitante"
                if clave.strip() == "DEMO"
                else st.secrets["access_keys"][clave.strip()]
            )
            st.session_state.usuario_activo = nombre
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [
            {
                "role": "assistant",
                "content": (
                    "Hola, soy tu tutor Quantum. "
                    "Cuéntame qué tema, tarea o concepto quieres comprender mejor."
                )
            }
        ]
            
            st.rerun()
        else:
            st.error("Acceso Denegado")
    st.stop()

    
#st.download_button(
    #label="📥 Descargar sesión en PDF",
    #data=open("/mnt/data/sesion_quantum_university.pdf", "rb").read(),
    #file_name="sesion_quantum_university.pdf",
    #mime="application/pdf"
#)

# ==========================================
# 🤖 2. CONEXIÓN IA (DEEPSEEK)
# ==========================================
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", None)
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

def deepseek_request(messages, model="deepseek-chat", temperature=0.7):
    if not DEEPSEEK_API_KEY:
        raise Exception("Falta DEEPSEEK_API_KEY en secrets.")

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    resp = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"DeepSeek Error: {resp.text}")
    data = resp.json()
    return data["choices"][0]["message"]["content"]


# ==========================================
# 📚 3. DATOS EDUCATIVOS (EJEMPLO SIMPLE)
# ==========================================
# Aquí podrías conectar un Google Sheet con profesores, materias, etc.
PROFESORES_EJEMPLO = [
    {
        "nombre": "Prof. Ana Torres",
        "materia": "Física",
        "nivel": "Preparatoria",
        "ciudad": "CDMX"
    },
    {
        "nombre": "Dr. Luis Ríos",
        "materia": "Historia",
        "nivel": "Universidad",
        "ciudad": "Monterrey"
    },
    {
        "nombre": "Mtra. Sofía Pérez",
        "materia": "Matemáticas",
        "nivel": "Secundaria",
        "ciudad": "Guadalajara"
    },
]

# ==========================================
# 🧭 4. SIDEBAR – CONTROLES QUANTUM UNIVERSITY
# ==========================================
with st.sidebar:
    try:
        st.image("logo_quantum.png", use_container_width=True)
    except:
        st.header("QUANTUM UNIVERSITY")

    st.success(f"Hola, {st.session_state.usuario_activo}")

    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: #262730; padding: 10px; border-radius: 5px; text-align: center;">
            <span style="color: white; font-weight: bold;">📊 Sesiones:</span>
            <img src="https://api.visitorbadge.io/api/visitors?path=quantum-university.com&label=&countColor=%2300C2FF&style=flat&labelStyle=none" style="height: 20px;" />
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### ⚙️ Ajustes de Tutoría")

    nivel_educativo = st.selectbox(
        "Nivel Educativo:",
        ["Primaria", "Secundaria", "Preparatoria", "Universidad", "Posgrado"]
    )

    materia = st.selectbox(
        "Materia:",
        [
            "Matemáticas",
            "Física",
            "Química",
            "Biología",
            "Historia",
            "Lengua y Literatura",
            "Programación",
            "Economía",
            "Otra"
        ]
    )

    modo = st.radio(
        "Modo de Ayuda:",
        [
            "Explicación guiada",
            "Resolver tarea (con explicación)",
            "Generar ejercicios",
            "Simulación de examen",
            "Ruta de estudio"
        ]
    )

    profundidad = st.radio(
        "Nivel de profundidad:",
        ["Básica", "Media", "Experta"],
        index=1
    )

    st.markdown("---")
    if st.button("🗑️ Limpiar Chat"):
        st.session_state.mensajes = []
        st.rerun()

    if st.button("🔒 Salir"):
        st.session_state.usuario_activo = None
        st.rerun()

    st.markdown("---")
    st.markdown("### 👨‍🏫 Profesores Quantum")

    if "prof_idx" not in st.session_state:
        st.session_state.prof_idx = 0

    prof = PROFESORES_EJEMPLO[st.session_state.prof_idx % len(PROFESORES_EJEMPLO)]

    tarjeta = f"""
    <div style="background-color: #262730; padding: 15px; border-radius: 10px; border: 1px solid #444; margin-bottom: 10px;">
        <h4 style="margin:0; color:white;">{prof.get("nombre","Profesor Quantum")}</h4>
        <div style="color:#00C2FF; font-weight:bold;">{prof.get("materia","Materia")}</div>
        <small style="color:#bbb;">Nivel: {prof.get("nivel","General")} • {prof.get("ciudad","")}</small>
    </div>
    """
    st.markdown(tarjeta, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("⬅️"):
        st.session_state.prof_idx -= 1
        st.rerun()
    if c2.button("➡️"):
        st.session_state.prof_idx += 1
        st.rerun()
    # ==========================================
    # 📷 OCR – ESCANEO DE DOCUMENTOS
    # ==========================================
    st.markdown("---")
    st.markdown("### 📄 Escanear Documento (OCR)")

    archivo_ocr = st.file_uploader(
        "Sube una imagen con texto (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
        key="ocr_uploader"
    )

    if archivo_ocr:
        try:
            from PIL import Image
            import pytesseract

            img_ocr = Image.open(archivo_ocr)

            st.image(img_ocr, caption="Imagen cargada", use_container_width=True)

            st.markdown("🔍 **Extrayendo texto...**")

            texto_extraido = pytesseract.image_to_string(img_ocr, lang="spa")

            st.text_area("📌 Texto Detectado:", texto_extraido, height=150)

            if st.button("📚 Enviar al Tutor Quantum", key="btn_ocr_enviar"):
                st.session_state.mensajes.append({
                    "role": "user",
                    "content": f"Texto escaneado:\n\n{texto_extraido}"
                })
                st.rerun()

        except Exception as e:
            st.error(f"Error procesando la imagen: {e}")

# ==========================================
# 💬 5. PANTALLA PRINCIPAL – TUTOR ACADÉMICO
# ==========================================
st.markdown(
    '<h1 style="text-align: center; color: #00C2FF;">Quantum University</h1>',
    unsafe_allow_html=True
)
st.caption(
    f"Tutor IA para {nivel_educativo} • Materia: {materia} • Modo: {modo} • Profundidad: {profundidad}"
)

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant",
            "content": (
                "Hola, soy tu tutor Quantum. "
                "Cuéntame qué tema, tarea o concepto quieres comprender mejor."
            )
        }
    ]

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================================
# 🧠 6. LÓGICA DEL CHAT EDUCATIVO
# ==========================================
if prompt := st.chat_input("Escribe tu duda, tarea o tema que no entiendes..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    # Construimos el contexto educativo
    contexto_sistema = f"""
Eres 'Quantum University', un tutor académico experto.

OBJETIVO:
- Ayudar al estudiante a COMPRENDER, no solo a obtener la respuesta.
- Adaptar el lenguaje al nivel educativo: {nivel_educativo}.
- Enfocarte en la materia: {materia}.
- Modo de ayuda: {modo}.
- Nivel de profundidad: {profundidad}.

REGLAS:
- Explica paso a paso.
- Usa ejemplos claros y cercanos al nivel del estudiante.
- Si resuelves una tarea, explica el razonamiento detrás.
- Si el usuario lo permite, sugiere ejercicios adicionales para practicar.
- Evita respuestas excesivamente técnicas si el nivel es básico.
"""

    user_prompt = f"""
Estudiante:
{prompt}
"""

    try:
        respuesta = deepseek_request(
            messages=[
                {"role": "system", "content": contexto_sistema},
                {"role": "user", "content": user_prompt}
            ],
            model="deepseek-chat"  # puedes cambiar a deepseek-reasoner si quieres más profundidad
        )

        st.session_state.mensajes.append(
            {"role": "assistant", "content": respuesta}
        )
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")

# ==========================================
# 📄 DESCARGA DE SESIÓN EN PDF
# ==========================================
try:
    ruta_pdf = generar_pdf_sesion()
    with open(ruta_pdf, "rb") as f:
        st.download_button(
            label="📥 Descargar sesión en PDF",
            data=f.read(),
            file_name="sesion_quantum_university.pdf",
            mime="application/pdf"
        )
except Exception as e:
    st.error(f"No se pudo generar el PDF: {e}")


