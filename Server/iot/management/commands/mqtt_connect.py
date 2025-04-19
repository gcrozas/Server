#paho: Proporciona herramientas para la implementacion de MQTT
from paho.mqtt import client as mqtt
from Server.settings import MQTT_CONFIG, MQTT_TOPICS, CLIENT_ID
from datetime import datetime
from django.utils import timezone
from time import sleep
import pytz
import os
from iot.models import Temperatura_exterior, Humedad_exterior, Humedad_piso

from django.core.management.base import BaseCommand

santiagoClTz = pytz.timezone("America/Caracas")

#Borra el texto de la terminal
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def save(message, topic, date_time):
    print("Guardando datos del topico " + topic)
    if (topic == MQTT_TOPICS["topic_temp"]):
        message_instance = Temperatura_exterior.objects.create(temp=message,dia_hora_leida=date_time)
    elif(topic == MQTT_TOPICS["topic_hum"]):
        message_instance = Humedad_exterior.objects.create(hum=message,dia_hora_leida=date_time)
    elif(topic == MQTT_TOPICS["topic_floor"]):
        message_instance = Humedad_piso.objects.create(mojado=message,dia_hora_leida=date_time)
    #print("Guardado!")
    
def connect_mqtt():
    client = mqtt.Client(CLIENT_ID) #Crea la instancia client
    client.on_connect = on_connect #Llamada al metodo on_connect
    client.username_pw_set(MQTT_CONFIG["mqtt_username"],MQTT_CONFIG["mqtt_password"])
    client.connect(
        MQTT_CONFIG["mqtt_broker"], 
        MQTT_CONFIG["mqtt_port"]
    )
    return client

#El broker responde con un mensaje CONNACK que contiene el resultado de la conexion.
def on_connect(client, userdata, flags, rc):
    #El valor de rc indica el estado de conexion
    #Si el rc (resultado de la conexion) es diferente de 0 significa que hubo un error de conexion
    if (rc!=0):
        print("Error de conexion MQTT, codigo de retorno: %d", rc)
    """else:
        print("Conexion MQTT exitosa.")"""
        

def subscribe(client: mqtt):
    def on_message_temp(client, userdata, msg):        
        temp = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        #now = timezone.localtime(timezone.now())
        print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "temperatura: " + temp + " C")
        save(temp,msg.topic,now)

    def on_message_hum(client, userdata, msg):
        hum = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        #now = timezone.localtime(timezone.now())
        print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "humedad: " + hum + "%")
        save(hum,msg.topic,now)

    def on_message_water(client, userdata, msg):
        agua = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        #now = timezone.localtime(timezone.now())
        if (agua=='0'):
            message = 'Seco'
        else:
            message = 'Humedo'
        print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "humedad del piso: " + message)
        save(agua,msg.topic,now)

    def on_message(client, userdata, msg):
        pass
        #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))

    #Agrega callbacks que solo se activaran a una suscripcion especifica
    client.message_callback_add(MQTT_TOPICS["topic_temp"], on_message_temp) #topico temperatura
    client.message_callback_add(MQTT_TOPICS["topic_hum"], on_message_hum) #topico humedad
    client.message_callback_add(MQTT_TOPICS["topic_floor"], on_message_water) #topico del estado de la luz cuando cambia
    client.on_message = on_message
    client.subscribe(MQTT_TOPICS["topic_sub"],MQTT_CONFIG["mqtt_qos"])

class Command(BaseCommand):

    help = ('Muestra la lecturas de los sensores' 
    + 'del modulo 1')

    def handle(self, *args, **kwargs):
        cont = 1
        try:
            client = connect_mqtt()
            client.loop_start()
            print("Conectando...")
            #subscribe(client)
            while True:
                cls()
                print("Lectura " + str(cont) + ":")
                subscribe(client)
                cont= cont + 1
                sleep(10)
        except KeyboardInterrupt:
            print("La comunicacion se detuvo")

