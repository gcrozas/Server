function draw_columnChart(request,prom_week,prom_week2,elementID){
    var data = new google.visualization.DataTable();

    //Definir datos de la grafica
    data.addColumn('string','Dia');

    if (request == 2){
        if (elementID == 'result_graph'){
            data.addColumn('number','Nivel (Seccion 1)');
            data.addColumn('number','Nivel (Seccion 2)');
            vAxis_title = 'Nivel de luminosidad';
            min_data = 0;
            max_data = 255;
            vAxis_count = 5;
        } else {
            data.addColumn('number','Horas (Seccion 1)');
            data.addColumn('number','Horas (Seccion 2)');
            vAxis_title = 'Horas de encendido';
            min_data = 0;
            max_data = 12;
            vAxis_count = 2;
        }

        chart_table = [
            ['Lunes',prom_week[0],prom_week2[0]],
            ['Martes',prom_week[1],prom_week2[1]],
            ['Miercoles',prom_week[2],prom_week2[2]],
            ['Jueves',prom_week[3],prom_week2[3]],
            ['Viernes',prom_week[4],prom_week2[4]]
        ];
    } else {
        data.addColumn('number','Horas');
        chart_table = [
            ['Lunes',prom_week[0]],
            ['Martes',prom_week[1]],
            ['Miercoles',prom_week[2]],
            ['Jueves',prom_week[3]],
            ['Viernes',prom_week[4]]
        ];
        vAxis_title = 'Horas de presencia';
        vAxis_count = 2;
        min_data = 0;
        max_data = 12;
    }

    data.addRows(chart_table);

    //Opciones
    var options = {
        'title': "Promedio de la semana",
        hAxis: {
            title: 'Dia de la semana (Lunes a viernes)'
        },
        vAxis: {
            title: vAxis_title,
            gridlines: { count: vAxis_count},
            viewWindow : {
                min: min_data,
                max: max_data
            }
        },
        'width':1100,
        'height':700,
    };

    //Dibuja la grafica
    var chart = new google.visualization.ColumnChart(document.getElementById(elementID));
    chart.draw(data, options);
}

function draw_lineChart(request,prom_week){

    var data = new google.visualization.DataTable();

    //Definir datos de la grafica
    switch(request){
        case 0:
            graph_label = 'Temperatura (°C)';
            hex_color = '#ff3333';
            datos = 'Temp';
            max_result = 21;
            min_value = 10;
            max_value = 40;
            break;
        case 1:
            graph_label = 'Humedad (%)';
            hex_color = '#3399ff';
            datos = 'Hum';
            max_result = 85;
            min_value = 0;
            max_value = 100;
            break;
    }

    data.addColumn('string','Dia');
    data.addColumn('number',graph_label);
    data.addColumn('number','Limite');
    
    
    data.addRows([
        ['Lunes',prom_week[0],max_result],
        ['Martes',prom_week[1],null],
        ['Miercoles',prom_week[2],null],
        ['Jueves',prom_week[3],null],
        ['Viernes',prom_week[4],max_result]
    ]);

    //Opciones
    var options = {
        'title': "Promedio semanal",
        hAxis: {
            title: 'Dia de la semana (Lunes a viernes)'
        },
        vAxis: {
            title: graph_label,
            gridlines: { count: 4},
            viewWindow : {
                min: min_value,
                max: max_value
            }
        },
        series: {
            0: {color: hex_color},
            1: {lineDashStyle: [2,2,20,2,20,2],
                lineWidth: 2,
                color: '#333333'}
        }, 
        'width':1100,
        'height':700,
        curveType: 'function',
        pointsVisible: true,
        interpolateNulls: true,
        crosshair: {
            color: '#000',
            trigger: 'selection'
        }
    };

    //Dibuja la grafica
    var chart = new google.visualization.LineChart(document.getElementById('result_graph'));
    chart.draw(data, options);
}

function removeTable(){
    if (document.getElementById("myTable")){
        var tbl = document.getElementById("myTable");
        tbl.parentNode.removeChild(tbl);
    }

    if (document.getElementById("myTable_2")){
        var tbl = document.getElementById("myTable_2");
        tbl.parentNode.removeChild(tbl);
    }

    if (document.getElementById("myTable_3")){
        var tbl = document.getElementById("myTable_3");
        tbl.parentNode.removeChild(tbl);
    }

    if (document.getElementById("myTable_4")){
        var tbl = document.getElementById("myTable_4");
        tbl.parentNode.removeChild(tbl);
    }
}

function addText(date_begin, date_end){
    var p_text = document.getElementById("week");
    p_text.innerHTML = "Historico de la semana " + date_begin + " al " + date_end;
}

function deleteText(){
    var p_text = document.getElementById("week");    
}

function showInfo(){
    removeTable();
    var option_selected = document.getElementById("historical").selectedIndex;
    socket.send(JSON.stringify({
        'type': 'user_request',
        'message': option_selected
    }));
}

/* Para conocer el nivel de luz leido por el sensor */
function lightLevel(value){
    if ((value >= 0) && (value <= 30)){
        return "Muy fuerte";
    } else if ((value > 30) && (value <= 102)){
        return "Fuerte";
    } else if ((value > 102) && (value <= 153)) {
        return "Media";
    } else if ((value > 153) && (value <= 204)){
        return "Debil";
    } else if ((value > 204) && (value <= 255)){
        return "Nula";
    }
}

/* Para conocer si las luces estaban encendidas/apagadas segun el nivel de luz */
function lightStatus(value){
    if ((value>=0) && (value<=15)){
        return '1'; // Luces encendidas
    } else if ((value>15) && (value<=255)){
        return '0'; // Luces apagadas
    }
}

//Crea un array a partir de la fuente de luz que se desea encontrar (Ejemplo: Seccion)
function lights_order(event_data,find){
    var newArray = [];
    for (let i = 0; i < event_data.length; i++){
        if (event_data[i].fuente == find){
            newArray.push(event_data[i]);
        }
    }
    return newArray;
}

function addTable(tableContent, request, type_table, table_id){
    let week = ['','Lunes','Martes','Miércoles','Jueves','Viernes'];
    let hours_begin = ["07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00"];
    let hours_end = ["08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00"];
    
    /* Div en el que se insertara la nueva tabla */
    let tableDiv = document.getElementById(table_id);

    /* Datos para la grafica */
    var graph_data = [];

    switch(request){
        case 0:
            simbol_text = ' °C';
            break;
        case 1:
            simbol_text = ' %';
            break;
        default:
            simbol_text = '';
            break;
    }

    /*Crea la tabla */
    var table = document.createElement('table');

    switch(table_id){
        case 'historical_results':
            table.setAttribute('id', 'myTable');
            break;
        /* Tabla que contiene las veces que se encendio la luz del mesa */
        case 'historical_results_2':
            table.setAttribute('id', 'myTable_2');
            break;
        /* Tabla que contiene el nivel de luz del sensor cerca de la lampara de mesa */
        case 'historical_results_3':
            table.setAttribute('id', 'myTable_3');
            break;
        /* Tabla que contiene las veces que se encendio la luz del techo */
        case 'historical_results_4':
            table.setAttribute('id', 'myTable_4');
    }

    // Inserta un nuevo elemento row (fila) en el elemento table (tabla) */
    var row = table.insertRow(0);
    row.style.backgroundColor = '#0c67b1';
    row.style.color = 'white';

    /* Fila Lunes - Viernes */
    for (let i = 0; i < week.length; i++){
        var newCell = row.insertCell(i);
        newCell.innerHTML = week[i];
    }

    var row_number = 1; // Numero de fila
    var total_day = [0,0,0,0,0]; //Total del promedio por dia
    var total_register = [0,0,0,0,0]; //Numero de valores registrados por dia

    /* Iniciamos en la columna 0*/
    for (let m = 0; m < hours_begin.length; m++){
        /* Fila */
        // Casilla hora inicio - hora fin
        var row_2 = table.insertRow(row_number);
        var blank_space = row_2.insertCell(0);
        var week_day = 0;
        blank_space.innerHTML = hours_begin[m] + ' - ' + hours_end[m];
        // Columna en fila
        for (let j = 1; j < week.length; j++){
            var encontrado;
            encontrado = 0;
            var newCell = row_2.insertCell(j);
            for (let k = 0;k < tableContent.length; k++){
                // Si no ha encontrado el elemento correspondiente al horario
                if (encontrado == 0){
                    // Si corresponde al dia de la semana, la hora de inicio y la hora fin
                    if ((tableContent[k].dia_semana == week_day) && (tableContent[k].hora_inicio == hours_begin[m]) && (tableContent[k].hora_fin == hours_end[m])){
                        if ((request == 2) && (type_table == 1)) {
                            newCell.innerHTML = lightLevel(tableContent[k].value);
                            total_day[week_day] = total_day[week_day] + parseInt(tableContent[k].value);
                            total_register[week_day] = total_register[week_day] + 1;
                        } else if (((request == 2) && (type_table == 2))) {
                            light_status = lightStatus(tableContent[k].value);
                            if (light_status == '1') {
                                newCell.innerHTML = 'Si';
                                total_day[week_day] = total_day[week_day] + 1;
                                total_register[week_day] = total_register[week_day] + 1;
                            } else if (light_status == '0') {
                                newCell.innerHTML = 'No';
                                total_register[week_day] = total_register[week_day] + 1;
                            }
                        } else if (request == 3){
                            if (tableContent[k].value == '1') {
                                newCell.innerHTML = 'Si';
                                total_day[week_day] = total_day[week_day] + 1;
                                total_register[week_day] = total_register[week_day] + 1;
                            } else if (tableContent[k].value == '0') {
                                newCell.innerHTML = 'No';
                                total_register[week_day] = total_register[week_day] + 1;
                            }
                        } else {
                            newCell.innerHTML = tableContent[k].value + simbol_text;
                            total_day[week_day] = total_day[week_day] + parseInt(tableContent[k].value);
                            total_register[week_day] = total_register[week_day] + 1;
                        }
                        encontrado = 1; // Elemento encontrado
                    }
                }
                // Si la casilla esta vacia
                if (newCell.innerHTML == ''){
                    newCell.innerHTML = ' - ';
                }
            }
            week_day = week_day + 1;
        }
        row_number = row_number + 1;
    }

    var row3 = table.insertRow(row_number);
    row3.style.backgroundColor = '#1468ad';
    row3.style.color = 'white';

    var t = 0;

    var newCell = row3.insertCell(0);

    //Tabla y grafica de 'horas de presencia' y 'horas de encendido de la luz'
    if ((request == 3) || ((request == 2) && (type_table == 2))) {
        newCell.innerHTML = 'Total horas';
        for (let i = 1; i < week.length; i++){
            var newCell = row3.insertCell(i);
            if (total_register[t] == 0){
                newCell.innerHTML = ' - '; //Datos para la tabla
                graph_data.push(null); //Datos para la grafica
            } else {
                newCell.innerHTML = total_day[t]; //Datos para la tabla
                graph_data.push(total_day[t]); //Datos para grafica
            }
            t = t + 1;
        }
    } else if ((request == 2) && (type_table == 1)){
        newCell.innerHTML = 'Promedio';
        for (let i = 1; i < week.length; i++){
            var newCell = row3.insertCell(i);
            if (total_register[t] == 0){
                newCell.innerHTML = ' - ';
                graph_data.push(null);
            } else {
                var total = (total_day[t] / total_register[t]);
                newCell.innerHTML = lightLevel(Math.trunc(total));
                graph_data.push(255-Math.trunc(total)); //Datos para grafica
            }
            t = t + 1;
        }
    } else {
        newCell.innerHTML = 'Promedio';
        for (let i = 1; i < week.length; i++){
            var newCell = row3.insertCell(i);
            if (total_register[t] == 0){
                newCell.innerHTML = ' - '; //Datos para la tabla
                graph_data.push(null); //Datos para la grafica
            } else {
                var total = (total_day[t] / total_register[t]);
                newCell.innerHTML = Math.trunc(total) + simbol_text; //Datos para la tabla
                graph_data.push(Math.trunc(total)); //Datos para la grafica
            }
            t = t + 1;
        }
        
        /*switch (request){
        //Luminosidad
        case 2:
            //google.charts.load('current',{packages:['corechart','bar']});
            //google.charts.setOnLoadCallback(function () {draw_columnChart(request,graph_data)});
            break;*/
    }
    
    //Dibujando la tabla
    document.body.appendChild(table);
    tableDiv.append(table);
    
    return graph_data;
}

var socket = new WebSocket('ws://' + window.location.host + '/ws/lab-two/')

socket.onmessage = function(event) {
    var djangoData = JSON.parse(event.data);
    var event_update = djangoData.type;

    if (event_update==='user_request'){
        var js_message = djangoData.message;
        var graph_data;
        var graph_data2;
        var graph_data3;
        var graph_data4;

        //console.log(js_message);

        if (djangoData.weeks == 0){
            addText(djangoData.date_begin, djangoData.date_end);
            if (djangoData.request == 2){
                document.getElementById('subs-1').style.display = "block"; //Mostramos la segunda tabla de la seccion 1
                document.getElementById('subs-3').style.display = "block";
                document.getElementById('subs-4').style.display = "block";
                graph_data = addTable(lights_order(js_message,'Seccion 1'), djangoData.request,1,"historical_results");
                graph_data2 = addTable(lights_order(js_message,'Seccion 1'), djangoData.request,2,"historical_results_2");
                document.getElementById('subs-2').style.display = "block";
                document.getElementById('subs-5').style.display = "block";
                document.getElementById('subs-6').style.display = "block";
                graph_data3 = addTable(lights_order(js_message,'Seccion 2'), djangoData.request,1,"historical_results_3");
                graph_data4 = addTable(lights_order(js_message,'Seccion 2'), djangoData.request,2,"historical_results_4");

                //Niveles de luz
                console.log(graph_data);
                console.log(graph_data3);
                //Hora de encendido
                console.log(graph_data2);
                console.log(graph_data4);

                /*Dibujar las graficas de luminosidad */
                google.charts.load('current',{packages:['corechart','bar']}); //Mostramos la segunda tabla de la seccion 2
                document.getElementById('result_graph_2').style.display = "block"; 
                google.charts.setOnLoadCallback(function () {draw_columnChart(djangoData.request,graph_data,graph_data3,'result_graph')});
                google.charts.setOnLoadCallback(function () {draw_columnChart(djangoData.request,graph_data2,graph_data4,'result_graph_2')});
            } else {
                document.getElementById('subs-1').style.display = "none";
                document.getElementById('subs-2').style.display = "none";
                document.getElementById('subs-3').style.display = "none";
                document.getElementById('subs-4').style.display = "none";
                document.getElementById('subs-5').style.display = "none";
                document.getElementById('subs-6').style.display = "none";
                document.getElementById('result_graph_2').style.display = "none"; 
                graph_data = addTable(js_message, djangoData.request,0,"historical_results");

                if (djangoData.request == 3){
                    google.charts.load('current',{packages:['corechart','bar']});
                    google.charts.setOnLoadCallback(function () {draw_columnChart(djangoData.request,graph_data,graph_data,'result_graph')});
                } else {
                    //Dibuja la grafica para la temperatura o para la humedad
                    google.charts.load('current',{packages:['corechart','line']});
                    google.charts.setOnLoadCallback(function () {draw_lineChart(djangoData.request,graph_data)});
                }
            }
        } else {
            console.log(js_message);
        }
    }
}