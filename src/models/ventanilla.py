from src.database.db import db
from bson import ObjectId

ventanilla = db["ventanilla"]

# Obtener todas las ventanillas
def obtener_ventanillas():
    """Devuelve una lista de todas las ventanillas."""
    return list(ventanilla.find({}, {
        "_id": 1,
        "ubicacion": 1,
        "horarios": 1,
        "tramites": 1
    }))

# Obtener una ventanilla por su ID
def obtener_ventanilla_por_id(id):
    """Devuelve una ventanilla por su ID, o None si no existe o el ID es inválido."""
    try:
        return ventanilla.find_one({"_id": ObjectId(id)})
    except:
        return None
