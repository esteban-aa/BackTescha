from flask import Blueprint, jsonify
from src.database.db import db

from src.controller.edificios_con import (
    obtener_edificios_controller,
    obtener_edificio_controller
)

edificios = db["edificios"]

router = Blueprint("edificios", __name__)

@router.route("/", methods=["GET"])
def obtener_edificios_route():
    return obtener_edificios_controller()

@router.route("/<string:id>", methods=["GET"])
def obtener_edificio_route(id):
    return obtener_edificio_controller(id)

# Nueva ruta para obtener edificio por nombre
@router.route("/nombre/<string:nombre>", methods=["GET"])
def get_edificio_por_nombre(nombre):
    edificio = edificios.find_one({"nombre": nombre})
    if edificio:
        edificio.pop("_id", None)
        return jsonify(edificio), 200
    else:
        return jsonify({"error": "Edificio no encontrado"}), 404
