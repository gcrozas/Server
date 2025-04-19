# Server
Servidor para la interconexión de dispositivos IoT de los laboratorios de las Escuelas de Ingeniería Informática y Civil de la UCAB Guayana.

## Componentes utilizados para la construcción del prototipo y su aplicación

- Raspberry Pi 4 Modelo B (como servidor local y bróker MQTT)
- Arduino UNO R3 y MEGA 2560 R3 (Como controladores de los actuadores y sensores en el interior del laboratorio)
- ESP8266 NodeMCU (Como controlador de los sensores en el exterior del laboratorio)
- Sensor de luz LDR no lineal
- Sensor de agua ER-CT0042CWS
- Módulo de relé de 4 canales
- DIP Switch de 4 posiciones
- Sensores digitales de temperatura y humedad DHT11 y DHT22
- Sensor PIR de movimiento HC-SR501

## Tecnologías utilizdas
- Django (Python 3)
- Django Channels (Websockets)
- Daphne (ASGI)
- MQTT (Librería Paho-mqtt)
- HTML/CSS/JS para la interfaz de usuario
- Comunicación I2C (Librería Smbus2)
- Cronograma de tareas (Librería Django celery-beat)
- Sistema de caché con Redis (Librería Django-redis)
- Celery (Tareas asíncronas)
- JSON
- Pillow (Soporte para gestión de imágenes)
- Xlwt (Genera archivos en Microsoft Excel versiones de 95 y 2003)
- Datetime (Gestión de fecha y hora)
- Time (Funciones relacionadas con el tiempo)

## ¿Por qué lo hice?

Este proyecto refleja mi interés por la robótica, el IoT y el desarrollo de software que interactúa con hardware real. Fue una experiencia completa donde combiné conocimientos de redes, backend, protocolos de comunicación y sistemas iot.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Puedes usarlo, modificarlo y compartirlo libremente, siempre y cuando me des el crédito correspondiente.

© 2025 GabrielaRozas
