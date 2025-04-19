#include <Wire.h> //Libreria para la comunicacion I2C

#define SLAVE_ADDRESS 12

//Aires acondicionados del laboratorio (leds azules)
const int ledPin_A = 6;
const int ledPin_B = 5;
//Luces del laboratorio (leds amarillos)
const int ledPin_C = 4;
const int ledPin_D = 3;

void setup() {
  //Configura los pines como salidas
  pinMode(ledPin_A, OUTPUT);
  pinMode(ledPin_B, OUTPUT);
  pinMode(ledPin_C, OUTPUT);
  pinMode(ledPin_D, OUTPUT);

  digitalWrite(ledPin_A, HIGH);
  digitalWrite(ledPin_B, HIGH);
  digitalWrite(ledPin_C, HIGH);
  digitalWrite(ledPin_D, HIGH);
  
  Wire.begin(SLAVE_ADDRESS); //Se une al bus I2C como un esclavo con la direccion correspondiente

  //Llama a la funcion receiveEvent cuando recibe la data
  Wire.onReceive(receiveEvent);
}

void receiveEvent(int howMany){
  while (Wire.available()){
    int x = Wire.read(); //Recibe el byte como un entero
    switch (x){
      case 10:
        digitalWrite(ledPin_D, HIGH);
        break;
      case 11:
        digitalWrite(ledPin_D, LOW);
        break;
      case 20:
        digitalWrite(ledPin_C, HIGH);
        break;
      case 21:
        digitalWrite(ledPin_C, LOW);
        break;
      case 30:
        digitalWrite(ledPin_B, HIGH);
        break;
      case 31:
        digitalWrite(ledPin_B, LOW);
        break;
      case 40:
        digitalWrite(ledPin_A, HIGH);
        break;
      case 41:
        digitalWrite(ledPin_A, LOW);
        break;
    }
    
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
