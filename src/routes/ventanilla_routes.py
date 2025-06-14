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
router.route("/", methods=["GET"])(obtener_ventanillas_controller)
router.route("/<string:id>", methods=["GET"])(obtener_ventanilla_controller)
