from flask import Blueprint, request, jsonify
from src.chatbot.dialog_manager import generate_response

chatbot_bp = Blueprint('chatbot_bp', __name__)

@chatbot_bp.route('/chatbot/message', methods=['POST'])
def chatbot_message():
    data = request.get_json()
    user_message = data.get('message')
    user_role = data.get('role', 'usuario')  # Default a 'usuario' si no se envía
    user_matricula = data.get('matricula', None) # Se espera que el frontend envíe la matrícula si es alumno

    if not user_message:
        return jsonify({"response": "Mensaje vacío. Por favor, escribe algo."}), 400

    # Llama al gestor de diálogo para obtener la respuesta
    bot_response = generate_response(user_message, user_role, user_matricula)

    return jsonify({"response": bot_response})