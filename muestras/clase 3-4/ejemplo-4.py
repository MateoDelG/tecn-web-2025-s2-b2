# Filtros por campo usando query params (GET)

from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# 🔌 Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["api_iot"]
collection = db["items"]


# Filtrar documentos por nombre usando query params
# http://localhost:5000/items/filtrar?nombre=sensor-temp-003
@app.get("/items/filtrar")
def filtrar_por_nombre():
    nombre = request.args.get("nombre")  # Capturar ?nombre=...

    if not nombre:
        return {"error": "Debes enviar el parámetro 'nombre'"}, 400

    # Buscar por coincidencia exacta
    items = list(collection.find({"nombre": nombre}))

    # Convertir ObjectId -> string
    for item in items:
        item["_id"] = str(item["_id"])

    return items, 200


if __name__ == "__main__":
    app.run(debug=True)
