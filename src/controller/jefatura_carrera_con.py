# --- Imports estándar ---
from flask import request, jsonify

# --- Imports internos ---
from src.models.jefatura_carrera import (
    obtener_jefaturas,
    obtener_jefatura_por_id
)


def obtener_jefaturas_controller():
    docs = obtener_jefaturas()
    for d in docs:
        d["_id"] = str(d["_id"])
    return jsonify(docs), 200


def obtener_jefatura_controller(id):
    doc = obtener_jefatura_por_id(id)
    if not doc:
        return jsonify({"error": "Jefatura no encontrada"}), 404
    doc["_id"] = str(doc["_id"])
    return jsonify(doc), 200
