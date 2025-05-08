#include <Arduino.h>
#include <ClosedCube_HDC1080.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

// WiFi 
const char* ssid = "UPBWiFi";
const char* password = ""; 

// Server settings
const char* serverAddress = "http://10.8.158.153:4441//recibirdatos";
// Variables globales
String dataframe = "";
ClosedCube_HDC1080 sensor;
int n = 0;
float tempArray[10] = {0};   // Arreglo para almacenar temperaturas
float humArray[10] = {0};    // Arreglo para almacenar humedades
float tmean = 0;
float hmean = 0;
char estado;

// --- Funciones auxiliares
float mean(float arr[], int size) {
  float sum = 0;
  for (int i = 0; i < size; i++) {
    sum += arr[i];
  }
  return sum / size;
}

// Función para enviar datos via HTTP POST
void sendDataToServer(String jsonData) {
  WiFiClient client;
  HTTPClient http;
  
  Serial.println("Enviando datos al servidor...");
  Serial.println(jsonData);
  
  http.begin(client, serverAddress);
  http.addHeader("Content-Type", "application/json");
  
  int httpResponseCode = http.POST(jsonData);
  
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    String payload = http.getString();
    Serial.println("Response: " + payload);
  } else {
    Serial.print("Error en HTTP request. Código: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  sensor.begin(0x40);  // Inicializar sensor en la dirección por defecto
  
  // Conectar a WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado a WiFi, IP: ");
  Serial.println(WiFi.localIP());
  
  Serial.println("Sistema iniciado correctamente");
  estado = 'A';
}

void loop() {
  if (estado == 'A') {
    Serial.println("Estado A: Lecturas");

    for (n = 0; n < 10; n++) {
      delay(10000);  // Espera de 10 segundos entre mediciones

      float temp = sensor.readTemperature();
      float hum = sensor.readHumidity();

      // Prunning básico
      if ((temp >= -10 && temp <= 85) && (hum >= 0 && hum <= 100)) {
        tempArray[n] = temp;
        humArray[n] = hum;
        Serial.print("Lectura ");
        Serial.print(n + 1);
        Serial.print(": Temp = ");
        Serial.print(temp);
        Serial.print(" °C | Humedad = ");
        Serial.print(hum);
        Serial.println(" %");
      } else {
        Serial.println("Lectura inválida descartada (prunning)");
        n--;  // No contar esta medición
      }
    }
    estado = 'B';
  }

  else if (estado == 'B') {
    Serial.println("Estado B: Promediando lecturas");

    tmean = mean(tempArray, 10);
    hmean = mean(humArray, 10);

    Serial.print("Temperatura Promedio: ");
    Serial.println(tmean);
    Serial.print("Humedad Promedio: ");
    Serial.println(hmean);

    delay(1000);  // Pequeño retardo antes de construir JSON
    estado = 'C';
  }

  else if (estado == 'C') {
    Serial.println("Estado C: Creando Dataframe JSON");

    // Crear el JSON dataframe
    dataframe = "{\"id\":\"Sensor1791\",";
    dataframe += "\"temperatura\":" + String(tmean, 2) + ",";
    dataframe += "\"humedad\":" + String(hmean, 2) + "}";

    Serial.println("Dataframe JSON generado:");
    Serial.println(dataframe);
    
    // Verificar conexión WiFi antes de enviar
    if (WiFi.status() == WL_CONNECTED) {
      sendDataToServer(dataframe);
    } else {
      Serial.println("Error: WiFi desconectado. Reconectando...");
      WiFi.reconnect();
    }

    estado = 'D';
  }

  else if (estado == 'D') {
    Serial.println("Estado D: Esperando 50 segundos antes de reiniciar mediciones");
    delay(50000);  // 50 segundos de espera
    estado = 'A';  // Reiniciar ciclo
  }
}