import sys
import os

# Agrega la raíz del proyecto al path para que funcionen los imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.db import db  # Conexión a MongoDB

# 🔧 Definir la colección manualmente
ventanilla = db["ventanilla"]

# ---- Datos de ejemplo para ventanillas ----
ventanillas_data = [
    {
        "nombre": "Control Escolar",
        "coordenadas": [19.2327762, -98.840661],
        "horarios": ["Lunes a Viernes 09:00 AM - 15:00 PM y de 16:00 PM - 18:00 PM"],
        "tramites": ["Constancias", "Historial Académico", "Reinscripciones", "Bajas temporales", "Credenciales"]
    },
    {
        "nombre": "Departamento de servicio social y residencias profesionales",
        "coordenadas": [19.2331431, -98.8419580],
        "horarios": ["Lunes a Viernes 09:00 AM - 15:00 PM y de 16:00 PM - 18:00 PM"],
        "tramites": ["Trámites relacionados a Servicio Social", "Residencias Profesionales", "Seguimiento de Egresados"]
    }
]

# ---- Insertar en la base de datos ----
if __name__ == "__main__":
    result_ventanillas = ventanilla.insert_many(ventanillas_data)
    print(f"✅ Ventanillas insertadas con IDs: {result_ventanillas.inserted_ids}")
