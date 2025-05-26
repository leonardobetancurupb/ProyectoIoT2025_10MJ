import os
import json
from flask import Flask, request, jsonify
from collections import defaultdict

app = Flask(__name__)
last_values = defaultdict(dict)

# Asegurarnos de que exista la carpeta 'data'
if not os.path.isdir('data'):
    os.makedirs('data', exist_ok=True)


@app.route('/recibir', methods=['POST'])
def recibir():
    # 1) Leer el JSON entrante
    data_in = request.get_json(force=True)

    # 2) Construir la nueva estructura
    #    Asumimos que “h” viene con el valor de humedad
    sensor_id = data_in.get('id', 'unknown')
    raw_h = data_in.get('h', None)
    # Puedes ajustar aquí para leer otros sensores (p.ej. 't' para temperatura)
    # Fijamos el type a "moisture" para humedad de suelo
    transformed = {
        "id": sensor_id,
        "type": "moisture",
        "humedad_suelo": {
            "value": float(raw_h) if raw_h is not None else None,
            "type": "Float"
        }
    }

    # 3) Guardar en memoria
    last_values[sensor_id] = transformed

    # 4) Escribir/actualizar el archivo JSON en disco
    filepath = os.path.join('data', f"{sensor_id}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=2, ensure_ascii=False)

    # 5) Responder OK
    return jsonify(status="ok"), 200


if __name__ == '__main__':
    # Ejecutar en todas las interfaces, puerto 4491
    app.run(host='0.0.0.0', port=4491, debug=True)
