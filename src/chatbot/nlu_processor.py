# src/BackTescha/chatbot/nlu_processor.py
import spacy
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import random

# Descargar stopwords de NLTK si no están presentes
try:
    stopwords.words('spanish')
except LookupError:
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')

# Cargar el modelo de spaCy para español
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    print("Descargando modelo 'es_core_news_sm' de spaCy. Esto puede tardar un poco...")
    spacy.cli.download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

# --- Datos de Entrenamiento para NLTK (más ejemplos son mejores) ---
# Usamos una lista de tuplas: (texto, etiqueta)
training_data = [
    # Saludos
    ("Hola", "saludo"),
    ("Qué tal", "saludo"),
    ("Buenos días", "saludo"),
    ("Buenas tardes", "saludo"),
    ("Buenas noches", "saludo"),
    ("Saludos", "saludo"),
    ("Hey", "saludo"),
    ("Qué onda", "saludo"),
    ("Cómo estás", "saludo"),

    # Despedidas
    ("Adiós", "despedida"),
    ("Hasta luego", "despedida"),
    ("Nos vemos", "despedida"),
    ("Chao", "despedida"),
    ("Gracias, adiós", "despedida"),
    ("Me despido", "despedida"),

    # Ubicación Edificio
    ("Dónde está el edificio A", "consultar_ubicacion_edificio"),
    ("Ubicación del laboratorio de cómputo", "consultar_ubicacion_edificio"),
    ("Cómo llego a la cafetería", "consultar_ubicacion_edificio"),
    ("Necesito encontrar el auditorio principal", "consultar_ubicacion_edificio"),
    ("Cuál es la descripción del Edificio de Ingeniería", "consultar_ubicacion_edificio"),
    ("Muéstrame el camino al salón A201", "consultar_ubicacion_edificio"),
    ("Información sobre el gimnasio", "consultar_ubicacion_edificio"),
    ("Podrías decirme dónde está la biblioteca", "consultar_ubicacion_edificio"),
    ("Ubicación de la cancha de fútbol", "consultar_ubicacion_edificio"),
    ("Guíame al centro de idiomas", "consultar_ubicacion_edificio"),

    # Horario Profesor
    ("Cuál es el horario del profesor Juan Pérez", "consultar_horario_profesor"),
    ("A qué hora da clases el Dr. López", "consultar_horario_profesor"),
    ("Dónde encuentro al profesor de cálculo", "consultar_horario_profesor"),
    ("Horarios del Ing. García", "consultar_horario_profesor"),
    ("Clases de la Mtra. Ana Sánchez", "consultar_horario_profesor"),
    ("Cuándo está disponible el profesor de algoritmos", "consultar_horario_profesor"),
    ("Información del maestro de química", "consultar_horario_profesor"),

    # Ventanilla de Atención
    ("Qué trámites hago en Servicios Escolares", "consultar_ventanilla_atencion"),
    ("Dónde está la ventanilla de pagos", "consultar_ventanilla_atencion"),
    ("Horario de atención de caja", "consultar_ventanilla_atencion"),
    ("Información sobre Control Académico", "consultar_ventanilla_atencion"),
    ("Necesito ir a tesorería", "consultar_ventanilla_atencion"),
    ("Qué puedo hacer en la ventanilla de becas", "consultar_ventanilla_atencion"),

    # Jefatura de Carrera
    ("Dónde está la jefatura de sistemas", "consultar_jefatura_carrera"),
    ("Ubicación de la dirección de mecatrónica", "consultar_jefatura_carrera"),
    ("Contacto de la jefatura de arquitectura", "consultar_jefatura_carrera"),
    ("Información de la carrera de gestión empresarial", "consultar_jefatura_carrera"),
    ("Oficina del jefe de electromecánica", "consultar_jefatura_carrera"),

    # Administrar Usuarios (solo para admins)
    ("Quiero editar un usuario", "administrar_usuarios"),
    ("Modificar información de alumno", "administrar_usuarios"),
    ("Crear nuevo usuario", "administrar_usuarios"),
    ("Eliminar usuario con matrícula 12345", "administrar_usuarios"),
    ("Necesito modificar datos de usuarios", "administrar_usuarios"),
    ("Permiso para editar usuarios", "administrar_usuarios"),
    ("Gestionar cuentas", "administrar_usuarios"),
    ("Actualizar perfil de estudiante", "administrar_usuarios"),
    ("Dar de baja a un profesor", "administrar_usuarios"),
]

# Preprocesamiento para NLTK
stop_words_spanish = set(stopwords.words('spanish'))

def preprocess_text(text):
    """Limpia y tokeniza el texto para NLTK."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Elimina puntuación
    tokens = word_tokenize(text, language='spanish')
    filtered_tokens = [word for word in tokens if word not in stop_words_spanish]
    return dict([(word, True) for word in filtered_tokens])

# Entrenar el clasificador de Naive Bayes
featuresets = [(preprocess_text(text), category) for (text, category) in training_data]
classifier = NaiveBayesClassifier.train(featuresets)

def classify_intent_nltk(text):
    """Clasifica la intención del mensaje usando el clasificador de NLTK."""
    feats = preprocess_text(text)
    return classifier.classify(feats)

def extract_entities_spacy(text, intent):
    """
    Extrae entidades del texto usando spaCy, basado en la intención.
    Esto es más rudimentario que un NER pre-entrenado y depende de patrones.
    """
    doc = nlp(text.lower())
    entities = {}

    if intent == "consultar_ubicacion_edificio":
        # Intentar encontrar nombres de edificios comunes o patrones
        edificio_keywords = ["edificio", "laboratorio", "biblioteca", "cafetería", "auditorio",
                             "gimnasio", "salón", "cancha", "idiomas", "deportivo", "canchas", "centro"]
        found_names = []
        for token in doc:
            # Buscar entidades nombradas (Lugares, Organizaciones)
            if token.ent_type_ in ["LOC", "ORG"]: # LOC para lugares, ORG para organizaciones (ej. "Biblioteca Central")
                found_names.append(token.text)
        
        # También buscar palabras clave directas
        for keyword in edificio_keywords:
            if keyword in text.lower():
                # Extracción simple: toma las 1-3 palabras después de la palabra clave
                match = re.search(r'(?i)\b' + re.escape(keyword) + r'\b\s*(\w+\s*\w*\s*\w*)', text)
                if match:
                    found_names.append(match.group(1).strip())
                else: # Si no hay nada después, usa la palabra clave misma
                    found_names.append(keyword)

        # Eliminar duplicados y priorizar
        if found_names:
            entities['nombre_edificio'] = " ".join(list(set(found_names))).strip()
            # Una heurística simple: si "edificio" o "laboratorio" está presente, úsalo como parte del nombre
            if "edificio" in text.lower() and "edificio" not in entities['nombre_edificio'].lower():
                entities['nombre_edificio'] = "edificio " + entities['nombre_edificio']
            if "laboratorio" in text.lower() and "laboratorio" not in entities['nombre_edificio'].lower():
                entities['nombre_edificio'] = "laboratorio " + entities['nombre_edificio']
        
        # Último recurso: si hay un número de salón, tómalo
        salon_match = re.search(r'([a-zA-Z]\d{3})', text) # Ej. A201
        if salon_match:
            entities['nombre_edificio'] = salon_match.group(1).upper() # Convierte a mayúsculas

    elif intent == "consultar_horario_profesor":
        # Extraer nombres de personas (profesores)
        profesor_name_parts = []
        for ent in doc.ents:
            if ent.label_ == "PER": # PER para persona
                profesor_name_parts.append(ent.text)
        
        if profesor_name_parts:
            entities['nombre_profesor'] = " ".join(profesor_name_parts)
        else: # Si spaCy no encuentra PER, buscar patrones como "profesor X"
            match = re.search(r'(profesor|dr\.|ing\.|mtra\.|maestro)\s+([\w\s]+)', text, re.IGNORECASE)
            if match:
                entities['nombre_profesor'] = match.group(2).strip() # Solo el nombre después del título
            else: # Otra heurística: si solo hay un nombre propio, usarlo
                for token in doc:
                    if token.pos_ == "PROPN" and len(token.text) > 2 and token.text not in ["juan", "maria", "pedro", "anna"]: # Evitar nombres muy comunes que no sean profesores
                        entities['nombre_profesor'] = token.text
                        break


    elif intent == "consultar_ventanilla_atencion":
        # Extraer nombres de ventanillas o departamentos
        ventanilla_keywords = ["servicios escolares", "caja", "tesorería", "control académico",
                               "becas", "pagos", "recursos humanos", "ventanilla"]
        found_ventanillas = []
        for keyword in ventanilla_keywords:
            if keyword in text.lower():
                found_ventanillas.append(keyword)
        if found_ventanillas:
            entities['nombre_ventanilla'] = " ".join(list(set(found_ventanillas)))
        else:
            # Buscar patrones como "ventanilla de X"
            match = re.search(r'(ventanilla de|oficina de|departamento de)\s+([\w\s]+)', text, re.IGNORECASE)
            if match:
                entities['nombre_ventanilla'] = match.group(2).strip()

    elif intent == "consultar_jefatura_carrera":
        # Extraer nombres de carrera
        carrera_keywords = ["sistemas", "mecatrónica", "arquitectura", "gestión empresarial",
                            "electromecánica", "computación", "civil", "química"]
        found_carreras = []
        for keyword in carrera_keywords:
            if keyword in text.lower():
                found_carreras.append(keyword)
        if found_carreras:
            entities['nombre_carrera'] = " ".join(list(set(found_carreras)))
        else:
            match = re.search(r'(carrera de|jefatura de|dirección de)\s+([\w\s]+)', text, re.IGNORECASE)
            if match:
                entities['nombre_carrera'] = match.group(2).strip()

    elif intent == "administrar_usuarios":
        # Extraer acción y posible identificador/tipo de usuario
        action_match = re.search(r'(editar|modificar|crear|eliminar|actualizar|dar de baja)', text, re.IGNORECASE)
        if action_match:
            entities['accion_admin'] = action_match.group(1).lower()

        # Buscar matrícula
        matricula_match = re.search(r'(matricula|id)\s*(\d+)', text, re.IGNORECASE)
        if matricula_match:
            entities['identificador_usuario'] = matricula_match.group(2)
        else: # Buscar nombres de usuario o correos
            user_id_match = re.search(r'(usuario|estudiante|profesor)\s+([\w\s.@-]+)', text, re.IGNORECASE)
            if user_id_match:
                entities['identificador_usuario'] = user_id_match.group(2).strip()
                entities['tipo_usuario'] = user_id_match.group(1).lower()


    return entities

def process_nlu(user_message):
    """Función principal para procesar el lenguaje natural."""
    intent = classify_intent_nltk(user_message)
    entities = extract_entities_spacy(user_message, intent)
    return {"intent": intent, "entities": entities}

if __name__ == '__main__':
    # Pequeñas pruebas rápidas
    print(process_nlu("Hola chatbot"))
    print(process_nlu("Dónde está el edificio de sistemas"))
    print(process_nlu("Horario del profesor Pedro Sánchez"))
    print(process_nlu("Qué trámites hago en la ventanilla de servicios escolares"))
    print(process_nlu("Ubicación de la jefatura de ingeniería civil"))
    print(process_nlu("Quiero editar el usuario 12345"))
    print(process_nlu("Eliminar al estudiante Juan Perez"))
    print(process_nlu("Adiós"))