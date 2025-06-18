from flask import Blueprint, request, jsonify
from src.auth.login import login_unificado

# Crear blueprint
auth_router = Blueprint("auth", __name__)

# Ruta para login
@auth_router.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()

    correo = data.get('correo')
    contraseña = data.get('contraseña')

    if not correo or not contraseña:
        return jsonify({"error": "Correo y contraseña son requeridos"}), 400

    return login_unificado(correo, contraseña)