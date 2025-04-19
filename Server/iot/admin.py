from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group

from .models import Temperatura_exterior, Humedad_exterior, Humedad_piso 
from .models import Interior, Promedio_temperatura, Promedio_luminosidad, Promedio_presencia, Promedio_humedad
	
class ServerAdminArea(admin.AdminSite):
    site_header = 'Servidor IoT - Area Administrativa'
    site_title = 'Servidor IoT'
    index_title = 'Laboratorio'

server_site = ServerAdminArea(name='ServerAdmin')

server_site.register(Temperatura_exterior)
server_site.register(Humedad_exterior)
server_site.register(Humedad_piso)
server_site.register(Interior)
server_site.register(User)
server_site.register(Group)
server_site.register(Promedio_temperatura)
server_site.register(Promedio_humedad)
server_site.register(Promedio_luminosidad)
server_site.register(Promedio_presencia)
