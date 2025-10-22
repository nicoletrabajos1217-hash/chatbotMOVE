import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Cargar clave desde archivo .env ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Crear modelo Gemini 2.5 Flash ---
model = genai.GenerativeModel("models/gemini-2.5-flash")

# --- Información oficial de MOVE ---
TELEFONO_URGENCIAS = "322 8157581"
FISIOTERAPEUTA = "Santiago Ortiz"

SERVICIOS_FISIOTERAPIA = (
    "💆‍♂️ *FISIOTERAPIA:*\n"
    "- Descarga Muscular: $75.000\n"
    "- Sesión en Consultorio: $75.000\n"
    "- Valoración en Consultorio: $45.000\n"
    "- Sesión a Domicilio: $80.000\n"
    "- Valoración a Domicilio: $50.000\n"
    "💎 *COMBOS (Ahorra hasta 20%):*\n"
    "  - 5 sesiones: $375.000\n"
    "  - 7 sesiones: $525.000\n"
    "  - 10 sesiones: $750.000\n\n"
    "💙 Cada sesión con nuestro fisioterapeuta *Santiago Ortiz* está pensada para ayudarte a sentirte mejor, recuperar tu movilidad y bienestar paso a paso."
)

SERVICIOS_ENTRENAMIENTO = (
    "💪 *ENTRENAMIENTO PERSONALIZADO:*\n"
    "🏋️ *PRESENCIAL:*\n"
    "- 3 días/semana: $350.000\n"
    "- 4 días/semana: $400.000\n"
    "👫 *PLAN PAREJA:*\n"
    "- 3 días/semana: $450.000\n"
    "- 4 días/semana: $520.000\n"
    "💻 *VIRTUAL:*\n"
    "- 3 días/semana: $240.000\n"
    "- 4 días/semana: $300.000\n"
    "👫 *PLAN PAREJA VIRTUAL:*\n"
    "- 3 días/semana: $350.000\n"
    "- 4 días/semana: $400.000\n\n"
    "✨ Entrenar con MOVE es invertir en ti. Diseñamos cada plan para que disfrutes tu proceso y celebres cada avance."
)

HORARIOS_MOVE = (
    "🕒 *HORARIOS:*\n"
    "- Lunes a Viernes: 7:00am a 7:00pm\n"
    "- Sábados: 7:00am a 4:00pm\n"
    "- Domingos: Cerrado\n\n"
    "💙 Siempre hay un momento para cuidarte. Elige el horario que mejor se adapte a ti."
)

UBICACION_MOVE = (
    "📍 *Ubicación:* Calle 17, Barrio Balmoral\n"
    "Te esperamos en un espacio diseñado para tu bienestar y recuperación. 🌿"
)

# --- Función principal para responder mensajes ---
def responder_mensaje(mensaje, estado):
    try:
        # Inicializar historial y variables de estado si no existen
        if "historial" not in estado:
            estado["historial"] = []
        if "nombre_usuario" not in estado:
            estado["nombre_usuario"] = None
        if "nombre_preguntado" not in estado:
            estado["nombre_preguntado"] = False
        if "cita_paso" not in estado:
            estado["cita_paso"] = 0
        if "cita_info" not in estado:
            estado["cita_info"] = {}

        # --- Preguntar nombre al inicio ---
        if not estado["nombre_usuario"]:
            if not estado["nombre_preguntado"]:
                estado["nombre_preguntado"] = True
                respuesta = (
                    "¡Hola! 😊 Qué alegría tenerte aquí. Soy *MoveAssist*, tu acompañante virtual en MOVE. "
                    "Antes de comenzar, ¿me compartes tu nombre por favor?"
                )
                estado["historial"].append({"usuario": mensaje, "bot": respuesta})
                return respuesta
            else:
                estado["nombre_usuario"] = mensaje.strip()
                saludo = (
                    f"✨ ¡Qué gusto conocerte, {estado['nombre_usuario']}! 💙\n"
                    "Soy *MoveAssist*, tu asistente virtual en MOVE.\n"
                    "Estoy aquí para acompañarte en tu proceso de bienestar físico y mental. 🙌\n"
                    "Puedo ayudarte a conocer precios, horarios, ubicación o agendar tu cita.\n"
                    "¿Qué te gustaría saber hoy?"
                )
                estado["historial"].append({"usuario": mensaje, "bot": saludo})
                return saludo

        # --- Agendamiento de citas paso a paso ---
        if estado["cita_paso"] > 0:
            paso = estado["cita_paso"]
            if paso == 1:
                estado["cita_info"]["fecha"] = mensaje.strip()
                estado["cita_paso"] = 2
                respuesta = "Perfecto 🗓️ ¿Qué hora te gustaría para tu cita? (Ejemplo: 10:00am)"
            elif paso == 2:
                estado["cita_info"]["hora"] = mensaje.strip()
                estado["cita_paso"] = 3
                respuesta = "Genial 💙 ¿A nombre de quién registramos la cita?"
            elif paso == 3:
                estado["cita_info"]["nombre_cita"] = mensaje.strip()
                estado["cita_paso"] = 0  # Reset
                cita = estado["cita_info"]
                respuesta = (
                    f"✅ ¡Tu cita ha sido registrada exitosamente!\n"
                    f"- Fecha: {cita['fecha']}\n"
                    f"- Hora: {cita['hora']}\n"
                    f"- Nombre: {cita['nombre_cita']}\n\n"
                    f"Nuestro fisioterapeuta *{FISIOTERAPEUTA}* confirmará la cita o te contactará si hay algún cambio. 🌟\n"
                    "¡Gracias por confiar en MOVE, cada paso cuenta para tu bienestar! 💪💙"
                )
                estado["cita_info"] = {}
            estado["historial"].append({"usuario": mensaje, "bot": respuesta})
            return respuesta

        # --- Detectar intención básica usando palabras clave ---
        msg_lower = mensaje.lower()

        if "cita" in msg_lower or "agendar" in msg_lower or "reservar" in msg_lower:
            estado["cita_paso"] = 1
            respuesta_texto = "¡Excelente decisión! 💙 Vamos a agendar tu cita. ¿Qué fecha te gustaría?"
        elif "precio" in msg_lower or "costo" in msg_lower or "tarifa" in msg_lower:
            if "fisioterapia" in msg_lower:
                respuesta_texto = SERVICIOS_FISIOTERAPIA
            elif "entrenamiento" in msg_lower:
                respuesta_texto = SERVICIOS_ENTRENAMIENTO
            else:
                respuesta_texto = (
                    "¿Quieres conocer los precios de *fisioterapia* o de *entrenamiento*? "
                    "Dímelo y te comparto los detalles. 💬"
                )
        elif "a domicilio" in msg_lower:
            respuesta_texto = (
                "🏠 Claro que sí. Contamos con *servicios de fisioterapia a domicilio*, ideales si prefieres atención en casa. 💙\n\n"
                f"{SERVICIOS_FISIOTERAPIA}"
            )
        elif "fisioterapia" in msg_lower or "terapia" in msg_lower:
            respuesta_texto = SERVICIOS_FISIOTERAPIA
        elif "entrenamiento" in msg_lower:
            respuesta_texto = SERVICIOS_ENTRENAMIENTO
        elif "horario" in msg_lower:
            respuesta_texto = HORARIOS_MOVE
        elif "ubicación" in msg_lower or "dónde" in msg_lower:
            respuesta_texto = UBICACION_MOVE
        elif "urgencia" in msg_lower or "doctor" in msg_lower:
            respuesta_texto = (
                f"📞 En caso de urgencias, comunícate al {TELEFONO_URGENCIAS}. "
                "Siempre habrá alguien dispuesto a ayudarte. 💙"
            )
        elif (
            "fisioterapeuta" in msg_lower
            or "fisio" in msg_lower
            or "quién atiende" in msg_lower
            or "quien atiende" in msg_lower
            or "quien hace las terapias" in msg_lower
            or "quién hace las terapias" in msg_lower
        ):
            respuesta_texto = (
                f"👨‍⚕️ El fisioterapeuta de MOVE es *{FISIOTERAPEUTA}*, un profesional apasionado por el bienestar y la recuperación de cada persona. 🌟\n"
                "Puedes agendar tus sesiones directamente con él, tanto en consultorio como a domicilio. 💙"
            )
        else:
            # Gemini solo usa información real de MOVE
            prompt = (
                "Eres MoveAssist, asistente virtual de MOVE (Fisioterapia y Entrenamiento).\n"
                "Usa un lenguaje empático, emocional y profesional. Aplica principios de neuromarketing: transmite confianza, bienestar y motivación.\n"
                "Responde únicamente con información real de MOVE (precios, horarios, ubicación, fisioterapeuta, servicios).\n"
                "Si no sabes algo, indica con amabilidad que no tienes ese dato.\n"
                "Si preguntan por fisioterapia a domicilio, confirma que sí está disponible.\n"
                "Si preguntan por el fisioterapeuta, di que es Santiago Ortiz y sugiere agendar con él.\n\n"
                f"Historial: {estado['historial']}\n"
                f"Usuario: {mensaje}"
            )
            respuesta = model.generate_content(prompt)
            respuesta_texto = respuesta.text.strip()

        # Guardar historial
        estado["historial"].append({"usuario": mensaje, "bot": respuesta_texto})
        return respuesta_texto

    except Exception as e:
        return f"⚠️ Ocurrió un error: {e}"
