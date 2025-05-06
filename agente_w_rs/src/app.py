import os
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/recibir", methods=["POST"])
def getData():
    ruta_directorio = "data"
    ruta_archivo = os.path.join(ruta_directorio, "agente_w_rs.json")

    try:
        # Asegurar que el directorio exista
        os.makedirs(ruta_directorio, exist_ok=True)
        data = request.get_json()

        nuevos_datos = {
            'id': data['id'],
            'type': data['type'],
            'radiacion': {
                'type': 'float',
                'value': data['radiacion']
            }
        }

        with open(ruta_archivo, 'w') as archivo_json:
            json.dump(nuevos_datos, archivo_json, indent=3)

        return jsonify({"mensaje": "Ok", "data": nuevos_datos})

    except Exception as e:
        return jsonify({"mensaje": "Error", "error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4451)

