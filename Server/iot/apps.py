from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
class ServerAdminConfig(AdminConfig):
    default_site = 'iot.admin.ServerAdminArea'
class IotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iot'