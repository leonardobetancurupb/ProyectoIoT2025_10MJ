#Samuel Arroyave 000199426
#Pablo Peralta  000484263

import json
import time
import os
import glob
from flask import Flask, jsonify, request, render_template_string

# Base directory for sensor data
BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'agente_w_ht', 'data')

# Default data file path for backward compatibility
DEFAULT_DATA_FILE = os.path.join(BASE_DATA_DIR, 'sensor_w_ht', 'lectura.json')

# Initialize Flask application
app = Flask(__name__)

# Create a variable to store the latest data
latest_data = {}

def leer_datos(sensor_id='001'):
    """
    Read data from a sensor's data file based on the sensor ID.
    If the specific sensor file doesn't exist, falls back to the default file.
    """
    try:
        # Try to read from the specific sensor directory first
        sensor_file = os.path.join(BASE_DATA_DIR, f'sensor_w_ht_{sensor_id}', 'lectura.json')
        
        # If sensor-specific file doesn't exist, use the default file
        if not os.path.exists(sensor_file):
            sensor_file = DEFAULT_DATA_FILE
            print(f"Sensor file for {sensor_id} not found, using default: {DEFAULT_DATA_FILE}")
        
        with open(sensor_file, 'r') as f:
            raw_data = json.load(f)
            # Transform the data to match the required format
            formatted_data = {
                'id': f'sensor_w_ht_{sensor_id}',
                'type': 'sensor_w_ht',
                'humedad': {
                    'type': 'float',
                    'value': float(raw_data.get('humedad', 0))
                },
                'temperatura': {
                    'type': 'float',
                    'value': float(raw_data.get('temperatura', 0))
                }
            }
            return formatted_data
    except FileNotFoundError:
        print(f"Archivo no encontrado: {sensor_file}")
        return {
            'id': f'sensor_w_ht_{sensor_id}',
            'type': 'sensor_w_ht',
            'humedad': {'type': 'float', 'value': 0.0},
            'temperatura': {'type': 'float', 'value': 0.0}
        }
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON desde: {sensor_file}")
        return {
            'id': f'sensor_w_ht_{sensor_id}',
            'type': 'sensor_w_ht',
            'humedad': {'type': 'float', 'value': 0.0},
            'temperatura': {'type': 'float', 'value': 0.0}
        }

# Root route to display HTML with sensor data
@app.route('/', methods=['GET'])
def index():
    data = leer_datos()
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sensor W_HT Data</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            .data-container { background-color: #f5f5f5; border-radius: 5px; padding: 15px; margin-top: 20px; }
            pre { background-color: #e0e0e0; padding: 10px; border-radius: 3px; overflow-x: auto; }
        </style>
    </head>
    <body>
        <h1>Sensor W_HT Data</h1>
        <div class="data-container">
            <h2>Current Sensor Readings:</h2>
            <pre>{{ data_json }}</pre>
        </div>
    </body>
    </html>
    """
    # Use ensure_ascii=False to properly handle UTF-8 characters
    # Use single quotes for JSON output
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False).replace('"', "'")
    return render_template_string(html_template, data_json=formatted_json)

# Dynamic route to handle any sensor with the pattern sensor_w_ht_00X
@app.route('/sensor_w_ht_<sensor_id>', methods=['GET'])
def sensor_w_ht_dynamic(sensor_id):
    try:
        # For now, we're reading from a single data file
        # In a real scenario with multiple sensors, you'd have different data sources
        data = leer_datos(sensor_id)
        
        # Update the ID to match the requested sensor
        data['id'] = f'sensor_w_ht_{sensor_id}'
        
        response = jsonify(data)
        # Customize the JSON response to use single quotes
        response.data = response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return response
    except Exception as e:
        error_response = jsonify({"error": str(e)})
        error_response.data = error_response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return error_response, 500

# Keeping the original specific route for backward compatibility
@app.route('/sensor_w_ht_001', methods=['GET'])
def sensor_w_ht_001():
    return sensor_w_ht_dynamic('001')

# Create a data monitoring thread
def monitor_data():
    global latest_data
    print(f"Vigilando datos en: {DEFAULT_DATA_FILE}")
    last_data = {}
    while True:
        try:
            datos = leer_datos()
            if datos and datos != last_data:
                print(f"Nuevos datos recibidos: {datos}")
                latest_data = datos.copy()
                last_data = datos.copy()
            elif not datos:
                print("No hay datos para procesar o archivo no disponible")
        except Exception as e:
            print(f"Error al procesar datos: {e}")
        time.sleep(10)

if __name__ == "__main__":
    # Start the data monitoring in a separate thread
    import threading
    monitor_thread = threading.Thread(target=monitor_data, daemon=True)
    monitor_thread.start()
    
    # Start the Flask server
    print("Iniciando servidor Flask en puerto 4440...")
    app.run(host="0.0.0.0", port=4440)
