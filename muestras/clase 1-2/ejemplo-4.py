from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "sensores.json"


# ---------- Funciones auxiliares ----------

def cargar_datos():
    """Lee el archivo JSON y devuelve la lista de sensores."""
    if not os.path.exists(DATA_FILE):
        # Si el archivo no existe, crearlo vacío
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []

    with open(DATA_FILE, "r") as f:
        return json.load(f)


def guardar_datos(data):
    """Guarda la lista de sensores en el archivo JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- Rutas de la API ----------

@app.route("/")
def home():
    return jsonify({"mensaje": "API con persistencia en archivo JSON ✔️"})


# --- GET ---
@app.route("/sensores", methods=["GET"])
def obtener_sensores():
    datos = cargar_datos()
    return jsonify({"sensores": datos})


# --- POST ---
@app.route("/sensores", methods=["POST"])
def crear_sensor():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibió JSON"}), 400

    campos = ["tipo", "valor", "ubicacion", "fecha"]
    for c in campos:
        if c not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {c}"}), 400

    sensores = cargar_datos()
    sensores.append(data)
    guardar_datos(sensores)

    return jsonify({
        "mensaje": "Sensor creado",
        "sensor": data
    }), 201


# --- PUT ---
@app.route("/sensores/<int:index>", methods=["PUT"])
def actualizar_sensor(index):
    sensores = cargar_datos()

    if index < 0 or index >= len(sensores):
        return jsonify({"error": "Sensor no encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No se recibió JSON"}), 400

    sensores[index].update(data)
    guardar_datos(sensores)

    return jsonify({
        "mensaje": "Sensor actualizado",
        "sensor": sensores[index]
    })


# --- DELETE ---
@app.route("/sensores/<int:index>", methods=["DELETE"])
def eliminar_sensor(index):
    sensores = cargar_datos()

    if index < 0 or index >= len(sensores):
        return jsonify({"error": "Sensor no encontrado"}), 404

    eliminado = sensores.pop(index)
    guardar_datos(sensores)

    return jsonify({
        "mensaje": "Sensor eliminado",
        "sensor": eliminado
    })


# --- Ejecutar servidor ---
# Se ejecuta solo cuando el archivo se ejecuta directamente
if __name__ == "__main__":
    app.run(debug=True)
