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
  SAMPLING
};

// Variables globales
Ai_AP3216_AmbientLightAndProximity aps = Ai_AP3216_AmbientLightAndProximity();
float measurements[CHIRP_SIZE];  // Almacenar las medidas del chirp
int measurementIndex = 0;        // Índice para el chirp
State currentState = IDLE;       // Estado inicial
unsigned long lastStateChange = 0;

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
        currentState = SAMPLING;
        measurementIndex = 0;
        lastStateChange = millis();
        Serial.println("Estado: SAMPLING - Iniciando toma de muestras");
      }
      break;

    case SAMPLING:
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

        // Si se completó el chirp, generar JSON y volver a IDLE
        if (measurementIndex >= CHIRP_SIZE) {
          createJsonPacket();
          currentState = IDLE;
          Serial.println("Estado: IDLE - Muestreo completado");
        }
      }
      break;
  }
}

// Función para crear el paquete JSON
void createJsonPacket() {
  unsigned long timestamp = millis() / 1000;
  StaticJsonDocument<512> doc;
  doc["id"] = DEVICE_ID;
  doc["timestamp"] = timestamp;
  JsonArray measurementsArray = doc.createNestedArray("measurements");
  for (int i = 0; i < CHIRP_SIZE; i++) {
    measurementsArray.add(measurements[i]);
  }
  String packet;
  serializeJson(doc, packet);
  Serial.println("Paquete JSON creado: " + packet);
}