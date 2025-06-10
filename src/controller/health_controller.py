from flask import jsonify
from src.database.db import db # Importa la instancia de la DB

def test_db_connection():
    try:
        test_collection = db["test"]
        test_doc = {"mensaje": "¡Conexión exitosa a MongoDB Atlas!"}
        result = test_collection.insert_one(test_doc)

        inserted = test_collection.find_one({"_id": result.inserted_id})
        test_collection.delete_one({"_id": result.inserted_id})

        return jsonify({"status": "ok", "mensaje": inserted["mensaje"]})
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500