from flask import Blueprint
from controller.edificios_con import (
    obtener_edificios_controller,
    obtener_edificio_controller  # ✅ nombre corregido aquí también
)

router = Blueprint("edificios", __name__)

router.route("/", methods=["GET"])(obtener_edificios_controller)
router.route("/<string:edificio_id>", methods=["GET"])(obtener_edificio_controller)
