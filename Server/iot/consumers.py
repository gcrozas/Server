import json
from time import sleep
from datetime import timedelta, datetime
from .management.commands.i2creader import read_module

#import iot.custom_datetime as custom_datetime

from asgiref.sync import async_to_sync

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.db import database_sync_to_async
from iot.models import Interior as lab
from iot.models import Temperatura_exterior, Humedad_exterior, Humedad_piso, Promedio_temperatura, Promedio_humedad, Promedio_presencia, Promedio_luminosidad
#from channels.exceptions import StopConsumer
from iot.management.commands.i2cwriter import write_module

class Lab2Consumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_lab_data(self):
        myData = lab.objects.order_by('dia_hora_leida').last()
        return myData #El ultimo contenido registrado en la tabla

    @database_sync_to_async
    def get_temp_ext_data(self):
        myData = Temperatura_exterior.objects.order_by('dia_hora_leida').last()
        return myData #El ultimo contenido registrado en la tabla
    
    @database_sync_to_async
    def get_hum_ext_data(self):
        myData = Humedad_exterior.objects.order_by('dia_hora_leida').last()
        return myData #El ultimo contenido registrado en la tabla
    
    @database_sync_to_async
    def get_hum_floor_data(self):
        myData = Humedad_piso.objects.order_by('dia_hora_leida').last()
        return myData #El ultimo contenido registrado en la tabla

    async def connect(self):
        print('Conectado al websocket...')

        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            # Nos unimos al grupo
            await self.channel_layer.group_add("lab_events", self.channel_name)
            
            # Aceptamos la conexion
            await self.accept()
            
            try:
                # Obtenemos informacion de la base de datos
                db_data = await self.get_lab_data()

                # Obtenemos la fecha-hora en la que la informacion fue leida
                some_datetime = db_data.dia_hora_leida
                iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

                json_data = json.dumps({
                    'event_update': 'Datos del laboratorio', 
                    'temperature': db_data.temp,
                    'humidity': db_data.hum,
                    'presence': db_data.presencia,
                    'lum1': db_data.lum_1,
                    'lum2': db_data.lum_2,
                    'door': db_data.seg_puerta,
                    'ac1': db_data.AC_1,
                    'ac2': db_data.AC_2,
                    'iso_datetime': iso_datetime
                })
                await self.send(json_data)
            except Exception as e:
                print(e)

            try:
                db_data = await self.get_temp_ext_data()

                # Obtenemos la fecha-hora en la que la informacion fue leida
                some_datetime = db_data.dia_hora_leida
                iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

                json_data = json.dumps({
                    'event_update': 'Temperatura exterior', 
                    'temp_ext': db_data.temp,
                    'iso_datetime': iso_datetime
                })
                await self.send(json_data)
            except Exception as e:
                print(e)

            try:
                db_data = await self.get_hum_ext_data()

                # Obtenemos la fecha-hora en la que la informacion fue leida
                some_datetime = db_data.dia_hora_leida
                iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

                json_data = json.dumps({
                    'event_update': 'Humedad exterior', 
                    'hum_ext': db_data.hum,
                    'iso_datetime': iso_datetime
                })

                await self.send(json_data)
            except Exception as e:
                print(e)

            try:
                db_data = await self.get_hum_floor_data() 

                # Obtenemos la fecha-hora en la que la informacion fue leida
                some_datetime = db_data.dia_hora_leida
                iso_datetime = some_datetime.isoformat() #Transformandola a formato ISO para guardarla en JSON

                json_data = json.dumps({
                    'event_update': 'Humedad del piso', 
                    'hum_floor': db_data.mojado,
                    'iso_datetime': iso_datetime
                })
                await self.send(json_data)
            except Exception as e:
                print(e)
            
    async def disconnect(self, code):
        print('Desconectadose de websocket...codigo: ', code)

        # Desconectamos al usuario del grupo
        await self.channel_layer.group_discard("lab_events",self.channel_name)
        #raise StopConsumer()

    async def update_lab_data(self, event):
        text_message = {
            'event_update': 'Datos del laboratorio',
            'temperature': event['temperature'],
            'humidity': event['humidity'],
            'presence': event['presence'],
            'lum1': event['lum1'],
            'lum2': event['lum2'],
            'door': event['door'],
            'ac1': event['ac1'],
            'ac2': event['ac2'],
            'iso_datetime': event['iso_datetime']  
        }
        json_data = json.dumps(text_message)
        await self.send(json_data)

    async def update_temp_ext(self, event):
        text_message = {
            'event_update': 'Temperatura exterior',
            'temp_ext': event['temp_ext'],
            'iso_datetime': event['iso_datetime']
        }
        json_data = json.dumps(text_message)
        await self.send(json_data)
    
    async def update_hum_ext(self, event):
        text_message = {
            'event_update': 'Humedad exterior',
            'hum_ext': event['hum_ext'],
            'iso_datetime': event['iso_datetime']
        }
        json_data = json.dumps(text_message)
        await self.send(json_data)
    
    async def update_hum_floor(self, event):
        text_message = {
                'event_update': 'Humedad del piso',
                'hum_floor': event['hum_floor'],
                'iso_datetime': event['iso_datetime']
        }
        json_data = json.dumps(text_message)
        await self.send(json_data)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        type_message = str(text_data_json["type"])

        #print("Mensaje recibido por websockets: " + type_message)

        if (type_message=='action_event'):
            #print("Mensaje recibido por websockets: " + str(message))
            write_module(12,message)
        

    async def action_event(self, event):
        # Mensaje que se le enviara al esclavo
        text_data_json = json.loads(event)
        action = str(text_data_json['message'])

        print("Recibiendo accion: " + action)


class RecordConsumer(WebsocketConsumer):
    def connect(self):
        print('Conectado al websocket...')
        if self.scope["user"].is_anonymous:
            self.close()
        else:
            # Aceptamos la conexion
            self.accept()
    
    def disconnect(self, code):
        # Desconectamos al usuario
        print('Desconectadose de websocket...codigo: ', code)
        #raise StopConsumer()
    
    def get_previousweek_data(self, option, week):
        current_date = datetime.today() #Obtenemos la fecha y tiempo de ahora
        current_weekday = current_date.weekday() # Obtenemos el dia de la semana de hoy
        past_days = current_weekday + week # Numero de dias a retroceder, hasta llegar al lunes de la semana correspondiente

        previous_week = current_date - timedelta(days=past_days) # Nos ubicamos el dia lunes de esa semana
        end_of_week = previous_week + timedelta(days=5) # Dia viernes de esa semana

        date_begin = previous_week.date() # Fecha del lunes de esa semana
        date_end = end_of_week.date() # Fecha del sabado de esa semana

        myData = []

        if (option==0):
            # Extrae la informacion entre el dia lunes y viernes de esa semana
            readings = Promedio_temperatura.objects.filter(dia_inicio__range=[date_begin,date_end])

            if (readings):
                for reading_info in readings:
                    # Revisa si la lectura es de entre las 7 am y las 7 pm
                    if ((reading_info.dia_inicio.hour >= 7) and (reading_info.dia_inicio.hour < 19)):
                        dataInfo = {
                            "value": str(reading_info.temp),
                            "fecha": reading_info.dia_inicio.strftime('%d/%m/%Y'),
                            "dia_semana": str(reading_info.dia_inicio.weekday()),
                            "hora_inicio": reading_info.dia_inicio.strftime('%H:%M'),
                            "hora_fin": reading_info.dia_fin.strftime('%H:%M')
                        }
                        myData.append(dataInfo)
        elif (option==1):
            readings = Promedio_humedad.objects.filter(dia_inicio__range=[date_begin,date_end])

            if (readings):
                for reading_info in readings:
                    # Revisa si la lectura es de entre las 7 am y las 7 pm
                    if ((reading_info.dia_inicio.hour >= 7) and (reading_info.dia_inicio.hour < 19)):
                        dataInfo = {
                            "value": str(reading_info.hum),
                            "fecha": reading_info.dia_inicio.strftime('%d/%m/%Y'),
                            "dia_semana": str(reading_info.dia_inicio.weekday()),
                            "hora_inicio": reading_info.dia_inicio.strftime('%H:%M'),
                            "hora_fin": reading_info.dia_fin.strftime('%H:%M')
                        }
                        myData.append(dataInfo)
        elif (option==2):
            readings = Promedio_luminosidad.objects.filter(dia_inicio__range=[date_begin,date_end])

            if (readings):
                for reading_info in readings:
                    # Revisa si la lectura es de entre las 7 am y las 7 pm
                    if ((reading_info.dia_inicio.hour >= 7) and (reading_info.dia_inicio.hour < 19)):
                        dataInfo = {
                            "value": str(reading_info.lum),
                            "fuente": reading_info.lum_object,
                            "fecha": reading_info.dia_inicio.strftime('%d/%m/%Y'),
                            "dia_semana": str(reading_info.dia_inicio.weekday()),
                            "hora_inicio": reading_info.dia_inicio.strftime('%H:%M'),
                            "hora_fin": reading_info.dia_fin.strftime('%H:%M')
                        }
                        myData.append(dataInfo)
        elif (option==3):
            readings = Promedio_presencia.objects.filter(dia_inicio__range=[date_begin,date_end])

            if (readings):
                for reading_info in readings:
                    # Revisa si la lectura es de entre las 7 am y las 7 pm
                    if ((reading_info.dia_inicio.hour >= 7) and (reading_info.dia_inicio.hour < 19)):
                        dataInfo = {
                            "value": str(reading_info.mov),
                            "fecha": reading_info.dia_inicio.strftime('%d/%m/%Y'),
                            "dia_semana": str(reading_info.dia_inicio.weekday()),
                            "hora_inicio": reading_info.dia_inicio.strftime('%H:%M'),
                            "hora_fin": reading_info.dia_fin.strftime('%H:%M')
                        }
                        myData.append(dataInfo)
            
        #print(myData)
        # Envia los datos de esa semana
        self.send(text_data=json.dumps({
                'type': 'user_request',
                'request': option,
                'weeks': week // 7,
                'date_begin': date_begin.strftime('%d/%m/%Y'),
                'date_end': date_end.strftime('%d/%m/%Y'),
                'message': myData}))
    
    # Esta funcion recibe mensajes del WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print ("Opcion seleccionada: " + str(message))

        if ((message>=0) and (message<=3)):
            self.get_previousweek_data(message,0)
            #self.get_previousweek_data(message,7)
            #self.get_previousweek_data(message,14)
