# Actualizar documento usando el campo nombre (PUT)

from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

# 🔌 Conexión a MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["api_iot"]
collection = db["items"]



# {
#   "valor": 42,
#   "activo": false
# }
# Actualizar un documento usando el campo 'nombre'
@app.put("/items/nombre/<nombre>")
def update_by_nombre(nombre):
    data = request.get_json()  # Nuevos datos a actualizar

    # Ejecutar la actualización
    result = collection.update_one(
        {"nombre": nombre},   # Filtro por el nombre
        {"$set": data}        # Actualización parcial
    )

    if result.matched_count == 0:
        return {"error": "No existe un documento con ese nombre"}, 404

    return {"message": f"Documento '{nombre}' actualizado correctamente"}, 200


if __name__ == "__main__":
    app.run(debug=True)
