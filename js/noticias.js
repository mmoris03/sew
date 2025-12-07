"use strict";
class Noticias {
    #busqueda
    #url
    #apiToken

    constructor() {
        this.#busqueda = "MotoGP";
        this.#url = "https://api.thenewsapi.com/v1/news/all";
        this.#apiToken = "m6bltkqM3vkmqCr0zJTlfw3446BlOWr3tj1Bp2rd";
    }

    buscar() {
        // Construir la URL completa con los parámetros
        const urlCompleta = `${this.#url}?api_token=${this.#apiToken}&search=${this.#busqueda}&language=en&limit=10`;

        // Realizar la petición con fetch()
        fetch(urlCompleta)
            .then(response => response.json())
            .then(data => {
                this.#procesarInformacion(data);
            })
            .catch(error => {
                console.error('Error al obtener las noticias:', error);
            });
    }

    #procesarInformacion(data) {
        this.#mostrarNoticias(data.data);
    }

    #mostrarNoticias(noticias) {
        // Crear una sección para las noticias
        const seccion = $("<section></section>");
        const titulo = $("<h3></h3>").text("Noticias de MotoGP");
        seccion.append(titulo);

        // Añadir cada noticia como un artículo
        $.each(noticias, (i, noticia) => {
            const article = $("<article></article>");

            // Título de la noticia
            const tituloNoticia = $("<h4></h4>").text(noticia.title);
            article.append(tituloNoticia);

            // Imagen
            const imagen = $("<img />")
                .attr("src", noticia.image_url)
                .attr("alt", noticia.title);
            article.append(imagen);

            // Descripción/entradilla
            const descripcion = $("<p></p>").text(noticia.description);
            article.append(descripcion);

            // Enlace a la noticia completa
            const parrafoEnlace = $("<p></p>");
            const enlace = $("<a></a>")
                .attr("href", noticia.url)
                .text("Leer más");
            parrafoEnlace.append(enlace);
            article.append(parrafoEnlace);

            // Fuente de la noticia
            const fuente = $("<p></p>").text(`Fuente: ${noticia.source}`);
            article.append(fuente);

            // Fecha de publicación
            const fecha = new Date(noticia.published_at);
            const fechaFormateada = fecha.toLocaleDateString(noticia.language, {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
            const parrafoFecha = $("<p></p>").text(`Publicado: ${fechaFormateada}`);
            article.append(parrafoFecha);

            seccion.append(article);
        });

        // Añadir la sección al body
        $("body").append(seccion);
    }
}
