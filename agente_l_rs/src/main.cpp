#include <Wire.h>
#include "Ai_AP3216_AmbientLightAndProximity.h"
#include <ArduinoJson.h>

// Definiciones
#define DEVICE_ID "DEVICE_001"  // Identificador del dispositivo
#define CHIRP_SIZE 10          // Número de medidas por chirp
#define SEND_INTERVAL 10000    // Enviar cada 10 segundos (en milisegundos)

// Estados de la máquina de estados
enum State {
  IDLE,
  CHIRP,
  PRUNNING,
  BUNDLING
};

// Variables globales
Ai_AP3216_AmbientLightAndProximity aps = Ai_AP3216_AmbientLightAndProximity();
float measurements[CHIRP_SIZE];  // Almacenar las medidas del chirp
int measurementIndex = 0;        // Índice para el chirp
State currentState = IDLE;       // Estado inicial
unsigned long lastStateChange = 0;
float averageLight = 0.0;        // Promedio de las medidas

// Función para calcular el promedio
float calculateAverage(float arr[], int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += arr[i];
  }
  return sum / size;
}

void createJsonPacket(); // Declaración de la función para crear el paquete JSON

void setup() {
  Serial.begin(115200);
  Wire.begin(); // SDA 21, SCL 22
  aps.begin();
  aps.startAmbientLightAndProximitySensor();
  Serial.println("Sensor CJMCU-3216 iniciado correctamente");
}

void loop() {
  switch (currentState) {
    case IDLE:
      // Esperar hasta que pase el intervalo de 10 segundos
      if (millis() - lastStateChange >= SEND_INTERVAL) {
        currentState = CHIRP;
        measurementIndex = 0;
        lastStateChange = millis();
        Serial.println("Estado: CHIRP - Iniciando toma de muestras");
      }
      break;

    case CHIRP:
      // Tomar una medida cada segundo
      if (millis() - lastStateChange >= 1000) {
        long alsValue = aps.getAmbientLight();
        if (alsValue < 0) {
          Serial.println("Error: Lectura de luz ambiental fallida");
        } else {
          measurements[measurementIndex] = alsValue;
          measurementIndex++;
          Serial.print("Medida ");
          Serial.print(measurementIndex);
          Serial.print(": ");
          Serial.print(alsValue);
          Serial.println(" lx");
        }
        lastStateChange = millis();

        // Si se completó el chirp, pasar a PRUNNING
        if (measurementIndex >= CHIRP_SIZE) {
          currentState = PRUNNING;
          Serial.println("Estado: PRUNNING - Calculando promedio");
        }
      }
      break;

    case PRUNNING:
      // Calcular el promedio de las medidas
      averageLight = calculateAverage(measurements, CHIRP_SIZE);
      Serial.print("Promedio de luz ambiental: ");
      Serial.print(averageLight);
      Serial.println(" lx");
      currentState = BUNDLING;
      Serial.println("Estado: BUNDLING - Generando paquete JSON");
      break;

    case BUNDLING:
      // Generar y mostrar el paquete JSON
      createJsonPacket();
      currentState = IDLE;
      Serial.println("Estado: IDLE - Proceso completado");
      lastStateChange = millis(); // Reiniciar el temporizador
      break;
  }
}

// Función para crear el paquete JSON
void createJsonPacket() {
  unsigned long timestamp = millis() / 1000;
  StaticJsonDocument<512> doc;
  doc["id"] = DEVICE_ID;
  doc["timestamp"] = timestamp;
  doc["averageLight"] = averageLight; // Incluir el promedio
  String packet;
  serializeJson(doc, packet);
  Serial.println("Paquete JSON creado: " + packet);
 
}