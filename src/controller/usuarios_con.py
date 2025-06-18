# --- Imports estándar ---
from flask import request, jsonify

# --- Imports internos ---
from src.models.usuario import (
    crear_usuario,
    obtener_usuarios,
    obtener_usuario_por_id,
    actualizar_usuario,
    eliminar_usuario
)
from bson import ObjectId

# --- Controladores ---
def crear_usuario_controller():
    data = request.json

    # Validaciones mínimas
    required = {"correo", "usuario", "contraseña"}
    if not required.issubset(data.keys()):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    resultado = crear_usuario(data["correo"], data["usuario"], data["contraseña"])
    return jsonify({"mensaje": "Usuario creado", "id": str(resultado.inserted_id)}), 201


def obtener_usuarios_controller():
    usuarios = obtener_usuarios()
    for u in usuarios:
        u["_id"] = str(u["_id"])
    return jsonify(usuarios), 200


def obtener_usuario_controller(id):
    usuario = obtener_usuario_por_id(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    usuario["_id"] = str(usuario["_id"])
    return jsonify(usuario), 200


def actualizar_usuario_controller(id):
    data = request.json
    resultado = actualizar_usuario(id, data)
    if resultado.matched_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"mensaje": "Usuario actualizado"}), 200


def eliminar_usuario_controller(id):
    resultado = eliminar_usuario(id)
    if resultado.deleted_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"mensaje": "Usuario eliminado"}), 200