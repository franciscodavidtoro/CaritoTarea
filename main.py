from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import figuras as fg

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Cubo con hueco esferico")

from objetos.terreno import terreno
from objetos.carro import carro

if __name__ == "__main__":
    # Inicializar GLUT y ventana
    carro.posicion = (0, -0.1, 0)
    
    # Variables para controlar el movimiento del carro
    carro_velocidad = 0.2  # Velocidad reducida para movimiento suave
    carro_direccion = 0  # ángulo en grados
    
    # Diccionario para rastrear teclas presionadas
    teclas_presionadas = {
        b'w': False,
        b's': False,
        b'a': False,
        b'd': False
    }
    
    def keyboard_down(key, x, y):
        """Función llamada cuando se presiona una tecla"""
        if key in teclas_presionadas:
            teclas_presionadas[key] = True
    
    def keyboard_up(key, x, y):
        """Función llamada cuando se suelta una tecla"""
        if key in teclas_presionadas:
            teclas_presionadas[key] = False
    
    def procesar_teclas():
        """Procesa las teclas que están siendo presionadas"""
        global carro_direccion, carro
        
        if teclas_presionadas[b'w']:
            # Avanzar
            dx = carro_velocidad * np.sin(np.radians(carro_direccion))
            dz = carro_velocidad * np.cos(np.radians(carro_direccion))
            px, py, pz = carro.posicion
            carro.posicion = (px + dx, py, pz + dz)
        
        if teclas_presionadas[b's']:
            # Retroceder
            dx = carro_velocidad * np.sin(np.radians(carro_direccion))
            dz = carro_velocidad * np.cos(np.radians(carro_direccion))
            px, py, pz = carro.posicion
            carro.posicion = (px - dx, py, pz - dz)
        
        if teclas_presionadas[b'a']:
            # Girar a la izquierda
            carro_direccion += 2  # Velocidad de giro reducida
        
        if teclas_presionadas[b'd']:
            # Girar a la derecha
            carro_direccion -= 2
    
    def set_camera():
        camera_distance = 10
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        px, py, pz = carro.posicion
        rad = np.radians(carro_direccion)
        
        cam_x = px - camera_distance * np.sin(rad)
        cam_y = py + 5
        cam_z = pz - camera_distance * np.cos(rad)
        carro.rotacion = (0, 270 + carro_direccion, 0)
        gluLookAt(cam_x, cam_y, cam_z, px, py, pz, 0, 1, 0)
    
    # Configurar callbacks de teclado
    glutKeyboardFunc(keyboard_down)
    glutKeyboardUpFunc(keyboard_up)
    glutIgnoreKeyRepeat(1)  # Ignorar repetición automática del sistema
    
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.7, 0.9, 1.0, 1.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Luz global
    luz = fg.LuzGlobal()
    luz.habilitar()
    
    # Variables para el ángulo de la cámara y control del mouse
    angulo = [0]
    
    
    def display():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        set_camera()
        carro.dibujar()
        terreno.dibujar()
        glutSwapBuffers()
    
    def idle():
        
        
        # Procesar teclas continuamente
        procesar_teclas()
        
        if carro.posicion[0] < 0:
            luz.color_ambiente = (0.1, 0.1, 0.1, 1)
        else:
            luz.color_ambiente = (0.6, 0.6, 0.6, 1)
        
        luz.habilitar()
        glutPostRedisplay()
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()