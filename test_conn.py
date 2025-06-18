# === Endpoint de prueba de conexión a la BD ===
from database import db


@app.route('/api/test_conn', methods=['GET'])
def test_db():
    try:
        # Accede a la colección "test"
        test_collection = db["test"]

        # Crea un documento temporal
        test_doc = {"mensaje": "¡Conexión exitosa a MongoDB Atlas!"}
        result = test_collection.insert_one(test_doc)

        # Recupera el documento insertado
        inserted = test_collection.find_one({"_id": result.inserted_id})

        # Limpieza: elimina el documento de prueba
        test_collection.delete_one({"_id": result.inserted_id})

        # Devuelve el resultado
        return jsonify({
            "status": "ok",
            "mensaje": inserted["mensaje"]
        }), 200

    except Exception as e:
        # En caso de error, devuelve el mensaje
        return jsonify({
            "status": "error",
            "mensaje": str(e)
        }), 500
