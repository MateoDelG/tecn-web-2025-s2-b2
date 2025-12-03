# Obtener documentos y convertir ObjectId (GET)

from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 🔌 Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["api_iot"]          # <<< Nombre de la BD actualizado
collection = db["items"]


# Obtener todos los documentos
@app.get("/items")
def get_items():
    items = list(collection.find())  # Leer todos los docs

    # Convertir ObjectId a string
    for item in items:
        item["_id"] = str(item["_id"])

    return items, 200


if __name__ == "__main__":
    app.run(debug=True)
