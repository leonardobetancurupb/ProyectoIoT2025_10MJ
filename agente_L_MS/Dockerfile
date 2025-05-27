FROM python:3.11-slim
WORKDIR /app

# Copia únicamente el app.py del agente
COPY app.py ./

RUN pip install --no-cache-dir flask
EXPOSE 4491

# Arranca el agente
CMD ["python", "app.py"]
