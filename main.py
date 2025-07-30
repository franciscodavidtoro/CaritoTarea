from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import figuras as fg

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(800, 600)
glutCreateWindow(b"Carro en Carretera Curva")

from objetos.terreno import terreno
from objetos.carro import carro

def obtener_direccion_carretera(z):
    """Obtiene la dirección de la carretera para determinar si va hacia izquierda o derecha"""
    amplitud_curva = 50
    factor_z = z / 60
    # Derivada para obtener la pendiente/dirección
    derivada = amplitud_curva * np.cos(factor_z) * (1 + 0.5 * np.sin(factor_z * 3)) / 60
    derivada += amplitud_curva * np.sin(factor_z) * 0.5 * np.cos(factor_z * 3) * 3 / 60
    return derivada

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
        gluPerspective(45, 800/600, 0.1, 200)  # Aumentar el far plane para ver más lejos
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
    rotacion_iniciales = [0]  # Variable para la rotación de las iniciales
    
    
    def dibujar_iniciales():
        """Dibuja las iniciales D y F en 3D en la esquina superior izquierda"""
        glPushMatrix()
        
        # Cambiar a proyección ortográfica para HUD
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -50, 50)  # Mayor rango de profundidad
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Posicionar en esquina superior izquierda y hacer más grandes
        glTranslatef(120, 500, 0)
        glScalef(1.2, 1.2, 1.2)  # Más grandes
        
        # Aplicar rotación para efecto 3D
        glRotatef(rotacion_iniciales[0], 0, 1, 0)  # Rotación en Y
        glRotatef(15, 1, 0, 0)  # Inclinación ligera en X para efecto 3D
        
        # Habilitar iluminación para mejor efecto 3D
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Configurar material para las letras
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.8, 0.8, 0.9, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)
        
        # Dibujar letra "D" con mayor profundidad
        glPushMatrix()
        glTranslatef(-40, 0, 0)
        
        # Parte vertical izquierda de la D (columna de rectángulos)
        for i in range(15):  # 15 rectángulos verticales
            glPushMatrix()
            glTranslatef(-20, -28 + i * 4, 0)
            glScalef(4, 3, 15)
            glutSolidCube(1)
            glPopMatrix()
        
        # Parte superior horizontal de la D (línea de rectángulos)
        for i in range(8):  # 8 rectángulos horizontales
            glPushMatrix()
            glTranslatef(-16 + i * 3, 28, 0)
            glScalef(2.5, 3, 15)
            glutSolidCube(1)
            glPopMatrix()
        
        # Parte inferior horizontal de la D (línea de rectángulos)
        for i in range(8):  # 8 rectángulos horizontales
            glPushMatrix()
            glTranslatef(-16 + i * 3, -28, 0)
            glScalef(2.5, 3, 15)
            glutSolidCube(1)
            glPopMatrix()
        
        # Curva superior derecha de la D (rectángulos siguiendo una curva)
        for i in range(12):
            angle = i * 90.0 / 11  # De 0 a 90 grados
            radius = 18
            x_pos = 8 + radius * np.cos(np.radians(90 - angle))
            y_pos = 10 + radius * np.sin(np.radians(90 - angle))
            glPushMatrix()
            glTranslatef(x_pos, y_pos, 0)
            glRotatef(angle - 45, 0, 0, 1)  # Rotar para seguir la curva
            glScalef(2.5, 3, 15)
            glutSolidCube(1)
            glPopMatrix()
        
        # Curva inferior derecha de la D (rectángulos siguiendo una curva)
        for i in range(12):
            angle = i * 90.0 / 11  # De 0 a 90 grados
            radius = 18
            x_pos = 8 + radius * np.cos(np.radians(90 - angle))
            y_pos = -10 - radius * np.sin(np.radians(90 - angle))
            glPushMatrix()
            glTranslatef(x_pos, y_pos, 0)
            glRotatef(-angle + 45, 0, 0, 1)  # Rotar para seguir la curva
            glScalef(2.5, 3, 15)
            glutSolidCube(1)
            glPopMatrix()
        
        # Parte vertical derecha central de la D (rectángulos)
        for i in range(5):  # 5 rectángulos verticales en el centro derecho
            glPushMatrix()
            glTranslatef(24, -8 + i * 4, 0)
            glScalef(3, 2.5, 15)
            glutSolidCube(1)
            glPopMatrix()
        
        glPopMatrix()
        
        # Dibujar letra "F" con mayor profundidad
        glPushMatrix()
        glTranslatef(40, 0, 0)
        
        # Parte vertical izquierda de la F (más gruesa)
        glPushMatrix()
        glTranslatef(-20, 0, 0)
        glScalef(8, 60, 15)  # Más profundidad (Z=15)
        glutSolidCube(1)
        glPopMatrix()
        
        # Parte superior horizontal de la F
        glPushMatrix()
        glTranslatef(-5, 25, 0)
        glScalef(20, 8, 15)
        glutSolidCube(1)
        glPopMatrix()
        
        # Parte media horizontal de la F
        glPushMatrix()
        glTranslatef(-10, 0, 0)
        glScalef(15, 8, 15)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
        
        # Restaurar proyección
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glPopMatrix()

    def display():
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        set_camera()
        carro.dibujar()
        terreno.dibujar()
        dibujar_iniciales()
        glutSwapBuffers()
    
    def idle():
        # Procesar teclas continuamente
        procesar_teclas()
        
        # Animar la rotación de las iniciales
        rotacion_iniciales[0] += 0.5  # Velocidad de rotación
        if rotacion_iniciales[0] >= 360:
            rotacion_iniciales[0] = 0
        
        # Sistema de iluminación según la dirección de la carretera
        px, py, pz = carro.posicion
        direccion_carretera = obtener_direccion_carretera(pz)
        
        if direccion_carretera > 0:
            # Carretera va hacia la izquierda - DÍA
            luz.color_ambiente = (0.8, 0.8, 0.7, 1)  # Luz de día (amarillo claro)
            glClearColor(0.7, 0.9, 1.0, 1.0)  # Cielo azul de día
        else:
            # Carretera va hacia la derecha - NOCHE
            luz.color_ambiente = (0.1, 0.1, 0.2, 1)  # Luz de noche (azul muy oscuro)
            glClearColor(0.05, 0.05, 0.15, 1.0)  # Cielo oscuro de noche
        
        luz.habilitar()
        glutPostRedisplay()
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutMainLoop()