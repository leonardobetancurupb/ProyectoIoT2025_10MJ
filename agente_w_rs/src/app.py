import flask
from flask import Flask, request, jsonify
import json


## App de Flask

app = Flask(__name__)

@app.route("/recibir", methods=["POST"])
def getData():
    
    try:
        data = request.get_json()
        
        with open('/data/agente_w_rs.json', 'w') as archivo_json:
            json.dump(data, archivo_json, indent=3)
        
        return jsonify({"mensaje": "Ok", "data": data})
    
    except Exception as e:
        return jsonify({"mensaje": "Error", "error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4451)