# src/database/db.py (si lo ubicas en src/database/)
# o simplemente db.py (si lo dejas en la raíz de tu proyecto, pero preferible la estructura src/)

from pymongo import MongoClient
import os
from dotenv import load_dotenv
import sys # Importar sys para sys.exit()

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Validar que las variables de entorno están cargadas
if not MONGO_URI:
    print("--- ERROR FATAL DE CONFIGURACIÓN ---")
    print("La variable de entorno 'MONGO_URI' no está configurada en tu archivo .env.")
    print("Asegúrate de tener un archivo .env en la raíz de tu proyecto con MONGO_URI='tu_cadena_de_conexion'.")
    sys.exit(1) # Salir si la URI no está configurada

if not DB_NAME:
    print("--- ERROR FATAL DE CONFIGURACIÓN ---")
    print("La variable de entorno 'DB_NAME' no está configurada en tu archivo .env.")
    print("Asegúrate de tener un archivo .env en la raíz de tu proyecto con DB_NAME='nombre_de_tu_db'.")
    sys.exit(1) # Salir si el nombre de la DB no está configurado


try:
    # Intentar la conexión a MongoDB Atlas
    client = MongoClient(MONGO_URI)

    # Seleccionar la base de datos
    db = client[DB_NAME]

    # Opcional: Probar la conexión con un comando 'ping'
    # Esto asegura que la conexión está activa y que se puede comunicar con el servidor de MongoDB.
    client.admin.command('ping')

    print(f"¡Conexión a MongoDB Atlas ('{DB_NAME}') establecida con éxito!")

except Exception as e:
    print(f"--- ERROR FATAL AL CONECTAR A MONGO DB ---")
    print(f"No se pudo establecer conexión con MongoDB Atlas usando la URI: {MONGO_URI}")
    print(f"Posibles causas:")
    print(f"  1. La 'MONGO_URI' en tu .env es incorrecta (usuario, contraseña, URL del clúster).")
    print(f"  2. Tu dirección IP actual no está en la lista blanca de acceso a la red de MongoDB Atlas.")
    print(f"  3. Problemas de red o el clúster de MongoDB Atlas no está disponible.")
    print(f"Error detallado: {e}")
    sys.exit(1) # Salir del programa si la conexión a la base de datos falla