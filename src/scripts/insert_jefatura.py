import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.database.db import db
jefatura_carrera = db["jefatura_carrera"]

jefaturas_data = [
    {
        "encargado": "Dra. Fabiola",
        "horario": [
            "Lunes a Viernes 09:00 AM - 15:00 PM y 16:00 PM - 18:00 PM"
        ],
        "carreras": [
            "Ingeniería en Sistemas Computacionales"
        ],
        "descripcion": "Oficina que atiende temas académicos de las carreras de sistemas",
        "coordenadas": [19.2328927, -98.8412992]
    },
    {
        "encargado": "Ing Marino",
        "horario": [
            "Lunes a Viernes 09:00 AM - 15:00 PM y 16:00 PM - 18:00 PM"
        ],
        "carreras": [
            "Ingeniería Electrónica"
        ],
        "descripcion": "Oficina que supervisa programas de Electrónica",
       "coordenadas": [19.2328927, -98.8412992]
    },
    {
        "encargado": "Ing Maximo",
        "horario": [
            "Lunes a Viernes 09:00 AM - 15:00 PM y 16:00 PM - 18:00 PM"
        ],
        "carreras": [
            "Ingeniería Industrial"
        ],
        "descripcion": "Oficina que supervisa programas de Industrial",
       "coordenadas": [19.2328927, -98.8412992]
    }
]

# 🚀 Insertar los documentos
if __name__ == "__main__":
    result_jefaturas = jefatura_carrera.insert_many(jefaturas_data)
    print(f"✅ Jefaturas insertadas con IDs: {result_jefaturas.inserted_ids}")
