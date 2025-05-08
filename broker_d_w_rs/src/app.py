import os
from flask import Flask, jsonify, Response
import json
import os

app = Flask(__name__)
carpeta = '/data/'
archivos = os.listdir(carpeta)

@app.route("/", methods=["GET"])
def ver_datos():
    try:
        if not os.path.exists(carpeta):
            return Response("<h1>No se encontraron datos.</h1>", mimetype="text/html"), 404

        archivos = os.listdir(carpeta)
        archivos_json = [archivo for archivo in archivos if archivo.endswith('.json') and "W_RS" in archivo]

        if not archivos_json:
            return Response("<h1>No se encontraron archivos JSON con 'W_RS'.</h1>", mimetype="text/html")

        # Construir el HTML manualmente
        html = "<h1>Archivos JSON encontrados:</h1><ul>"
        for archivo in archivos_json:
            html += f"<li>{archivo}</li>"
        html += "</ul>"

        return Response(html, mimetype="text/html")
    
    except Exception as e:
        return Response(f"<h1>Error al leer los datos:</h1><p>{str(e)}</p>", mimetype="text/html"), 500

    
@app.route("/<string:idSensor>", methods = ["GET"])
def getSensorData(idSensor):

    nombre_archivo = idSensor + ".json"
    archivo = [archivo for archivo in archivos if nombre_archivo in archivo]

    try:
        if archivo:

            ruta_archivo = 'data/' + nombre_archivo
            with open(ruta_archivo, 'r') as archivo_json:
                    datos = json.load(archivo_json)

            if isinstance(datos, dict):
                datos = [datos]

            return jsonify(datos)
        else:
            return jsonify({"error": f"El sensor no existe"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al leer los datos: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4450)

