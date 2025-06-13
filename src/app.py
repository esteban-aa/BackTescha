from flask import Flask, request, jsonify
from flask_cors import CORS

# Importar funciones desde tus archivos renombrados
from models.usuario import crear_usuario
from models.estudiante import crear_estudiante
from models.profesores import crear_horario_profesor
from models.ventanilla import crear_horario_ventanilla
from models.edificios import crear_edificio
from auth.login import login_usuario
from auth.verify_token import token_required

from src.database.db import db

app = Flask(__name__)
CORS(app)

# --- Usuarios ---
@app.route('/usuarios', methods=['POST'])
def api_crear_usuario():
    data = request.json
    crear_usuario(data['correo'], data['usuario'], data['contraseña'])
    return jsonify({"mensaje": "Usuario creado correctamente"})

@app.route('/usuarios', methods=['GET'])
@token_required
def api_listar_usuarios():
    usuarios = list(db["usuarios"].find({}, {"contraseña": 0}))
    for u in usuarios:
        u.pop('_id', None)
    return jsonify(usuarios)

# --- Estudiantes ---
@app.route('/estudiantes', methods=['POST'])
def api_crear_estudiante():
    data = request.json
    crear_estudiante(data['correo'], data['usuario'], data['contraseña'], data['matricula'])
    return jsonify({"mensaje": "Estudiante creado correctamente"})

@app.route('/estudiantes', methods=['GET'])
def api_listar_estudiantes():
    estudiantes = list(db["estudiantes"].find({}, {"contraseña": 0}))
    for e in estudiantes:
        e.pop('_id', None)
    return jsonify(estudiantes)

# --- Profesores ---
@app.route('/profesores', methods=['POST'])
def api_crear_profesor():
    data = request.json
    crear_horario_profesor(data['nombre'], data['horarios'], data['edificio'], data['salon'])
    return jsonify({"mensaje": "Horario de profesor creado correctamente"})

@app.route('/profesores', methods=['GET'])
def api_listar_profesores():
    profesores = list(db["horarios_profesores"].find())
    for p in profesores:
        p.pop('_id', None)
    return jsonify(profesores)

# --- Ventanilla ---
@app.route('/ventanilla', methods=['POST'])
def api_crear_ventanilla():
    data = request.json
    crear_horario_ventanilla(data['ubicacion'], data['horarios'], data['tramites'])
    return jsonify({"mensaje": "Horario de ventanilla creado correctamente"})

@app.route('/ventanilla', methods=['GET'])
def api_listar_ventanilla():
    ventanillas = list(db["horarios_ventanilla"].find())
    for v in ventanillas:
        v.pop('_id', None)
    return jsonify(ventanillas)

# --- Edificios ---
@app.route('/edificios', methods=['POST'])
def api_crear_edificio():
    data = request.json
    crear_edificio(data['nombre'], data['coordenadas'], data['salones'], data['descripcion'])
    return jsonify({"mensaje": "Edificio creado correctamente"})

@app.route('/edificios', methods=['GET'])
def api_listar_edificios():
    edificios = list(db["edificios"].find())
    for e in edificios:
        e.pop('_id', None)
    return jsonify(edificios)

# --- INICIO ---
if __name__ == '__main__':
    app.run(debug=True)

# --- login ---
@app.route('/login', methods=['POST'])
def api_login():
    data = request.json
    return login_usuario(data['correo'], data['contraseña'])

# --- verify_token ---
@app.route('/usuarios', methods=['GET'])
@token_required
def api_listar_usuarios():