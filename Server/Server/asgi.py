"""
ASGI config for Server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

from iot.routing import ws_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

#application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket':AuthMiddlewareStack(
            URLRouter(ws_urlpatterns),
        )
        # Agregar otros protocolos de comunicacion
    }
)