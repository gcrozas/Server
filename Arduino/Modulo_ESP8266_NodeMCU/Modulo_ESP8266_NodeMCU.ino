// Librerias
#include <DHT.h>
#include <ESP8266WiFi.h>
#include <Ticker.h>
#include <AsyncMqttClient.h>

// WiFi
#define WIFI_SSID "Rozas"
#define WIFI_PASSWORD "Bolivar23"

//WIFI_PASSWORD NULL

// MQTT Broker
#define MQTT_HOST IPAddress(192, 168, 100, 18)
// Para MQTT broker en la nube
//#define MQTT_HOST "https://test.mosquitto.org/"
#define MQTT_PORT 1883
#define MQTT_QOS 1

// Topicos MQTT
#define MQTT_PUB_TEMP "esp8266/temperature"
#define MQTT_PUB_HUM "esp8266/humidity"
#define MQTT_PUB_WATER "esp8266/water"

// Pines
const int WATERPIN = 5;
#define DHTPIN 4 //Pin donde se encuentra conectado del sensor DHT (de temperatura y humedad)

#define DHTTYPE DHT11 //Tipo de sensor de temperatura y humedad

// Inicializamos el sensor DHT
DHT dht(DHTPIN, DHTTYPE);

//Variables que manejan la comunicacion MQTT
AsyncMqttClient mqttClient;
Ticker mqttReconnectTimer;

//Variables que manejan el estado de conexion del Wifi
WiFiEventHandler wifiConnectHandler;
WiFiEventHandler wifiDisconnectHandler;
Ticker wifiReconnectTimer;

unsigned long event_dht = 0;
unsigned long event_water = 0;

//Variables para determinar cada tanto lee los sensores y envia los mensajes
const unsigned long interval_dht = 60000; //1 minuto
const unsigned long interval_water = 300000; //5 minutos

void connectToWifi() {
  Serial.println("Conectadose a la red WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

void onWifiConnect(const WiFiEventStationModeGotIP& event) {
  Serial.println("");
  Serial.print("Conectado a la red ");
  Serial.println(WIFI_SSID);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  connectToMqtt();
}

void onWifiDisconnect(const WiFiEventStationModeDisconnected& event) {
  Serial.println("Desconectado de la red WiFi.");
  mqttReconnectTimer.detach(); // Nos aseguramos que no intente conectarse a MQTT mientras intentamos reconectarnos al WiFi
  wifiReconnectTimer.once(2, connectToWifi);
}

void connectToMqtt() {
  Serial.println("Conectadose al broker MQTT...");
  mqttClient.connect();
}

void onMqttConnect(bool sessionPresent) {
  Serial.println("Conectado al broker MQTT.");
  Serial.print("Session: ");
  Serial.println(sessionPresent);
}

void onMqttDisconnect(AsyncMqttClientDisconnectReason reason) {
  Serial.println("Desconectado del broker MQTT.");

  if (WiFi.isConnected()) {
    mqttReconnectTimer.once(2, connectToMqtt);
  }
}

void onMqttPublish(uint16_t packetId) {
  Serial.print("Se publico un mensaje.");
  Serial.print("  packetId: ");
  Serial.println(packetId);
}

void setup(){
  Serial.begin(9600);
  pinMode(WATERPIN,INPUT);

  dht.begin();
  
  wifiConnectHandler = WiFi.onStationModeGotIP(onWifiConnect);
  wifiDisconnectHandler = WiFi.onStationModeDisconnected(onWifiDisconnect);

  mqttClient.onConnect(onMqttConnect);
  mqttClient.onDisconnect(onMqttDisconnect);

  mqttClient.onPublish(onMqttPublish);
  mqttClient.setServer(MQTT_HOST, MQTT_PORT);
  // Si el broker requiere autenticacion (usuario y contrasena), y posee una credencial, se configura con la siguiente funcion
  mqttClient.setCredentials("rasp-broker", "ucab*ucab");

  connectToWifi();
}

void PublishTemp(){
  String payload;
  int temp = int(round(dht.readTemperature())); // Lee la temperatura en Celsius (default)
  // Lee la temperatura en Fahrenheit (isFahrenheit = true)
  //float temp = dht.readTemperature(true);
  if (isnan(temp)) {
    payload = "error";
    Serial.println("Mensaje: error.");
  } else{
   payload = String(temp);
   Serial.printf("Mensaje: %i \n", temp);
  }
  // Publica un mensaje MQTT al topico esp8266/temperature
  uint16_t packetIdPub1 = mqttClient.publish(MQTT_PUB_TEMP, MQTT_QOS, true, payload.c_str());                       
  Serial.printf("Publicando al topico %s en QoS 1, packetId: %i \n", MQTT_PUB_TEMP, packetIdPub1);
}

void PublishHum(){
  String payload;
  int hum = int(round(dht.readHumidity())); // Lee la humedad relativa
  if (isnan(hum)) {
    payload = "error";
    Serial.println("Mensaje: error.");
  } else{
   payload = String(hum);
   Serial.printf("Mensaje: %i \n", hum);
  }
  // Publica un mensaje MQTT al topico esp8266/humidity
  uint16_t packetIdPub2 = mqttClient.publish(MQTT_PUB_HUM, MQTT_QOS, true, payload.c_str());                       
  Serial.printf("Publicando al topico %s en QoS 1, packetId: %i \n", MQTT_PUB_HUM, packetIdPub2);
}

void PublishWater(){
  String payload;
  if (! digitalRead(WATERPIN)){
    payload = "1"; //Hay humedad (el sensor esta mojado)
  } else {
    payload = "0"; //No hay humedad (el sensor esta seco)
  }
  Serial.printf("Mensaje: %s \n",payload);
  uint16_t packetIdPub3 = mqttClient.publish(MQTT_PUB_WATER, MQTT_QOS, true, payload.c_str());                       
  Serial.printf("Publicando al topico %s en QoS 1, packetId %i: \n", MQTT_PUB_WATER, packetIdPub3);
}

void loop(){
  unsigned long currentMillis = millis();

  if (currentMillis - event_dht >= interval_dht) {
    PublishTemp(); //Publica la temperatura
    PublishHum(); //Publica la humedad
    event_dht = currentMillis; // Guarda el tiempo en que una nueva lectura fue publicada
  }

  if (currentMillis - event_water >= interval_water) {
    PublishWater(); //Publica si hay o no humedad en el sensor de agua
    event_water = currentMillis; // Guarda el tiempo en que una nueva lectura fue publicada
  }
}
