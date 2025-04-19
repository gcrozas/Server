# Comunicacion entre Raspberry Pi y Arduino usando el protocolo I2C

# Librerias
import os
import smbus2 as smbus
import time

from django.core.management.base import BaseCommand

# Direccion bus del servidor
DEVICE_BUS = 1
# Direccion de los esclavos en el bus
I2C_SLAVE2_ADDRESS = 12 #0X0c ou 12

#Instancia del bus I2C
I2Cbus = smbus.SMBus(1)

#Borra el texto de la terminal
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Envia un comando en concreto al modulo
def write_module(slave_address,message):
    with smbus.SMBus(1) as I2Cbus:
        try:
            I2Cbus.write_byte_data(slave_address, 0, message)
        except Exception as e:
            print("Error remoto i/o")
            print(e)

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            while True:
                cls()
                #print("Conectando...")
                #print("Activando actuadores...")
                flag = True
                while (flag):
                    print("Luces (1-2)")
                    print("AC (3-4)")
                    relaySelect = int(input("Opcion seleccionada: "))
                    if ((relaySelect > 0) and (relaySelect < 5)):
                        status = int(input("Encender/Apagar (1-0): "))
                        if ((status == 1) or (status==0)):
                            message = (relaySelect * 10) + status
                            #print("orden: ",str(message))
                            write_module(I2C_SLAVE2_ADDRESS, message)
                            flag = False
                    time.sleep(10) #Tiempo de espera de 10 segundos
        except KeyboardInterrupt:
            print("La comunicacion se detuvo")