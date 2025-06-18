from src.database.db import db
from bson import ObjectId
import bcrypt


estudiantes = db["estudiantes"]

def crear_estudiante(correo, usuario, contraseña, matricula):
    hashed = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    return estudiantes.insert_one({
        "correo": correo,
        "usuario": usuario,
        "contraseña": hashed.decode('utf-8'),
        "matricula": matricula
    })

def obtener_estudiantes():
    return list(estudiantes.find())

def obtener_estudiante_por_id(id):
    return estudiantes.find_one({"_id": ObjectId(id)})

def actualizar_estudiante(id, datos):
    return estudiantes.update_one({"_id": ObjectId(id)}, {"$set": datos})

def eliminar_estudiante(id):
    return estudiantes.delete_one({"_id": ObjectId(id)})
