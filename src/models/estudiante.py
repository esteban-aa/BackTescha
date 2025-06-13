from src.database.db import db

estudiantes = db["estudiantes"]

# Ejemplo de inserción:
def crear_estudiante(correo, usuario, contraseña, matricula):
    nuevo_estudiante = {
        "correo": correo,
        "usuario": usuario,
        "contraseña": contraseña,
        "matricula": matricula
    }
    return estudiantes.insert_one(nuevo_estudiante)
