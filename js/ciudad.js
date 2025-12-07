"use strict";
class Ciudad {
    #nombre;
    #pais;
    #gentilicio;
    #poblacion;
    #latitud;
    #longitud;

    constructor(nombre, pais, gentilicio) {
        this.#nombre = nombre;
        this.#pais = pais;
        this.#gentilicio = gentilicio;
        this.#rellenarDatos();
    }

    #rellenarDatos() {
        this.#poblacion = 1686208;
        this.#latitud = 41.57006598057092;
        this.#longitud = 119.8145058344016;
    }

    #getNombre() {
        return this.#nombre;
    }

    #getPais() {
        return this.#pais;
    }

    #getInfoSecundaria() {
        return `<ul>
            <li>Gentilicio: ${this.#gentilicio}</li>
            <li>Población: ${this.#poblacion}</li>
        </ul>`;
    }

    escribirNombrePais() {
        const seccion = document.createElement("section");

        const titulo = document.createElement("h2");
        titulo.textContent = "Información principal";
        seccion.appendChild(titulo);

        const nombrePais = document.createElement("p");
        nombrePais.textContent = `Ciudad: ${this.#getNombre()}, País: ${this.#getPais()}`;
        seccion.appendChild(nombrePais);

        document.body.appendChild(seccion);
    }

    escribirInfoSecundaria() {
        const seccion = document.createElement("section");

        const titulo = document.createElement("h2");
        titulo.textContent = "Información secundaria";
        seccion.appendChild(titulo);

        seccion.insertAdjacentHTML("beforeend", this.#getInfoSecundaria());
        document.body.appendChild(seccion);
    }

    escribirCoordenadas() {
        const coordenadas = document.createElement("p");
        coordenadas.textContent = `Coordenadas: Latitud ${this.#latitud}, Longitud ${this.#longitud}`;
        document.body.appendChild(coordenadas);
    }

    getMeteorologiaCarrera() {
        // Fecha de la carrera de MotoGP en Barcelona (ejemplo: 5 de mayo de 2024)
        const fechaCarrera = "2024-05-05";
        
        $.ajax({
            dataType: "json",
            url: "https://archive-api.open-meteo.com/v1/archive",
            data: {
                latitude: this.#latitud,
                longitude: this.#longitud,
                start_date: fechaCarrera,
                end_date: fechaCarrera,
                hourly: "temperature_2m,apparent_temperature,precipitation,relative_humidity_2m,wind_speed_10m,wind_direction_10m",
                daily: "sunrise,sunset",
                timezone: "Europe/Madrid"
            },
            success: this.#procesarMeteorologiaCarrera.bind(this)
        });
    }

    #procesarMeteorologiaCarrera(data) {
        console.log("Datos meteorológicos recibidos:", data);
        this.#procesarJSONCarrera(data);
    }

    #procesarJSONCarrera(data) {
        // Mostrar los datos procesados en el HTML
        this.#mostrarDatosMeteorologicos(data);
    }

    getMeteorologiaEntrenos() {
        // Fechas de los 3 días de entrenamientos previos a la carrera
        // Si la carrera es el 5 de mayo, los entrenamientos son 2, 3 y 4 de mayo
        const fechaInicioEntrenos = "2024-05-02";
        const fechaFinEntrenos = "2024-05-04";
        
        $.ajax({
            dataType: "json",
            url: "https://archive-api.open-meteo.com/v1/archive",
            data: {
                latitude: this.#latitud,
                longitude: this.#longitud,
                start_date: fechaInicioEntrenos,
                end_date: fechaFinEntrenos,
                hourly: "temperature_2m,precipitation,wind_speed_10m,relative_humidity_2m",
                timezone: "Europe/Madrid"
            },
            success: this.#procesarMeteorologiaEntrenos.bind(this)
        });
    }

    #procesarMeteorologiaEntrenos(data) {
        console.log("Datos meteorológicos de entrenamientos recibidos:", data);
        this.#procesarJSONEntrenos(data);
    }

    #procesarJSONEntrenos(data) {
        // Extraer información del objeto JSON y calcular medias por día
        
        // Arrays con todos los datos horarios
        const horas = data.hourly.time;
        const temperaturas = data.hourly.temperature_2m;
        const precipitacion = data.hourly.precipitation;
        const velocidadViento = data.hourly.wind_speed_10m;
        const humedad = data.hourly.relative_humidity_2m;
        
        // Agrupar datos por día (24 horas por día)
        const dias = [];
        const horasPorDia = 24;
        const numDias = 3;
        
        for (let dia = 0; dia < numDias; dia++) {
            const inicio = dia * horasPorDia;
            const fin = inicio + horasPorDia;
            
            // Extraer datos del día actual
            const tempDia = temperaturas.slice(inicio, fin);
            const precipDia = precipitacion.slice(inicio, fin);
            const vientoDia = velocidadViento.slice(inicio, fin);
            const humedadDia = humedad.slice(inicio, fin);
            
            // Calcular medias del día
            const mediaTemp = this.#calcularMedia(tempDia);
            const mediaPrecip = this.#calcularMedia(precipDia);
            const mediaViento = this.#calcularMedia(vientoDia);
            const mediaHumedad = this.#calcularMedia(humedadDia);
            
            // Guardar medias del día
            dias.push({
                fecha: horas[inicio].split('T')[0], // Extraer solo la fecha
                temperaturaMedia: mediaTemp,
                precipitacionMedia: mediaPrecip,
                vientoMedio: mediaViento,
                humedadMedia: mediaHumedad
            });
        }
        
        // Mostrar los datos procesados en el HTML
        this.#mostrarDatosEntrenos(dias);
    }

    #calcularMedia(array) {
        const suma = array.reduce((acum, valor) => acum + valor, 0);
        const media = suma / array.length;
        return media.toFixed(2); // Ajustar a 2 decimales
    }

    #mostrarDatosEntrenos(dias) {
        // Crear sección para mostrar la información de entrenamientos
        const seccion = $("<section></section>");
        const titulo = $("<h3></h3>").text("Meteorología de los días de entrenamientos");
        seccion.append(titulo);
        
        // Información de medias por día
        const infoMedias = $("<article></article>");
        const tituloArticle = $("<h4></h4>").text("Medias diarias de los entrenamientos");
        infoMedias.append(tituloArticle);
        
        // Crear tabla para las medias
        const tabla = $("<table></table>");
        const caption = $("<caption></caption>").text("Medias meteorológicas de los 3 días de entrenamientos");
        tabla.append(caption);
        
        // Encabezado de la tabla
        const thead = $("<thead></thead>");
        const filaEncabezado = $("<tr></tr>");
        filaEncabezado.append($("<th scope='col' id='fecha_ent'></th>").text("Fecha"));
        filaEncabezado.append($("<th scope='col' id='temp_ent'></th>").text("Temp. Media (°C)"));
        filaEncabezado.append($("<th scope='col' id='precip_ent'></th>").text("Precip. Media (mm)"));
        filaEncabezado.append($("<th scope='col' id='viento_ent'></th>").text("Viento Medio (km/h)"));
        filaEncabezado.append($("<th scope='col' id='humedad_ent'></th>").text("Humedad Media (%)"));
        thead.append(filaEncabezado);
        tabla.append(thead);
        
        // Cuerpo de la tabla con las medias de cada día
        const tbody = $("<tbody></tbody>");
        
        for (let i = 0; i < dias.length; i++) {
            const fila = $("<tr></tr>");
            const idFila = "dia" + (i + 1);
            fila.append($("<th scope='row' id='" + idFila + "' headers='fecha_ent'></th>").text(dias[i].fecha));
            fila.append($("<td headers='" + idFila + " temp_ent'></td>").text(dias[i].temperaturaMedia));
            fila.append($("<td headers='" + idFila + " precip_ent'></td>").text(dias[i].precipitacionMedia));
            fila.append($("<td headers='" + idFila + " viento_ent'></td>").text(dias[i].vientoMedio));
            fila.append($("<td headers='" + idFila + " humedad_ent'></td>").text(dias[i].humedadMedia));
            tbody.append(fila);
        }
        
        tabla.append(tbody);
        infoMedias.append(tabla);
        seccion.append(infoMedias);
        
        // Añadir la sección al body
        $("body").append(seccion);
    }

    #mostrarDatosMeteorologicos(data) {
        
        // Crear sección para mostrar la información
        const seccion = $("<section></section>");
        const titulo = $("<h3></h3>").text("Meteorología del día de la carrera");
        seccion.append(titulo);
        
        // Información diaria (sunrise y sunset)
        if (data.daily) {
            const infoDiaria = $("<article></article>");
            const tituloArticle = $("<h4></h4>").text("Información diaria");
            infoDiaria.append(tituloArticle);
            
            const listaDiaria = $("<ul></ul>");
            listaDiaria.append($("<li></li>").text(`Amanecer: ${data.daily.sunrise[0]}`));
            listaDiaria.append($("<li></li>").text(`Atardecer: ${data.daily.sunset[0]}`));
            
            infoDiaria.append(listaDiaria);
            seccion.append(infoDiaria);
        }
        
        // Información horaria
        if (data.hourly) {
            const infoHoraria = $("<article></article>");
            const tituloArticle = $("<h4></h4>").text("Información horaria");
            infoHoraria.append(tituloArticle);
            
            // Crear tabla para datos horarios
            const tabla = $("<table></table>");
            const caption = $("<caption></caption>").text("Datos meteorológicos horarios del día de la carrera");
            tabla.append(caption);
            
            // Encabezado de la tabla
            const thead = $("<thead></thead>");
            const filaEncabezado = $("<tr></tr>");
            filaEncabezado.append($("<th scope='col' id='hora'></th>").text("Hora"));
            filaEncabezado.append($("<th scope='col' id='temp'></th>").text("Temp. (°C)"));
            filaEncabezado.append($("<th scope='col' id='sens_term'></th>").text("Sens. Térmica (°C)"));
            filaEncabezado.append($("<th scope='col' id='precip'></th>").text("Precipitación (mm)"));
            filaEncabezado.append($("<th scope='col' id='humedad'></th>").text("Humedad (%)"));
            filaEncabezado.append($("<th scope='col' id='vel_viento'></th>").text("Vel. Viento (km/h)"));
            filaEncabezado.append($("<th scope='col' id='dir_viento'></th>").text("Dir. Viento (°)"));
            thead.append(filaEncabezado);
            tabla.append(thead);
            
            // Cuerpo de la tabla
            const tbody = $("<tbody></tbody>");
            const numDatos = data.hourly.time.length;
            
            for (let i = 0; i < numDatos; i++) {
                const fila = $("<tr></tr>");
                const idFila = "hora" + i;
                fila.append($("<th scope='row' id='" + idFila + "' headers='hora'></th>").text(data.hourly.time[i]));
                fila.append($("<td headers='" + idFila + " temp'></td>").text(data.hourly.temperature_2m[i]));
                fila.append($("<td headers='" + idFila + " sens_term'></td>").text(data.hourly.apparent_temperature[i]));
                fila.append($("<td headers='" + idFila + " precip'></td>").text(data.hourly.precipitation[i]));
                fila.append($("<td headers='" + idFila + " humedad'></td>").text(data.hourly.relative_humidity_2m[i]));
                fila.append($("<td headers='" + idFila + " vel_viento'></td>").text(data.hourly.wind_speed_10m[i]));
                fila.append($("<td headers='" + idFila + " dir_viento'></td>").text(data.hourly.wind_direction_10m[i]));
                tbody.append(fila);
            }
            
            tabla.append(tbody);
            infoHoraria.append(tabla);
            seccion.append(infoHoraria);
        }
        
        // Añadir la sección al body
        $("body").append(seccion);
    }
}