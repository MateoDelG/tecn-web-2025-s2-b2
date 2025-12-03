from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

#conexión a la base de datos
client = MongoClient('mongodb://localhost:27017/')
db = client["api_clase"]
collection = db["items"]


# Ruta para crear un nuevo ítem
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    print(data.get("nombre"))
    #validar que el documento con el campo "nombre" no exista ya
    existing_item = collection.find_one({"nombre": data.get("nombre")})
    if existing_item:
        return {"error": "elemento con el campo <nombre> ya existe."}, 400  

    result = collection.insert_one(data)

    data["_id"] = str(result.inserted_id)
    return data, 201


# Ruta para obtener todos los ítems
@app.route('/items', methods=['GET'])
def get_items():
    items = list(collection.find()) #traemos todos los documentos de la colección

    for item in items:
        item["_id"] = str(item["_id"])  # Convertimos ObjectId a string para JSON
    return items, 200


# Ruta para obtener un ítem por su nombre
@app.route('/items/<string:nombre>', methods=['GET'])
def get_item_by_name(nombre):
    item = collection.find_one({"nombre": nombre})
    if item:
        item["_id"] = str(item["_id"])  # Convertimos ObjectId a string para JSON
        return item, 200
    else:
        return {"error": "Elemento no encontrado."}, 404


#ruta para actualizar un elemento por su nombre
@app.route('/items/<string:nombre>', methods=['PUT'])
def update_item(nombre):
    data = request.get_json()
    result = collection.update_one({"nombre": nombre}, 
                                   {"$set": data})

    if result.matched_count == 0:
        return {"error": "Elemento no encontrado."}, 404

    updated_item = collection.find_one({"nombre": nombre})
    updated_item["_id"] = str(updated_item["_id"])  # Convertimos ObjectId a string para JSON
    return updated_item, 200


#ruta para eliminar un elemento por su nombre
@app.route('/items/<string:nombre>', methods=['DELETE'])
def delete_item(nombre):
    result = collection.delete_one({"nombre": nombre})

    if result.deleted_count == 0:
        return {"error": "Elemento no encontrado."}, 404

    return {"message": "Elemento eliminado correctamente."}, 200




if __name__ == '__main__':
    app.run(debug=True)