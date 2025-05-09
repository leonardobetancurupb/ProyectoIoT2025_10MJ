from flask import Flask, jsonify, request
import serial
import json
import os
import threading
import time

SERIAL_PORT = "COM4"
BAUD_RATE = 115200
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DEFAULT_DATA_FILE = os.path.join(DATA_DIR, 'lectura.json')

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
                    linea = ser.readline().decode('utf-8').strip()
                    if linea:
                        print(f"Datos recibidos: {linea}")
                        try:
                            datos = json.loads(linea)
                            ultimo_dato = datos
                            guardar_en_archivo(datos)
                        except json.JSONDecodeError:
                            print("Advertencia: Datos recibidos no son JSON válido")
                time.sleep(0.5)
    except Exception as e:
        print(f"Error escuchando el serial: {e}")

# Función para guardar los datos JSON en un archivo
def guardar_en_archivo(datos):
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Simplemente guardar el JSON en el archivo lectura.json
    with open(DEFAULT_DATA_FILE, "w") as f:
        json.dump(datos, f, indent=2)

# Ruta HTTP para recibir datos del sensor ESP32 mediante POST
@app.route("/recibirdatos", methods=["POST"])
def recibir_datos():
    try:
        datos = request.json
        
        if datos:
            print(f"Datos recibidos vía HTTP: {datos}")
            global ultimo_dato
            ultimo_dato = datos
            
            # Guardar datos en el archivo
            guardar_en_archivo(datos)
            
            return jsonify({"status": "success", "message": "Datos recibidos correctamente"}), 200
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
