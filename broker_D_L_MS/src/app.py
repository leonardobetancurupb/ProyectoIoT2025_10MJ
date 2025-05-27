import os
import json
from flask import Flask, jsonify, abort, render_template_string

app = Flask(__name__)
DATA_DIR = 'data'  # Directorio donde están los archivos JSON


def get_sensors():
    try:
        files = os.listdir(DATA_DIR)
        return [os.path.splitext(f)[0] for f in files if f.endswith('.json')]
    except FileNotFoundError:
        return []


def load_sensor_data(sensor_id):
    filepath = os.path.join(DATA_DIR, f'{sensor_id}.json')
    if not os.path.isfile(filepath):
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/', methods=['GET'])
def index():
    sensores = get_sensors()
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Listado de Sensores</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Listado de Sensores</h1>
        <ul>
            {% for sensor in sensores %}
                <li><a href="/{{ sensor }}">{{ sensor }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html, sensores=sensores)


@app.route('/<sensor_id>', methods=['GET'])
def ver_sensor(sensor_id):
    data = load_sensor_data(sensor_id)
    if not data:
        abort(404, description="Sensor no encontrado")

    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4490, debug=True)
