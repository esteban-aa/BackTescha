from flask import Blueprint, jsonify
import os

file_routes = Blueprint('file_routes', __name__)

@file_routes.route('/leer-archivo', methods=['GET'])
def leer_archivo():
    try:
        ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'files', 'ejemplo.txt')
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return jsonify({"contenido": contenido})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
