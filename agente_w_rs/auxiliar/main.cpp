#include <Arduino.h>
#include "Ai_AP3216_AmbientLightAndProximity.h"
#include <ESP8266WiFi.h>

String data = "";
String tipo = "W_SR";
String codigo = "sensor_w_sr_01";

const int n = 10;
float radiaciones[n];
float mean = 0;
char estado = 'A';

WiFiClient client;

const char* server = "172.17.192.1";
const char* ssid = "UPBWiFi";

Ai_AP3216_AmbientLightAndProximity aps = Ai_AP3216_AmbientLightAndProximity();
//Ai_AP3216_AmbientLightAndProximity aps = Ai_AP3216_AmbientLightAndProximity(D5, D6);//custompins

void bundling(float radiacion) {
  data = "{";
  data += "\"id\": \"" + codigo + "\", ";
  data += "\"type\": " + tipo + ", ";
  data += "\"radiacion\": " + String(radiacion) + ", ";
  data += "}";
}

void readRadiaciones(){
  for(int i=0; i<n; i++){
    radiaciones[i] = aps.getAmbientLight();
    Serial.println(radiaciones[i]);
    delay(1000);
  }
}

void prunning(){
  float suma=0;
  for(int i=0; i<n; i++){
    suma += radiaciones[i];
  }
  mean = suma/n;
}

void sendthingspeak(String postData){
  Serial.println("Datos para enviar");
  Serial.println(postData);

  if(client.connect(server, 4451)){
    Serial.print("conectado");
    client.print("POST /recibir HTTP/1.1\r\n");
    client.print("Host: 127.0.0.1\r\n");
    client.println("User-Agent: Arduino/1.0");
    client.println("Connection: close");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();  
    client.println(postData);
  }else{
    Serial.println("error de conexión");
  }

}

void setup() {
	Serial.begin(115200);
	aps.begin();
	aps.startAmbientLightAndProximitySensor ();
  //Conexión Wifi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, "");
  Serial.println("Iniciando conexión");
  while(WiFi.status() != WL_CONNECTED){
    Serial.println(".");
    delay(100);
  }
  Serial.println("conectado");
}

void loop() {
  
  if (estado == 'A'){
    readRadiaciones();
    prunning();
    estado = 'B';
  }else if (estado =='B'){
    bundling(mean);
    Serial.println("Transmisión");
    sendthingspeak(data);
    Serial.println(data);
    delay(10);
    estado = 'C';
  }else if(estado == 'C'){
    Serial.println("Dormir");
    delay(10000);
    estado = 'A';
  }

}
