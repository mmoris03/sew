import xml.etree.ElementTree as ET

class Html(object):
    def __init__(self):
        """
        Crea el elemento raíz HTML y estructura básica
        """
        self.raiz = ET.Element('html', lang='es')
        self.head = ET.SubElement(self.raiz, 'head')
        self.body = ET.SubElement(self.raiz, 'body')

    def addHead(self, titulo, autor, descripcion, palabras_clave, favicon, estilos):
        """
        Genera el head completo del documento HTML con metadatos y enlaces
        Mantiene el mismo orden que clasificaciones.html
        @param titulo: Título del documento
        @param autor: Nombre del autor
        @param descripcion: Descripción del documento
        @param palabras_clave: Palabras clave separadas por comas
        @param favicon: Ruta del favicon
        @param estilos: Lista de rutas de archivos CSS
        """
        # 1. Meta charset
        ET.SubElement(self.head, 'meta', charset='UTF-8')
        
        # 2. Title
        ET.SubElement(self.head, 'title').text = titulo
        
        # 3. Meta author
        ET.SubElement(self.head, 'meta', name='author', content=autor)
        
        # 4. Meta description
        ET.SubElement(self.head, 'meta', name='description', content=descripcion)
        
        # 5. Meta keywords
        ET.SubElement(self.head, 'meta', name='keywords', content=palabras_clave)
        
        # 6. Meta viewport
        ET.SubElement(self.head, 'meta', name='viewport', content='width=device-width, initial-scale=1.0')
        
        # 7-8. Links stylesheet (mismo orden de atributos que clasificaciones.html)
        for estilo in estilos:
            ET.SubElement(self.head, 'link', rel='stylesheet', type='text/css', href=estilo)
        
        # 9. Link icon
        ET.SubElement(self.head, 'link', rel='icon', href=favicon)

    def addHeading(self, nivel, texto):
        """
        Añade un heading (h1-h6) al body
        @param nivel: Nivel del heading (1-6)
        @param texto: Contenido del heading
        """
        ET.SubElement(self.body, f'h{nivel}').text = texto

    def addParagraph(self, texto):
        """
        Añade un párrafo al body
        @param texto: Contenido del párrafo
        """
        ET.SubElement(self.body, 'p').text = texto

    def addList(self, items):
        """
        Añade una lista desordenada al body
        @param items: Lista de elementos
        """
        lista = ET.SubElement(self.body, 'ul')
        for item in items:
            ET.SubElement(lista, 'li').text = item

    def addOrderedList(self, items):
        """
        Añade una lista ordenada al body
        @param items: Lista de elementos
        """
        lista = ET.SubElement(self.body, 'ol')
        for item in items:
            ET.SubElement(lista, 'li').text = item

    def addListWithLinks(self, items_links):
        """
        Añade una lista desordenada con enlaces al body
        @param items_links: Lista de tuplas (texto, url)
        """
        lista = ET.SubElement(self.body, 'ul')
        for texto, url in items_links:
            li = ET.SubElement(lista, 'li')
            enlace = ET.SubElement(li, 'a', href=url)
            enlace.text = texto

    def addImage(self, src, alt):
        """
        Añade una imagen al body
        @param src: Ruta de la imagen
        @param alt: Texto alternativo
        """
        ET.SubElement(self.body, 'img', src=src, alt=alt)

    def addVideo(self, src, alt):
        """
        Añade un video al body
        @param src: Ruta del video
        @param alt: Texto alternativo (se muestra como párrafo antes del video)
        """
        ET.SubElement(self.body, 'p').text = alt
        video = ET.SubElement(self.body, 'video', controls='controls')
        ET.SubElement(video, 'source', src=src, type='video/mp4')

    def escribir(self, nombreArchivoHTML):
        """
        Escribe el archivo HTML con indentación y codificación
        @param nombreArchivoHTML: Nombre del archivo de salida
        """
        arbol = ET.ElementTree(self.raiz)
        
        """
        Introduce indentación y saltos de línea
        para generar HTML en modo texto
        """
        ET.indent(arbol)
        arbol.write(nombreArchivoHTML, 
                    encoding='utf-8', 
                    xml_declaration=False,
                    method='html')

    def addDocType(self, nombreArchivoHTML):
        """
        Añade DOCTYPE al principio del archivo HTML
        @param nombreArchivoHTML: Nombre del archivo HTML
        """
        # Leer el archivo generado
        with open(nombreArchivoHTML, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Escribir el archivo con DOCTYPE al principio
        with open(nombreArchivoHTML, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE HTML>\n\n' + contenido)

    def ver(self):
        """
        Muestra el archivo HTML. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)

        if self.raiz.text != None:
            print("Contenido = ", self.raiz.text.strip('\n'))
        else:
            print("Contenido = ", self.raiz.text)
        
        print("Atributos = ", self.raiz.attrib)

        # Recorrido de los elementos del árbol
        for hijo in self.raiz.findall('.//'):
            print("\nElemento = ", hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n'))
            else:
                print("Contenido = ", hijo.text)    
            print("Atributos = ", hijo.attrib)


def main():
    """
    Genera InfoCircuito.html a partir de circuitoEsquema.xml
    """
    archivoXML = "circuitoEsquema.xml"

    try:
        arbol = ET.parse(archivoXML)
    except IOError:
        print("No se encuentra el archivo ", archivoXML)
        exit()
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()

    raiz = arbol.getroot()
    namespace = {"uniovi": "http://www.uniovi.es"}

    # Crear documento HTML
    nombreHTML = "InfoCircuito.html"
    nuevoHTML = Html()

    # Nombre del circuito
    nombre = raiz.find('.//uniovi:nombre', namespace).text.strip()
    
    # Generar el head
    nuevoHTML.addHead(
        titulo=f"Información del {nombre}",
        autor="miguel",
        descripcion=f"Información del circuito {nombre}",
        palabras_clave="moto, circuito, motogp",
        favicon="../multimedia/favicon-gp.ico",
        estilos=["../estilo/estilo.css", "../estilo/layout.css"]
    )

    # Título principal
    nuevoHTML.addHeading(1, nombre)
    
    # Longitud del circuito
    longitud_elem = raiz.find('.//uniovi:longitudCircuito', namespace)
    longitud_circuito = longitud_elem.text.strip()
    longitud_unidades = longitud_elem.get('unidades')
    nuevoHTML.addParagraph(f"Longitud: {longitud_circuito} {longitud_unidades}")
    
    # Anchura media
    anchura_elem = raiz.find('.//uniovi:anchuraMedia', namespace)
    anchura_media = anchura_elem.text.strip()
    anchura_unidades = anchura_elem.get('unidades')
    nuevoHTML.addParagraph(f"Anchura media: {anchura_media} {anchura_unidades}")
    
    # Fecha
    fecha = raiz.find('.//uniovi:fecha', namespace).text.strip()
    nuevoHTML.addParagraph(f"Fecha: {fecha}")
    
    # Hora
    hora = raiz.find('.//uniovi:hora', namespace).text.strip()
    nuevoHTML.addParagraph(f"Hora: {hora}")
    
    # Número de vueltas
    numero_vueltas = raiz.find('.//uniovi:numeroVueltas', namespace).text.strip()
    nuevoHTML.addParagraph(f"Número de vueltas: {numero_vueltas}")
    
    # Localidad próxima
    localidad_proxima = raiz.find('.//uniovi:localidadProxima', namespace).text.strip()
    nuevoHTML.addParagraph(f"Localidad próxima: {localidad_proxima}")
    
    # País
    pais = raiz.find('.//uniovi:pais', namespace).text.strip()
    nuevoHTML.addParagraph(f"País: {pais}")
    
    # Patrocinador
    patrocinador = raiz.find('.//uniovi:patrocinador', namespace).text.strip()
    nuevoHTML.addParagraph(f"Patrocinador: {patrocinador}")
    
    # Referencias
    referencias = []
    for ref in raiz.findall('.//uniovi:referencias/uniovi:referencia', namespace):
        nombre_ref = ref.get('nombre')
        url = ref.text.strip()
        referencias.append((nombre_ref, url))
    nuevoHTML.addHeading(2, "Referencias")
    nuevoHTML.addListWithLinks(referencias)
    
    # Fotos
    fotos = []
    for foto in raiz.findall('.//uniovi:fotos/uniovi:foto', namespace):
        alt = foto.get('alt')
        ruta = foto.text.strip()
        fotos.append((ruta, alt))
    nuevoHTML.addHeading(2, "Fotos")
    for src, alt in fotos:
        nuevoHTML.addImage(f"../{src}", alt)
    
    # Videos
    videos = []
    for video in raiz.findall('.//uniovi:videos/uniovi:video', namespace):
        alt = video.get('alt')
        ruta = video.text.strip()
        videos.append((ruta, alt))
    nuevoHTML.addHeading(2, "Videos")
    for src, alt in videos:
        nuevoHTML.addVideo(f"../{src}", alt)
    
    # Coordenadas del punto inicial
    coord_long_elem = raiz.find('.//uniovi:coordenadas/uniovi:longitud', namespace)
    coord_long = coord_long_elem.text.strip()
    coord_long_unidades = coord_long_elem.get('unidades')
    
    coord_lat_elem = raiz.find('.//uniovi:coordenadas/uniovi:latitud', namespace)
    coord_lat = coord_lat_elem.text.strip()
    coord_lat_unidades = coord_lat_elem.get('unidades')
    
    coord_alt_elem = raiz.find('.//uniovi:coordenadas/uniovi:altitud', namespace)
    coord_alt = coord_alt_elem.text.strip()
    coord_alt_unidades = coord_alt_elem.get('unidades')
    
    coord_sector = raiz.find('.//uniovi:coordenadas/uniovi:sector', namespace).text.strip()
    
    nuevoHTML.addHeading(2, "Coordenadas del Punto Inicial")
    nuevoHTML.addParagraph(f"Longitud: {coord_long} {coord_long_unidades}")
    nuevoHTML.addParagraph(f"Latitud: {coord_lat} {coord_lat_unidades}")
    nuevoHTML.addParagraph(f"Altitud: {coord_alt} {coord_alt_unidades}")
    nuevoHTML.addParagraph(f"Sector: {coord_sector}")
    
    # Vencedor
    vencedor_elem = raiz.find('.//uniovi:vencedor', namespace)
    vencedor = vencedor_elem.text.strip()
    duracion = vencedor_elem.get('duracion')
    nuevoHTML.addHeading(2, "Vencedor")
    nuevoHTML.addParagraph(f"{vencedor} - Duración: {duracion}")
    
    # Podio
    primero = raiz.find('.//uniovi:podio/uniovi:primero', namespace).text.strip()
    segundo = raiz.find('.//uniovi:podio/uniovi:segundo', namespace).text.strip()
    tercero = raiz.find('.//uniovi:podio/uniovi:tercero', namespace).text.strip()
    nuevoHTML.addHeading(2, "Podio")
    nuevoHTML.addOrderedList([primero, segundo, tercero])

    # Escribir el archivo HTML
    nuevoHTML.escribir(nombreHTML)
    nuevoHTML.addDocType(nombreHTML)
    print(f"Creado el archivo: {nombreHTML}")


if __name__ == "__main__":
    main()
