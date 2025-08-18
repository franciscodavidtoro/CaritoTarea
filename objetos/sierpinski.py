"""
Tetraedro de Sierpinski - Fractal 3D
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
import figuras as fg
import math


def crear_sierpinski(pos_x, pos_z, color=None, iteraciones=4):
    """Crea un tetraedro de Sierpinski en 3D con triángulos reales"""
    if color is None:
        color = [0.2, 0.4, 0.8, 1.0]  # Color azul por defecto
    
    class FractalSierpinski:
        def __init__(self, posicion, color, iteraciones):
            self.tipo = "sierpinski"
            self.posicion = list(posicion)
            self.rotacion = [0, 0, 0]  # [X, Y, Z] en grados
            self.color = color
            self.seleccionado = False
            self.figuras = []
            self.triangulos = []  # Lista para almacenar triángulos directamente
            self._crear_sierpinski_3d(iteraciones)

        def _crear_sierpinski_3d(self, iteraciones):
            """Crea un tetraedro de Sierpinski en 3D con triángulos reales"""
            # Tamaño inicial del tetraedro
            tamaño = 4.0
            altura = tamaño * math.sqrt(2/3)  # Altura de tetraedro regular
            
            # Vértices de un tetraedro regular
            vertices = [
                # Vértice superior (punta de la pirámide)
                (self.posicion[0], self.posicion[1] + altura, self.posicion[2]),
                
                # Base triangular (triángulo equilátero)
                (self.posicion[0] - tamaño/2, self.posicion[1] - altura/3, self.posicion[2] + tamaño/(2*math.sqrt(3))),
                (self.posicion[0] + tamaño/2, self.posicion[1] - altura/3, self.posicion[2] + tamaño/(2*math.sqrt(3))),
                (self.posicion[0], self.posicion[1] - altura/3, self.posicion[2] - tamaño/math.sqrt(3))
            ]
            
            # Generar el fractal recursivamente
            self._generar_tetraedro_recursivo(vertices, iteraciones, tamaño)

        def _generar_tetraedro_recursivo(self, vertices, nivel, tamaño):
            """Genera recursivamente el tetraedro de Sierpinski"""
            if nivel == 0:
                # Crear tetraedro sólido con sus 4 caras triangulares
                self._crear_tetraedro_solido(vertices, tamaño)
                return
            
            nuevo_tamaño = tamaño / 2
            
            # Crear 4 tetraedros más pequeños, uno en cada vértice del tetraedro original
            for i in range(4):
                # Para cada vértice, crear un tetraedro más pequeño
                nuevos_vertices = [vertices[i]]  # El vértice principal
                
                # Calcular los otros 3 vértices como puntos medios de las aristas
                for j in range(4):
                    if i != j:
                        punto_medio = (
                            (vertices[i][0] + vertices[j][0]) / 2,
                            (vertices[i][1] + vertices[j][1]) / 2,
                            (vertices[i][2] + vertices[j][2]) / 2
                        )
                        nuevos_vertices.append(punto_medio)
                
                # Recursión para crear el tetraedro más pequeño
                self._generar_tetraedro_recursivo(nuevos_vertices, nivel - 1, nuevo_tamaño)

        def _crear_tetraedro_solido(self, vertices, tamaño):
            """Crea un tetraedro sólido dibujando sus 4 caras triangulares"""
            # Las 4 caras del tetraedro (cada cara es un triángulo)
            caras = [
                [1, 2, 3],  # Base (triángulo inferior)
                [0, 1, 2],  # Cara lateral 1
                [0, 2, 3],  # Cara lateral 2
                [0, 3, 1]   # Cara lateral 3
            ]
            
            # Crear cada cara triangular del tetraedro
            for i, cara in enumerate(caras):
                vertices_cara = [vertices[cara[0]], vertices[cara[1]], vertices[cara[2]]]
                
                # Color ligeramente diferente para cada cara para mejor visualización
                factor_color = 1.0 - (i * 0.1)  # Variar ligeramente el color por cara
                color_cara = (
                    self.color[0] * factor_color,
                    self.color[1] * factor_color,
                    self.color[2] * factor_color,
                    self.color[3]
                )
                
                self.triangulos.append({
                    'vertices': vertices_cara,
                    'color': color_cara,
                    'tamaño': tamaño,
                    'es_base': (i == 0)  # Marcar si es la base para orientar normales
                })

        def _dibujar_triangulo_3d(self, vertices, color, grosor=0.05, es_base=False):
            """Dibuja un triángulo 3D con grosor real"""
            
            # Calcular normal del triángulo
            v1 = vertices[0]
            v2 = vertices[1]
            v3 = vertices[2]
            
            # Vectores del triángulo
            u = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
            v = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])
            
            # Producto cruz para obtener la normal
            nx = u[1] * v[2] - u[2] * v[1]
            ny = u[2] * v[0] - u[0] * v[2]
            nz = u[0] * v[1] - u[1] * v[0]
            
            # Normalizar
            length = (nx*nx + ny*ny + nz*nz)**0.5
            if length > 0:
                nx /= length
                ny /= length
                nz /= length
            
            # Si es la base, invertir normal para que apunte hacia abajo
            if es_base:
                nx, ny, nz = -nx, -ny, -nz
            
            # Dibujar cara frontal del triángulo
            glBegin(GL_TRIANGLES)
            glColor4f(*color)
            glNormal3f(nx, ny, nz)
            for vertex in vertices:
                glVertex3f(vertex[0] + nx*grosor/2, vertex[1] + ny*grosor/2, vertex[2] + nz*grosor/2)
            glEnd()
            
            # Dibujar cara trasera del triángulo (más oscura)
            color_trasera = (color[0]*0.7, color[1]*0.7, color[2]*0.7, color[3])
            glBegin(GL_TRIANGLES)
            glColor4f(*color_trasera)
            glNormal3f(-nx, -ny, -nz)
            # Invertir orden para que la normal apunte correctamente
            for i in reversed(range(3)):
                vertex = vertices[i]
                glVertex3f(vertex[0] - nx*grosor/2, vertex[1] - ny*grosor/2, vertex[2] - nz*grosor/2)
            glEnd()
            
            # Dibujar los lados del triángulo (bordes con grosor)
            color_lateral = (color[0]*0.8, color[1]*0.8, color[2]*0.8, color[3])
            for i in range(3):
                v_a = vertices[i]
                v_b = vertices[(i + 1) % 3]
                
                # Crear un pequeño rectángulo para cada arista
                glBegin(GL_QUADS)
                glColor4f(*color_lateral)
                
                # Calcular normal lateral (perpendicular a la arista y a la normal del triángulo)
                edge = (v_b[0] - v_a[0], v_b[1] - v_a[1], v_b[2] - v_a[2])
                lateral_nx = ny * edge[2] - nz * edge[1]
                lateral_ny = nz * edge[0] - nx * edge[2]
                lateral_nz = nx * edge[1] - ny * edge[0]
                
                # Normalizar
                lat_length = (lateral_nx*lateral_nx + lateral_ny*lateral_ny + lateral_nz*lateral_nz)**0.5
                if lat_length > 0:
                    lateral_nx /= lat_length
                    lateral_ny /= lat_length
                    lateral_nz /= lat_length
                
                glNormal3f(lateral_nx, lateral_ny, lateral_nz)
                
                # Vértices del rectángulo lateral
                glVertex3f(v_a[0] - nx*grosor/2, v_a[1] - ny*grosor/2, v_a[2] - nz*grosor/2)
                glVertex3f(v_b[0] - nx*grosor/2, v_b[1] - ny*grosor/2, v_b[2] - nz*grosor/2)
                glVertex3f(v_b[0] + nx*grosor/2, v_b[1] + ny*grosor/2, v_b[2] + nz*grosor/2)
                glVertex3f(v_a[0] + nx*grosor/2, v_a[1] + ny*grosor/2, v_a[2] + nz*grosor/2)
                glEnd()

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
            
            # Configurar material para los triángulos
            glEnable(GL_LIGHTING)
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)
            
            # Dibujar todos los triángulos del tetraedro
            for triangulo in self.triangulos:
                # Aplicar gradiente de color azul basado en el tamaño (nivel de recursión)
                factor_gradiente = triangulo['tamaño'] / 4.0  # Normalizar basado en tamaño inicial
                
                # Crear gradiente de azules más bonito
                color_modificado = (
                    triangulo['color'][0] + factor_gradiente * 0.3,  # Más rojo para azules más claros
                    triangulo['color'][1] + factor_gradiente * 0.4,  # Más verde para tonos cyan
                    min(1.0, triangulo['color'][2] + factor_gradiente * 0.5),  # Más azul
                    triangulo['color'][3]
                )
                
                # Asegurar que los valores estén entre 0 y 1
                color_modificado = tuple(max(0, min(1, c)) for c in color_modificado)
                
                # Ajustar vértices relativo al centro del objeto
                vertices_ajustados = []
                for vertex in triangulo['vertices']:
                    vertices_ajustados.append((
                        vertex[0] - self.posicion[0],
                        vertex[1] - self.posicion[1],
                        vertex[2] - self.posicion[2]
                    ))
                
                # Dibujar el triángulo 3D con grosor proporcional a su tamaño
                grosor = max(0.03, triangulo['tamaño'] / 30)
                self._dibujar_triangulo_3d(
                    vertices_ajustados, 
                    color_modificado, 
                    grosor,
                    triangulo['es_base']
                )
            
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

    return FractalSierpinski([pos_x, 0, pos_z], color, iteraciones)
