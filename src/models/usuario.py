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