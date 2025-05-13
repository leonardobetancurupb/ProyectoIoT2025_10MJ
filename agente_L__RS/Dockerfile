FROM python:3.10-slim

# Establece el directorio de trabajo 
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crea carpeta de datos (si no existe)
RUN mkdir -p data

# Exponer el puerto que usará Flask (4481 para el agente)
EXPOSE 4481

# Ejecutar la aplicación Flask
CMD ["python", "app.py"]