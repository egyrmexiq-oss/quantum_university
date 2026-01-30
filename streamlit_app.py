# ==========================================
# 📄 DESCARGA DE SESIÓN EN PDF (SEGURO)
# ==========================================
if (
    "usuario_activo" in st.session_state 
    and st.session_state.usuario_activo 
    and "mensajes" in st.session_state 
    and len(st.session_state.mensajes) > 0
):
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
else:
    st.info("Inicia sesión y genera al menos un mensaje para habilitar la descarga en PDF.")
