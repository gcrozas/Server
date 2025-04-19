# Comunicacion entre Raspberry Pi y Arduino usando el protocolo I2C

# Librerias
import os
import smbus2 as smbus
import time
import json
from datetime import datetime

from django.core.management.base import BaseCommand

from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer

from iot.models import Interior

# Direccion bus del servidor
DEVICE_BUS = 1
# Direccion de los esclavos en el bus
I2C_SLAVE1_ADDRESS = 11 #0X0b ou 11

#Instancia del bus I2C
I2Cbus = smbus.SMBus(1)

def save(x):
    print("Guardando datos leidos")
    y = json.loads(x)
    
    message_instance = Interior.objects.create(
        temp = str(y["temperature"]),
        hum = str(y["humidity"]),
        presencia = str(y["movement"]),
        lum_1 = str(y["lum-1"]),
        lum_2 = str(y["lum-2"]),
        seg_puerta = str(y["door"]),
        AC_1 = str(y["ac-1"]),
        AC_2 = str(y["ac-2"]),
        dia_hora_leida = y["datetime_reader"]
    )
    print("Guardado!")

#Borra el texto de la terminal
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#Recibe la lectura de los sensores en el modulo
def read_module(dir_slave):
    with smbus.SMBus(1) as I2Cbus:
        try:
            #print("Comunicandose con el esclavo " + str(dir_slave) + "...")
            Modulo = I2Cbus.read_i2c_block_data(dir_slave,0,15)
            #print("Comunicacion exitosa")
            #print(Modulo)
            print("Temperatura: " + str(Modulo[7]) + " C")
            print("Humedad: " + str(Modulo[8]) + "%")

            if (Modulo[9]==1):
                print("Hay presencia")
            else:
                print("No hay presencia")

            lumi_A = Modulo[10]
            print("luminosidad A: ", lumi_A)

            if ((lumi_A>=0) and (lumi_A<=43)):
                print("Estado de luz: ON")
                print("Nivel de luz: Alto")
            elif ((lumi_A>43) and (lumi_A<=200)):
                print("Estado de luz: ON")
                print("Nivel de luz: Medio")
            elif ((lumi_A>200) and (lumi_A<255)):
                print("Estado de luz: OFF")
                print("Nivel de luz: Bajo")
            elif (lumi_A==255):
                print("Estado de luz: OFF")
                print("Nivel de luz: Nulo")

            lumi_B = Modulo[11]
            print("luminosidad B: ", lumi_B)

            if ((lumi_B>=0) and (lumi_B<=43)):
                print("Estado de luz: ON")
                print("Nivel de luz: Alto")
            elif ((lumi_B>43) and (lumi_B<=200)):
                print("Estado de luz: ON")
                print("Nivel de luz: Medio")
            elif ((lumi_B>200) and (lumi_B<255)):
                print("Estado de luz: OFF")
                print("Nivel de luz: Bajo")
            elif (lumi_B==255):
                print("Estado de luz: OFF")
                print("Nivel de luz: Nulo")

            if (Modulo[12]==1):
                print("Puerta cerrada")
            else:
                print("Puerta abierta")

            if (Modulo[13]==1):
                print("AC 1: Encendido")
            else:
                print("AC 1: Apagado")

            if (Modulo[14]==1):
                print("AC 2: Encendido")
            else:
                print("AC 2: Apagado")

            now = datetime.now()
            
            x = {'id': dir_slave,
                     'temperature':Modulo[7],
                     'humidity':Modulo[8],
                     'movement':Modulo[9],
                     'brightness_A':Modulo[10],
                     'brightness_B':Modulo[11],
                     'door':Modulo[12],
                     'ac-1': Modulo[13],
                     'ac-2': Modulo[14],
                     'datetime_reader': now.isoformat()
            }
            payload = json.dumps(x)
            return payload
        except Exception as e:
                print("Error remoto i/o")
                print(e)

class Command(BaseCommand):

    help = ('Muestra la lecturas de los sensores' 
    + 'del modulo 1')

    def handle(self, *args, **kwargs):
        try:
            print("Conectando...")
            while True:
                cls() #limpia la pantalla
                datos = read_module(I2C_SLAVE1_ADDRESS)
                #save(datos)
                time.sleep(60) # Tiempo de espera de 1 minuto
        except KeyboardInterrupt:
            print("La comunicacion se detuvo")