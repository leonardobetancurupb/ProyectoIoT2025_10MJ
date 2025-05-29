from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_session import Session
from config import SECRET_KEY, SESSION_TYPE, SQLALCHEMY_DATABASE_URI, ORION_URL
from models import Base, Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = SESSION_TYPE

CORS(app, supports_credentials=True)
Session(app)

# Configura la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

#DECORADOR LOGIN REQUIRED
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'No autorizado, Inicie Sesión'})
        return f(*args, **kwargs)
    return decorated_function


#MANEJO DE REGISTRO DE USUAIRO INTERNAMENTE MEDIANTE PETICION HTTP
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if db_session.query(Usuario).filter_by(username=username).first():
        return jsonify({"mensaje": "Usuario ya existe"}), 400

    password_hash = generate_password_hash(password)
    nuevo_usuario = Usuario(username=username, password_hash=password_hash)
    db_session.add(nuevo_usuario)
    db_session.commit()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

#INICIO DE SESION
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    usuario = db_session.query(Usuario).filter_by(username=username).first()

    if usuario and check_password_hash(usuario.password_hash, password):
        session['usuario'] = usuario.username
        return jsonify({"mensaje": "Login exitoso", "usuario": usuario.username}), 200
    else:
        return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401

#CIERRE DE SESION
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return jsonify({"mensaje": "Sesión cerrada"}), 200

#CRUD A ORION CONTEXT BROKER

#LISTAR ENTIDADES EXISTENTES EN ORION CONTEXT BROKER
@app.route('/api/listar_sensores', methods = ['GET'])
#@login_required
def listar_sensores():
    try:
        response = requests.get(ORION_URL)
        response.raise_for_status()
        entities = response.json()
        return jsonify(entities)
    except requests.exceptions.RequestException as e:
        return jsonify({'error' : str(e)}), 500
    

#CREAR UNA ENTIDAD EN ORION CONTEXT BROKER
@app.route('/api/sensores', methods=['POST'])
#@login_required
def crear_sensor():
    data = request.get_json()

    # Validar que tenga los campos necesarios
    if not data or 'id' not in data or 'moisture' not in data:
        return jsonify({'error': 'Faltan campos requeridos (id, moisture).'}), 400

    # Si no se incluye type, lo forzamos por defecto
    if 'type' not in data:
        data['type'] = 'sensor_w_ms'

    # Si no se incluye el tipo del campo moisture, lo forzamos
    if 'type' not in data['moisture']:
        data['moisture']['type'] = 'float'

    # Petición a Orion Context Broker
    response = requests.post(
        ORION_URL,
        json=data,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'}
    )

    if response.status_code == 201:
        return jsonify({'message': f"Sensor {data['id']} creado exitosamente."}), 201
    else:
        return jsonify({'error': response.text or 'Error desconocido'}), response.status_code


#ELIMINAR UNA ENTIDAD DE ORION
@app.route('/api/eliminar_entidad/<entity_id>', methods = ['DELETE'])
#@login_required
def eliminar_entidad(entity_id):
    url = f"{ORION_URL}/{entity_id}"
    response = requests.delete(url)
    if response.status_code == 204:
        return jsonify({'message': 'Entidad eliminada exitosamente.'}), 200
    else:
        return jsonify({'error': response.text}), response.status_code

#DATA PARA ALIMENTAR EL DASHBOARD


#EJECUTAR APP
if __name__ == '__main__':
    app.run(debug=True)