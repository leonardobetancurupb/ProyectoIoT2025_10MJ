#include <Wire.h>
#include "Ai_AP3216_AmbientLightAndProximity.h"

Ai_AP3216_AmbientLightAndProximity aps = Ai_AP3216_AmbientLightAndProximity();

void setup() {
  Serial.begin(115200);
  Wire.begin(); // SDA 21, SCL 22
  aps.begin(); // Removed the if-condition
  aps.startAmbientLightAndProximitySensor();
  Serial.println("Sensor CJMCU-3216 iniciado correctamente");
}

void loop() {
  long alsValue = aps.getAmbientLight();

  if (alsValue < 0) {
    Serial.println("Error: Lectura de luz ambiental fallida");
  } else {
    Serial.print("Luz Ambiental (lux): ");
    Serial.println(alsValue);
  }

  delay(1000);
}
