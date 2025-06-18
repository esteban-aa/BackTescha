from src.database.db import db
from bson.objectid import ObjectId

# Colección
edificios = db["edificios"]

# Obtener todos los edificios
def obtener_edificios():
    """Devuelve una lista de todos los edificios."""
    return list(edificios.find({}, {"_id": 1, "nombre": 1, "coordenadas": 1, "descripcion": 1}))

# Obtener un edificio por su ID
def obtener_edificio_por_id(edificio_id: str):
    """Devuelve un edificio por su ID como dict o None si no existe."""
    try:
        return edificios.find_one({"_id": ObjectId(edificio_id)})
    except:
        return None  # En caso de ID mal formado
