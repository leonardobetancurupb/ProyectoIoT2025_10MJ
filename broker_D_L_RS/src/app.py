import os
import json
from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)
DATA_DIR = 'data'

@app.route('/', methods=['GET'])
def lista_sensores():
    sensores = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    if not sensores:
        return "<h2>No hay sensores disponibles.</h2>"

    # HTML con hipervínculos a cada sensor
    html = "<h2>Sensores disponibles:</h2><ul>"
    for sensor in sensores:
        nombre = sensor.replace('.json', '')  # Ej: sensor_l_rs_001
        html += f'<li><a href="/{nombre}">{nombre}</a></li>'
    html += "</ul>"

    return html

@app.route('/sensor_l_rs_001', methods=['GET'])
def sensor_001():
    try:
        with open(os.path.join(DATA_DIR, 'sensor_l_rs_001.json'), 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {'error': 'Archivo no encontrado'}, 404

@app.route('/sensor_l_rs_00<int:n>.json', methods=['GET'])
def sensor_personalizado(n):
    filename = f"sensor_l_rs_00{n}.json"
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return {'error': f'{filename} no encontrado'}, 404
    return send_from_directory(DATA_DIR, filename)

# Esta ruta dinámica permite que los links en la página funcionen
@app.route('/<sensor_id>', methods=['GET'])
def ver_sensor(sensor_id):
    filename = f"{sensor_id}.json"
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return f"<h3>El sensor <code>{sensor_id}</code> no existe.</h3>", 404

    with open(path, 'r') as f:
        data = json.load(f)

    # Mostrar contenido como HTML
    html = f"<h2>Datos del sensor <code>{sensor_id}</code></h2><pre>{json.dumps(data, indent=2)}</pre>"
    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4480)