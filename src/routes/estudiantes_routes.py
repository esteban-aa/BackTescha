# --- Imports estándar ---
from flask import Blueprint, request

# --- Imports internos ---

from src.auth.verify_token import token_required
from src.controller.estudiantes_con import (
    crear_estudiante_controller,
    obtener_estudiantes_controller,
    obtener_estudiante_controller,
    actualizar_estudiante_controller,
    eliminar_estudiante_controller
)

# --- Blueprint ---
router = Blueprint("estudiantes", __name__)

# --- Endpoints ---

# Solo usuarios con rol 'admin' pueden crear estudiantes
@router.route("/", methods=["POST"])
def crear_estudiante_route():
    return crear_estudiante_controller()

# Usuarios con rol 'admin' o 'estudiante' pueden ver todos los estudiantes
@router.route("/", methods=["GET"])
@token_required(allowed_roles=["admin", "estudiante"])
def obtener_estudiantes_route():
    return obtener_estudiantes_controller()

# Usuarios con rol 'admin' o 'estudiante' pueden ver estudiante por id
@router.route("/<string:id>", methods=["GET"])
@token_required(allowed_roles=["admin", "estudiante"])
def obtener_estudiante_route(id):
    return obtener_estudiante_controller(id)

# Solo 'admin' puede actualizar estudiante
@router.route("/<string:id>", methods=["PUT"])
@token_required(allowed_roles=["admin", "estudiante"])
def actualizar_estudiante_route(id):
    return actualizar_estudiante_controller(id, request)

# Solo 'admin' puede eliminar estudiante
@router.route("/<string:id>", methods=["DELETE"])
@token_required(allowed_roles=["admin", "estudiante"])
def eliminar_estudiante_route(id):
    return eliminar_estudiante_controller(id)

