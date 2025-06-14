# --- Imports estándar ---
from flask import Blueprint, jsonify

# --- Imports internos ---
from auth.verify_token import token_required
from src.controller.usuarios_con import (
    crear_usuario_controller,
    obtener_usuarios_controller,
    obtener_usuario_controller,
    actualizar_usuario_controller,
    eliminar_usuario_controller
)

# --- Blueprint ---
router = Blueprint("usuarios", __name__)

# --- Endpoints ---
router.route("/", methods=["POST"])(crear_usuario_controller)
router.route("/", methods=["GET"])(obtener_usuarios_controller)
router.route("/<string:id>", methods=["GET"])(obtener_usuario_controller)
router.route("/<string:id>", methods=["PUT"])(actualizar_usuario_controller)
router.route("/<string:id>", methods=["DELETE"])(eliminar_usuario_controller)
