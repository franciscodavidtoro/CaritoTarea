from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import figuras as fg

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Cubo con hueco esferico")

from objetos.ventaBug import test

if __name__ == "__main__":
    carro_direccion=0
    
    def set_camera():
        global carro_direccion
        camera_distance = 10
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 800/600, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        px, py, pz = (0,0,0)
        rad = np.radians(carro_direccion)
        
        cam_x = px - camera_distance * np.sin(rad)
        cam_y = py + 5
        cam_z = pz - camera_distance * np.cos(rad)
        
        gluLookAt(cam_x, cam_y, cam_z, px, py, pz, 0, 1, 0)
    
    # Configurar callbacks de teclado
    
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
        test.dibujar()
        
        glutSwapBuffers()
    
    def idle():
        global carro_direccion
        carro_direccion=(carro_direccion+0.05) % 360
        
        luz.habilitar()
        glutPostRedisplay()
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()