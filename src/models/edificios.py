from src.database.db import db

edificios = db["edificios"]

# Ejemplo de inserción:
def crear_edificio(nombre, coordenadas, salones, descripcion):
    nuevo_edificio = {
        "nombre": nombre,
        "coordenadas": {  # ejemplo: {"lat": 19.295, "lng": -99.176}
            "lat": coordenadas["lat"],
            "lng": coordenadas["lng"]
        },
        "descripcion": descripcion
    }
    return edificios.insert_one(nuevo_edificio)
