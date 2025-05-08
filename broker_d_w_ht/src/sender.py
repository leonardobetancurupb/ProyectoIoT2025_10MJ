# Samuel Arroyave 000199426
# Pablo Peralta  000484263

import json
import time
import os
import glob
from flask import Flask, jsonify, request, render_template_string

# Directorio base donde se encuentran los datos del sensor
BASE_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'agente_w_ht', 'data')

# Ruta por defecto del archivo de datos para compatibilidad hacia atrás
DEFAULT_DATA_FILE = os.path.join(BASE_DATA_DIR, 'sensor_w_ht', 'lectura.json')

# Inicializa la aplicación Flask
app = Flask(__name__)

# Variable global para almacenar los últimos datos
latest_data = {}

def leer_datos(sensor_id='001'):
    """
    Lee los datos del archivo de un sensor según el ID del sensor.
    Si no existe un archivo específico para el sensor, se utiliza el archivo por defecto.
    """
    try:
        # Intenta leer primero desde el directorio específico del sensor
        sensor_file = os.path.join(BASE_DATA_DIR, f'sensor_w_ht_{sensor_id}', 'lectura.json')
        
        # Si no existe el archivo específico, usa el archivo por defecto
        if not os.path.exists(sensor_file):
            sensor_file = DEFAULT_DATA_FILE
            print(f"Archivo del sensor {sensor_id} no encontrado, usando por defecto: {DEFAULT_DATA_FILE}")
        
        with open(sensor_file, 'r') as f:
            raw_data = json.load(f)
            
            # Extraer valores de temperatura y humedad
            # Intentar diferentes formatos posibles en el JSON
            temperatura = 0
            humedad = 0
            
            # Intentar obtener los valores de humedad y temperatura
            if 'temperatura' in raw_data:
                temperatura = raw_data['temperatura']
            elif 'temperature' in raw_data:
                temperatura = raw_data['temperature']
                
            if 'humedad' in raw_data:
                humedad = raw_data['humedad']
            elif 'humidity' in raw_data:
                humedad = raw_data['humidity']
            
            # Transforma los datos al formato requerido
            formatted_data = {
                'id': f'sensor_w_ht_{sensor_id}',
                'type': 'sensor_w_ht',
                'humedad': {
                    'type': 'float',
                    'value': float(humedad)
                },
                'temperatura': {
                    'type': 'float',
                    'value': float(temperatura)
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
    except Exception as e:
        print(f"Error inesperado al leer datos: {e}")
        return {
            'id': f'sensor_w_ht_{sensor_id}',
            'type': 'sensor_w_ht',
            'humedad': {'type': 'float', 'value': 0.0},
            'temperatura': {'type': 'float', 'value': 0.0}
        }

# Ruta raíz que muestra los datos del sensor en una página HTML
@app.route('/', methods=['GET'])
def index():
    data = leer_datos()
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
    # Only pass the sensor ID to the template
    return render_template_string(html_template, sensor_id=data['id'])

# Ruta dinámica que atiende cualquier sensor with el patrón sensor_w_ht_00X
@app.route('/sensor_w_ht_<sensor_id>', methods=['GET'])
def sensor_w_ht_dynamic(sensor_id):
    try:
        # Por ahora se lee desde un solo archivo de datos
        # En un caso real con múltiples sensores, se tendrían diferentes fuentes de datos
        data = leer_datos(sensor_id)
        
        # Actualiza el ID para que coincida con el sensor solicitado
        data['id'] = f'sensor_w_ht_{sensor_id}'
        
        response = jsonify(data)
        # Personaliza la respuesta JSON para usar comillas simples
        response.data = response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return response
    except Exception as e:
        error_response = jsonify({"error": str(e)})
        error_response.data = error_response.data.decode('utf-8').replace('"', "'").encode('utf-8')
        return error_response, 500

# Ruta específica mantenida para compatibilidad hacia atrás
@app.route('/sensor_w_ht_001', methods=['GET'])
def sensor_w_ht_001():
    return sensor_w_ht_dynamic('001')

# Función para vigilar los datos en segundo plano
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

# Add a new route to list available sensors
@app.route('/sensores', methods=['GET'])
def listar_sensores():
    """Lista todos los sensores disponibles en el sistema"""
    try:
        # Buscar todos los directorios de sensores
        sensor_dirs = glob.glob(os.path.join(BASE_DATA_DIR, 'sensor_w_ht_*'))
        
        # Extraer los IDs de los sensores de los nombres de directorios
        sensor_ids = [os.path.basename(d).replace('sensor_w_ht_', '') for d in sensor_dirs]
        
        # Crear una lista de sensores con sus datos básicos
        sensors_list = []
        for sensor_id in sensor_ids:
            data = leer_datos(sensor_id)
            sensors_list.append({
                'id': data['id'],
                'temperatura': data['temperatura']['value'],
                'humedad': data['humedad']['value']
            })
            
        return jsonify(sensors_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Inicia la vigilancia de datos en un hilo separado
    import threading
    monitor_thread = threading.Thread(target=monitor_data, daemon=True)
    monitor_thread.start()
    
    # Inicia el servidor Flask
    print("Iniciando servidor Flask en puerto 4440...")
    app.run(host="0.0.0.0", port=4440)
