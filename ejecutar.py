import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar la clave desde .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Listar los modelos disponibles
try:
    print("📋 Modelos disponibles en tu cuenta:\n")
    modelos = genai.list_models()
    for m in modelos:
        print(m.name)
except Exception as e:
    print(f"⚠️ Error al listar modelos: {e}")
