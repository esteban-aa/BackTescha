import os
import sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Almacenar la conexión globalmente
_db_connection = None

def get_db_connection():
    """
    Retorna la instancia de la base de datos de MongoDB.
    Establece la conexión si aún no existe.
    """
    global _db_connection
    if _db_connection is None:
        if not MONGO_URI:
            print("--- ERROR FATAL DE CONFIGURACIÓN ---")
            print("La variable 'MONGO_URI' no está configurada en el archivo .env.")
            sys.exit(1)
        if not DB_NAME:
            print("--- ERROR FATAL DE CONFIGURACIÓN ---")
            print("La variable 'DB_NAME' no está configurada en el archivo .env.")
            sys.exit(1)

        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            _db_connection = client[DB_NAME]
            # Test de conexión
            client.admin.command("ping")
            print(f"✅ ¡Conexión a MongoDB Atlas ('{DB_NAME}') establecida con éxito desde chatbot!")
        except Exception as e:
            print("--- ERROR FATAL AL CONECTAR A MONGODB DESDE CHATBOT ---")
            print("Posibles causas:")
            print("   - MONGO_URI incorrecta.")
            print("   - IP no autorizada en MongoDB Atlas.")
            print("   - Clúster no disponible o red bloqueada.")
            print(f"Detalles del error: {e}")
            sys.exit(1)
    return _db_connection

# --- Funciones de Consulta a la Base de Datos ---

def get_edificio_info(nombre_edificio):
    db = get_db_connection()
    # Colección: 'edificios', Campo para buscar: 'nombre'
    return db.edificios.find_one({"nombre": {"$regex": nombre_edificio, "$options": "i"}})

def get_profesor_info(nombre_profesor):
    db = get_db_connection()
    return db.profesores.find_one({"nombre": {"$regex": nombre_profesor, "$options": "i"}})

def get_ventanilla_info(nombre_ventanilla):
    db = get_db_connection()
    return db.ventanilla.find_one({"nombre": {"$regex": nombre_ventanilla, "$options": "i"}})


def get_jefatura_info(nombre_carrera):
    db = get_db_connection()
    return db.jefaturas.find_one({"nombre_carrera": {"$regex": nombre_carrera, "$options": "i"}})

def get_user_by_matricula(matricula):
    db = get_db_connection()
    return db.estudiantes.find_one({"matricula": matricula})

def get_user_by_id_or_identifier(user_identifier):
    db = get_db_connection()
    # Colección: 'usuarios', Campo para buscar: '_id', 'correo', 'usuario', 'identificador'
    try:
        obj_id = ObjectId(user_identifier)
        user = db.usuarios.find_one({"_id": obj_id})
        if user:
            return user
    except Exception:
        pass # No es un ObjectId válido

    user = db.usuarios.find_one({"$or": [
        {"correo": user_identifier},
        {"usuario": user_identifier}
    ]})
    return user

def update_user_info(user_id, new_data):
    db = get_db_connection()
    try:
        result = db.usuarios.update_one({"_id": ObjectId(user_id)}, {"$set": new_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False