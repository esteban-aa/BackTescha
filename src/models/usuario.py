from src.database.db import db
from bson.objectid import ObjectId
import bcrypt

usuarios = db["usuarios"]

def crear_usuario(correo, usuario, contraseña):
    hashed_pw = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
    nuevo_usuario = {
        "correo": correo,
        "usuario": usuario,
        "contraseña": hashed_pw.decode('utf-8')  # Convertimos el hash a str
    }
    return usuarios.insert_one(nuevo_usuario)

def obtener_usuarios():
    return list(usuarios.find())  # ✅ Esta función estaba faltando

def obtener_usuario_por_id(id):
    return usuarios.find_one({"_id": ObjectId(id)})

def actualizar_usuario(id, datos):
    return usuarios.update_one({"_id": ObjectId(id)}, {"$set": datos})

def eliminar_usuario(id):
    return usuarios.delete_one({"_id": ObjectId(id)})
