from src.database.db import db
from bson import ObjectId

profesores = db["profesores"]

# Obtener todos los profesores
def obtener_profesores():
    """Devuelve una lista de todos los profesores."""
    return list(profesores.find({}, {
        "nombre": 1,
        "horarios": 1,
        "edificio": 1
    }))

# Obtener un profesor por su ID
def obtener_profesor_por_id(id):
    """Devuelve un profesor por su ID, o None si no existe o el ID es inválido."""
    try:
        return profesores.find_one({"_id": ObjectId(id)})
    except:
        return None
