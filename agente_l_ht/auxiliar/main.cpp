#include <LoRa.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "LoRaBoards.h"
#include <vector>
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

// -------- CONFIGURACIÓN WiFi Y AGENTE -----------
const char *ssid = "UPBWiFi";

// -------------------------------------------------
void conectarWiFi()
{
    Serial.print("Conectando a WiFi...");
    WiFi.begin(ssid);
    unsigned long start = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - start < 10000)
    {
        Serial.print(".");
        delay(500);
    }
    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("\nWiFi conectado");
        Serial.println("IP local: " + WiFi.localIP().toString());
    }
    else
    {
        Serial.println("\n⚠️ No se pudo conectar a WiFi");
    }
}

String obtenerTimestampISO()
{
    time_t now = time(nullptr);
    struct tm *timeinfo = localtime(&now);
    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%dT%H:%M:%S", timeinfo);
    return String(buffer);
}

String extractValue(String json, String key) {
  int start = json.indexOf("\"" + key + "\":\"");
  if (start == -1) return "";
  start += key.length() + 4;
  int end = json.indexOf("\"", start);
  return json.substring(start, end);
}

void enviarJSONAlAgente(String recv)
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("WiFi desconectado. Reintentando...");
        conectarWiFi();
        if (WiFi.status() != WL_CONNECTED)
            return;
    }

      // Crear un objeto JSON
    String port = extractValue(recv, "p");
    String ip = extractValue(recv, "ip");
    String id = extractValue(recv, "id");
    String url = "http://" + ip + ":" + port + "/recibir"; 

    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    String mensaje = "";

    if(port == "4471"){

        String t = extractValue(recv, "t");
        String h = extractValue(recv, "h");

        mensaje = "{" 
            "\"id\":\"" + String(id) + "\", "
            "\"t\":" + String(t)  + ", "
            "\"h\":" + String(h)  +
        "}";

    }else if(port == "6491"){

        String h = extractValue(recv, "h");

        mensaje = "{"
            "\"id\":\"" + String(id) + "\", "
            "\"h\":" + String(h)  +
        "}";

    }

    Serial.println(mensaje);
    int httpCode = http.POST(mensaje);

    if (httpCode > 0)
    {
        Serial.printf("✅ Enviado al agente. HTTP: %d\n", httpCode);
        Serial.println("📨 Respuesta: " + http.getString());

    }
    else
    {
        Serial.printf("❌ Error HTTP: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
}

void setup()
{
    setupBoards(true);
    delay(1500);
    Serial.begin(115200);

    Serial.println("🌐 Receptor LoRa + HTTP JSON");

#ifdef RADIO_TCXO_ENABLE
    pinMode(RADIO_TCXO_ENABLE, OUTPUT);
    digitalWrite(RADIO_TCXO_ENABLE, HIGH);
#endif

    conectarWiFi();

    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DIO0_PIN);
    if (!LoRa.begin(CONFIG_RADIO_FREQ * 1000000))
    {
        Serial.println("❌ Falló LoRa");
        while (true)
            ;
    }

    LoRa.setTxPower(CONFIG_RADIO_OUTPUT_POWER);
    LoRa.setSignalBandwidth(CONFIG_RADIO_BW * 1000);
    LoRa.setSpreadingFactor(10);
    LoRa.setPreambleLength(16);
    LoRa.setSyncWord(0xAB);
    LoRa.disableCrc();
    LoRa.disableInvertIQ();
    LoRa.setCodingRate4(7);
    LoRa.receive();

    configTime(0, 0, "pool.ntp.org"); // Sin zona horaria, hora UTC
}

void loop()
{
    int packetSize = LoRa.parsePacket();
    if (packetSize)
    {
        String recv = "";
        String recvp = "";
        while (LoRa.available())
        {
            recv += (char)LoRa.read();
        }

        Serial.println("📥 Recibido por LoRa: " + recv);
        recvp = recv;
        Serial.println("🚀 Enviando a agente...");
        enviarJSONAlAgente(String(recvp));
    }
}
