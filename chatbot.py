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
    "💆‍♂️ FISIOTERAPIA:\n"
    "- Descarga Muscular: $75.000\n"
    "- Sesión en Consultorio: $75.000\n"
    "- Valoración en Consultorio: $45.000\n"
    "- Sesión a Domicilio: $80.000\n"
    "- Valoración a Domicilio: $50.000\n"
    "💎 COMBOS (Ahorra hasta 20%):\n"
    "  - 5 sesiones: $375.000\n"
    "  - 7 sesiones: $525.000\n"
    "  - 10 sesiones: $750.000"
)

SERVICIOS_ENTRENAMIENTO = (
    "💪 ENTRENAMIENTO PERSONALIZADO:\n"
    "🏋️ PRESENCIAL:\n"
    "- 3 días/semana: $350.000\n"
    "- 4 días/semana: $400.000\n"
    "👫 PLAN PAREJA:\n"
    "- 3 días/semana: $450.000\n"
    "- 4 días/semana: $520.000\n"
    "💻 VIRTUAL:\n"
    "- 3 días/semana: $240.000\n"
    "- 4 días/semana: $300.000\n"
    "👫 PLAN PAREJA VIRTUAL:\n"
    "- 3 días/semana: $350.000\n"
    "- 4 días/semana: $400.000"
)

HORARIOS_MOVE = (
    "🕒 HORARIOS:\n"
    "- Lunes a Viernes: 7:00am a 7:00pm\n"
    "- Sábados: 7:00am a 4:00pm\n"
    "- Domingos: Cerrado"
)

UBICACION_MOVE = "📍 Ubicación: Calle 17, Barrio Balmoral"

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
                respuesta = "¡Hola! 😊 Antes de empezar, ¿me puedes decir tu nombre, por favor?"
                estado["historial"].append({"usuario": mensaje, "bot": respuesta})
                return respuesta
            else:
                estado["nombre_usuario"] = mensaje.strip()
                saludo = (
                    f"¡Encantada de conocerte, {estado['nombre_usuario']}! "
                    "Soy MoveAssist, tu asistente virtual en MOVE.\n"
                    "Puedes preguntarme por precios, horarios, ubicación, agendar citas, o cualquier duda sobre fisioterapia y entrenamiento.\n"
                    "¿En qué puedo ayudarte hoy?"
                )
                estado["historial"].append({"usuario": mensaje, "bot": saludo})
                return saludo

        # --- Agendamiento de citas paso a paso ---
        if estado["cita_paso"] > 0:
            paso = estado["cita_paso"]
            if paso == 1:
                estado["cita_info"]["fecha"] = mensaje.strip()
                estado["cita_paso"] = 2
                respuesta = "Perfecto, ahora dime la hora que deseas para tu cita (ej. 10:00am)."
            elif paso == 2:
                estado["cita_info"]["hora"] = mensaje.strip()
                estado["cita_paso"] = 3
                respuesta = "Genial, ¿con qué nombre registramos la cita?"
            elif paso == 3:
                estado["cita_info"]["nombre_cita"] = mensaje.strip()
                estado["cita_paso"] = 0  # Reset
                cita = estado["cita_info"]
                respuesta = (
                    f"✅ Tu cita ha sido registrada correctamente:\n"
                    f"- Fecha: {cita['fecha']}\n"
                    f"- Hora: {cita['hora']}\n"
                    f"- Nombre: {cita['nombre_cita']}\n\n"
                    f"Nuestro fisioterapeuta {FISIOTERAPEUTA} o su asistente se pondrán en contacto si hay algún cambio.\n"
                    "¡Gracias por confiar en MOVE! 💙"
                )
                estado["cita_info"] = {}
            estado["historial"].append({"usuario": mensaje, "bot": respuesta})
            return respuesta

        # --- Detectar intención básica usando palabras clave ---
        msg_lower = mensaje.lower()

        if "cita" in msg_lower or "agendar" in msg_lower or "reservar" in msg_lower:
            estado["cita_paso"] = 1
            respuesta_texto = "¡Perfecto! Vamos a agendar tu cita. 😊 ¿Qué fecha deseas?"
        elif "precio" in msg_lower or "costo" in msg_lower or "tarifa" in msg_lower:
            if "fisioterapia" in msg_lower:
                respuesta_texto = SERVICIOS_FISIOTERAPIA
            elif "entrenamiento" in msg_lower:
                respuesta_texto = SERVICIOS_ENTRENAMIENTO
            else:
                respuesta_texto = (
                    "¿Deseas conocer los precios de fisioterapia o de entrenamiento?\n"
                    "Escribe 'fisioterapia' o 'entrenamiento' para ver los detalles."
                )
        elif "a domicilio" in msg_lower:
            # Si preguntan por servicios a domicilio, mostrar los de fisioterapia
            respuesta_texto = (
                "Sí, contamos con servicios de fisioterapia a domicilio. 🏠\n\n"
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
            respuesta_texto = f"📞 Para urgencias, comunícate al {TELEFONO_URGENCIAS}."
        elif (
            "fisioterapeuta" in msg_lower
            or "fisio" in msg_lower
            or "quién atiende" in msg_lower
            or "quien atiende" in msg_lower
            or "quien hace las terapias" in msg_lower
            or "quién hace las terapias" in msg_lower
        ):
            respuesta_texto = (
                f"👨‍⚕️ Nuestro fisioterapeuta es {FISIOTERAPEUTA}. "
                "Él se encarga de todas las sesiones de fisioterapia, "
                "y puedes agendar tu cita directamente con él. 💙"
            )
        else:
            # Gemini solo usa información real de MOVE
            prompt = (
                "Eres MoveAssist, asistente virtual de MOVE (Fisioterapia y Entrenamiento).\n"
                "Responde solo con base en la siguiente información oficial:\n\n"
                f"- Servicios de fisioterapia:\n{SERVICIOS_FISIOTERAPIA}\n\n"
                f"- Servicios de entrenamiento:\n{SERVICIOS_ENTRENAMIENTO}\n\n"
                f"- Horarios:\n{HORARIOS_MOVE}\n\n"
                f"- Ubicación:\n{UBICACION_MOVE}\n\n"
                f"- Teléfono de urgencias: {TELEFONO_URGENCIAS}\n"
                f"- Fisioterapeuta: {FISIOTERAPEUTA}\n\n"
                "⚠️ No inventes información. Si no sabes algo, indica que no tienes ese dato.\n"
                "Si preguntan por fisioterapia a domicilio, confirma que sí está disponible.\n"
                "Si preguntan por el fisioterapeuta, responde que es Santiago Ortiz y "
                "sugiere agendar la cita con él.\n\n"
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
