"""
Esponja de Sierpinski - Fractal 3D
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
import figuras as fg


def crear_esponja_sierpinski(pos_x, pos_z, color=None, iteraciones=3):
    """Crea una Esponja de Sierpinski (Sierpinski Sponge) en 3D"""
    if color is None:
        color = [0.6, 0.2, 0.8, 1.0]  # Color púrpura por defecto
    
    class EsponjaSierpinski:
        def __init__(self, posicion, color, iteraciones):
            self.tipo = "esponja"
            self.posicion = list(posicion)
            self.rotacion = [0, 0, 0]  # [X, Y, Z] en grados
            self.color = color
            self.seleccionado = False
            self.figuras = []
            self._crear_esponja_recursiva(self.posicion, 4.0, iteraciones)

        def _crear_esponja_recursiva(self, centro, tamaño, nivel):
            """Crea recursivamente la esponja de Sierpinski"""
            if nivel == 0:
                # Crear cubo sólido en el nivel base
                cubo = fg.Figura(
                    tipo='cubo',
                    posicion=centro,
                    escala=(tamaño, tamaño, tamaño),
                    color=self.color
                )
                self.figuras.append(cubo)
                return
            
            nuevo_tamaño = tamaño / 3.0
            
            # Para cada posición en la grilla 3x3x3, excepto las que deben estar vacías
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        # Contar cuántas coordenadas son iguales a 1 (centro)
                        coords_centro = sum([x == 1, y == 1, z == 1])
                        
                        # Omitir posiciones que están en el centro de caras o el centro absoluto
                        # La esponja de Sierpinski omite cubos donde 2 o más coordenadas son centrales
                        if coords_centro >= 2:
                            continue
                            
                        # Calcular nueva posición
                        nueva_x = centro[0] + (x - 1) * nuevo_tamaño
                        nueva_y = centro[1] + (y - 1) * nuevo_tamaño
                        nueva_z = centro[2] + (z - 1) * nuevo_tamaño
                        
                        nueva_posicion = [nueva_x, nueva_y, nueva_z]
                        
                        # Recursión para crear sub-esponjas
                        self._crear_esponja_recursiva(nueva_posicion, nuevo_tamaño, nivel - 1)

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
            
            # Configurar material específico para la esponja (menos reflectivo)
            glEnable(GL_LIGHTING)
            
            # Material más opaco y menos reflectivo
            material_ambient = [self.color[0] * 0.4, self.color[1] * 0.4, self.color[2] * 0.4, self.color[3]]
            material_diffuse = [self.color[0] * 0.8, self.color[1] * 0.8, self.color[2] * 0.8, self.color[3]]
            material_specular = [0.1, 0.1, 0.1, 1.0]  # Muy poco brillo especular
            
            glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material_ambient)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material_diffuse)
            glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material_specular)
            glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 8.0)  # Muy poco brillo
            
            # Dibujar todas las figuras de la esponja con gradiente
            for i, figura in enumerate(self.figuras):
                # Crear gradiente basado en la distancia al centro
                distancia_al_centro = (
                    (figura.posicion[0] - self.posicion[0])**2 +
                    (figura.posicion[1] - self.posicion[1])**2 +
                    (figura.posicion[2] - self.posicion[2])**2
                )**0.5
                
                # Normalizar la distancia para crear el gradiente
                factor_distancia = min(1.0, distancia_al_centro / 6.0)
                
                # Aplicar gradiente púrpura/magenta más intenso y menos lavado
                color_modificado = (
                    min(0.9, self.color[0] * 0.7 + factor_distancia * 0.3),  # Más rojo controlado
                    max(0.1, self.color[1] * 0.6 - factor_distancia * 0.2),  # Menos verde
                    min(0.9, self.color[2] * 0.8 + factor_distancia * 0.2),  # Más azul controlado
                    self.color[3]
                )
                
                # Configurar material para cada cubo individualmente
                cubo_ambient = [color_modificado[0] * 0.4, color_modificado[1] * 0.4, color_modificado[2] * 0.4, color_modificado[3]]
                cubo_diffuse = [color_modificado[0] * 0.8, color_modificado[1] * 0.8, color_modificado[2] * 0.8, color_modificado[3]]
                
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, cubo_ambient)
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, cubo_diffuse)
                
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

    return EsponjaSierpinski([pos_x, 0, pos_z], color, iteraciones)
