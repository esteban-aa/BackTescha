from flask import Flask, jsonify
from flask_cors import CORS
from src.database.db import db  
from waitress import serve 

app = Flask(__name__)
CORS(app)

@app.route('/test-db')
def test_db():
    try:
        # Prueba: inserta un documento de prueba y luego lo elimina
        test_collection = db["test"]
        test_doc = {"mensaje": "¡Conexión exitosa a MongoDB Atlas!"}
        result = test_collection.insert_one(test_doc)

        # Recupera el documento insertado
        inserted = test_collection.find_one({"_id": result.inserted_id})

        # Limpieza (elimina el documento de prueba)
        test_collection.delete_one({"_id": result.inserted_id})

        return jsonify({"status": "ok", "mensaje": inserted["mensaje"]})
    except Exception as e:
        return jsonify({"status": "error", "mensaje": str(e)}), 500

if __name__ == '__main__':
    print("Iniciando la aplicación con Waitress...")
    # ¡CAMBIA ESTA LÍNEA!
    serve(app, host='0.0.0.0', port=5001) 