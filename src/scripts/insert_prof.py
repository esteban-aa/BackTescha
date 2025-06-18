import sys
import os

# Agrega la raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.db import db

# Colección
profesores = db["profesores"]

# ---- Datos de ejemplo para profesores ----
profesores_data = [
    {
        "nombre": "Dra Tenorio",
        "horarios": ["Lunes a Viernes de 9:00 AM a 4:00 PM"],
        "edificio": "Revolución",
        "salon": "A1"
    },
    {
        "nombre": "Ladislao",
        "horarios": ["Lunes a Viernes de 7:00 AM a 2:00 PM"],
        "edificio": "Revolución",
        "salon": "A2"
    },
    {
        "nombre": "Tacubeño",
        "horarios": ["Lunes a Viernes de 4:00 PM a 8:00 PM"],
        "edificio": "Sor Juana",
        "salon": "B1"
    },
    {
        "nombre": "Azamar",
        "horarios": ["Lunes a Viernes de 7:00 AM a 8:00 PM"],
        "edificio": "Revolución",
        "salon": "A3"
    },
    {
        "nombre": "Eduardo",
        "horarios": ["Lunes a Viernes de 7:00 AM a 2:00 PM"],
        "edificio": "Morelos",
        "salon": "M1"
    },
    {
        "nombre": "Miguel",
        "horarios": ["Lunes a Viernes de 7:00 AM a 3:00 PM"],
        "edificio": "Nezahualcoyotl",
        "salon": "N1"
    }
]

if __name__ == "__main__":
    result_profesores = profesores.insert_many(profesores_data)
    print(f"✅ Profesores insertados con IDs: {result_profesores.inserted_ids}")
