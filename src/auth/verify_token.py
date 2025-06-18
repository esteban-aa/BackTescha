from datetime import date
from functools import wraps
from flask import request, jsonify
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY")  # Carga desde .env o config

def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization')

            if not auth_header:
                return jsonify({"mensaje": "Token requerido"}), 401

            parts = auth_header.split()

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"mensaje": "Formato de token inválido"}), 401

            token = parts[1]

            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                print("DATA JWT DECODIFICADO:", data)
            except jwt.ExpiredSignatureError:
                return jsonify({"mensaje": "Token expirado"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"mensaje": "Token inválido"}), 401

            if allowed_roles and data.get("rol") not in allowed_roles:
                return jsonify({"mensaje": "Permiso denegado"}), 403

            request.user = data  # info para usar en las rutas

            return f(*args, **kwargs)
        return decorated
    return decorator


