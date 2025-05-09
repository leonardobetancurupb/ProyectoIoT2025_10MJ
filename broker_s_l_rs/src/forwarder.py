from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DESTINO_ORION = "http://10.38.32.137:4441/recibir"

@app.route("/forward", methods=["POST"])
def reenviar():
    data = request.json

    try:
        headers = {"Content-Type": "application/json"}
        response = requests.post(DESTINO_ORION, json=data, headers=headers)
        return jsonify({"status": response.status_code}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4441)
