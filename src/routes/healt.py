# src/routes/health.py
from flask import Blueprint
from src.controller.health_controller import test_db_connection

health_bp = Blueprint('health', __name__)

@health_bp.route('/test-db', methods=['GET'])
def test_db():
    return test_db_connection()