"""
Gestión de interfaz adaptable para diferentes tamaños de pantalla
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import OpenGL.GLUT as GLUT
import config_global as cfg

class InterfazAdaptable:
    def __init__(self):
        self.actualizar_tamano(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
    
    def actualizar_tamano(self, ancho, alto):
        """Actualiza el tamaño de la ventana y recalcula la interfaz"""
        cfg.window_width = ancho
        cfg.window_height = alto
        cfg.aspect_ratio = ancho / alto
        
        # Recalcular tamaños de botones
        self.button_width = (ancho - (cfg.BUTTON_COUNT + 1) * cfg.BUTTON_MARGIN) // cfg.BUTTON_COUNT
        self.button_height = cfg.BUTTON_HEIGHT
        self.button_y = cfg.BUTTON_MARGIN
        
        # Posiciones de botones
        self.button_positions = []
        for i in range(cfg.BUTTON_COUNT):
            x = cfg.BUTTON_MARGIN + i * (self.button_width + cfg.BUTTON_MARGIN)
            self.button_positions.append((x, self.button_y))
    
    def configurar_proyeccion_2d(self):
        """Configura proyección 2D para la interfaz"""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, cfg.window_width, cfg.window_height, 0, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
    
    def restaurar_proyeccion_3d(self):
        """Restaura la proyección 3D"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
    
    def configurar_proyeccion_3d(self):
        """Configura la proyección 3D con aspect ratio correcto"""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, cfg.aspect_ratio, 0.1, 100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

class Boton:
    def __init__(self, x, y, ancho, alto, texto, modo, color):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.texto = texto
        self.modo = modo
        self.color = color
        self.activo = False
    
    def actualizar_posicion(self, x, y, ancho, alto):
        """Actualiza la posición y tamaño del botón"""
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
    
    def contiene_punto(self, x, y):
        return (self.x <= x <= self.x + self.ancho and 
                self.y <= y <= self.y + self.alto)
    
    def dibujar(self, interfaz):
        """Dibuja el botón usando la interfaz adaptable"""
        interfaz.configurar_proyeccion_2d()
        
        # Color del botón
        if self.activo:
            glColor3f(min(1.0, self.color[0] + 0.3), 
                     min(1.0, self.color[1] + 0.3), 
                     min(1.0, self.color[2] + 0.3))
        else:
            glColor3f(*self.color)
        
        # Dibujar fondo del botón
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.ancho, self.y)
        glVertex2f(self.x + self.ancho, self.y + self.alto)
        glVertex2f(self.x, self.y + self.alto)
        glEnd()
        
        # Borde del botón
        glColor3f(0, 0, 0)
        glLineWidth(2)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.ancho, self.y)
        glVertex2f(self.x + self.ancho, self.y + self.alto)
        glVertex2f(self.x, self.y + self.alto)
        glEnd()
        glLineWidth(1)
        
        # Texto del botón (centrado)
        glColor3f(1, 1, 1)
        texto_x = self.x + 10
        texto_y = self.y + self.alto // 2 + 5
        glRasterPos2f(texto_x, texto_y)
        
        # Ajustar tamaño de fuente según el tamaño del botón
        fuente = GLUT.GLUT_BITMAP_HELVETICA_10 if self.ancho < 100 else GLUT.GLUT_BITMAP_HELVETICA_12
        
        for char in self.texto:
            glutBitmapCharacter(fuente, ord(char))
        
        interfaz.restaurar_proyeccion_3d()

def callback_redimensionar(ancho, alto):
    """Callback para cuando se redimensiona la ventana"""
    if alto == 0:
        alto = 1
    
    glViewport(0, 0, ancho, alto)
    
    # Actualizar configuración global
    cfg.window_width = ancho
    cfg.window_height = alto
    cfg.aspect_ratio = ancho / alto
    
    print(f"Ventana redimensionada: {ancho}x{alto}")
