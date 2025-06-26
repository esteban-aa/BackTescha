# --- Imports estándar ---
from flask import Blueprint

# --- Imports internos ---
from src.controller.jefatura_carrera_con import (
    obtener_jefaturas_controller,
    obtener_jefatura_controller
)

# --- Blueprint ---
router = Blueprint("jefatura_carrera", __name__)

# --- Endpoints ---
@router.route("/", methods=["GET"])
def obtener_jefaturas_route():
    return obtener_jefaturas_controller()

@router.route("/<string:id>", methods=["GET"])
def obtener_jefatura_route(id):
    return obtener_jefatura_controller(id)


