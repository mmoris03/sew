"use strict";
class Carrusel {
    #busqueda
    #actual
    #maximo
    #fotografias

    constructor() {
        this.#busqueda = "Montmelo, MotoGP";
        this.#actual = 0;
        this.#maximo = 5;
        this.#fotografias = [];
    }

    getFotografias() {
        $.ajax({
            dataType: "json",
            url: "https://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?",
            data: {
                tags: this.#busqueda,
                tagmode: "any",
                format: "json"
            },
            success: this.#procesarJSONFotografias.bind(this)
        });
    }

    #procesarJSONFotografias(data) {
        // Extraer información de 5 fotografías del objeto JSON
        $.each(data.items, (i, item) => {
            if (i < this.#maximo) {
                // Modificar la URL para obtener imágenes de 640px (sufijo _z)
                let urlFoto = item.media.m.replace("_m.jpg", "_z.jpg");
                
                // Almacenar la información de cada fotografía
                this.#fotografias.push({
                    url: urlFoto,
                    titulo: item.title || "Imagen de Flickr"
                });
            }
        });
        
        // Llamar a mostrarFotografias después de procesar
        this.#mostrarFotografias();
    }

    #mostrarFotografias() {
        // Mostrar solo la primera imagen
        if (this.#fotografias.length > 0) {
            let primeraFoto = this.#fotografias[this.#actual];
            
            // Crear un article con h2 e img
            let article = $("<article></article>");
            let h2 = $("<h2></h2>").text("Imágenes del circuito de Barcelona-Catalunya, Montmeló");
            let img = $("<img />").attr("src", primeraFoto.url).attr("alt", primeraFoto.titulo);
            
            // Añadir h2 e img al article
            article.append(h2);
            article.append(img);
            
            // Añadir el article a la primera section
            $("section:first-of-type").append(article);
            
            // Programar el cambio automático cada 3 segundos
            setInterval(this.#cambiarFotografia.bind(this), 3000);
        }
    }

    #cambiarFotografia() {
        // Incrementar el índice actual
        this.#actual++;
        
        // Si llegamos al final, volver al principio
        if (this.#actual >= this.#fotografias.length) {
            this.#actual = 0;
        }
        
        // Obtener la nueva foto
        let foto = this.#fotografias[this.#actual];
        
        // Actualizar la imagen en el DOM
        $("section:first-of-type article img").attr("src", foto.url).attr("alt", foto.titulo);
    }
}