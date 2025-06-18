# --- Imports estándar ---
from flask import Blueprint

# --- Imports internos ---
from src.controller.profesores_con import (
    obtener_profesores_controller,
    obtener_profesor_controller
)

# --- Blueprint ---
router = Blueprint("profesores", __name__)

# --- Endpoints ---
@router.route("/", methods=["GET"])
def obtener_profesores_route():
    return obtener_profesores_controller()

@router.route("/<string:id>", methods=["GET"])
def obtener_profesor_route(id):
    return obtener_profesor_controller(id)
