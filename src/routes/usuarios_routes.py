from flask import Blueprint
from src.auth.verify_token import token_required
from src.controller.usuarios_con import (
    crear_usuario_controller,
    obtener_usuarios_controller,
    obtener_usuario_controller,
    actualizar_usuario_controller,
    eliminar_usuario_controller
)

router = Blueprint("usuarios", __name__)

@router.route("/", methods=["POST"])
def crear_usuario_route():
    return crear_usuario_controller()

@router.route("/", methods=["GET"])
@token_required
def obtener_usuarios_route():
    return obtener_usuarios_controller()

@router.route("/<string:id>", methods=["GET"])
def obtener_usuario_route(id):
    return obtener_usuario_controller(id)

@router.route("/<string:id>", methods=["PUT"])
def actualizar_usuario_route(id):
    return actualizar_usuario_controller(id)

@router.route("/<string:id>", methods=["DELETE"])
def eliminar_usuario_route(id):
    return eliminar_usuario_controller(id)