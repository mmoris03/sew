<!DOCTYPE HTML>

<html lang="es">

<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Circuito</title>
    <link rel=icon href=multimedia/favicon-gp.ico>
    <meta name="author" content="miguel" />
    <meta name="description" content="" />
    <meta name="keywords" content="" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />
</head>

<body>
    <!-- Datos con el contenidos que aparece en el navegador -->
    <header>
        <h1><a href="index.html" title="Ir a la página principal">MotoGP Desktop</a></h1>
        <nav>
            <a href="index.html" title="Información de MotoGP">Inicio</a>
            <a href="piloto.html" title="Información del piloto">Piloto</a>
            <a href="circuito.html" title="Información del circuito">Circuito</a>
            <a href="meteorologia.html" title="Información de meteorología">Meteorologia</a>
            <a href="clasificaciones.html" title="Información de la clasificación">Clasificaciones</a>
            <a href="juegos.html" title="Información de los juegos">Juegos</a>
            <a href="ayuda.html" title="Información de ayuda">Ayuda</a>
        </nav>
    </header>
    <p>Estás en: <a href="index.html">Inicio</a> >> <strong>Cronometro</strong></p>
    <main>
        <h2>Cronometro de PHP de MotoGP-Desktop</h2>
        <form action='#' method='post' name='botones'>
            <input type = 'submit' name = 'arrancar' value = 'Arrancar'/>
            <input type = 'submit' name = 'parar' value = 'Parar'/>
            <input type = 'submit' name = 'mostrar' value = 'Mostrar'/>          
        </form>
        <?php
        
        class Cronometro {
            public function __construct() {
                $this->tiempo = 0;
            }

            public function arrancar() {
                $this->inicio = microtime(true);
            }
    
            public function parar(): void {
                $tiempo_actual = microtime(true);
                $this->tiempo = $tiempo_actual - $this->inicio;
            }
    
            // Devuelve el tiempo en formato mm:ss.s
            public function mostrar() {
                $duracion_total = $this->tiempo;

                // 1. Calcular Minutos (mm)
                // Obtenemos los minutos completos
                $minutos = floor($duracion_total / 60);

                // 2. Calcular Segundos (ss) y Décimas (s)
                // Segundos restantes después de calcular los minutos
                $segundos_restantes = $duracion_total - ($minutos * 60);
        
                // La parte entera de los segundos restantes es 'ss'
                $segundos = floor($segundos_restantes);
        
                // La parte decimal de los segundos restantes, multiplicada por 10, es 's'
                // Esto asegura que solo se toma la primera cifra decimal.
                $decimas = floor(($segundos_restantes - $segundos) * 10);

                // 3. Formateo y retorno
                
                // str_pad asegura que minutos y segundos tengan 2 dígitos, rellenando con '0' a la izquierda
                $formatoMinutos = str_pad((string)$minutos, 2, '0', STR_PAD_LEFT);
                $formatoSegundos = str_pad((string)$segundos, 2, '0', STR_PAD_LEFT);
                
                // El formato final es mm:ss.s
                return "{$formatoMinutos}:{$formatoSegundos}.{$decimas}";
            }
        }

        session_start();

        // Meter if count($_POST)>0 para que no se cree el objeto hasta que se pulse un botón????

        if(!isset($_SESSION['cronometro'])) {
            $_SESSION['cronometro'] = new Cronometro();
        }
        $cronometro = $_SESSION['cronometro'];

        if(isset($_POST['arrancar'])) $cronometro->arrancar();
        if(isset($_POST['parar'])) $cronometro->parar();
        if(isset($_POST['mostrar'])) echo "<p>" . $cronometro->mostrar() . "</p>";

        ?>
    </main>

</body>

</html>