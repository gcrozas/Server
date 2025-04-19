from django.contrib import admin
from .models import Perfil
from iot.admin import server_site

server_site.register(Perfil)