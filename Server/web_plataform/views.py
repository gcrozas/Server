# web_plataform/wiews.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.template.defaulttags import register
import xlwt
from django.http import HttpResponse
from datetime import datetime
from iot.models import Promedio_temperatura, Promedio_humedad, Promedio_presencia, Promedio_luminosidad

days_of_week = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
months_of_year = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Noviembre", "Diciembre"]

#Vistas
def home(request):
	return render(request,'home.html')

@login_required(login_url='/login/')
def backup(request):
	if request.user.is_superuser:
		return render(request,'backup.html',{'title':'Backup'})
	else:
		return render(request,'home.html')

@login_required(login_url='/login/')
def export_excel(request):
    if request.user.is_superuser:
        nombre_archivo = "registro_lab_prototipos_" + (datetime.now()).strftime('%d/%m/%Y') + ".xls"
        
        response = HttpResponse(content_type="application/ms-excel")
        
        contenido = "attactment; filename = {0}".format(nombre_archivo)
        
        response['Content-Disposition']= contenido
        
        wb = xlwt.Workbook(encoding='uft-8')
        style = xlwt.XFStyle()
        
        # Agregamos la primera hoja
        
        ws = wb.add_sheet('Temperatura')
        row_num = 0
        
        # Tipo de letra
        font = xlwt.Font()
        font.bold = True #negrita
        style.font = font
        
        # bordes
        borders = xlwt.Borders()
        borders.bottom = xlwt.Borders.DASHED
        style.borders = borders
        
        columns = ['Dia de semana','Fecha','Hora inicio','Hora fin','Temperatura (C)']
        
        for col_num in range(len(columns)):
            # Escribiendo en las celdas de la primera fila
            ws.write(row_num, col_num, columns[col_num],style=style)
        
        font_style = xlwt.XFStyle()
        
        rows = Promedio_temperatura.objects.order_by('dia_inicio').all()
        
        for row in rows:
            row_num += 1
            ws.write(row_num,0,str(days_of_week[row.dia_inicio.weekday()]),font_style)
            ws.write(row_num,1,row.dia_inicio.strftime('%d/%m/%Y'),font_style)
            ws.write(row_num,2,row.dia_inicio.strftime('%H:%M'),font_style)
            ws.write(row_num,3,row.dia_fin.strftime('%H:%M'),font_style)
            ws.write(row_num,4,str(row.temp),font_style)
        
        ws = wb.add_sheet('Humedad')
        row_num = 0
        
        columns = ['Dia de semana','Fecha','Hora inicio','Hora fin','Humedad (%)']
        
        for col_num in range(len(columns)):
            # Escribiendo en las celdas de la primera fila
            ws.write(row_num, col_num, columns[col_num],style=style)
        
        rows = Promedio_humedad.objects.order_by('dia_inicio').all()
        
        for row in rows:
            row_num += 1
            ws.write(row_num,0,str(days_of_week[row.dia_inicio.weekday()]),font_style)
            ws.write(row_num,1,row.dia_inicio.strftime('%d/%m/%Y'),font_style)
            ws.write(row_num,2,row.dia_inicio.strftime('%H:%M'),font_style)
            ws.write(row_num,3,row.dia_fin.strftime('%H:%M'),font_style)
            ws.write(row_num,4,str(row.hum),font_style)
        
        ws = wb.add_sheet('Luminosidad (Seccion 1)')
        row_num = 0
        
        columns = ['Dia semana','Fecha','Hora inicio','Hora fin','Nivel de luz','Encendido/Apagado']
        
        for col_num in range(len(columns)):
            # Escribiendo en las celdas de la primera fila
            ws.write(row_num, col_num, columns[col_num],style=style)
        
        rows = Promedio_luminosidad.objects.filter(lum_object__icontains="Seccion 1").order_by('dia_inicio')
        
        for row in rows:
            row_num += 1
            ws.write(row_num,0,str(days_of_week[row.dia_inicio.weekday()]),font_style)
            ws.write(row_num,1,row.dia_inicio.strftime('%d/%m/%Y'),font_style)
            ws.write(row_num,2,row.dia_inicio.strftime('%H:%M'),font_style)
            ws.write(row_num,3,row.dia_fin.strftime('%H:%M'),font_style)
            
            lum_value = int(row.lum)
            
            if ((lum_value >= 0) and (lum_value <= 30)):
                ws.write(row_num,4,'Muy fuerte',font_style)
                ws.write(row_num,5,'Encendido',font_style)
            elif ((lum_value > 30) and (lum_value <= 102)):
                ws.write(row_num,4,'Fuerte',font_style)
                ws.write(row_num,5,'Apagado',font_style)
            elif ((lum_value > 102) and (lum_value <= 153)):
                ws.write(row_num,4,'Media',font_style)
                ws.write(row_num,5,'Apagado',font_style)
            elif ((lum_value > 153) and (lum_value <= 204)):
                ws.write(row_num,4,'Debil',font_style)
                ws.write(row_num,5,'Apagado',font_style)
            elif ((lum_value > 204) and (lum_value <= 255)):
                ws.write(row_num,4,'Nula',font_style)
                ws.write(row_num,5,'Apagado',font_style)
        
        ws = wb.add_sheet('Luminosidad (Seccion 2)')
        row_num = 0
        
        columns = ['Dia semana','Fecha','Hora inicio','Hora fin','Nivel de luz','Encendido/Apagado']
        
        for col_num in range(len(columns)):
            # Escribiendo en las celdas de la primera fila
            ws.write(row_num, col_num, columns[col_num],style=style)
        
        rows = Promedio_luminosidad.objects.filter(lum_object__icontains="Seccion 2").order_by('dia_inicio')
        
        for row in rows:
            row_num += 1
            ws.write(row_num,0,str(days_of_week[row.dia_inicio.weekday()]),font_style)
            ws.write(row_num,1,row.dia_inicio.strftime('%d/%m/%Y'),font_style)
            ws.write(row_num,2,row.dia_inicio.strftime('%H:%M'),font_style)
            ws.write(row_num,3,row.dia_fin.strftime('%H:%M'),font_style)
            
            lum_value = int(row.lum)
            
            if ((lum_value >= 0) and (lum_value <= 30)):
                ws.write(row_num,4,'Muy fuerte',font_style)
                ws.write(row_num,5,'Encendido',font_style)
            elif ((lum_value > 30) and (lum_value <= 102)):
                ws.write(row_num,4,'Fuerte',font_style)
                ws.write(row_num,5,'Apagado',font_style)
            elif ((lum_value > 102) and (lum_value <= 153)):
                ws.write(row_num,4,'Media',font_style)
                ws.write(row_num,5,'Apagado',font_style)
            elif ((lum_value > 153) and (lum_value <= 204)):
                ws.write(row_num,4,'Debil',font_style)
                ws.write(row_num,5,'Apagado',font_style)
            elif ((lum_value > 204) and (lum_value <= 255)):
                ws.write(row_num,4,'Nula',font_style)
                ws.write(row_num,5,'Apagado',font_style)
        
        ws = wb.add_sheet('Presencia')
        row_num = 0
        
        columns = ['Dia semana','Fecha','Hora inicio','Hora fin','Presencia']
        
        for col_num in range(len(columns)):
            # Escribiendo en las celdas de la primera fila
            ws.write(row_num, col_num, columns[col_num],style=style)
        
        rows = Promedio_presencia.objects.order_by('dia_inicio').all()
        
        for row in rows:
            row_num += 1
            ws.write(row_num,0,str(days_of_week[row.dia_inicio.weekday()]),font_style)
            ws.write(row_num,1,row.dia_inicio.strftime('%d/%m/%Y'),font_style)
            ws.write(row_num,2,row.dia_inicio.strftime('%H:%M'),font_style)
            ws.write(row_num,3,row.dia_fin.strftime('%H:%M'),font_style)
            if (int(row.mov)==1):
                ws.write(row_num,4,'Si',font_style)
            else:
                ws.write(row_num,4,'No',font_style)
        
        # Guardamos el archivo
        wb.save(response)
        return response
    else:
        return render(request,'home.html')
	

def about(request):
	return render(request,'about.html',{'title':'About'})

@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)
