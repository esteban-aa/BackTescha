from flask import Blueprint, request, jsonify
from src.auth.login import login_usuario

auth_router = Blueprint("auth", __name__)

@auth_router.route('/login', methods=['POST'])
def api_login():
    data = request.json
    correo = data.get('correo')
    contraseña = data.get('contraseña')

    if not correo or not contraseña:
        return jsonify({"error": "Correo y contraseña requeridos"}), 400

    return login_usuario(correo, contraseña)

