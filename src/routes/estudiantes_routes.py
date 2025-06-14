# --- Imports estándar ---
from flask import Blueprint

# --- Imports internos ---
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
router.route("/", methods=["POST"])(crear_estudiante_controller)
router.route("/", methods=["GET"])(obtener_estudiantes_controller)
router.route("/<string:id>", methods=["GET"])(obtener_estudiante_controller)
router.route("/<string:id>", methods=["PUT"])(actualizar_estudiante_controller)
router.route("/<string:id>", methods=["DELETE"])(eliminar_estudiante_controller)
