# --- Imports estándar ---
from flask import Blueprint

# --- Imports internos ---
from src.controller.ventanilla_con import (
    obtener_ventanillas_controller,
    obtener_ventanilla_controller
)

# --- Blueprint ---
router = Blueprint("ventanilla", __name__)

# --- Endpoints ---
@router.route("/", methods=["GET"])
def obtener_ventanillas_route():
    return obtener_ventanillas_controller()

@router.route("/<string:id>", methods=["GET"])
def obtener_ventanilla_route(id):
    return obtener_ventanilla_controller(id)
