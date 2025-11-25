from flask import Flask, request, jsonify

app = Flask(__name__)

# "Base de datos" temporal en memoria
sensores = []


@app.route("/")
def home():
    return jsonify({"mensaje": "API con CRUD básico funcionando"})


# ---------- GET /sensores ----------
@app.route("/sensores", methods=["GET"])
def obtener_sensores():
    return jsonify({"sensores": sensores})


# ---------- POST /sensores ----------
@app.route("/sensores", methods=["POST"])
def crear_sensor():
    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON no proporcionado"}), 400

    campos = ["tipo", "valor", "ubicacion", "fecha"]
    for c in campos:
        if c not in data:
            return jsonify({"error": f"Falta el campo: {c}"}), 400

    sensores.append(data)
    return jsonify({"mensaje": "Sensor creado", "sensor": data}), 201


# ---------- PUT /sensores/<int:index> ----------
# Actualiza el sensor según su posición en la lista
@app.route("/sensores/<int:index>", methods=["PUT"])
def actualizar_sensor(index):
    if index < 0 or index >= len(sensores):
        return jsonify({"error": "Sensor no encontrado"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON no proporcionado"}), 400

    sensores[index].update(data)

    return jsonify({
        "mensaje": "Sensor actualizado",
        "sensor": sensores[index]
    })


# ---------- DELETE /sensores/<int:index> ----------
@app.route("/sensores/<int:index>", methods=["DELETE"])
def eliminar_sensor(index):
    if index < 0 or index >= len(sensores):
        return jsonify({"error": "Sensor no encontrado"}), 404

    eliminado = sensores.pop(index)

    return jsonify({
        "mensaje": "Sensor eliminado",
        "sensor": eliminado
    })


# ---------- Ejecutar servidor ----------
# Este bloque se ejecuta solo si corremos este archivo directamente.
# debug=True permite recarga automática y muestra errores detallados.
if __name__ == "__main__":
    app.run(debug=True)
