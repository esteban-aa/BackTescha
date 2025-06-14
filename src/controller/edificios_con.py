from flask import request, jsonify
from src.models.edificios import (
    obtener_edificios,
    obtener_edificio_por_id
)

def obtener_edificios_controller():
    edificios = obtener_edificios()
    for edificio in edificios:
        edificio["_id"] = str(edificio["_id"])
    return jsonify(edificios), 200

def obtener_edificio_controller(edificio_id):  # ✅ nombre corregido
    edificio = obtener_edificio_por_id(edificio_id)
    if not edificio:
        return jsonify({"error": "Edificio no encontrado"}), 404
    edificio["_id"] = str(edificio["_id"])
    return jsonify(edificio), 200