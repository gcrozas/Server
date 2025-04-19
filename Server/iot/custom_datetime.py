from datetime import date, timedelta, datetime

def get_date(days_ago):
    # Obtenemos la fecha de hoy
    today = date.today()
    # Obtenemos la fecha que queremos
    day_before = today - timedelta(days = days_ago)
    return day_before

def get_inicial():
    # Obtenemos la hora actual
    now = datetime.now()
    # Obtenemos la hora inicial
    inicial = now.replace(minute=0,second=0,microsecond=0)
    return inicial

def get_hour(hours_ago):
    # Obtenemos la hora actual
    now = datetime.now()
    # Obtenemos la hora anterior
    hour_before = now - timedelta(hours= hours_ago)
    return hour_before

def get_week_month(date_data):
    week_month = datetime.isocalendar(date_data)
    return str(week_month)

if __name__ == "__main__":
    last_week = 7
    yesterday = 1
    print("Esto es una prueba")
    print("Fecha de hoy: " + str(date.today()))
    print("Fecha de ayer: " + str(get_date(yesterday)))
    print("Fecha de hace una semana: " + str(get_date(last_week)))
    print("Hora inicial: " + get_inicial().strftime('%H:%M'))
    print("Hora final: " + datetime.now().strftime('%H:%M'))
    print("Hace una hora eran las: " + str(get_hour(1).hour))
    print("Hace una hora eran las: " + get_hour(1).strftime('%d/%m/%y - %H:%M'))
    print("Dia de la semana del calendario: " + get_week_month(datetime.now()))

