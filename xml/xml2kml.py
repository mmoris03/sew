import xml.etree.ElementTree as ET

class Kml(object):
    """
    Genera archivo KML con puntos y líneas
    @version 1.1 19/Octumbre/2024
    @author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
    """
    def __init__(self):
        """
        Crea el elemento raíz y el espacio de nombres
        """
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz,'Document')

    def addPlacemark(self,nombre,descripcion,long,lat,alt, modoAltitud):
        """
        Añade un elemento <Placemark> con puntos <Point>
        """
        pm = ET.SubElement(self.doc,'Placemark')
        ET.SubElement(pm,'name').text = nombre
        ET.SubElement(pm,'description').text = descripcion
        punto = ET.SubElement(pm,'Point')
        ET.SubElement(punto,'coordinates').text = '{},{},{}'.format(long,lat,alt)
        ET.SubElement(punto,'altitudeMode').text = modoAltitud

    def addLineString(self,nombre,extrude,tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        ET.SubElement(self.doc,'name').text = nombre
        pm = ET.SubElement(self.doc,'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls,'extrude').text = extrude
        ET.SubElement(ls,'tessellation').text = tesela
        ET.SubElement(ls,'coordinates').text = listaCoordenadas
        ET.SubElement(ls,'altitudeMode').text = modoAltitud 

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement (linea, 'color').text = color
        ET.SubElement (linea, 'width').text = ancho

    def escribir(self,nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)
    
    def ver(self):
        """
        Muestra el archivo KML. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)

        if self.raiz.text != None:
            print("Contenido = "    , self.raiz.text.strip('\n')) #strip() elimina los '\n' del string
        else:
            print("Contenido = "    , self.raiz.text)
        
        print("Atributos = "    , self.raiz.attrib)

        # Recorrido de los elementos del árbol
        for hijo in self.raiz.findall('.//'): # Expresión XPath
            print("\nElemento = " , hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n')) #strip() elimina los '\n' del string
            else:
                print("Contenido = ", hijo.text)    
            print("Atributos = ", hijo.attrib)

def main():
    archivoXML = "circuitoEsquema.xml"

    try:
        arbol = ET.parse(archivoXML)
    except IOError:
        print ("No se encuentra el archivo ", archivoXML)
        exit()
        
    except ET.ParseError:
        print("Error procesando en el archivo XML = ", archivoXML)
        exit()
       
    raiz = arbol.getroot()
    namespace = {"uniovi":"http://www.uniovi.es"}

    longitud_salida_circuito_xpath = ".//uniovi:coordenadas/uniovi:longitud"
    latitud_salida_circuito_xpath = ".//uniovi:coordenadas/uniovi:latitud"

    longitud_salida_circuito = raiz.find(longitud_salida_circuito_xpath, namespace).text.strip('\n')
    latitud_salida_circuito = raiz.find(latitud_salida_circuito_xpath, namespace).text.strip('\n')

    nombreKML = "circuito.kml"
    nuevoKML = Kml()
    
    nuevoKML.addPlacemark(nombre='Circuit de Barcelona-Catalunya',
                          descripcion='Salida del circuito',
                          long=longitud_salida_circuito,
                          lat=latitud_salida_circuito,
                          alt=0.0,
                          modoAltitud='relativeToGround')
    
    coordenadasCircuito = ""
    for punto in raiz.findall('.//uniovi:tramos/uniovi:tramo/uniovi:coordenadas', namespace):
            long = punto.find('uniovi:longitud', namespace).text.strip('\n')
            lat = punto.find('uniovi:latitud', namespace).text.strip('\n')
            coordenadasCircuito += "{},{},{}\n".format(long, lat, 0.0)
    coordenadasCircuito += f"{longitud_salida_circuito},{latitud_salida_circuito},0.0"  # Cierra el circuito
    
    nuevoKML.addLineString(nombre="Ruta Circuito",
                           extrude="1",
                           tesela="1",
                           listaCoordenadas=coordenadasCircuito,
                           modoAltitud='relativeToGround',
                           color='#ff0000ff',
                           ancho="5")
    
    """Visualización del KML creado"""
    # nuevoKML.ver()
    
    """Creación del archivo en formato KML"""
    nuevoKML.escribir(nombreKML)
    print("Creado el archivo: ", nombreKML)
    
if __name__ == "__main__":
    main()