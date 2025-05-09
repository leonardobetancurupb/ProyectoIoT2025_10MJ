# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Directorio donde guardar los datos
DATA_FOLDER = './data'
os.makedirs(DATA_FOLDER, exist_ok=True)

@app.route('/recibir', methods=['POST'])
def recibir_datos():
    try:
        # Suponemos que el payload LoRa ya está en formato JSON correcto
        data = request.get_json()

        data['type'] = "L_HyT"

        if 't' in data:
            data['temperatura'] = {"value": data.pop('t'),"type":"Float"}

        if 'h' in data:
            data['humedad'] = {"value": data.pop('h'),"type":"Float"}

        # Guardar el archivo
        filename = os.path.join(DATA_FOLDER, f"{data['id'].replace(':', '_')}.json")
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        return jsonify({"status": "success", "message": "Datos recibidos y guardados"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4471)
