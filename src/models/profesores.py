from src.database.db import db

profesores = db["profesores"]

# Ejemplo de inserción:
def crear_profesores(nombre, horarios, edificio, salon):
    nuevo_horario = {
        "nombre": nombre,
        "horarios": {  # puede tener formato: {"lunes": "8-10", "martes": "10-12"}
            "lunes": horarios.get("lunes", ""),
            "martes": horarios.get("martes", ""),
            "miércoles": horarios.get("miércoles", ""),
            "jueves": horarios.get("jueves", ""),
            "viernes": horarios.get("viernes", "")
        },
        "edificio": edificio
    }
    return profesores.insert_one(nuevo_horario)