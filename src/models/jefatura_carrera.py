from src.database.db import db
from bson import ObjectId

# Colección en MongoDB
jefatura_carrera = db["jefatura_carrera"]

# 🧭 Obtener todas las jefaturas
def obtener_jefaturas():
    """
    Devuelve una lista de todas las jefaturas de carrera.
    Incluye: encargado, horario, carreras, descripcion, coordenadas.
    """
    return list(
        jefatura_carrera.find(
            {},
            {
                "encargado": 1,
                "horario": 1,
                "carreras": 1,
                "descripcion": 1,
                "coordenadas": 1
            }
        )
    )

# 🧭 Obtener una jefatura por su ID
def obtener_jefatura_por_id(id):
    """
    Devuelve una jefatura por su ID, o None si el ID es inválido o no existe.
    """
    try:
        return jefatura_carrera.find_one({"_id": ObjectId(id)})
    except:
        return None

# 🧭 Insertar una nueva jefatura
def insertar_jefatura(encargado, horario, carreras, descripcion, coordenadas):
    """
    Inserta una nueva jefatura en la base de datos.
    `encargado`: nombre del responsable (str)
    `horario`: lista o cadena con los horarios (list o str)
    `carreras`: lista de carreras a cargo (list)
    `descripcion`: descripción del área (str)
    `coordenadas`: dict con campos lat y lon
    Retorna el ID insertado.
    """
    nuevo_doc = {
        "encargado": encargado,
        "horario": horario,
        "carreras": carreras,
        "descripcion": descripcion,
        "coordenadas": coordenadas
    }
    resultado = jefatura_carrera.insert_one(nuevo_doc)
    return str(resultado.inserted_id)

# 🧭 Actualizar una jefatura por su ID
def actualizar_jefatura(id, campos):
    """
    Actualiza campos específicos en la jefatura.
    `campos`: dict con los campos a actualizar.
    """
    try:
        resultado = jefatura_carrera.update_one(
            {"_id": ObjectId(id)},
            {"$set": campos}
        )
        return resultado.modified_count
    except:
        return 0

# 🧭 Eliminar una jefatura por su ID
def eliminar_jefatura(id):
    """
    Elimina una jefatura por su ID.
    """
    try:
        resultado = jefatura_carrera.delete_one({"_id": ObjectId(id)})
        return resultado.deleted_count
    except:
        return 0
