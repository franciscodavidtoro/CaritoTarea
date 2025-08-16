from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np

from PIL import Image

def cargarTextura(path):
    img = Image.open(path)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(img.convert("RGBA"), dtype=np.uint8)

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glBindTexture(GL_TEXTURE_2D, 0)
    return textura_id




class LuzGlobal:
    """Clase para manejar la luz global en la escena OpenGL"""

    def __init__(self, posicion=(10.0, 10.0, 10.0, 0.0), color_ambiente=(0.6, 0.6, 0.6, 1.0), color_difusa=(0.01, 0.01, 0.01, 1.0), color_especular=(0.01, 0.01, 0.01, 1.0)):
        self.posicion = posicion
        self.color_ambiente = color_ambiente
        self.color_difusa = color_difusa
        self.color_especular = color_especular

    def habilitar(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, self.posicion)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.color_ambiente)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.color_difusa)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.color_especular)

    def deshabilitar(self):
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)


class Figura:
    """Clase base para las figuras primitivas que componen los objetos 3D"""
    
    def __init__(self, tipo='cubo', posicion=(0, 0, 0), rotacion=(0, 0, 0), escala=(1,1,1), color=(1.0, 1.0, 1.0,1.0), textura=None, argumentos=None, sombra=True):
        """
        Inicializa una figura 3D genérica. Puede representar cualquier figura primitiva (cubo, esfera, toroide, tetera, cono, etc).
        - tipo: tipo de figura ('cubo', 'esfera', 'toroide', 'tetera', 'cono', etc)
        - posicion: tupla (x, y, z)
        - rotacion: tupla (rx, ry, rz)
        - color: tupla RGBA
        - textura_id: id de textura OpenGL
        - argumentos: parámetros adicionales para la figura (por ejemplo, radio y altura para el cono)
        """
        self.tipo = tipo
        self.posicion = posicion
        self.rotacion = rotacion
        self.color = color
        self.textura_id = textura
        self.show_wireframe = False
        self.argumentos = argumentos
        self.escala = escala
        self.sombra=sombra
        
    def dibujar(self):
        glPushMatrix()
        
        
        
        glTranslatef(*self.posicion)
        glRotatef(self.rotacion[0], 1, 0, 0)
        glRotatef(self.rotacion[1], 0, 1, 0)
        glRotatef(self.rotacion[2], 0, 0, 1)
        glScale(self.escala[0], self.escala[1], self.escala[2])
        glColor4f(*self.color)
        # Configurar el material para que el color funcione con iluminación
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, self.color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0.0)
        
        if self.show_wireframe:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self.tipo == 'cubo' and self.textura_id is not None:
            # Dibuja el cubo normalmente
            glutSolidCube(1)
            # Dibuja la cara superior con textura encima
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textura_id)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            glBegin(GL_QUADS)
            glNormal3f(0, 1, 0)
            glTexCoord2f(0, 0)
            glVertex3f(-0.5, 0.51, -0.5)
            glTexCoord2f(1, 0)
            glVertex3f(0.5, 0.51, -0.5)
            glTexCoord2f(1, 1)
            glVertex3f(0.5, 0.51, 0.5)
            glTexCoord2f(0, 1)
            glVertex3f(-0.5, 0.51, 0.5)
            glEnd()
            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)
        elif self.tipo == 'cubo':
            glutSolidCube(1)
        elif self.tipo == 'esfera':
            quad = gluNewQuadric()
            gluSphere(quad, self.argumentos, 32, 32)
        elif self.tipo == 'toroide':
            glutSolidTorus(self.argumentos[0], self.argumentos[1], 32, 32)
        elif self.tipo == 'tetera':
            glutSolidTeapot(1)
        elif self.tipo == 'cono':
            # argumentos: (base, altura)
            base = self.argumentos[0] if self.argumentos and len(self.argumentos) > 0 else 0.5
            altura = self.argumentos[1] if self.argumentos and len(self.argumentos) > 1 else 1.0
            quad = gluNewQuadric()
            gluCylinder(quad, base, 0.0, altura, 32, 32)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPopMatrix()
        
    def dibujarSombra(self, y):
        if self.sombra:
            glPushMatrix()
            glTranslatef(self.posicion[0], y, self.posicion[2])
            glScalef(self.escala[0], 0.001, self.escala[2])  # Aplana la figura para simular la sombra
            glRotatef(self.rotacion[0], 1, 0, 0)
            glRotatef(self.rotacion[1], 0, 1, 0)
            glRotatef(self.rotacion[2], 0, 0, 1)
            
            glColor4f(0.0, 0.0, 0.0, 0.5)  # Sombra semitransparente

            glDisable(GL_LIGHTING)
            if hasattr(self, 'tipo'):
                if self.tipo == 'cubo':
                    glutSolidCube(1)
                elif self.tipo == 'esfera':
                    quad = gluNewQuadric()
                    gluSphere(quad, self.argumentos, 32, 32)
                elif self.tipo == 'toroide':
                    glutSolidTorus(self.argumentos[0], self.argumentos[1], 32, 32)
                elif self.tipo == 'tetera':
                    glutSolidTeapot(1)
                elif self.tipo == 'cono':
                    base = self.argumentos[0] if self.argumentos and len(self.argumentos) > 0 else 0.5
                    altura = self.argumentos[1] if self.argumentos and len(self.argumentos) > 1 else 1.0
                    quad = gluNewQuadric()
                    gluCylinder(quad, base, 0.0, altura, 32, 32)
                elif self.tipo == 'cono':
                # argumentos: (base, altura)
                    base = self.argumentos[0] if self.argumentos and len(self.argumentos) > 0 else 0.5
                    altura = self.argumentos[1] if self.argumentos and len(self.argumentos) > 1 else 1.0
                    quad = gluNewQuadric()
                    gluCylinder(quad, base, 0.0, altura, 32, 32)
            glEnable(GL_LIGHTING)

            glPopMatrix()
        
    def __repr__(self):
        return (f"Figura(tipo={self.tipo}, posicion={self.posicion}, escala={self.escala}, "
                f"color={self.color}, rotacion={self.rotacion}, argumentos={self.argumentos})")
    
    


class Objeto3D:
    """Clase base para objetos 3D complejos"""
    
    def __init__(self, posicion=(0, 0, 0), rotacion=(0, 0, 0), escala=(1, 1, 1)):
        self.posicion = posicion
        self.rotacion = rotacion
        self.escala = escala
        self.figuras = []
        
    
    
    
    def dibujar(self):
        glPushMatrix()
        
        # Aplicar transformaciones del objeto
        glTranslatef(*self.posicion)
        
        glRotatef(self.rotacion[0], 1, 0, 0)
        glRotatef(self.rotacion[1], 0, 1, 0)
        glRotatef(self.rotacion[2], 0, 0, 1)
        glScalef(*self.escala)
        
        # Dibujar cada figura
        for item in self.figuras:
            item.dibujar()
            #item.dibujarSombra(-1)
        
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(*self.posicion)
        glScalef(*self.escala)
        glRotatef(self.rotacion[0], 1, 0, 0)
        glRotatef(self.rotacion[1], 0, 1, 0)
        glRotatef(self.rotacion[2], 0, 0, 1)
        
        
        # Dibujar cada figura
        for item in self.figuras:
            
            item.dibujarSombra(-0.4)
        
        glPopMatrix()