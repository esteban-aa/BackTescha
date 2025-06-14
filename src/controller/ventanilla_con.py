# --- Imports estándar ---
from flask import request, jsonify

# --- Imports internos ---
from src.models.ventanilla import (
    obtener_ventanillas,
    obtener_ventanilla_por_id
)

# --- Controladores ---

def obtener_ventanillas_controller():
    docs = obtener_ventanillas()
    for v in docs:
        v["_id"] = str(v["_id"])
    return jsonify(docs), 200


def obtener_ventanilla_controller(id):
    doc = obtener_ventanilla_por_id(id)
    if not doc:
        return jsonify({"error": "Ventanilla no encontrada"}), 404
    doc["_id"] = str(doc["_id"])
    return jsonify(doc), 200

