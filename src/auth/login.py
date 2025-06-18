import os
import bcrypt
import jwt
import datetime
from flask import jsonify
from src.database.db import db

SECRET_KEY = os.getenv("SECRET_KEY")

def login_unificado(correo, contraseña):
    usuario = db["usuarios"].find_one({"correo": correo})
    rol = None
    data_user = None

    if usuario:
        rol = "usuario"
        data_user = usuario
    else:
        estudiante = db["estudiantes"].find_one({"correo": correo})
        if estudiante:
            rol = "estudiante"
            data_user = estudiante
        else:
            return jsonify({"mensaje": "Correo no registrado"}), 401

    # --- Validación de contraseña ---
    hashed_pass = data_user.get('contraseña')
    if not hashed_pass:
        return jsonify({"mensaje": "Usuario sin contraseña registrada"}), 401

    if isinstance(hashed_pass, str):
        hashed_pass = hashed_pass.encode('utf-8')

    if not bcrypt.checkpw(contraseña.encode('utf-8'), hashed_pass):
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    # --- Generación de token JWT ---
    payload = {
        "correo": data_user['correo'],
        "rol": rol,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }

    if rol == "usuario":
        payload["usuario"] = data_user.get('usuario', '')
    elif rol == "estudiante":
        payload["matricula"] = data_user.get("matricula", "")

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    # Asegura que el token sea string (en algunas versiones es bytes)
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({"token": token}), 200
