FROM python:3.11-slim
WORKDIR /app

# Copia únicamente el app.py del broker
COPY app.py ./

RUN pip install --no-cache-dir flask
EXPOSE 4490

# Arranca el broker
CMD ["python", "app.py"]