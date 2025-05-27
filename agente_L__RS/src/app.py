import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
DATA_DIR = 'data'
FILENAME = os.path.join(DATA_DIR, 'sensor_L_RS_001.json')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

@app.route('/recibirdatos', methods=['POST'])
def recibir_datos():
    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({'error': 'Formato de datos inválido'}), 400

    #Validaciones de datos recibidos
    if 'id' not in data:
        data['id'] = 'sensor_L_RS_001'
    if 'rs' not in data:
        return jsonify({'error': 'Falta el valor de radiación (rs)'}), 400

    try:
        data['rs'] = float(data.get('rs', 0))  # fuerza a float
    except ValueError:
        return jsonify({'error': 'rs debe ser numérico'}), 400

    # Guardar el archivo en data
    with open(FILENAME, 'w') as f:
        json.dump(data, f)

    return jsonify({'status': 'dato guardado', 'data': data}), 200

if __name__ == '__main__':
    ensure_data_dir()
    app.run(host='0.0.0.0', port=4481)