from django.apps import AppConfig

from threading import Thread
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
from time import sleep

from Server.settings import MQTT_CONFIG, MQTT_TOPICS, CLIENT_ID

class MqttClient(Thread):
    def __init__(self, broker, port, topics):
        super(MqttClient, self).__init__()
        self.client = mqtt.Client() #Cuando se coloca el client_id el programa tiende a fallar
        self.broker = broker
        self.port = port
        self.topics = topics
        self.total_messages = 0
    
    def on_message_temp(self,client, userdata, msg):
        from iot.models import Temperatura_exterior
        mqtt_temp = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        #now = timezone.localtime(timezone.now())
        if (len(mqtt_temp) < 3):
            last_time = now - timedelta(minutes=5)
            message_instance = Temperatura_exterior.objects.create(temp=int(mqtt_temp),dia_hora_leida=now)
            Temperatura_exterior.objects.filter(dia_hora_leida__lt=last_time).delete() # Borrar < fecha actual
            #print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "temperatura: " + mqtt_temp + " C" + " - Total: {}".format(self.total_messages))
        

    def on_message_hum(self, client, userdata, msg):
        from iot.models import Humedad_exterior
        mqtt_hum = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        #now = timezone.localtime(timezone.now())
        if (len(mqtt_hum) < 3):
            last_time = now - timedelta(minutes=5)
            message_instance = Humedad_exterior.objects.create(hum=int(mqtt_hum),dia_hora_leida=now)
            Humedad_exterior.objects.filter(dia_hora_leida__lt=last_time).delete() # Borras < fecha actual
            #print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "humedad: " + mqtt_hum + "%" + " - Total: {}".format(self.total_messages))
        

    def on_message_water(self,client, userdata, msg):
        from iot.models import Humedad_piso
        mqtt_agua = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        #now = timezone.localtime(timezone.now())
        last_time = now - timedelta(minutes=10)
        if (mqtt_agua=='0'):
            message = 'Seco'
            message_instance = Humedad_piso.objects.create(mojado=int(mqtt_agua),dia_hora_leida=now)
            Humedad_piso.objects.filter(dia_hora_leida__lt=last_time).delete() # Borrar < fecha actual
            #print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "humedad del piso: " + message + " - Total: {}".format(self.total_messages))
        elif (mqtt_agua=='1'):
            message = 'Humedo'
            message_instance = Humedad_piso.objects.create(mojado=int(mqtt_agua),dia_hora_leida=now)
            Humedad_piso.objects.filter(dia_hora_leida__lt=last_time).delete()
            #print((now.strftime("%d/%m/%Y %H:%M")) + " - " + "humedad del piso: " + message + " - Total: {}".format(self.total_messages))

    def connect_to_broker(self):
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(MQTT_CONFIG["mqtt_username"],MQTT_CONFIG["mqtt_password"])
        self.client.message_callback_add(MQTT_TOPICS["topic_temp"], self.on_message_temp) #topico temperatura
        self.client.message_callback_add(MQTT_TOPICS["topic_hum"], self.on_message_hum) #topico humedad
        self.client.message_callback_add(MQTT_TOPICS["topic_floor"], self.on_message_water) #topico del estado de la luz cuando cambia
    
        self.client.on_message = self.on_message
        self.client.connect_async(self.broker,self.port)
        self.client.loop_start()

    # The callback for when a PUBLISH message is received from the server
    def on_message(self, client, userdata, msg):
        self.total_messages = self.total_messages + 1
        sleep(10)
        """mqtt_payload = msg.payload.decode("utf-8").strip() #convierte el payload a utf-8
        now = datetime.now()
        print (now.strftime("%d/%m/%Y %H:%M") + ": " + mqtt_payload + " - Total: {}".format(self.total_messages))
        """
    # run method override from Thread class
    def run(self):
        #print("Conectandose al broker mqtt...")
        self.connect_to_broker()

    # The callback for when the client receives a CONNACK response from the server   
    def on_connect(self, client, userdata, flags, rc):
        # Subscribe to a list of topics using a lock to guarantee that a topic is only subscribed once
        #client.subscribe(MQTT_TOPICS["topic_sub"],MQTT_CONFIG["mqtt_qos"])
        for topic in self.topics:
            client.subscribe(topic,MQTT_CONFIG["mqtt_qos"])

class MqttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mqtt'

    def ready(self):
        MqttClient(MQTT_CONFIG["mqtt_broker"], MQTT_CONFIG["mqtt_port"],[MQTT_TOPICS["topic_temp"], MQTT_TOPICS["topic_hum"], MQTT_TOPICS["topic_floor"]]).start()
