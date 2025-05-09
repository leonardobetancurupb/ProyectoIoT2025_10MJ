# Samuel Arroyave 000199426
# Pablo Peralta  000484263

import json
import os
from flask import Flask, jsonify, request, render_template_string

# Directorio base donde se encuentra el archivo de datos
BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'agente_w_ht', 'data')
DATA_FILE = os.path.join(BASE_DATA_DIR, 'lectura.json')

# Inicializa la aplicación Flask
app = Flask(__name__)

def leer_datos():
    """Lee los datos del archivo lectura.json"""
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al leer datos: {e}")
        return {"id": "Sin datos", "temperatura": 0, "humedad": 0}

# Ruta raíz que muestra los datos del sensor en una página HTML
@app.route('/', methods=['GET'])
def index():
    # Obtener los datos del sensor
    data = leer_datos()
    sensor_id = data.get('id', 'Sin datos')
    
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Datos del Sensor W_HT</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .sensor-id { font-size: 24px; font-weight: bold; color: #0066cc; }
            .data-container { background-color: #f5f5f5; border-radius: 5px; padding: 15px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>Datos del Sensor W_HT</h1>
        <div class="data-container">
            <h2>Sensor ID:</h2>
            <div class="sensor-id">{{ sensor_id }}</div>
        </div>
    </body>
    </html>
    """
    # Solo pasar el ID del sensor a la plantilla
    return render_template_string(html_template, sensor_id=sensor_id)

# Ruta dinámica que atiende cualquier sensor con el patrón sensor_w_ht_{id}
@app.route('/sensor_w_ht_<sensor_id>', methods=['GET'])
def sensor_w_ht_dynamic(sensor_id):
    try:
        # Leer los datos del archivo
        data = leer_datos()
        
        # Formatear los datos para la respuesta
        formatted_data = {
            'id': f'sensor_w_ht_{sensor_id}',
            'type': 'sensor_w_ht',
            'humedad': {
                'type': 'float',
                'value': float(data.get('humedad', 0))
            },
            'temperatura': {
                'type': 'float',
                'value': float(data.get('temperatura', 0))
            }
        }
        
        response = jsonify(formatted_data)
        # Personaliza la respuesta JSON para usar comillas simples
        response.data = response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return response
    except Exception as e:
        error_response = jsonify({"error": str(e)})
        error_response.data = error_response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return error_response, 500

if __name__ == "__main__":
    # Inicia el servidor Flask
    print("Iniciando servidor Flask en puerto 4440...")
    app.run(host="0.0.0.0", port=4440)

