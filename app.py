from flask import Flask, request
from flask_cors import CORS

# --- Auth ---
from src.auth.login import login_unificado

# --- Rutas externas (Blueprints) ---
from src.routes.auth_routes import auth_router
from src.routes.edificios_routes import router as edificios_router
from src.routes.usuarios_routes import router as usuarios_router
from src.routes.estudiantes_routes import router as estudiantes_router
from src.routes.profesores_routes import router as profesores_router
from src.routes.ventanilla_routes import router as ventanilla_router

# --- Base de datos ---
from src.database.db import db

# --- App Init ---
app = Flask(__name__)
CORS(app)

# === Registro de Blueprints ===
app.register_blueprint(auth_router, url_prefix="/api")
app.register_blueprint(edificios_router, url_prefix="/api/edificios")
app.register_blueprint(usuarios_router, url_prefix="/api/usuarios")
app.register_blueprint(estudiantes_router, url_prefix="/api/estudiantes")
app.register_blueprint(profesores_router, url_prefix="/api/profesores")
app.register_blueprint(ventanilla_router, url_prefix="/api/ventanilla")

# === Rutas individuales ===
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    return login_usuario(data['correo'], data['contraseña'])

# === Inicio de servidor ===
if __name__ == '__main__':
    app.run(debug=True)
