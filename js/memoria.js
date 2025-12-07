"use strict";
class Memoria {
    #tablero_bloqueado;
    #primera_carta;
    #segunda_carta;
    #cronometro;

    constructor() {
        this.#tablero_bloqueado = true;
        this.#primera_carta = null;
        this.#segunda_carta = null;

        this.#barajarCartas();
        this.#tablero_bloqueado = false;
        this.#cronometro = new Cronometro();
        this.#cronometro.arrancar();
        
        //asignar click a cada article
        const articulos = document.querySelectorAll('main article');
        articulos.forEach(art => {
            art.addEventListener('click', this.voltearCarta.bind(this, art));
        });
    }

    voltearCarta(carta) {
        if (this.#tablero_bloqueado) {
            return;
        }
        if (carta.dataset.estado === "volteada") {
            return;
        }
        if (carta.dataset.estado === "revelada") {
            return;
        }

        carta.dataset.estado = "volteada";

        if (!this.#primera_carta) {
            this.#primera_carta = carta;
            return;
        }
        this.#segunda_carta = carta;
        this.#comprobarPareja();
    }

    #barajarCartas() {
        const contenedor = document.querySelector("main");

        const cartas = contenedor.children;

        // Tomamos solo los hijos que queremos barajar (excluimos los dos primeros)
        const arrayCartas = Array.from(cartas).slice(2);

        // Fisher–Yates: mezclar TODOS los elementos del arrayCartas
        for (let i = arrayCartas.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            const temp = arrayCartas[i];
            arrayCartas[i] = arrayCartas[j];
            arrayCartas[j] = temp;

            // Aplicar los cambios al DOM
            contenedor.appendChild(arrayCartas[i]);
        }

        arrayCartas.forEach(carta => contenedor.appendChild(carta));
    }

    #reiniciarAtributos() {
        this.#tablero_bloqueado = false;
        this.#primera_carta = null;
        this.#segunda_carta = null;
    }

    #deshabilitarCartas() {
        this.#primera_carta.dataset.estado = "revelada";
        this.#segunda_carta.dataset.estado = "revelada";
        this.#comprobarJuego();
        this.#reiniciarAtributos();
    }

    #cubrirCartas() {
        this.#tablero_bloqueado = true;

        setTimeout(() => {
            delete this.#primera_carta.dataset.estado;
            delete this.#segunda_carta.dataset.estado;
            this.#reiniciarAtributos();
        }, 1000);
    }

    #comprobarJuego() {
        const cartas = document.querySelectorAll('main article');

        // Comprobar que todas las cartas tienen estado 'revelada'
        for (let i = 0; i < cartas.length; i++) {
            if (cartas[i].dataset.estado !== 'revelada') {
                return false;
            }
        }
        this.#cronometro.parar();

        return true;
    }

    #comprobarPareja() {
        const alt_primera_carta = this.#primera_carta.querySelector('img').alt;
        const alt_segunda_carta = this.#segunda_carta.querySelector('img').alt;

        alt_primera_carta === alt_segunda_carta ? this.#deshabilitarCartas() : this.#cubrirCartas();
    }
}