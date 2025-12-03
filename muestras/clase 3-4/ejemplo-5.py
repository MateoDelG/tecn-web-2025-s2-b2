from flask import Flask, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# ============================================================
# 🔌 CONEXIÓN A MONGODB
# ============================================================
# Se conecta al servidor MongoDB local y selecciona la base de datos "api_iot"
client = MongoClient("mongodb://localhost:27017/")
db = client["api_iot"]
collection = db["items"]



# ============================================================
# 1) POST /items  → CREAR DOCUMENTO
# ============================================================
@app.post("/items")
def create_item():
    """
    Crea un nuevo documento en la colección 'items'.

     LO QUE SE ENVÍA (JSON en el body):
    {
        "nombre": "Sensor1",
        "valor": 25.3,
        "activo": true
    }

     LO QUE RETORNA (JSON con _id incluido):
    {
        "_id": "67520491a13e52d708bcf412",
        "nombre": "Sensor1",
        "valor": 25.3,
        "activo": true
    }

    Flask recibe el JSON enviado por el cliente.
    MongoDB inserta el documento y genera un ObjectId único.
    Convertimos ese ObjectId a string porque JSON no permite tipos especiales.
    """

    data = request.get_json()           # Recibir el JSON
    result = collection.insert_one(data)  # Insertar en MongoDB

    # Agregar el _id generado al JSON original
    data["_id"] = str(result.inserted_id)

    return data, 201   # Código 201 = Created



# ============================================================
# 2) GET /items  → LISTAR TODOS LOS DOCUMENTOS
# ============================================================
@app.get("/items")
def get_items():
    """
    Retorna todos los documentos almacenados en la colección.

     EJEMPLO DE RETORNO:
    [
        {
            "_id": "675203c8fb55302eb2ac7811",
            "nombre": "Sensor1",
            "valor": 25.3,
            "activo": true
        },
        {
            "_id": "675203d9fb55302eb2ac7822",
            "nombre": "Sensor2",
            "valor": 18.5,
            "activo": false
        }
    ]

    MongoDB devuelve ObjectId → hay que convertirlo a str.
    Retornamos una lista completa en formato JSON.
    """

    items = list(collection.find())     # Obtener todos los documentos

    # Convertir ObjectId → string para que sea compatible con JSON
    for item in items:
        item["_id"] = str(item["_id"])

    return items, 200



# ============================================================
# 3) PUT /items/nombre/<nombre> → ACTUALIZAR POR NOMBRE
# ============================================================
@app.put("/items/nombre/<nombre>")
def update_by_nombre(nombre):
    """
    Actualiza un documento filtrado por el campo 'nombre'.

     LO QUE SE ENVÍA (JSON en el body):
    {
        "valor": 50,
        "activo": false
    }

    Solo se actualizan los campos enviados.
    Si el nombre no existe, retorna 404.

     RESPUESTA EN CASO DE ÉXITO:
    {
        "message": "Documento 'Sensor1' actualizado correctamente"
    }
    """

    data = request.get_json()   # Recibir datos nuevos

    result = collection.update_one(
        {"nombre": nombre},  # Buscar documento cuyo "nombre" coincida
        {"$set": data}       # Actualizar solo los campos enviados
    )

    if result.matched_count == 0:
        # No existe ningún documento con ese nombre
        return {"error": "No existe un documento con ese nombre"}, 404

    return {"message": f"Documento '{nombre}' actualizado correctamente"}, 200



# ============================================================
# 4) GET /items/filtrar?nombre=XYZ → FILTRO POR NOMBRE
# ============================================================
@app.get("/items/filtrar")
def filtrar_por_nombre():
    """
    Filtra documentos que coincidan con un nombre específico.

     LO QUE SE ENVÍA (por query param):
    /items/filtrar?nombre=Sensor1

    Si no se envía el parámetro, responde con error.

     EJEMPLO DE RETORNO:
    [
        {
            "_id": "675203c8fb55302eb2ac7811",
            "nombre": "Sensor1",
            "valor": 25.3,
            "activo": true
        }
    ]
    """

    nombre = request.args.get("nombre")  # Capturar argumento "nombre"

    if not nombre:
        return {"error": "Debes enviar el parámetro 'nombre'"}, 400

    # Buscar coincidencia exacta en el campo 'nombre'
    items = list(collection.find({"nombre": nombre}))

    # Convertir ObjectId → string
    for item in items:
        item["_id"] = str(item["_id"])

    return items, 200


# ============================================================
# 5) DELETE /items/nombre/<nombre>  → ELIMINAR POR NOMBRE
# ============================================================
@app.delete("/items/nombre/<nombre>")
def delete_by_nombre(nombre):
    """
    Elimina el documento que tenga el campo 'nombre' igual al especificado.

     EJEMPLO:
    DELETE /items/nombre/Sensor1

     RESPUESTA (éxito):
    {
        "message": "Documento 'Sensor1' eliminado correctamente"
    }

     RESPUESTA (si no existe):
    {
        "error": "No existe un documento con ese nombre"
    }
    """

    result = collection.delete_one({"nombre": nombre})

    if result.deleted_count == 0:
        return {"error": f"No existe un documento con nombre '{nombre}'"}, 404

    return {"message": f"Documento '{nombre}' eliminado correctamente"}, 200

# ============================================================
# EJECUCIÓN DEL SERVIDOR FLASK
# ============================================================
if __name__ == "__main__":
    # Modo debug permite ver cambios sin reiniciar y muestra errores detallados
    app.run(debug=True)
