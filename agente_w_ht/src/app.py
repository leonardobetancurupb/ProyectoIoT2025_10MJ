from flask import Flask, jsonify
import serial
import json
import os
import threading
import time

# Configuración
SERIAL_PORT = "COM4"   # Cambia a tu puerto real (ej: /dev/ttyUSB0 en Linux)
BAUD_RATE = 115200
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'lectura.json')

# Inicializar Flask
app = Flask(__name__)

# Variable para guardar el último dato leído
ultimo_dato = {"status": "Esperando datos..."}

# Función para escuchar el Serial continuamente
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

# Función para guardar el JSON en un archivo
def guardar_en_archivo(datos):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(datos, f, indent=2)

# Ruta de la API para consultar el último dato recibido
@app.route("/lectura", methods=["GET"])
def obtener_lectura():
    return jsonify(ultimo_dato)

# Iniciar la escucha del Serial en un hilo separado
if __name__ == "__main__":
    hilo_serial = threading.Thread(target=escuchar_serial, daemon=True)
    hilo_serial.start()
    app.run(host="0.0.0.0", port=4441)
