#Samuel Arroyave 000199426
#Pablo Peralta  000484263


import json
import time
import os
from flask import Flask, jsonify, request, render_template_string

# Update the data file path to point to the new location
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'agente_w_ht', 'data', 'sensor_w_ht', 'lectura.json')

# Initialize Flask application
app = Flask(__name__)

# Create a variable to store the latest data
latest_data = {}

def leer_datos():
    try:
        with open(DATA_FILE, 'r') as f:
            raw_data = json.load(f)
            # Transform the data to match the required format
            formatted_data = {
                'id': 'sensor_w_ht_001',
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
        print(f"Archivo no encontrado: {DATA_FILE}")
        return {
            'id': 'sensor_w_ht_001',
            'type': 'sensor_w_ht',
            'humedad': {'type': 'float', 'value': 0.0},
            'temperatura': {'type': 'float', 'value': 0.0}
        }
    except json.JSONDecodeError:
        print(f"Error al decodificar JSON desde: {DATA_FILE}")
        return {
            'id': 'sensor_w_ht_001',
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

# Route to get the current data - renamed from get_data to sensor_w_ht_00x
@app.route('/sensor_w_ht_001', methods=['GET'])
def sensor_w_ht_00x():
    try:
        data = leer_datos()
        response = jsonify(data)
        # Customize the JSON response to use single quotes
        response.data = response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return response
    except Exception as e:
        error_response = jsonify({"error": str(e)})
        error_response.data = error_response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return error_response, 500

# Create a data monitoring thread
def monitor_data():
    global latest_data
    print(f"Vigilando datos en: {DATA_FILE}")
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
