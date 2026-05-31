# 02030-SVG.py
# # -*- coding: utf-8 -*-
""""
Crea archivos SVG con rectángulos, círculos, líneas, polilíneas y texto

@version 1.0 18/Octubre/2024
@author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
"""

import xml.etree.ElementTree as ET

class Svg(object):
    """
    Genera archivos SVG con rectángulos, círculos, líneas, polilíneas y texto
    @version 1.0 18/Octubre/2024
    @author: Juan Manuel Cueva Lovelle. Universidad de Oviedo
    """
    def __init__(self):
        """
        Crea el elemento raíz, el espacio de nombres y la versión
        """
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")

    def setViewBox(self, x, y, width, height):
        """
        Define el viewBox del SVG
        """
        self.raiz.set('viewBox', f"{x} {y} {width} {height}")
    
    def addRect(self,x,y,width,height,fill, strokeWidth,stroke):
        """
        Añade un elemento rect
        """
        ET.SubElement(self.raiz,'rect',
                      x=x,
                      y=y,
                      width=width,
                      height=height,
                      fill=fill, 
                      strokeWidth=strokeWidth,
                      stroke=stroke)
        
    def addCircle(self,cx,cy,r,fill):
        """
        Añade un elemento circle
        """
        ET.SubElement(self.raiz,'circle',
                      cx=cx,
                      cy=cy,
                      r=r,
                      fill=fill)
        
    def addLine(self,x1,y1,x2,y2,stroke,strokeWith):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz,'line',
                      x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      stroke=stroke,
                      strokeWith=strokeWith)

    def addPolyline(self,points,stroke,strokeWith,fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz,'polyline',
                      points=points,
                      stroke=stroke,
                      strokeWith=strokeWith,
                      fill=fill)
        
    def addText(self,texto,x,y,fontFamily,fontSize,style):
        """
        Añade un elemento texto
        """
        ET.SubElement(self.raiz,'text',
                      x=x,
                      y=y,
                      fontFamily=fontFamily,
                      fontSize=fontSize,
                      style=style).text=texto

    def escribir(self,nombreArchivoSVG):
        """ de
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        
        """
        Introduce indentacióon y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        
        arbol.write(nombreArchivoSVG, 
                    encoding='utf-8', 
                    xml_declaration=True
                    )
    
    def ver(self):
        """
        Muestra el archivo SVG. Se utiliza para depurar
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


FONT_FAMILY = "Verdana"
FONT_AXIS = "34"
FONT_TICKS = "26"
FONT_START = "45"
DIST_TICK_STEP = 500
ALT_TICK_STEP = 5
PADDING_IZQ = 150
PADDING_DER = 100
PADDING_SUP = 80
PADDING_INF = 50


def construir_puntos(tramos, namespace):
    """Devuelve distancias, altitudes, cadena de puntos y el punto de salida para cerrar el circuito."""
    puntos = []
    distancias = []
    altitudes = []
    dist_acc = 0.0

    for tramo in tramos:
        dist = float(tramo.find('uniovi:distancia', namespace).text.strip('\n'))
        dist_acc += dist
        alt = float(tramo.find('uniovi:coordenadas/uniovi:altitud', namespace).text.strip('\n'))

        distancias.append(dist_acc)
        altitudes.append(alt)
        puntos.append(f"{dist_acc},{alt}")

    # Cierra el circuito
    dist_salida = float(tramos[0].find('uniovi:distancia', namespace).text.strip('\n'))
    alt_salida = float(tramos[0].find('uniovi:coordenadas/uniovi:altitud', namespace).text.strip('\n'))
    puntos.append(f"{dist_salida},{alt_salida}")

    return distancias, altitudes, " ".join(puntos), dist_salida, alt_salida


def configurar_viewbox(svg, min_dist, max_dist, min_alt, max_alt):
    viewbox_x = min_dist - PADDING_IZQ
    viewbox_y = min_alt - PADDING_SUP
    viewbox_width = max_dist + PADDING_DER + PADDING_IZQ
    viewbox_height = (max_alt - min_alt) + PADDING_SUP + PADDING_INF
    svg.setViewBox(viewbox_x, viewbox_y, viewbox_width, viewbox_height)


def add_axis_labels(svg, min_dist, min_alt, max_dist, max_alt):
    svg.addText(texto="Altitud (m)",
                x=str(min_dist + 20),
                y=str(min_alt - 30),
                fontFamily=FONT_FAMILY,
                fontSize=FONT_AXIS,
                style="fill: black; font-weight: bold;")

    svg.addText(texto="Distancia (m)",
                x=str(max_dist / 2),
                y=str(max_alt + 40),
                fontFamily=FONT_FAMILY,
                fontSize=FONT_AXIS,
                style="fill: black; font-weight: bold;")


def add_distance_grid(svg, min_alt, max_alt, max_dist):
    dist_actual = DIST_TICK_STEP
    while dist_actual < max_dist:
        svg.addLine(x1=str(dist_actual),
                    y1=str(min_alt),
                    x2=str(dist_actual),
                    y2=str(max_alt),
                    stroke='lightgray',
                    strokeWith='1')
        svg.addText(texto=str(int(dist_actual)),
                    x=str(dist_actual),
                    y=str(min_alt - 20),
                    fontFamily=FONT_FAMILY,
                    fontSize=FONT_TICKS,
                    style="fill: black;")
        dist_actual += DIST_TICK_STEP


def add_altitude_grid(svg, min_dist, min_alt, max_dist, min_alt_tick, max_alt, alt_media_redondeada):
    alt_actual = min_alt_tick
    while alt_actual <= max_alt:
        if alt_actual >= min_alt:
            svg.addLine(x1=str(min_dist),
                        y1=str(alt_actual),
                        x2=str(max_dist),
                        y2=str(alt_actual),
                        stroke='lightgray',
                        strokeWith='1')
            if (abs(alt_actual - min_alt) < ALT_TICK_STEP or
                abs(alt_actual - alt_media_redondeada) < ALT_TICK_STEP or
                abs(alt_actual - max_alt) < ALT_TICK_STEP):
                svg.addText(texto=str(int(alt_actual)),
                            x=str(min_dist + 50),
                            y=str(alt_actual + 5),
                            fontFamily=FONT_FAMILY,
                            fontSize=FONT_TICKS,
                            style="fill: black;")
        alt_actual += ALT_TICK_STEP

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

    tramos = raiz.findall('.//uniovi:tramos/uniovi:tramo', namespace)
    distancias, altitudes, puntos, dist_salida_circuito, alt_salida_circuito = construir_puntos(tramos, namespace)

    min_dist = 0
    max_dist = max(distancias)
    min_alt = min(altitudes)
    max_alt = max(altitudes)
    
    print(f"Rango de distancias: {min_dist} - {max_dist}")
    print(f"Rango de altitudes: {min_alt} - {max_alt}")
    
    nombreSVG = "altimetria.svg"
    nuevoSVG = Svg()
    
    configurar_viewbox(nuevoSVG, min_dist, max_dist, min_alt, max_alt)
    add_axis_labels(nuevoSVG, min_dist, min_alt, max_dist, max_alt)

    add_distance_grid(nuevoSVG, min_alt, max_alt, max_dist)

    alt_media = (min_alt + max_alt) / 2
    alt_media_redondeada = round(alt_media / ALT_TICK_STEP) * ALT_TICK_STEP
    alt_inicio = int(min_alt / ALT_TICK_STEP) * ALT_TICK_STEP
    add_altitude_grid(nuevoSVG, min_dist, min_alt, max_dist, alt_inicio, max_alt, alt_media_redondeada)

    nuevoSVG.addText(texto="Salida del circuito",
                     x=str(dist_salida_circuito),
                     y=str(alt_salida_circuito),
                     fontFamily="Verdana",
                     fontSize="45",
                     style="writing-mode: tb; glyph-orientation-vertical: 0; fill: black;")
    
    # Traza el perfil altimétrico del circuito
    nuevoSVG.addPolyline(points=puntos,
                         stroke='red',
                         strokeWith='4',
                         fill='blue')
    
    """Visualización del SVG creado"""
    # nuevoSVG.ver()
    
    """Creación del archivo en formato SVG"""
    nuevoSVG.escribir(nombreSVG)
    print("Creado el archivo: ", nombreSVG)
    
if __name__ == "__main__":
    main()    
