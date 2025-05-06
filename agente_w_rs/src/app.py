import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/recibir", methods=["POST"])
def getData():
    ruta_directorio = "data"
    ruta_archivo = os.path.join(ruta_directorio, "agente_w_rs.json")
    nuevos_datos = request.get_json()

    try:
        os.makedirs(ruta_directorio, exist_ok=True)
        if os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'r') as archivo_json:
                datos_existentes = json.load(archivo_json)
        else:
            datos_existentes = []

        if not isinstance(datos_existentes, list):
            datos_existentes = [datos_existentes]

        datos_existentes.append(nuevos_datos)

        with open(ruta_archivo, 'w') as archivo_json:
            json.dump(datos_existentes, archivo_json, indent=3)

        return jsonify({"mensaje": "Ok", "data": nuevos_datos})

    except Exception as e:
        return jsonify({"mensaje": "Error", "error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4451)
