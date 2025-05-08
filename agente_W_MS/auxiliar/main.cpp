//Miembros
//Sebastián Franco Cataño
//Antony Javier Sanchez Herrera

#include <ESP8266WiFi.h>
#include <numeric>

const int moisturePinPower = 16;  //Entrada Digital
const int analogPin = A0;        //Entrada Analogica

//Información de red
const char* ssid = "UPBWiFi";
const char* psw = "";
const char* serverIP = "10.38.32.137";
const int serverPort = 4461;

//Información del sensor
const char* id = "sensor_W_MS_001";
const char* typeSensor = "sensor_W_MS";

WiFiClient client;

float arr[5];
int n=0;

void setup() {
  Serial.begin(115200);

  pinMode(moisturePinPower, OUTPUT);
  digitalWrite(moisturePinPower, LOW);  // Asegura que está apagado inicialmente

  WiFi.begin(ssid, psw);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
}

//Media de los datos de un arreglo
float mean(const float arr[], int size) {
  return std::accumulate(arr, arr + size, 0.0) / size;
}

float readSensor() {
  int arrSize = sizeof(arr)/sizeof(arr[0]);
  float moistureMean;

  //Enciende
  digitalWrite(moisturePinPower, HIGH);

  for (n = 0; n < arrSize; n++){
    delay(10);  //Deja un espacio para que el sensor pueda mandar información
    
    //Lee información del sensor
    arr[n] = analogRead(analogPin);
  }

  //Apaga
  digitalWrite(moisturePinPower, LOW);

  //Saca la media de los datos en el arreglo
  moistureMean = mean(arr, arrSize);
  
  return moistureMean;
}

void loop() {
  float moistureValue = readSensor();
  Serial.print("Humedad leída: ");
  Serial.println(moistureValue);

  String jsonData = "{\"id\":\""+String(id)+
      "\",\"type\":\""+String(typeSensor)+
      "\",\"moisture\":{" 
      +"\"type\":\"float\","
      +"\"value\":"+String(moistureValue)
      + "}" + "}";

  if (client.connect(serverIP, serverPort)) {
    Serial.println("Conectado al servidor");

    client.println("POST /recibir HTTP/1.1");
    client.println("Host: " + String(serverIP));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonData.length());
    client.println();
    client.println(jsonData);
  } else {
    Serial.println("Error de conexión");
  }

  client.stop();
  delay(300000); //Tiempo de espera de 5 minutos
}