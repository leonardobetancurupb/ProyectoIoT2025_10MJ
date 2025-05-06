#Miembros:
#Sebastián Franco Cataño
#Antony Javier Sanchez Herrera

import os
import json
from flask import Flask, request, jsonify
 
app = Flask(__name__)
DATA_FOLDER = 'data'
os.makedirs(DATA_FOLDER, exist_ok=True)
 
@app.route('/recibir', methods=['POST'])
def recibir():
    try:
        data = request.get_json(force=True)
 
        if not data:
            return jsonify({'error': 'Se recibió un JSON vacío'}), 400
 
        # Validar que exista un campo 'id'
        if 'id' not in data:
            return jsonify({'error': 'El JSON debe contener un campo "id"'}), 400
 
        # Extraer y limpiar el ID
        raw_id = str(data['id'])
        clean_id = raw_id.replace('sensor_w_m_', '')
 
        # Crear el nombre de archivo correcto
        filename = f'sensor_w_m_{clean_id}.json'
        filepath = os.path.join(DATA_FOLDER, filename)
 
        # Guardar o sobrescribir el archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
 
        return jsonify({'mensaje': 'Datos guardados correctamente', 'archivo': filename}), 200
 
    except Exception as e:
        return jsonify({'error': f'Error al procesar o guardar los datos: {str(e)}'}), 500
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4461)