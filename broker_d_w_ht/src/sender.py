import requests
import json
import time
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'lectura.json')
BROKER_SEGURIDAD_URL = "http://broker_s_l_rs:4441/forward"

def leer_datos():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    while True:
        try:
            datos = leer_datos()
            response = requests.post(BROKER_SEGURIDAD_URL, json=datos)
            print("Enviado al broker de seguridad:", response.status_code)
        except Exception as e:
            print("Error al enviar:", e)
        time.sleep(10)
