from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

sensores = []

#"Base de datos"
data_base_file = "sensores_db.json"

def cargar_sensores():
    if not os.path.exists(data_base_file):
        with open(data_base_file, "w") as f:
            json.dump([], f)
        return []
    with open(data_base_file, "r") as f:
        return json.load(f)
    
def guardar_datos(data):
    with open(data_base_file, "w") as f:
        json.dump(data, f, indent=4)
    

@app.route("/")
def home():
    return {"mensaje":"Hola, Mundo"}

@app.route("/sensores", methods=["GET"])
def obtener_sensores():
    return jsonify({"sensores": sensores})

@app.route("/sensores", methods=["POST"])
def agregar_sensor():
    data = request.get_json()

    campos_requeridos = ["id", "tipo", "ubicacion", "valor"]
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400
    
    sensores.append(data)

    return jsonify({"mensaje": "Sensor agregado exitosamente",
                     "sensor": data}), 201

@app.route("/sensores-persist/", methods=["GET"])
def obtener_sensores_persistentes():
    sensores_persistentes = cargar_sensores()
    return jsonify({"sensores": sensores_persistentes})

@app.route("/sensores-persist/", methods=["POST"])
def agregar_sensor_persistente():
    data = request.get_json()

    campos_requeridos = ["id", "tipo", "ubicacion", "valor"]
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400
    
    sensores_persistentes = cargar_sensores()
    sensores_persistentes.append(data)
    guardar_datos(sensores_persistentes)

    return jsonify({"mensaje": "Sensor agregado exitosamente",
                     "sensor": data}), 201


if __name__ == "__main__":
    app.run(debug=True)
