from pymongo import MongoClient
import os
from dotenv import load_dotenv
import sys

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

print("DEBUG‑MONGO_URI =>", MONGO_URI)

# Validaciones básicas
if not MONGO_URI:
    print("--- ERROR FATAL DE CONFIGURACIÓN ---")
    print("La variable 'MONGO_URI' no está configurada en el archivo .env.")
    sys.exit(1)

if not DB_NAME:
    print("--- ERROR FATAL DE CONFIGURACIÓN ---")
    print("La variable 'DB_NAME' no está configurada en el archivo .env.")
    sys.exit(1)

# Conexión a MongoDB
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]

    # Test de conexión
    client.admin.command("ping")
    print(f"✅ ¡Conexión a MongoDB Atlas ('{DB_NAME}') establecida con éxito!")

except Exception as e:
    print("--- ERROR FATAL AL CONECTAR A MONGODB ---")
    print("Posibles causas:")
    print("  - MONGO_URI incorrecta.")
    print("  - IP no autorizada en MongoDB Atlas.")
    print("  - Clúster no disponible o red bloqueada.")
    print(f"Detalles del error: {e}")
    sys.exit(1)
