#Conexión a MongoDB + Insertar documento (POST)

from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 🔌 Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["api_iot"]
collection = db["items"]


# {
#   "nombre": "sensor-temp-001",
#   "valor": 23.5,
#   "activo": true
# }
# Endpoint POST: crear un nuevo documento y retornar todo
@app.post("/items")
def create_item():
    data = request.get_json()  # Recibir JSON enviado

    # Insertar documento en MongoDB
    result = collection.insert_one(data)

    # Agregar el _id al JSON original
    data["_id"] = str(result.inserted_id)

    # Retornar el documento completo creado
    return data, 201


if __name__ == "__main__":
    app.run(debug=True)
