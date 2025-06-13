from src.database.db import db

ventanilla = db["ventanilla"]

# Ejemplo de inserción:
def crear_ventanilla(ubicacion, horarios, tramites):
    nuevo_horario = {
        "ubicacion": ubicacion,
        "horarios": horarios,  # ejemplo: {"lunes": "9-13", "viernes": "10-12"}
    }
    return ventanilla.insert_one(nuevo_horario)
