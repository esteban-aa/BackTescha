from flask import Blueprint

from src.controller.edificios_con import (
    obtener_edificios_controller,
    obtener_edificio_controller
)

router = Blueprint("edificios", __name__)

@router.route("/", methods=["GET"])
def obtener_edificios_route():
    return obtener_edificios_controller()

@router.route("/<string:id>", methods=["GET"])
def obtener_edificio_route(id):
    return obtener_edificio_controller(id)
