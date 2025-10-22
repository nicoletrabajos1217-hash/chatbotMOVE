import streamlit as st
from chatbot import responder_mensaje

# --- Inicializar historial y estado ---
if "historial" not in st.session_state:
    st.session_state.historial = []
if "estado" not in st.session_state:
    st.session_state.estado = {}

# --- CSS estilo MOVE (Azul y Blanco) ---
st.markdown("""
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        max-height: 500px;
        overflow-y: auto;
        padding: 15px;
        border: 2px solid #2196F3;
        border-radius: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
    }
    .mensaje {
        margin: 8px;
        padding: 12px 18px;
        border-radius: 20px;
        max-width: 80%;
        word-wrap: break-word;
        font-family: 'Arial', sans-serif;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        line-height: 1.4;
    }
    .usuario {
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 5px;
    }
    .bot {
        background: linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
        border: 2px solid #2196F3;
        align-self: flex-start;
        border-bottom-left-radius: 5px;
        color: #1565C0;
    }
    .stChatInput {
        border: 2px solid #2196F3 !important;
        border-radius: 25px !important;
    }
    .header-move {
        text-align: center; 
        padding: 15px; 
        background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); 
        border-radius: 15px; 
        color: white; 
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header MOVE ---
st.markdown("""
    <div class='header-move'>
        <h1>🏃‍♂️ MOVE - PLATAFORMA DE BIENESTAR</h1>
        <p style='margin: 0; font-size: 16px;'>💬 Asistente Virtual - MoveAssist</p>
    </div>
""", unsafe_allow_html=True)

# --- Campo de entrada ---
mensaje = st.chat_input("Escribe tu mensaje aquí...")

# --- Procesar mensaje ---
if mensaje:
    respuesta = responder_mensaje(mensaje, st.session_state.estado)
    st.session_state.historial.append(("Tú", mensaje))
    st.session_state.historial.append(("MoveAssist", respuesta))

# --- Mostrar historial ---
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for emisor, texto in st.session_state.historial:
        if emisor == "Tú":
            st.markdown(f"<div class='mensaje usuario'><b>{emisor}:</b> {texto}</div>", unsafe_allow_html=True)
        else:
            texto_formateado = texto.replace('\n', '<br>')
            st.markdown(f"<div class='mensaje bot'><b>{emisor}:</b> {texto_formateado}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <div style='text-align: center; margin-top: 20px; color: #2196F3; font-size: 14px; font-weight: bold;'>
        📞 WhatsApp: +57 322 8157581 | 📧 info@move.com | 🌐 www.move.com
    </div>
""", unsafe_allow_html=True)
