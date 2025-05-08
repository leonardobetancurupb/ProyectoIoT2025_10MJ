from flask import Flask, jsonify, request
import serial  # Para la comunicación con el puerto serial
import json
import os  # Para manipular rutas y directorios
import threading  # Para ejecutar procesos en paralelo (hilos)
import time  # Para gestionar tiempos de espera

# Configuración de parámetros
SERIAL_PORT = "COM4"   # Puerto serial al que está conectado el dispositivo (cambiar según el sistema)
BAUD_RATE = 115200  # Velocidad de transmisión serial
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'lectura.json')  # Ruta donde se guarda el archivo de datos

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Variable global para almacenar el último dato recibido
ultimo_dato = {"status": "Esperando datos..."}

# Función que se ejecuta continuamente para leer datos desde el puerto serial
def escuchar_serial():
    global ultimo_dato
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Escuchando en {SERIAL_PORT} a {BAUD_RATE} baudios...")
            while True:
                if ser.in_waiting:
                    linea = ser.readline().decode('utf-8').strip()  # Leer línea y decodificar
                    if linea:
                        print(f"Datos recibidos: {linea}")
                        try:
                            datos = json.loads(linea)  # Intentar convertir la línea a JSON
                            ultimo_dato = datos  # Guardar como último dato
                            guardar_en_archivo(datos)  # Guardar en archivo
                        except json.JSONDecodeError:
                            print("Advertencia: Datos recibidos no son JSON válido")
                time.sleep(0.5)  # Esperar medio segundo antes de leer otra vez
    except Exception as e:
        print(f"Error escuchando el serial: {e}")

# Función para guardar los datos JSON en un archivo
def guardar_en_archivo(datos):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # Crear directorio si no existe
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f, indent=2)  # Guardar los datos con formato legible

# Ruta HTTP para recibir datos del sensor ESP32 mediante POST
@app.route("/recibirdatos", methods=["POST"])
def recibir_datos():
    try:
        datos = request.json  # Obtener los datos enviados por el cliente
        
        if datos:
            print(f"Datos recibidos vía HTTP: {datos}")
            global ultimo_dato
            ultimo_dato = datos  # Actualizar el último dato recibido
            
            # Obtener el ID del sensor desde los datos
            # Puede venir como 'sensor_id', 'id' o generarse basado en los datos
            sensor_id = None
            
            # Intentar diferentes claves para obtener el ID
            if 'sensor_id' in datos:
                sensor_id = datos['sensor_id']
            elif 'id' in datos:
                sensor_id = datos['id']
                # Si el ID ya tiene el prefijo, extraerlo
                if sensor_id.startswith('sensor_w_ht_'):
                    sensor_id = sensor_id[12:]
            
            # Si no se encuentra un ID, generar uno basado en timestamp
            if not sensor_id:
                import time
                sensor_id = f"{int(time.time())}"
                
            print(f"Usando sensor_id: {sensor_id}")
            
            # Crear directorio específico para el sensor
            sensor_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', f'sensor_w_ht_{sensor_id}')
            os.makedirs(sensor_data_dir, exist_ok=True)
            
            # Guardar los datos en el archivo del sensor correspondiente
            sensor_data_file = os.path.join(sensor_data_dir, 'lectura.json')
            with open(sensor_data_file, "w") as f:
                json.dump(datos, f, indent=2)
            
            # También guardar una copia en la ruta de compatibilidad antigua (legacy)
            legacy_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'sensor_w_ht')
            os.makedirs(legacy_dir, exist_ok=True)
            legacy_file = os.path.join(legacy_dir, 'lectura.json')
            with open(legacy_file, "w") as f:
                # Asegurarse de que el JSON guardado tenga el ID correcto
                datos_with_id = datos.copy()
                if 'sensor_id' not in datos_with_id:
                    datos_with_id['sensor_id'] = sensor_id
                json.dump(datos_with_id, f, indent=2)
                
            return jsonify({"status": "success", "message": f"Datos de sensor {sensor_id} recibidos correctamente"}), 200
        else:
            return jsonify({"status": "error", "message": "No se recibieron datos válidos"}), 400
    
    except Exception as e:
        print(f"Error al recibir datos: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Punto de entrada principal
if __name__ == "__main__":
    # Crear e iniciar un hilo para escuchar el puerto serial
    hilo_serial = threading.Thread(target=escuchar_serial, daemon=True)
    hilo_serial.start()
    
    # Iniciar el servidor Flask en el puerto 4441
    app.run(host="0.0.0.0", port=4441)
