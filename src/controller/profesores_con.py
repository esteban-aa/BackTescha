# --- Imports estándar ---
from flask import request, jsonify

# --- Imports internos ---
from src.models.profesores import (
    obtener_profesores,
    obtener_profesor_por_id
)

# --- Controladores ---
def obtener_profesores_controller():
    docs = obtener_profesores()
    for p in docs:
        p["_id"] = str(p["_id"])
    return jsonify(docs), 200


def obtener_profesor_controller(id):
    doc = obtener_profesor_por_id(id)
    if not doc:
        return jsonify({"error": "Profesor no encontrado"}), 404
    doc["_id"] = str(doc["_id"])
    return jsonify(doc), 200


