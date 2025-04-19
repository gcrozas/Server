//Librerias
#include <Wire.h> //Libreria Wire para la comunicacion I2C
#include <DHT.h> //Libreria para leer el sensor de temperatura y humedad

//Constantes
#define SLAVE_ADDRESS 11 // Define una direccion I2C para comunicarse con el Maestro (Raspberry Pi 4 Modelo B)
#define DHTPin 7 //Pin de entrada para el sensor de temperatura/humedad
const int LDRPin_A = A0; // Pin de entrada para el sensor de luz A
const int LDRPin_B = A1; // Pin de entrada para el sensor de luz B
//Nota: Los sensores PIR tardan 1 minuto en calibrarse (60000 milisegundos)
const int PIRPin_A = 2; //Pin de entrada para el sensor PIR A
const int PIRPin_B = 8; //Pin de entrada para el sensor PIR B
const int DOORPin = 3; //Pin de entrada para el sensor de puerta
const int ACPin_A = 10; //Pin de entrada para sensar el aire acondicionado A
const int ACPin_B = 11; //Pin de entrada para sensar el aire acondicionado B

//Sensor de temperatura/humedad
#define DHTType DHT22 //DHT 22 (AM2302)
DHT dht(DHTPin, DHTType);   //Configura el sensor DHT en el Arduino

void setup() {
  Wire.begin(SLAVE_ADDRESS); //Inicializa la comunicacion I2C con el Maestro
  pinMode(PIRPin_A, INPUT); //Pin digital de entrada conectado al sensor PIR A
  pinMode(PIRPin_B, INPUT); //Pin digital de entrada conectado al sensor PIR B
  pinMode(ACPin_A, INPUT); //Pin digital de entrada conectado a la salida de relay asociada al aire acondicionado A
  pinMode(ACPin_B, INPUT); //Pin digital de entrada conectado la salida de relay asociada al aire acondicionado A
  pinMode(DOORPin, INPUT); //Pin digital de entrada conectado al sensor de puerta
  pinMode(LDRPin_A, INPUT); //Pin analogico de entrada conectado al sensor de luz A
  pinMode(LDRPin_B, INPUT); //Pin analogico de entrada conectado al sensor de luz B
       
  dht.begin(); //Inicializa el sensor de temperatura y humedad

  Wire.onRequest(request_Event); //Cuando el maestro solicite informacion al esclavo, se activara esta funcion
}

//Eventos solicitados
void request_Event(){
  int i = 0;
  byte dato[8]; // Esta dato en bytes que se envia al raspberry pi
  while(i<8){
    switch(i){
      case 0:
        dato[i] = temperature_readings(); //Leemos la temperatura
        break;
      case 1:
        dato[i] = humidity_readings(); //Leemos la humedad
        break;
      case 2:
        dato[i] = pir_readings(); //Leemos si hay o no movimiento
        break;
      case 3:
        dato[i] = ldr_readings(LDRPin_A); //Leemos la luminosidad del ambiente
        break;
      case 4:
        dato[i] = ldr_readings(LDRPin_B); //Leemos la luminosidad del ambiente
        break;
       case 5:
        dato[i] = boolean_readings(DOORPin); //Leemos si la puerta esta abierta o cerrada
        //HIGH: Puerta cerrada. El circuito esta cerrado
        //LOW: Puerta abierta. El circuito esta abierto
        break;
      case 6:
        dato[i] = boolean_readings(ACPin_A); //Leemos si el aire acondicionado A esta encendido o apagado
        break;
      case 7:
        dato[i] = boolean_readings(ACPin_B); //Leemos si el aire acondicionado B esta encendido o apagado
        break;
    }
   i++;
  }
  Wire.write(dato,8); //Envia los datos leidos al maestro
}

byte temperature_readings(){
  int temp = dht.readTemperature(); //leyendo la temperatura por el pin conectado al sensor dht22
  byte temp_bytes;
  if (isnan(temp)){
    return 0;
  } else {
    temp_bytes=(byte)temp;
    return temp_bytes;
  }
}

byte humidity_readings(){
  int hum = dht.readHumidity(); //leyendo la humedad por el pin conectado al sensor dht22
  byte hum_bytes;
  if (isnan(hum)){
    return 0;
  } else {
    hum_bytes=(byte)hum;
    return hum_bytes;
  }
}

byte pir_readings(){
  int pir_valueA = digitalRead(PIRPin_A);
  int pir_valueB = digitalRead(PIRPin_B);
  int pir_total = (pir_valueA or pir_valueB);
  byte pir_bytes = (byte)pir_total;
  return pir_bytes;
}

byte ldr_readings(const int pin_value){
  int analogValue = analogRead(pin_value); // Leyendo el sensor de luz por el pin analogo A0

  //Mapea un valor analogo a 8 bits (0 a 255)
  analogValue = map(analogValue, 0, 1023, 0, 255);
  byte byte_value = (byte)analogValue;
  return byte_value;

  /*Luz que detecta el sensor
  analogValue < 10: Brillante
  analogValue < 200: Muy iluminado
  analogValue < 500: Iluminado
  analogValue < 800: Poco iluminado
  analogValue >= 800: Oscuro
  }*/
}

byte boolean_readings(const int pin_value){
  int sensor_value = digitalRead(pin_value);  //lectura digital de pin conectado al sensor
  byte sensor_byte=(byte)sensor_value;
  return sensor_byte;
}

void loop() {
  //Vacio
}
