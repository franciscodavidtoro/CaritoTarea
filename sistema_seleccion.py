"""
Sistema de selección y movimiento de objetos
"""

import config_global as cfg
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class SistemaSeleccion:
    def __init__(self):
        self.objeto_seleccionado = None
        self.arrastrando_objeto = False
        self.offset_arrastre = (0, 0, 0)
        self.pos_inicial_arrastre = None
    
    def detectar_objeto_bajo_cursor(self, objetos, pos_3d):
        """Detecta qué objeto está bajo el cursor del mouse"""
        objeto_cercano = None
        distancia_minima = float('inf')
        
        for objeto in objetos:
            # Calcular distancia entre cursor y objeto
            dx = pos_3d[0] - objeto.posicion[0]
            dz = pos_3d[2] - objeto.posicion[2]
            distancia = (dx**2 + dz**2)**0.5
            
            # Si está dentro del radio de selección y es más cercano
            if distancia < cfg.SELECTION_RADIUS and distancia < distancia_minima:
                distancia_minima = distancia
                objeto_cercano = objeto
        
        return objeto_cercano
    
    def deseleccionar_todos(self, objetos):
        """Deselecciona todos los objetos"""
        for objeto in objetos:
            objeto.seleccionado = False
        self.objeto_seleccionado = None
    
    def seleccionar_objeto(self, objeto):
        """Selecciona un objeto específico"""
        if objeto:
            objeto.seleccionado = True
            self.objeto_seleccionado = objeto
            print(f"Objeto seleccionado: {objeto.nombre}")
        else:
            self.objeto_seleccionado = None
    
    def iniciar_arrastre(self, pos_3d):
        """Inicia el arrastre de un objeto"""
        if self.objeto_seleccionado:
            self.arrastrando_objeto = True
            self.pos_inicial_arrastre = pos_3d
            # Calcular offset entre mouse y objeto
            self.offset_arrastre = (
                self.objeto_seleccionado.posicion[0] - pos_3d[0],
                self.objeto_seleccionado.posicion[1] - pos_3d[1],
                self.objeto_seleccionado.posicion[2] - pos_3d[2]
            )
            print(f"Iniciando arrastre de {self.objeto_seleccionado.nombre}")
    
    def actualizar_arrastre(self, pos_3d):
        """Actualiza la posición durante el arrastre"""
        if self.arrastrando_objeto and self.objeto_seleccionado:
            # Calcular nueva posición con offset
            nueva_pos = [
                pos_3d[0] + self.offset_arrastre[0],
                self.objeto_seleccionado.posicion[1],  # Mantener Y
                pos_3d[2] + self.offset_arrastre[2]
            ]
            
            # Limitar el área de movimiento
            nueva_pos[0] = max(-cfg.TERRAIN_LIMIT, min(cfg.TERRAIN_LIMIT, nueva_pos[0]))
            nueva_pos[2] = max(-cfg.TERRAIN_LIMIT, min(cfg.TERRAIN_LIMIT, nueva_pos[2]))
            
            # Calcular el desplazamiento
            dx = nueva_pos[0] - self.objeto_seleccionado.posicion[0]
            dy = nueva_pos[1] - self.objeto_seleccionado.posicion[1]
            dz = nueva_pos[2] - self.objeto_seleccionado.posicion[2]
            
            # Actualizar posición del objeto
            self.objeto_seleccionado.posicion = nueva_pos
            
            # Actualizar todas las figuras del objeto
            for figura in self.objeto_seleccionado.figuras:
                figura.posicion = (
                    figura.posicion[0] + dx,
                    figura.posicion[1] + dy,
                    figura.posicion[2] + dz
                )
    
    def terminar_arrastre(self):
        """Termina el arrastre"""
        if self.arrastrando_objeto and self.objeto_seleccionado:
            print(f"Objeto {self.objeto_seleccionado.nombre} movido a: ({self.objeto_seleccionado.posicion[0]:.1f}, {self.objeto_seleccionado.posicion[1]:.1f}, {self.objeto_seleccionado.posicion[2]:.1f})")
        self.arrastrando_objeto = False
        self.pos_inicial_arrastre = None
    
    def dibujar_indicador_seleccion(self, objetos, mouse_pos_3d, modo_actual):
        """Dibuja indicadores de selección"""
        if modo_actual == "seleccionar":
            # Indicador de hover
            for objeto in objetos:
                dx = mouse_pos_3d[0] - objeto.posicion[0]
                dz = mouse_pos_3d[2] - objeto.posicion[2]
                distancia = (dx**2 + dz**2)**0.5
                
                if distancia < cfg.SELECTION_RADIUS + 0.5:
                    glPushMatrix()
                    glTranslatef(*objeto.posicion)
                    glDisable(GL_LIGHTING)
                    glColor4f(*cfg.COLOR_HOVER)
                    glLineWidth(cfg.HOVER_LINE_WIDTH)
                    glutWireCube(3.5)
                    glLineWidth(1)
                    glEnable(GL_LIGHTING)
                    glPopMatrix()
                    break  # Solo mostrar para el más cercano
