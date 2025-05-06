import os
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def ver_datos():
    ruta_archivo = 'data/agente_w_rs.json'

    try:
        if not os.path.exists(ruta_archivo):
            return "<h2>No se encontraron datos.</h2>"

        with open(ruta_archivo, 'r') as archivo_json:
            datos = json.load(archivo_json)

        # Si es un solo objeto, lo convertimos en lista para procesar igual
        if isinstance(datos, dict):
            datos = [datos]

        html = datos;
        return html

    except Exception as e:
        return f"<h3>Error al leer los datos: {e}</h3>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4450)

