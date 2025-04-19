# Librerias
import smbus2 as smbus
import json
from datetime import datetime
from celery import shared_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from logging import Logger
from iot.custom_datetime import get_hour
#from iot.management.commands.i2cwriter import write_module

#Importar base de datos
from iot.models import Interior as Lab
from iot.models import Temperatura_exterior as temp_ext
from iot.models import Humedad_exterior as hum_ext
from iot.models import Humedad_piso as hum_floor

from iot.models import Promedio_temperatura as prom_temp
from iot.models import Promedio_humedad as prom_hum
from iot.models import Promedio_luminosidad as prom_lum
from iot.models import Promedio_presencia as prom_mov

# Direccion bus del servidor
DEVICE_BUS = 1
# Direccion de los esclavos en el bus
I2C_SLAVE1_ADDRESS = 11 #0X0b ou 11

# Instancia del bus I2C
I2Cbus = smbus.SMBus(1)

# Obtenemos los grupos de channel
channel_layer = get_channel_layer()

def save(x):
    y = json.loads(x)
    
    message_instance = Lab.objects.create(
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

@shared_task(bind=True)
def turn_on_AC(self):
    try:
        #write_module(12,31) #Encender A/A 1
        #write_module(12,41) #Encender A/A 2
        print("Encendiendo Aire Acondicionados!")
        pass
    except Exception as e:
        Logger.error('Ocurrio un error, la tarea turn_on_AC() se repetira en 5 segundos...')
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True)
def average_data(self):
    try :
        print("Calculando el promedio")
        now = datetime.now()
        hour_ago = get_hour(1) # El tiempo de hace 1 hora

        # Configura el tiempo inicial y el tiempo final a 0 minutos, 0 segundos, 0 milisegundos
        time_before = hour_ago.replace(minute=0,second=0,microsecond=0) #Hora anterior
        time_after = now.replace(minute=0,second=59,microsecond=59) #Hora actual

        # gte: dia_hora_leida >= time_before
        # lte: dia_hora_leida <= time_after
        # Buscamos lecturas tomadas entre la hora anterior y la hora actual
        # Ejemplo: 14:00:00:00 - 15:00:59:59 (hora:minuto:segundos:microsegundos)
        readings = Lab.objects.filter(dia_hora_leida__gte=time_before, dia_hora_leida__lte=time_after)

        #print(readings)

        cont = 0
        sum_temp = 0
        sum_hum = 0
        sum_lum1 = 0
        sum_lum2 = 0
        sum_mov = 0

        # Si se encontraron resultados, se calcula el promedio
        if (readings is not None):
            
            for reading_info in readings:
                temperature = reading_info.temp
                humidity = reading_info.hum
                lum1 = reading_info.lum_1
                lum2 = reading_info.lum_2
                mov = reading_info.presencia

                sum_temp += int(temperature)
                sum_hum += int(humidity)
                sum_lum1 += int(lum1)
                sum_lum2 += int(lum2)
                sum_mov += int(mov)

                cont += 1

            print ("Suma de presencia: " + str(sum_mov))

            temp_total = sum_temp // cont
            hum_total = sum_hum // cont
            lum1_total = sum_lum1 // cont
            lum2_total = sum_lum2 // cont
            mov_total = round((sum_mov / cont)) # Division redondeada hacia arriba si el resultado es mayor que 0.5

            print("Promedio temperatura: " + str(temp_total))
            print("Promedio humedad: " + str(hum_total))
            print("Promedio iluminacion (lampara de mesa): " + str(lum1_total))
            print("Promedio iluminacion (lampara de techo): " + str(lum2_total))
            print("Promedio presencia: " + str(mov_total))

            temp_instance = prom_temp.objects.create(
                temp = str(temp_total),
                dia_inicio = time_before,
                dia_fin = time_after.replace(minute=0,second=0,microsecond=0)
            )

            hum_instance = prom_hum.objects.create(
                hum = str(hum_total),
                dia_inicio = time_before,
                dia_fin = time_after.replace(minute=0,second=0,microsecond=0)
            )

            lum1_instance = prom_lum.objects.create(
                lum_object = 'Seccion 1',
                lum = str(lum1_total),
                dia_inicio = time_before,
                dia_fin = time_after.replace(minute=0,second=0,microsecond=0)
            )

            lum2_instance = prom_lum.objects.create(
                lum_object = 'Seccion 2',
                lum = str(lum2_total),
                dia_inicio = time_before,
                dia_fin = time_after.replace(minute=0,second=0,microsecond=0)
            )

            mov_instance = prom_mov.objects.create(
                mov = str(mov_total),
                dia_inicio = time_before,
                dia_fin = time_after.replace(minute=0,second=0,microsecond=0)
            )
            # Borra datos antiguos de la base de datos
            # dia_hora_leida < dia_fin
            dia_fin = time_after.replace(minute=0,second=0,microsecond=0)
            Lab.objects.filter(dia_hora_leida__lte=dia_fin).delete()
            print("Promedios registrados")


    except Exception as e:
        Logger.error('Ocurrio un error, la tarea aveage_data() se repetira en 5 segundos...')
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True)
def i2creader(self):
    try:
        with smbus.SMBus(1) as I2Cbus:
            Modulo = I2Cbus.read_i2c_block_data(I2C_SLAVE1_ADDRESS,0,15)
            now = datetime.now()
            
            x = {'id':I2C_SLAVE1_ADDRESS,
                'temperature':Modulo[7],
                'humidity':Modulo[8],
                'movement':Modulo[9],
                'lum-1':Modulo[10],
                'lum-2':Modulo[11],
                'door':Modulo[12],
                'ac-1': Modulo[13],
                'ac-2': Modulo[14],
                'datetime_reader': now.isoformat()
            }
            y = json.dumps(x)
            save(y)
    except Exception as e:
        Logger.error('Ocurrio un error, la tarea i2creader() se repetira en 5 segundos...')
        raise self.retry(exc=e, countdown=5)

@receiver(post_save, sender=Lab)
def event_post_add(sender, instance, created, **kwargs):
    if created:
        print ("Datos del laboratorio registrados")

        # Obtenemos informacion de la base de datos
        db_data = Lab.objects.order_by('dia_hora_leida').last()

        # Obtenemos la fecha-hora en la que la informacion fue leida
        some_datetime = db_data.dia_hora_leida
        iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

        dict_data = {
            'type': 'update_lab_data',
            'temperature': db_data.temp,
            'humidity': db_data.hum,
            'presence': db_data.presencia,
            'lum1': db_data.lum_1,
            'lum2': db_data.lum_2,
            'door': db_data.seg_puerta,
            'ac1': db_data.AC_1,
            'ac2': db_data.AC_2,
            'iso_datetime': iso_datetime        
        }
        # Enviamos la data al grupo 'lab_events'
        async_to_sync(channel_layer.group_send)('lab_events',dict_data)

@receiver(post_save, sender=temp_ext)
def event_post_temp_ext(sender, instance, created, **kwargs):
    if created:
        print ("Temperatura externa registrada")

        db_data = temp_ext.objects.order_by('dia_hora_leida').last()
            
        # Obtenemos la fecha-hora en la que la informacion fue leida
        some_datetime = db_data.dia_hora_leida
        iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

        dict_data = {
            'type': 'update_temp_ext',
            'temp_ext': db_data.temp,
            'iso_datetime': iso_datetime        
        }
            
        # Enviamos la data al grupo 'lab_events'
        async_to_sync(channel_layer.group_send)('lab_events',dict_data)

@receiver(post_save, sender=hum_ext)
def event_post_hum_ext(sender, instance, created, **kwargs):
    if created:
        print ("Humedad externa registrada")

        # Obtenemos informacion de la base de datos
        db_data = hum_ext.objects.order_by('dia_hora_leida').last()
            
        # Obtenemos la fecha-hora en la que la informacion fue leida
        some_datetime = db_data.dia_hora_leida
        iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

        dict_data = {
            'type': 'update_hum_ext',
            'hum_ext': db_data.hum,
            'iso_datetime': iso_datetime        
        }
            
        # Enviamos la data al grupo 'lab_events'
        async_to_sync(channel_layer.group_send)('lab_events',dict_data)

@receiver(post_save, sender=hum_floor)
def event_post_hum_floor(sender, instance, created, **kwargs):
    if created:
        print ("Humedad externa registrada")

        db_data = hum_floor.objects.order_by('dia_hora_leida').last()

        # Obtenemos la fecha-hora en la que la informacion fue leida
        some_datetime = db_data.dia_hora_leida
        iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

        dict_data = {
            'type': 'update_hum_floor',
            'hum_floor': db_data.mojado,
            'iso_datetime': iso_datetime        
        }
            
        # Enviamos la data al grupo 'lab_events'
        async_to_sync(channel_layer.group_send)('lab_events',dict_data)



