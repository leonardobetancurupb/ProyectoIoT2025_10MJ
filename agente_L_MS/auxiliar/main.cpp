#include <Arduino.h>
#include <LoRa.h>
#include "LoRaBoards.h"
#include <XPowersLib.h>
#include <ArduinoJson.h>

#ifndef CONFIG_RADIO_FREQ
#define CONFIG_RADIO_FREQ 915.0
#endif
#ifndef CONFIG_RADIO_OUTPUT_POWER
#define CONFIG_RADIO_OUTPUT_POWER 17
#endif
#ifndef CONFIG_RADIO_BW
#define CONFIG_RADIO_BW 125.0
#endif

#if !defined(USING_SX1276) && !defined(USING_SX1278)
#error "LoRa example is only allowed to run SX1276/78."
#endif

// Pines sensor
const int SOIL_ANALOG_PIN = 4;  // A0 → GPIO4
const int SOIL_DIGITAL_PIN = 0; // DO → GPIO0

// Datos transmisor
// #define MOISTURE_SENSOR_PIN 32 //Nueva linea
const char *sensorID = "sensor_L_M_002";
const char *ip_destino = "75.101.185.215";
const int puerto_destino = 4491;
const char *type = "Porcentaje humedad suelo";

// Calibración suelo
// const int DRY_CAL = 3700;
// const int WET_CAL = 1400;

// float readSoilPercentage()
// {
//   // Activa digital para dar referencia
//   digitalWrite(SOIL_DIGITAL_PIN, HIGH);
//   delay(100);
//   int raw = analogRead(SOIL_ANALOG_PIN);
//   raw = constrain(raw, WET_CAL, DRY_CAL);
//   digitalWrite(SOIL_DIGITAL_PIN, LOW);
//   return 100.0 * (DRY_CAL - raw) / (DRY_CAL - WET_CAL);
// }

void setup()
{
    pinMode(SOIL_DIGITAL_PIN, OUTPUT);
    pinMode(SOIL_ANALOG_PIN, INPUT);

    digitalWrite(SOIL_DIGITAL_PIN, LOW);
    Serial.begin(115200);
    // Importante: setupBoards(true) para ESP32 + SPI LoRa
    setupBoards(true);
    delay(1500);

#ifdef RADIO_TCXO_ENABLE
    pinMode(RADIO_TCXO_ENABLE, OUTPUT);
    digitalWrite(RADIO_TCXO_ENABLE, HIGH);
#endif

    Serial.println("LoRa Sender");

    // Inicializar LoRa
    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DIO0_PIN);
    if (!LoRa.begin(CONFIG_RADIO_FREQ * 1000000))
    {
        Serial.println("Starting LoRa failed!");
        while (1)
            ;
    }

    // Todas estas configuraciones deben ir **fuera** del if de fallo
    LoRa.setTxPower(CONFIG_RADIO_OUTPUT_POWER);
    LoRa.setSignalBandwidth(CONFIG_RADIO_BW * 1000);
    LoRa.setSpreadingFactor(10);
    LoRa.setPreambleLength(16);
    LoRa.setSyncWord(0xAB);
    LoRa.disableCrc();
    LoRa.disableInvertIQ();
    LoRa.setCodingRate4(7);
}

void loop()
{
    // 1) Lectura sensores
    // float moisture = readSoilPercentage();
    digitalWrite(0, HIGH);
    delay(500);
    int sensorValue = analogRead(4);
    delay(500);
    digitalWrite(0, LOW);
    // Print the sensor reading values
    Serial.print("Soil moisture sensor value: ");
    Serial.println(sensorValue);
    float lowlevel = 1800;
    float highlevel = 4096;
    float porcentaje = 100 - 100 * ((float(sensorValue) - lowlevel) / (highlevel - lowlevel));
    Serial.print("y el porcentaje es:");
    Serial.println(porcentaje);
    delay(4000);

    // JSON
    String postData = "";
    postData = String(
        "{"
        "\"p\":\"" +
        String(puerto_destino) + "\","
                                 "\"ip\":\"" +
        ip_destino + "\", "
                     "\"id\":\"" +
        sensorID + "\", "
                   "\"h\":\"" +
        String(porcentaje) + "\" "
                             "}");
    // // 2) Construye mensaje genérico
    // String mensaje = "id:" + String(sensorID) +
    //                  ",type" + String(type) +
    //                  ",value:" + String(porcentaje, 1) +
    //                  ",ip:" + String(ip_destino) +
    //                  ",p:" + String(puerto_destino);

    Serial.println("Enviando por LoRa: " + postData);

    // 3) Envío por LoRa
    LoRa.beginPacket();
    LoRa.print(postData);
    LoRa.endPacket();

    Serial.println("📡 Enviado");
    delay(30000); // envía cada 30 segundos
}
