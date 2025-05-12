#include <Wire.h>
#include "Ai_AP3216_AmbientLightAndProximity.h"
#include <LoRa.h>
#include "LoRaBoards.h"
 
// Parámetros del dispositivo
#define DEVICE_ID "sensor_L_RS_001"
#define DEVICE_TYPE "L_RS"
#define CHIRP_SIZE 10
#define SEND_INTERVAL 10000  // ms
 
enum State {
  IDLE,
  CHIRP,
  PRUNNING,
  BUNDLING,
  TRANSMIT
};
 
Ai_AP3216_AmbientLightAndProximity aps = Ai_AP3216_AmbientLightAndProximity();
float measurements[CHIRP_SIZE];
int measurementIndex = 0;
State currentState = IDLE;
unsigned long lastStateChange = 0;
float averageLight = 0.0;
unsigned long lastSampleTime = 0;
String finalMessage;
 
float calculateAverage(float arr[], int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += arr[i];
  }
  return sum / size;
}
 
void setup() {
  Serial.begin(115200);
  delay(1000);
 
  Wire.begin();  // SDA 21, SCL 22
  aps.begin();
  aps.startAmbientLightAndProximitySensor();
  Serial.println("✅ Sensor CJMCU-3216 iniciado");
 
  LoRa.setPins(18, 14, 26);
  if (!LoRa.begin(915E6)) {
    Serial.println("❌ Error iniciando LoRa");
    while (true);
  }
 
  LoRa.setTxPower(20);
  LoRa.setSignalBandwidth(125000);
  LoRa.setSpreadingFactor(10);
  LoRa.setPreambleLength(16);
  LoRa.setSyncWord(0xAB);
  LoRa.disableCrc();
  LoRa.disableInvertIQ();
  LoRa.setCodingRate4(7);
 
  Serial.println("✅ LoRa Transmisor listo");
}
 
void loop() {
  switch (currentState) {
    case IDLE:
      if (millis() - lastStateChange >= SEND_INTERVAL) {
        currentState = CHIRP;
        measurementIndex = 0;
        lastSampleTime = millis();
        lastStateChange = millis();
        Serial.println("🔄 Estado: CHIRP");
      }
      break;
 
    case CHIRP:
      if (millis() - lastSampleTime >= 1000) {
        long alsValue = aps.getAmbientLight();
        if (alsValue >= 0) {
          measurements[measurementIndex++] = alsValue;
          Serial.printf("📊 Medida %d: %ld lx\n", measurementIndex, alsValue);
        } else {
          Serial.println("⚠️ Lectura inválida");
        }
 
        lastSampleTime = millis();
 
        if (measurementIndex >= CHIRP_SIZE) {
          currentState = PRUNNING;
          Serial.println("➡️ Estado: PRUNNING");
        }
      }
      break;
 
    case PRUNNING:
      averageLight = calculateAverage(measurements, CHIRP_SIZE);
      Serial.printf("📈 Promedio: %.2f lx\n", averageLight);
      currentState = BUNDLING;
      Serial.println("➡️ Estado: BUNDLING");
      break;
 
    case BUNDLING:
      finalMessage = "{'P':4481,'ip':'54.197.173.173','id':'" + String(DEVICE_ID) + "','rs':" + String(averageLight, 2) + "}";
      Serial.println("📦 Mensaje: " + finalMessage);
      currentState = TRANSMIT;
      break;
 
    case TRANSMIT:
      Serial.println("➡️ Estado: TRANSMIT");
      LoRa.idle();
      LoRa.beginPacket();
      LoRa.print(finalMessage);
      bool success = LoRa.endPacket();
 
      if (success) {
        Serial.println("📤 Enviado: " + finalMessage);
      } else {
        Serial.println("❌ Error al transmitir (endPacket() == false)");
      }
 
      currentState = IDLE;
      lastStateChange = millis();
      Serial.println("🔁 Estado: IDLE");
      break;
  }
}