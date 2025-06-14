# --- Imports estándar ---
from flask import request, jsonify

# --- Imports internos ---
from src.models.estudiante import (
    crear_estudiante,
    obtener_estudiantes,
    obtener_estudiante_por_id,
    actualizar_estudiante,
    eliminar_estudiante
)

# --- Controladores ---
def crear_estudiante_controller():
    data = request.json

    required = {"correo", "usuario", "contraseña", "matricula"}
    if not required.issubset(data.keys()):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    resultado = crear_estudiante(
        data["correo"],
        data["usuario"],
        data["contraseña"],
        data["matricula"]
    )
    return jsonify({"mensaje": "Estudiante creado", "id": str(resultado.inserted_id)}), 201


def obtener_estudiantes_controller():
    docs = obtener_estudiantes()
    for e in docs:
        e["_id"] = str(e["_id"])
    return jsonify(docs), 200


def obtener_estudiante_controller(id):
    doc = obtener_estudiante_por_id(id)
    if not doc:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    doc["_id"] = str(doc["_id"])
    return jsonify(doc), 200


def actualizar_estudiante_controller(id):
    data = request.json
    resultado = actualizar_estudiante(id, data)
    if resultado.matched_count == 0:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    return jsonify({"mensaje": "Estudiante actualizado"}), 200


def eliminar_estudiante_controller(id):
    resultado = eliminar_estudiante(id)
    if resultado.deleted_count == 0:
        return jsonify({"error": "Estudiante no encontrado"}), 404
    return jsonify({"mensaje": "Estudiante eliminado"}), 200
