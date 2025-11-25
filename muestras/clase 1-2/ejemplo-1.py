from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"mensaje": "API base funcionando"}

# Este bloque se ejecuta solo si este archivo se ejecuta directamente
# (por ejemplo, usando: python ejemplo.py).
# En ese caso, Flask inicia el servidor web.
# debug=True permite recarga automática y muestra errores detallados.
if __name__ == "__main__":
    app.run(debug=True)
