#Miembros:
#Sebastián Franco Cataño
#Antony Javier Sanchez Herrera

import os
import json
import re
import time
import requests

DATA_FOLDER = '/data'
ID_PATTERN = re.compile(r'^sensor_W_MS_\d+$')
CONTEXT_BROKER_URL = 'http://10.38.32.137:5026/v2/entities'
INTERVALO_SEGUNDOS = 10  # Intervalo para revisar la carpeta

def procesar_archivos():
    archivos = [f for f in os.listdir(DATA_FOLDER)
                if f.startswith("sensor_W_MS_") and f.endswith(".json")]

    for archivo in archivos:
        ruta = os.path.join(DATA_FOLDER, archivo)
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)

            entity_id = data.get("id", "")
            if not ID_PATTERN.match(entity_id):
                print(f"[IGNORADO] {archivo} tiene ID no válido: {entity_id}")
                continue

            # Verificar si la entidad existe en el Context Broker
            url_check = f"{CONTEXT_BROKER_URL}/{entity_id}"
            response_check = requests.get(url_check)

            if response_check.status_code == 200:
                # Extraer solo los atributos para el PATCH (sin id ni type)
                atributos = {k: v for k, v in data.items() if k not in ['id', 'type']}

                if not atributos:
                    print(f"[SKIP] {archivo} no contiene atributos para actualizar")
                    continue

                patch_url = f"{CONTEXT_BROKER_URL}/{entity_id}/attrs"
                headers = {'Content-Type': 'application/json'}

                patch_response = requests.patch(patch_url, json=atributos, headers=headers)

                if patch_response.status_code in [204, 200]:
                    print(f"[PATCH] {archivo} actualizado correctamente. Status: {patch_response.status_code}")
                else:
                    print(f"[ERROR PATCH] {archivo}. Status: {patch_response.status_code}, Respuesta: {patch_response.text}")

            elif response_check.status_code == 404:
                print(f"[NO EXISTE] {archivo}: entidad {entity_id} no existe en el broker")

            else:
                print(f"[ERROR CHECK] {archivo}. Status: {response_check.status_code}, Respuesta: {response_check.text}")

        except Exception as e:
            print(f"[ERROR] Procesando {archivo}: {e}")

def run_broker_loop():
    print("Broker de seguridad iniciado. Monitoreando carpeta...")
    while True:
        procesar_archivos()
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == '__main__':
    run_broker_loop()