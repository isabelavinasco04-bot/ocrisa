import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import os
from io import BytesIO

st.set_page_config(page_title="OCR con Voz", page_icon="🧠", layout="centered")
st.title("🎙️ Reconocimiento Óptico de Caracteres con Voz")

# Captura de imagen
img_file_buffer = st.camera_input("📸 Toma una foto")

# Sidebar con filtro
with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

# Procesamiento de imagen
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)

    # OCR con pytesseract
    text = pytesseract.image_to_string(img_rgb)
    st.subheader("📝 Texto Detectado:")
    st.write(text if text.strip() else "No se detectó texto claramente.")

    if text.strip():
        # Generar audio con gTTS
        tts = gTTS(text=text, lang='es')
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        st.subheader("🔊 Escucha el texto reconocido:")
        st.audio(audio_buffer, format='audio/mp3')

        # Botón para descargar el audio
        st.download_button(
            label="⬇️ Descargar Audio",
            data=audio_buffer,
            file_name="texto_detectado.mp3",
            mime="audio/mp3"
        )
