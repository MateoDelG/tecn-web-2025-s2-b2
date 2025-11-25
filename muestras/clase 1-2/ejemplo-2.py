from flask import Flask, request, jsonify

app = Flask(__name__)

# "Base de datos" temporal en memoria (solo para pruebas)
sensores = []

@app.route("/")
def home():
    return jsonify({"mensaje": "API de sensores funcionando ✔️"})


# ---------- GET /sensores ----------
# Devuelve todos los sensores almacenados en la lista
@app.route("/sensores", methods=["GET"])
def obtener_sensores():
    return jsonify({"sensores": sensores})


# ---------- POST /sensores ----------
# Recibe un JSON con los datos del sensor y lo agrega a la lista
@app.route("/sensores", methods=["POST"])
def crear_sensor():
    data = request.get_json()  # Leer JSON del body de la petición

    # Ejemplo de estructura esperada:
    # {
    #   "tipo": "temperatura",
    #   "valor": 23.5,
    #   "ubicacion": "Zona A",
    #   "fecha": "2025-11-26"
    # }

    if not data:
        return jsonify({"error": "JSON no proporcionado"}), 400

    # Validación muy básica (solo verificar campos presentes)
    campos_obligatorios = ["tipo", "valor", "ubicacion", "fecha"]
    for campo in campos_obligatorios:
        if campo not in data:
            return jsonify({"error": f"Falta el campo obligatorio: {campo}"}), 400

    # Agregar a la "BD" en memoria
    sensores.append(data)

    return jsonify({
        "mensaje": "Sensor creado correctamente",
        "sensor": data
    }), 201


if __name__ == "__main__":
    app.run(debug=True)
