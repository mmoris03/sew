"use strict";
class Cronometro {
    #tiempo;
    #inicio;
    #corriendo;

    constructor() {
        this.#tiempo = 0;
        this.#mostrar();

        // Registrar listeners para los botones
        const btnArrancar = document.querySelector('main button:nth-of-type(1)');
        const btnParar = document.querySelector('main button:nth-of-type(2)');
        const btnReiniciar = document.querySelector('main button:nth-of-type(3)');

        if(btnArrancar) btnArrancar.addEventListener('click', this.arrancar.bind(this));
        if(btnParar) btnParar.addEventListener('click', this.parar.bind(this));
        if(btnReiniciar) btnReiniciar.addEventListener('click', this.reiniciar.bind(this));
    }

    arrancar() {
        try {
            this.#inicio = Temporal.Now.instant().epochMilliseconds;
        } catch (e) {
            this.#inicio = Date.now();
        }

        this.#corriendo = setInterval(this.#actualizar.bind(this), 100); // actualizar cada decima de segundo
    }

    #actualizar() {
        let ahora;
        try {
            ahora = Temporal.Now.instant().epochMilliseconds;
        } catch (e) {
            ahora = Date.now();
        }
        
        this.#tiempo = ahora - this.#inicio;
        this.#mostrar();
    }

    parar() {
        clearInterval(this.#corriendo);
    }

    reiniciar() {
        clearInterval(this.#corriendo);
        this.#tiempo = 0;
        this.#mostrar();
    }

    #mostrar() {
        let msTotal = this.#tiempo;

        const decimas = Math.floor((msTotal % 1000) / 100);

        const segundosTotal = Math.floor(msTotal / 1000);

        const segundos = segundosTotal % 60;

        const minutos = Math.floor(segundosTotal / 60);

        // Formatear para que siempre tengan dos dígitos (padding)
        const formatoMinutos = String(minutos).padStart(2, '0');
        const formatoSegundos = String(segundos).padStart(2, '0');

        const stringTiempo = `${formatoMinutos}:${formatoSegundos}.${decimas}`;

        document.querySelector("main p:first-of-type").textContent = stringTiempo;
    }
}