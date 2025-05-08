#Miembros:
#Sebastián Franco Cataño
#Antony Javier Sanchez Herrera

import os
from flask import Flask, render_template_string
 
# Inicializamos Flask con la carpeta "data" expuesta como estática
app = Flask(__name__, static_folder='/data', static_url_path='/data')
 
DATA_FOLDER = '/data'
os.makedirs(DATA_FOLDER, exist_ok=True)
 
# Uso de html para listar los datos en la dirección
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Listado de archivos sensor_w_m_</title>
</head>
<body>
    <h2>Archivos disponibles en la carpeta "data"</h2>
    {% if archivos %}
        <ul>
        {% for archivo in archivos %}
            <li>
                {{ archivo }}
                - <a href="/{{ archivo }}" target="_blank">Ver</a>
                - <a href="/data/{{ archivo }}" download>Descargar</a>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No hay archivos con la nomenclatura "sensor_w_m_".</p>
    {% endif %}
</body>
</html>
'''
 
# Ruta GET personalizada
@app.route('/', methods=['GET'])
def listar_archivos_sensor():
    archivos = [f for f in os.listdir(DATA_FOLDER)
                if f.startswith('sensor_W_MS_') and f.endswith('.json')]
    return render_template_string(HTML_TEMPLATE, archivos=archivos)
 
# Ruta para ver el contenido de un archivo
@app.route('/<nombre_archivo>', methods=['GET'])
def ver_archivo(nombre_archivo):
    try:
        with open(os.path.join(DATA_FOLDER, nombre_archivo), 'r', encoding='utf-8') as f:
            contenido = f.read()
        return f"<pre>{contenido}</pre>"
    except FileNotFoundError:
        return "Archivo no encontrado", 404
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4460)