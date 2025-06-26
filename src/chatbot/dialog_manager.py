# src/BackTescha/chatbot/dialog_manager.py
from .knowledge_base import (
    get_edificio_info, get_profesor_info, get_ventanilla_info,
    get_jefatura_info, get_user_by_matricula, get_user_by_id_or_identifier # Mantendremos get_user_by_id_or_identifier si queremos buscar el usuario por ID/nombre antes de intentar actualizar.
    # update_user_info # Ya no necesitamos importar esta, ya que la lógica de actualización se moverá a una llamada API.
)
from .nlu_processor import process_nlu
import random
import requests # Necesitarás instalar esta librería: pip install requests
import json # Para trabajar con JSON

# URL base de tu backend principal (ajusta si es necesario en producción)
BACKEND_BASE_URL = "http://localhost:5000"

def _call_backend_api(method, endpoint, data=None):
    """
    Función auxiliar para hacer llamadas HTTP a tu backend principal.
    """
    url = f"{BACKEND_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        if method.upper() == "PUT":
            response = requests.put(url, headers=headers, data=json.dumps(data))
        elif method.upper() == "POST": # Por si tu API de update es POST
            response = requests.post(url, headers=headers, data=json.dumps(data))
        else:
            return {"success": False, "message": "Método HTTP no soportado por el chatbot para esta acción."}

        response.raise_for_status() # Lanza una excepción para errores HTTP (4xx o 5xx)
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        print(f"Error al llamar al backend API ({url}): {e}")
        return {"success": False, "message": f"Error de conexión con el backend: {e}"}
    except json.JSONDecodeError:
        print(f"Error al decodificar la respuesta JSON: {response.text}")
        return {"success": False, "message": "Respuesta inválida del backend."}


def generate_response(user_message, user_role, user_matricula=None):
    """
    Genera la respuesta del chatbot basada en el mensaje del usuario,
    su rol y matrícula (si aplica).
    """
    nlu_result = process_nlu(user_message)
    intent = nlu_result['intent']
    entities = nlu_result['entities']

    response_text = "Lo siento, no entendí tu pregunta. ¿Podrías reformularla?"

    if intent == "saludo":
        greetings = ["¡Hola! ¿En qué puedo ayudarte hoy?", "¿Qué tal? Dime en qué te puedo asistir.", "¡Saludos! ¿Tienes alguna pregunta sobre la escuela?"]
        response_text = random.choice(greetings)

    elif intent == "despedida":
        farewells = ["¡Hasta luego! Que tengas un buen día.", "Adiós. Si necesitas algo más, aquí estoy.", "¡Nos vemos!"]
        response_text = random.choice(farewells)

    elif intent == "consultar_ubicacion_edificio":
        if (nombre_edificio := entities.get('nombre_edificio')):
            info = get_edificio_info(nombre_edificio)
            if info:
                response_text = f"El {info['nombre']} se encuentra: {info['descripcion']}."
                if 'coordenadas' in info and info['coordenadas']:
                    response_text += f" Sus coordenadas son: {info['coordenadas'][0]}, {info['coordenadas'][1]}."
            else:
                response_text = f"No encontré información sobre '{nombre_edificio}'. ¿Podrías ser más específico o revisar el nombre?"
        else:
            response_text = "Para darte la ubicación, necesito saber el nombre del edificio o lugar. Por ejemplo: '¿Dónde está la biblioteca?'"

    # --- Restricciones por Rol ---
    if user_role == "usuario":
        if intent in ["consultar_horario_profesor", "consultar_ventanilla_atencion", "consultar_jefatura_carrera", "administrar_usuarios"]:
            response_text = "Lo siento, como usuario invitado solo puedo ayudarte con la ubicación de los edificios. Para otras consultas, necesitas un rol de estudiante o administrador."
            return response_text

    # Lógica para 'estudiante' y 'admin'
    elif intent == "consultar_horario_profesor":
        if user_role == "estudiante" and not user_matricula:
            response_text = "Para consultar el horario de un profesor, necesito tu matrícula de estudiante. Por favor, asegúrate de haber iniciado sesión con tu matrícula."
        else:
            if (nombre_profesor := entities.get('nombre_profesor')):
                profesor = get_profesor_info(nombre_profesor)
                if profesor:
                    horarios_str = ", ".join(profesor['horarios']) if profesor['horarios'] else "no especificados"
                    response_text = f"El profesor {profesor['nombre']} tiene clases en el {profesor['edificio']}, salón {profesor['salon']}. Sus horarios son: {horarios_str}."
                else:
                    response_text = f"No encontré información sobre el profesor '{nombre_profesor}'. Asegúrate de escribir el nombre completo o correcto."
            else:
                response_text = "Para darte el horario de un profesor, necesito su nombre. Por ejemplo: 'Horario del profesor Juan Pérez'."

    elif intent == "consultar_ventanilla_atencion":
        if (nombre_ventanilla := entities.get('nombre_ventanilla')):
            info = get_ventanilla_info(nombre_ventanilla)
            if info:
                tramites_str = ", ".join(info['tramites']) if info['tramites'] else "no especificados"
                horarios_str = ", ".join(info['horarios']) if info['horarios'] else "no especificados"
                response_text = (f"La ventanilla/área de {info.get('nombre', nombre_ventanilla).capitalize()} se encuentra en {info['ubicacion']}. "
                                 f"Sus horarios de atención son: {horarios_str}. "
                                 f"Aquí puedes realizar trámites como: {tramites_str}.")
                # Usar info.get('nombre', nombre_ventanilla) para mostrar el nombre si existe en la DB
            else:
                response_text = f"No encontré información sobre la ventanilla/área '{nombre_ventanilla}'. ¿Podrías ser más específico?"
        else:
            response_text = "Para darte información sobre una ventanilla, necesito su nombre. Por ejemplo: 'Trámites en Servicios Escolares'."

    elif intent == "consultar_jefatura_carrera":
        if (nombre_carrera := entities.get('nombre_carrera')):
            info = get_jefatura_info(nombre_carrera)
            if info:
                response_text = (f"La jefatura de la carrera de {info['nombre_carrera']} se encuentra en {info['ubicacion_oficina']}. "
                                 f"Horario de atención: {info.get('horario_atencion', 'No especificado')}.")
            else:
                response_text = f"No encontré información sobre la jefatura de la carrera '{nombre_carrera}'. ¿Es un nombre completo o válido?"
        else:
            response_text = "Para darte la ubicación de una jefatura, necesito el nombre de la carrera. Por ejemplo: 'Ubicación de la jefatura de sistemas'."

    elif intent == "administrar_usuarios":
        if user_role == "admin":
            accion = entities.get('accion_admin')
            identificador_usuario = entities.get('identificador_usuario')
            tipo_usuario = entities.get('tipo_usuario') # Extraer el tipo de usuario si se detecta

            if accion == "editar" and identificador_usuario:
                # Aquí construiríamos los nuevos datos y el ID.
                # Esto es una SIMULACIÓN y necesitaría más inteligencia del chatbot
                # para preguntar por los *nuevos datos* específicos.
                # Por simplicidad para el demo, asumiremos que si dice "editar usuario X",
                # el chatbot solo puede confirmar que está listo para editar.
                
                # --- PASO CRÍTICO: ¿CÓMO OBTENER user_id y new_data? ---
                # El chatbot necesitaría preguntar al admin:
                # "Dime el ID del usuario (ObjectId) y los campos que deseas modificar en formato JSON (ej. {'campo': 'valor'})"
                # O bien, tener un flujo de diálogo más avanzado.
                
                # Para este ejemplo de 4 días, haremos algo más básico:
                # El chatbot le pedirá al admin el ID y los datos a cambiar.
                response_text = f"Entendido, como administrador, deseas '{accion}' al usuario '{identificador_usuario}'. " \
                                 "Para proceder, dime el ID exacto (ObjectId) del usuario y los datos a modificar en formato JSON, por ejemplo: " \
                                 "'modificar usuario 65f3f... de datos {'correo': 'nuevo@example.com'}' (¡requiere NLU más avanzado para extraer JSON del texto!)"
                
                # ALTERNATIVA SIMPLE para la demo: Si el admin ya dice todo en el mensaje:
                # Si tu `nlu_processor` pudiera extraer directamente un ID y un diccionario de datos del mensaje,
                # entonces lo pasarías a _call_backend_api.
                # Ejemplo de extracción (muy rudimentario, necesitaría NLU avanzado o un flujo de preguntas/respuestas):
                # user_id_from_msg = entities.get('user_id_from_msg') # Si se pudiera extraer '65f3f...'
                # data_to_update = entities.get('data_to_update') # Si se pudiera extraer {'correo': 'nuevo@example.com'}

                # if user_id_from_msg and data_to_update:
                #     api_response = _call_backend_api("PUT", f"/users/{user_id_from_msg}", data_to_update)
                #     if api_response["success"]:
                #         response_text = f"Usuario {user_id_from_msg} actualizado con éxito."
                #     else:
                #         response_text = f"Error al actualizar usuario: {api_response['message']}"
                # else:
                #    response_text = "Para editar un usuario, necesito su ID exacto y los datos a modificar."

            elif accion == "crear" or accion == "eliminar":
                # Lógica similar: el chatbot necesitaría más información para estas acciones.
                response_text = f"Comprendido, deseas '{accion}' un usuario. Por favor, proporciona todos los detalles necesarios para '{accion}'. Por ejemplo, para eliminar: 'eliminar usuario con ID 123'."

            else:
                response_text = "Como administrador, puedo ayudarte a gestionar usuarios. ¿Qué acción te gustaría realizar (editar, crear, eliminar) y a qué usuario te refieres?"
        else:
            response_text = "No tienes permisos para realizar acciones administrativas. Esta función es solo para administradores."

    return response_text