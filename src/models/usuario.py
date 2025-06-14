from src.database.db import db

usuarios = db["usuarios"]

# Ejemplo de inserción:
def crear_usuario(correo, usuario, contraseña):
    nuevo_usuario = {
        "correo": correo,
        "usuario": usuario,
        "contraseña": contraseña
    }
    return usuarios.insert_one(nuevo_usuario)

def obtener_usuarios():
    return list(usuarios.find())

def obtener_usuario_por_id(id):
    return usuarios.find_one({"_id": ObjectId(id)})

def actualizar_usuario(id, datos):
    return usuarios.update_one({"_id": ObjectId(id)}, {"$set": datos})

def eliminar_usuario(id):
    return usuarios.delete_one({"_id": ObjectId(id)})