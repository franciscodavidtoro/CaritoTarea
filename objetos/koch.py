"""
Fractal de Koch 3D - Copo de nieve de Koch en 3D
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
import figuras as fg
import math


def crear_koch(pos_x, pos_z, color=None, iteraciones=4):
    """Crea una curva de Koch en 3D más realista"""
    if color is None:
        color = [0.8, 0.6, 0.2, 1.0]  # Color dorado por defecto
    
    class FractalKoch:
        def __init__(self, posicion, color, iteraciones):
            self.tipo = "koch"
            self.posicion = list(posicion)
            self.rotacion = [0, 0, 0]  # [X, Y, Z] en grados
            self.color = color
            self.seleccionado = False
            self.figuras = []
            self.segmentos = []  # Lista para almacenar segmentos de línea
            self._crear_koch_3d(iteraciones)

        def _crear_koch_3d(self, iteraciones):
            """Crea una estructura 3D basada en la curva de Koch"""
            # Crear un hexágono base (Copo de nieve de Koch)
            radio = 3.0
            vertices_hex = []
            
            for i in range(6):
                angulo = i * math.pi / 3  # 60 grados entre cada vértice
                x = self.posicion[0] + radio * math.cos(angulo)
                z = self.posicion[2] + radio * math.sin(angulo)
                y = self.posicion[1]
                vertices_hex.append((x, y, z))
            
            # Crear los 6 lados del hexágono aplicando Koch
            for i in range(6):
                p1 = vertices_hex[i]
                p2 = vertices_hex[(i + 1) % 6]
                puntos_koch = self._generar_curva_koch_2d(p1, p2, iteraciones)
                
                # Crear la curva como una estructura 3D
                self._crear_estructura_3d_desde_puntos(puntos_koch, radio / (2 ** iteraciones))

        def _generar_curva_koch_2d(self, p1, p2, iteraciones):
            """Genera puntos de la curva de Koch entre dos puntos en 2D"""
            if iteraciones == 0:
                return [p1, p2]
            
            # Vector del segmento
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            dz = p2[2] - p1[2]
            
            # Puntos que dividen el segmento en tercios
            p_a = (p1[0] + dx/3, p1[1] + dy/3, p1[2] + dz/3)
            p_b = (p1[0] + 2*dx/3, p1[1] + 2*dy/3, p1[2] + 2*dz/3)
            
            # Calcular el punto del pico del triángulo equilátero
            # Vector perpendicular en el plano XZ (elevándolo ligeramente)
            longitud_segmento = math.sqrt(dx*dx + dz*dz)
            altura_triangulo = longitud_segmento * math.sqrt(3) / 6
            
            # Vector perpendicular normalizado
            if longitud_segmento > 0:
                perp_x = -dz / longitud_segmento * altura_triangulo
                perp_z = dx / longitud_segmento * altura_triangulo
            else:
                perp_x = perp_z = 0
            
            # Punto del pico (ligeramente elevado para efecto 3D)
            p_pico = (
                (p_a[0] + p_b[0])/2 + perp_x,
                p1[1] + altura_triangulo * 0.3,  # Elevar ligeramente
                (p_a[2] + p_b[2])/2 + perp_z
            )
            
            # Recursión para cada segmento
            resultado = []
            resultado.extend(self._generar_curva_koch_2d(p1, p_a, iteraciones-1)[:-1])  # Sin el último punto para evitar duplicados
            resultado.extend(self._generar_curva_koch_2d(p_a, p_pico, iteraciones-1)[:-1])
            resultado.extend(self._generar_curva_koch_2d(p_pico, p_b, iteraciones-1)[:-1])
            resultado.extend(self._generar_curva_koch_2d(p_b, p2, iteraciones-1))
            
            return resultado

        def _crear_estructura_3d_desde_puntos(self, puntos, grosor_base):
            """Crea estructura 3D a partir de una lista de puntos"""
            for i in range(len(puntos) - 1):
                p1 = puntos[i]
                p2 = puntos[i + 1]
                
                # Calcular punto medio
                punto_medio = (
                    (p1[0] + p2[0]) / 2,
                    (p1[1] + p2[1]) / 2,
                    (p1[2] + p2[2]) / 2
                )
                
                # Calcular longitud del segmento
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                dz = p2[2] - p1[2]
                longitud = math.sqrt(dx*dx + dy*dy + dz*dz)
                
                # Calcular ángulos de rotación
                if longitud > 0:
                    # Ángulo en el plano XZ
                    angulo_y = math.atan2(dx, dz) * 180 / math.pi
                    # Ángulo de elevación
                    angulo_x = -math.atan2(dy, math.sqrt(dx*dx + dz*dz)) * 180 / math.pi
                else:
                    angulo_y = angulo_x = 0
                
                # Crear segmento como cubo alargado
                grosor = max(grosor_base * 0.8, 0.05)
                segmento = fg.Figura(
                    tipo='cubo',
                    posicion=punto_medio,
                    rotacion=(angulo_x, angulo_y, 0),
                    escala=(grosor, grosor, longitud),
                    color=self.color
                )
                self.figuras.append(segmento)
                
                # Añadir esferas en los puntos de conexión para suavizar
                if i == 0:  # Primera esfera
                    esfera1 = fg.Figura(
                        tipo='esfera',
                        posicion=p1,
                        escala=(grosor * 1.2, grosor * 1.2, grosor * 1.2),
                        color=self.color,
                        argumentos=grosor * 0.6
                    )
                    self.figuras.append(esfera1)
                
                # Esfera en el segundo punto
                esfera2 = fg.Figura(
                    tipo='esfera',
                    posicion=p2,
                    escala=(grosor * 1.2, grosor * 1.2, grosor * 1.2),
                    color=self.color,
                    argumentos=grosor * 0.6
                )
                self.figuras.append(esfera2)

        def dibujar(self):
            # Aplicar transformaciones basadas en las propiedades del objeto
            glPushMatrix()
            
            # Aplicar posición
            glTranslatef(*self.posicion)
            
            # Aplicar rotación
            if self.rotacion[0] != 0:
                glRotatef(self.rotacion[0], 1, 0, 0)
            if self.rotacion[1] != 0:
                glRotatef(self.rotacion[1], 0, 1, 0)
            if self.rotacion[2] != 0:
                glRotatef(self.rotacion[2], 0, 0, 1)
            
            # Configurar material para el fractal de Koch
            glEnable(GL_LIGHTING)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)
            
            # Dibujar todas las figuras del fractal
            for i, figura in enumerate(self.figuras):
                # Aplicar gradiente de color basado en la posición
                factor_altura = (figura.posicion[1] - self.posicion[1] + 2) / 4
                factor_altura = max(0, min(1, factor_altura))
                
                # Crear gradiente dorado/amarillo para Koch
                color_modificado = (
                    min(1.0, self.color[0] + factor_altura * 0.4),  # Más rojizo en las alturas
                    min(1.0, self.color[1] + factor_altura * 0.3),  # Más verdoso
                    self.color[2] + factor_altura * 0.1,  # Poco azul
                    self.color[3]
                )
                
                # Asegurar que los valores estén entre 0 y 1
                color_modificado = tuple(max(0, min(1, c)) for c in color_modificado)
                
                # Aplicar el color modificado temporalmente y dibujar relativo al centro
                color_original = figura.color
                posicion_original = figura.posicion
                
                # Ajustar posición relativa al centro del objeto
                figura.posicion = [
                    figura.posicion[0] - self.posicion[0],
                    figura.posicion[1] - self.posicion[1], 
                    figura.posicion[2] - self.posicion[2]
                ]
                figura.color = color_modificado
                figura.dibujar()
                
                # Restaurar valores originales
                figura.color = color_original
                figura.posicion = posicion_original
            
            glPopMatrix()
            
            # Dibujar indicador de selección si está seleccionado
            if self.seleccionado:
                glPushAttrib(GL_CURRENT_BIT | GL_LIGHTING_BIT | GL_LINE_BIT)
                glPushMatrix()
                glTranslatef(*self.posicion)
                glDisable(GL_LIGHTING)
                glColor4f(1, 1, 0, 1)
                glLineWidth(4)
                glutWireCube(8.0)
                glPopMatrix()
                glPopAttrib()

    return FractalKoch([pos_x, 0, pos_z], color, iteraciones)
