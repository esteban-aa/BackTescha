import bcrypt
import jwt
import datetime
from flask import jsonify
from src.database.db import db

# Clave secreta para firmar el token
SECRET_KEY = "clave_supersecreta"  # Mejor cargarla desde .env

def login_usuario(correo, contraseña):
    usuario = db["usuarios"].find_one({"correo": correo})
    if not usuario:
        return jsonify({"mensaje": "Correo no registrado"}), 401

    if not bcrypt.checkpw(contraseña.encode('utf-8'), usuario['contraseña'].encode('utf-8')):
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    token = jwt.encode({
        "correo": usuario['correo'],
        "usuario": usuario['usuario'],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})
