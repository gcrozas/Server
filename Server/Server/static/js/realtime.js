const days_of_week = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

class custom_datetime {
    constructor(ms_datetime){ //Constructor de la clase
        // Cuerpo/propiedades de la clase
        this.day = days_of_week[ms_datetime.getDay()] //Retorna un dia de la semana (del 0-6)
        this.date = ms_datetime.getDate(); //Retorna un dia del mes (del 1-31)
        this.month = ms_datetime.getMonth() + 1; //Retorna el mes (del 0-11)
        this.year = ms_datetime.getFullYear(); //Retorna el anio
        this.hour = ms_datetime.getHours(); //Retorna la hora (de 0-23)
        this.minute = ms_datetime.getMinutes() //Retorna los minutos (de 0-59)
    }
}

function setGaugeValue(gauge, value) {
    if ((value >= 0) && (value <= 30)){
        gauge_value = 1;
        gauge_text = "Muy fuerte (" + value + ")";
    } else if ((value > 30) && (value <= 102)){
        gauge_value = 0.75;
        gauge_text = "Fuerte (" + value + ")";
    } else if ((value > 102) && (value <= 153)) {
        gauge_value = 0.5;
        gauge_text = "Media (" + value + ")";
    } else if ((value > 153) && (value <= 204)){
        gauge_value = 0.25;
        gauge_text = "Debil (" + value + ")";
    } else if ((value > 204) && (value <= 255)){
        gauge_value = 0;
        gauge_text = "Nula (" + value + ")";
    }
    /* Rotar entre 0 y 1*/
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${gauge_value / 2}turn)`;
    gauge.querySelector(".gauge__cover").textContent = gauge_text;
}

function setGaugeValueTemp(gauge, value) {
    if (value < 5) {
        ggauge_value = 0;
        gauge_text = "Muy bajo (" + value + " °C" + ")";
    } else if ((value >= 5) && (value < 21)){
        gauge_value = 0.25;
        gauge_text = "Bajo (" + value + " °C" + ")";
    } else if (value == 21){
        gauge_value = 0.5;
        gauge_text = "Normal (" + value + " °C" + ")";
    } else if ((value > 21) && (value <= 25)){
        gauge_value = 0.5;
        gauge_text = "Alto (" + value + " °C" + ")";
    } else if (value > 25) {
        gauge_value = 1;
        gauge_text = "Muy alto (" + value + " °C" + ")";
    }
    /* Rotar entre 0 y 1*/
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${gauge_value / 2}turn)`;
    gauge.querySelector(".gauge__cover").textContent = gauge_text;
}

function setGaugeValueHum(gauge, value) {
    if (value < 85){
        gauge_value = 0;
        gauge_text = "Normal (" + value + "%" + ")";
    } else {
        gauge_value = 1;
        gauge_text = "Alto (" + value + "%" + ")";
    }
    /* Rotar entre 0 y 1*/
    gauge.querySelector(".gauge__fill").style.transform = `rotate(${gauge_value / 2}turn)`;
    gauge.querySelector(".gauge__cover").textContent = gauge_text;
}

function ceiling_event(checkboxElem) {
    if (checkboxElem.checked) {
        option_selected = 21;
        console.log("Lampara del techo encendida!");
        document.getElementById('lum_seccion2-log').innerHTML = "Encendido";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    } else {
        option_selected = 20;
        console.log("Lampara del techo apagada!");
        document.getElementById('lum_seccion2-log').innerHTML = "Apagado";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    }
}

function desk_event(checkboxElem) {
    if (checkboxElem.checked) {
        option_selected = 11;
        console.log("Lampara de mesa encendida!");
        document.getElementById('lum_seccion1-log').innerHTML = "Encendido";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    } else {
        option_selected = 10;
        console.log("Lampara de mesa apagada!");
        document.getElementById('lum_seccion1-log').innerHTML = "Apagado";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    }
}

function ac1_event(checkboxElem) {
    if (checkboxElem.checked) {
        option_selected = 31;
        console.log("Aire acondicionado 1 encendido!")
        document.getElementById('ac1-log').innerHTML = "Encedido";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    } else {
        option_selected = 30;
        console.log("Aire acondicionado 1 apagado!");
        document.getElementById('ac1-log').innerHTML = "Apagado";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    }
}

function ac2_event(checkboxElem) {
    if (checkboxElem.checked) {
        option_selected = 41;
        console.log("Aire acondicionado 2 encendido!")
        document.getElementById('ac2-log').innerHTML = "Encendido";
        socket.send(JSON.stringify({
            'type': "action_event",
            'message': option_selected
        }));
    } else {
        option_selected = 40;
        console.log("Aire acondicionado 2 apagado!");
        document.getElementById('ac2-log').innerHTML = "Apagado";
        socket.send(JSON.stringify({
            'type': 'action_event',
            'message': option_selected
        }));
    }
}


var socket = new WebSocket('ws://' + window.location.host + '/ws/lab-one/')

socket.onmessage = function(event) {
    var djangoData = JSON.parse(event.data);
    var event_update = djangoData.event_update;
    
    console.log(event_update);
    console.log(djangoData);
    console.log("========");

    if (event_update==='Temperatura exterior'){
        var temp = djangoData.temp_ext;
        var js_datetime = new Date(djangoData.iso_datetime)

        datetime_log = new custom_datetime(js_datetime)
        js_date = datetime_log.date + '/' + datetime_log.month + '/' + datetime_log.year
        js_time = datetime_log.hour + ':' + ((datetime_log.minute)<10?'0':'') + datetime_log.minute
        last_update = js_date + ' ' + js_time;

        document.getElementById('ext_datetime-log').innerHTML = "Actualizado: " + last_update;
        document.getElementById('ext_temp-log').innerHTML = temp + '°C';

    imprimir = js_date + ' ' + js_time;
    } else if (event_update==='Humedad exterior'){
        var hum = djangoData.hum_ext;
        document.getElementById('ext_hum-log').innerHTML = hum + '%';
    } else if (event_update==='Humedad del piso'){
        var floor = djangoData.hum_floor;
        floorDiv = document.getElementById('floorDiv');

        if(floor==0){
            document.getElementById('floor-log').innerHTML = "Seco";
            floorDiv.style.backgroundColor = '#4CAF50';
        } else if (floor==1){
            document.getElementById('floor-log').innerHTML = "Mojado";
            floorDiv.style.backgroundColor = '#D0312D';
        }
    } else if (event_update==='Datos del laboratorio'){
        var temp = djangoData.temperature;
        var hum = djangoData.humidity;
        var js_mov = djangoData.presence;
        var js_lum1 = djangoData.lum1;
        var js_lum2 = djangoData.lum2;
        var js_door = djangoData.door;
        var js_ac1 = djangoData.ac1;
        var js_ac2 = djangoData.ac2;
        var js_datetime = new Date(djangoData.iso_datetime)

        datetime_log = new custom_datetime(js_datetime)
        js_date = datetime_log.date + '/' + datetime_log.month + '/' + datetime_log.year
        js_time = datetime_log.hour + ':' + ((datetime_log.minute)<10?'0':'') + datetime_log.minute

        last_update = js_date + ' ' + js_time;

        document.getElementById('datetime-log').innerHTML = "Actualizado: " + last_update;
        document.getElementById('temp-log').innerHTML = temp + '°C';
        document.getElementById('hum-log').innerHTML = hum + '%';
        
        const gaugeTemp = document.querySelector(".gauge3");
        const gaugeHum = document.querySelector(".gauge4");

        setGaugeValueTemp(gaugeTemp,temp);
        setGaugeValueHum(gaugeHum,hum);

        movDiv = document.getElementById('movDiv');
        doorDiv = document.getElementById('doorDiv');
        lum1Div = document.getElementById('lumiDiv-1');
        lum2Div = document.getElementById('lumiDiv-2');
        ac1Div = document.getElementById('ac1Div');
        ac2Div = document.getElementById('ac2Div');

        if(js_mov==0){
            document.getElementById('mov-log').innerHTML = "No";
            movDiv.style.backgroundColor = '#D0312D';
        } else if (js_mov==1){
            document.getElementById('mov-log').innerHTML = "Si";
            movDiv.style.backgroundColor = '#4CAF50';
        }

        if(js_door==0){
            document.getElementById('door-log').innerHTML = "Desbloqueado";
            doorDiv.style.backgroundColor = '#D0312D';
        } else if (js_door==1){
            document.getElementById('door-log').innerHTML = "Bloqueado";
            doorDiv.style.backgroundColor = '#4CAF50';
        }

        /* Estado del boton asociado a la luz de la mesa */
        if ((js_lum1>=0) && (js_lum1<=30)){
            document.getElementById('desk-switch').checked = true;
            document.getElementById('lum_seccion1-log').innerHTML = "Encendido";
        } else if ((js_lum1>30) && (js_lum1<=255)) {
            document.getElementById('desk-switch').checked = false;
            document.getElementById('lum_seccion1-log').innerHTML = "Apagado";
        }

        const gaugeElement_desk = document.querySelector(".gauge1");
        const gaugeElement_ceiling = document.querySelector(".gauge2");

        setGaugeValue(gaugeElement_desk,js_lum1);
        setGaugeValue(gaugeElement_ceiling,js_lum2);

        /* Estado del boton asociado a la luz del techo */
        if ((js_lum2>=0) && (js_lum2<=30)){
            document.getElementById('ceiling-switch').checked = true;
            document.getElementById('lum_seccion2-log').innerHTML = "Encendido";
        } else if ((js_lum2>30) && (js_lum2<=255)){
            document.getElementById('ceiling-switch').checked = false;
            document.getElementById('lum_seccion2-log').innerHTML = "Apagado";
        }

        if(js_ac1==0){
            document.getElementById('ac1-log').innerHTML = "Apagado";
            document.getElementById('ac1-switch').checked = false;
        } else if (js_ac1==1){
            document.getElementById('ac1-log').innerHTML = "Encendido";
            document.getElementById('ac1-switch').checked = true;
        }

        if(js_ac2==0){
            document.getElementById('ac2-log').innerHTML = "Apagado";
            document.getElementById('ac2-switch').checked = false;
        } else if (js_ac2==1){
            document.getElementById('ac2-log').innerHTML = "Encendido";
            document.getElementById('ac2-switch').checked = true;
        }
    }
}