from src.database.db import db
from bson import ObjectId

profesores = db["profesores"]

def crear_profesores(nombre, horarios, edificio, salon):
    return profesores.insert_one({
        "nombre": nombre,
        "horarios": {
            "lunes": horarios.get("lunes", ""),
            "martes": horarios.get("martes", ""),
            "miércoles": horarios.get("miércoles", ""),
            "jueves": horarios.get("jueves", ""),
            "viernes": horarios.get("viernes", "")
        },
        "edificio": edificio,
        "salon": salon
    })

def obtener_profesores():
    return list(profesores.find())

def obtener_profesor_por_id(id):
    return profesores.find_one({"_id": ObjectId(id)})

