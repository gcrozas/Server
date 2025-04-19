from django.db import models
from django.utils import timezone
import pytz

timezone.activate(pytz.timezone('America/Caracas'))
days_of_week = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

# MQTT
class Temperatura_exterior(models.Model):
    temp = models.CharField(max_length=2)
    dia_hora_leida = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Temperatura exterior")
        verbose_name_plural = ("Temperatura exterior")
        get_latest_by = ("dia_hora_leida")
    
    def __str__(self):
        #return days_of_week[self.dia_hora_leida.weekday()] + ' - ' + self.dia_hora_leida.strftime('%d/%m/%Y') + ' - ' + self.dia_hora_leida.strftime('%H:%M') + ' - ' + self.temp + ' C'
        return days_of_week[self.dia_hora_leida.weekday()] + ' - ' + self.dia_hora_leida.strftime('%d/%m/%Y') + ' - ' + self.dia_hora_leida.strftime('%H:%M') + ' - ' + self.temp + ' C'

class Humedad_exterior(models.Model):
    hum = models.CharField(max_length=2)
    dia_hora_leida = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Humedad exterior")
        verbose_name_plural = ("Humedad exterior")
        get_latest_by = ("dia_hora_leida")
    
    def __str__(self):
        return days_of_week[self.dia_hora_leida.weekday()] + ' - ' + self.dia_hora_leida.strftime('%d/%m/%Y') + ' - ' + self.dia_hora_leida.strftime('%H:%M') + ' - ' + self.hum + ' %'

class Humedad_piso(models.Model):
    mojado = models.CharField(max_length=1)
    dia_hora_leida = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Humedad del suelo")
        verbose_name_plural = ("Humedad del suelo")
        get_latest_by = ("dia_hora_leida")
    
    def __str__(self):
        if (self.mojado=='1'):
            estado = 'Mojado'
        elif (self.mojado=='0'):
            estado = 'Seco'
        else:
            estado = 'Error'
        return days_of_week[self.dia_hora_leida.weekday()] + ' - ' + self.dia_hora_leida.strftime('%d/%m/%Y') + ' - ' + self.dia_hora_leida.strftime('%H:%M') + ' - ' + estado

# I2C

class Interior(models.Model):
    temp = models.CharField(max_length=2)
    hum = models.CharField(max_length=2)
    presencia = models.CharField(max_length=1)
    lum_1 = models.CharField(max_length=3)
    lum_2 = models.CharField(max_length=3)
    seg_puerta = models.CharField(max_length=1)
    AC_1 = models.CharField(max_length=1)
    AC_2 = models.CharField(max_length=1)
    dia_hora_leida = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Interior del laboratorio")
        verbose_name_plural = ("Interior del laboratorio")
        get_latest_by = ("dia_hora_leida")
    
    def __str__(self):
        return days_of_week[self.dia_hora_leida.weekday()] + ' - ' + self.dia_hora_leida.strftime('%d/%m/%Y') + ' - ' + self.dia_hora_leida.strftime('%H:%M') + ' - ' + self.temp + ' C' + ' - ' + self.hum + ' %' + ' - ' + self.presencia

# Promedios
class Promedio_temperatura(models.Model):
    temp = models.CharField(max_length=2)
    dia_inicio = models.DateTimeField(auto_now_add=False)
    dia_fin = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Historico de la temperatura")
        verbose_name_plural = ("Historico de la temperatura")
        get_latest_by = ("dia_fin")
        ordering = ['-dia_fin']
    
    def __str__(self):
        return days_of_week[self.dia_inicio.weekday()] + ' - ' + self.dia_inicio.strftime('%d/%m/%Y') + ' - ' + self.dia_inicio.strftime('%H:%M') + ' - ' + self.dia_fin.strftime('%H:%M') + ' - ' + self.temp + ' C'

class Promedio_humedad(models.Model):
    hum = models.CharField(max_length=2)
    dia_inicio = models.DateTimeField(auto_now_add=False)
    dia_fin = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Historico de la humedad")
        verbose_name_plural = ("Historico de la humedad")
        get_latest_by = ("dia_fin")
        ordering = ['-dia_fin']
    
    def __str__(self):
        return days_of_week[self.dia_inicio.weekday()] + ' - ' + self.dia_inicio.strftime('%d/%m/%Y') + ' - ' + self.dia_inicio.strftime('%H:%M') + ' - ' + self.dia_fin.strftime('%H:%M') + ' - ' + self.hum + ' %'

class Promedio_luminosidad(models.Model):
    lum_object = models.CharField(max_length=24)
    lum = models.CharField(max_length=3)
    dia_inicio = models.DateTimeField(auto_now_add=False)
    dia_fin = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Historico de la luminosidad")
        verbose_name_plural = ("Historico de la luminosidad")
        get_latest_by = ("dia_fin")
        ordering = ['-dia_fin']
    
    def __str__(self):
        return days_of_week[self.dia_inicio.weekday()] + ' - ' + self.dia_inicio.strftime('%d/%m/%Y') + ' - ' + self.lum_object + ' - ' + self.dia_inicio.strftime('%H:%M') + ' - ' + self.dia_fin.strftime('%H:%M') + ' - ' + self.lum

class Promedio_presencia(models.Model):
    mov = models.CharField(max_length=1)
    dia_inicio = models.DateTimeField(auto_now_add=False)
    dia_fin = models.DateTimeField(auto_now_add=False)

    class Meta:
        verbose_name = ("Historico de presencia")
        verbose_name_plural = ("Historico de presencia")
        get_latest_by = ("dia_fin")
        ordering = ['-dia_fin']
    
    def __str__(self):
        if (self.mov=='1'):
            estado = 'Si'
        elif (self.mov=='0'):
            estado = 'No'
        else:
            estado = 'Error'
        return days_of_week[self.dia_inicio.weekday()] + ' - ' + self.dia_inicio.strftime('%d/%m/%Y') + ' - ' + self.dia_inicio.strftime('%H:%M') + ' - ' + self.dia_fin.strftime('%H:%M') + ' - ' + estado
