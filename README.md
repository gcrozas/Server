## Server
Servidor para la interconexión de dispositivos IoT de los laboratorios de las Escuelas de Ingeniería Informática y Civil de la UCAB Guayana.

## Objetivo general
Desarrollar un servidor para la interconexión de dispositivos IoT de los laboratorios de las Escuelas de Ingeniería Informática y Civil de la UCAB Guayana.

## Objetivos específicos
-	Caracterizar los requerimientos en el laboratorio de Desarrollo de Aplicaciones Móviles y Multimedia, y el laboratorio de Ingeniería Sanitaria.
-	Diseñar un servidor que interactúe con los dispositivos y usuarios, y que gestione la información recibida.
-	Construir un servidor que permita la interconexión entre dispositivos IoT y usuarios.
-	Validar el funcionamiento del sistema a través de un prototipo.
-	Elaborar la documentación formal del sistema.

## Alcance
La solución propuesta consiste en un proyecto de Ingeniería Informática, en el cual se desarrolló un prototipo que simula las condiciones del laboratorio de Ingeniería Sanitaria de la Escuela de Ingeniería Civil y el laboratorio de Desarrollo de Aplicaciones Móviles y Multimedia de la Escuela de Informática, de la UCAB Guayana.

Para el prototipo se desarrolló un servidor local, conectado a sensores y actuadores.

## Limitaciones
Por motivos externos se desarrolló un prototipo en dos ambientes similares, con algunas diferencias. Inicialmente, se empezó a desarrollar el prototipo en Venezuela de manera presencial, donde se estaba cerca de los laboratorios, se podía interactuar de manera inmediata con los tutores, tanto académico como el industrial, al igual que se tenían más recursos y apoyo disponibles. Posteriormente, se continuó trabajando con el mismo prototipo en Chile, bajo otras condiciones, donde las consultas se realizaban de forma remota.

## Componentes utilizados para la construcción del prototipo y su aplicación
- Raspberry Pi 4 Modelo B (como servidor local y bróker MQTT)
- Arduino UNO R3 y MEGA 2560 R3 (que actuan como controladores de los actuadores y sensores en el interior del laboratorio)
- ESP8266 NodeMCU (como controlador de los sensores en el exterior del laboratorio)
- Sensor de luz LDR no lineal
- Sensor de agua ER-CT0042CWS
- Módulo de relé de 4 canales
- DIP Switch de 4 posiciones
- Sensores digitales de temperatura y humedad DHT11 y DHT22
- Sensor PIR de movimiento HC-SR501

## Tecnologías utilizadas

**Backend y servidor**
- Django (Python 3)
- Django Channels (Websockets)
- Daphne (ASGI)
- Celery + Redis (Gestión de tareas asíncronas)
- Django celery-beat (Cronograma de tareas para los actuadores)
- Django-redis
- JSON
- Datetime, Time
- Pillow (gestión de imágenes)
- Xlwt (exportación a Excel)

**Protocolos de comunicación**
- MQTT (Paho-mqtt)
- Comunicación I2C (Smbus2)
- Websockets (Django Channels)

**Frontend**
- HTML / CSS / JavaScript

## Vista del prototipo

(foto aquí)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Puedes usarlo, modificarlo y compartirlo libremente, siempre y cuando me des el crédito correspondiente.

© 2025 GabrielaRozas
