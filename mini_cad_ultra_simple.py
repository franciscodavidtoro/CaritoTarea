from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import OpenGL.GLUT as GLUT
import numpy as np
import figuras as fg

# Importar módulos del sistema
import config_global as cfg
from interfaz_adaptable import InterfazAdaptable, Boton, callback_redimensionar
from sistema_seleccion import SistemaSeleccion

# Importar funciones de creación de objetos
from objetos.arboles import crear_arbol
from objetos.casas import crear_casa

# Función para crear montaña (basada en gupoMontannas.py)
def crear_montana(pos_x, pos_z):
    montana = fg.Figura(
        tipo='cono',
        posicion=(pos_x, -0.5, pos_z),
        rotacion=(-90, 0, 0),
        escala=(2.5, 3, 2.5),
        color=(0.3, 0.6, 0.2, 1.0),
        argumentos=(1.0, 1.5)
    )
    return [montana]

# Función para crear luz
def crear_luz(pos_x, pos_z):
    # Poste
    poste = fg.Figura(
        tipo='cubo',
        posicion=(pos_x, 1.5, pos_z),
        escala=(0.1, 3.0, 0.1),
        color=(0.3, 0.3, 0.3, 1.0)
    )
    # Lámpara
    lampara = fg.Figura(
        tipo='esfera',
        posicion=(pos_x, 3.0, pos_z),
        escala=(0.6, 0.6, 0.6),
        color=(0.9, 0.9, 0.2, 1.0),
        argumentos=0.3
    )
    return [poste, lampara]

# Inicializar GLUT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)
glutCreateWindow(b"Mini CAD Adaptable - Seleccionar y Mover")

# Inicializar sistemas
interfaz = InterfazAdaptable()
sistema_seleccion = SistemaSeleccion()

# Variables globales
objetos = []
modo_actual = "navegacion"
contador_objetos = 0
color_actual = [0.2, 0.8, 0.2, 1.0]
mouse_pos_3d = (0, 0, 0)

# Variables de cámara
camera_pos = list(cfg.DEFAULT_CAMERA_POS)
camera_target = list(cfg.DEFAULT_CAMERA_TARGET)
camera_speed = cfg.DEFAULT_CAMERA_SPEED
camera_angle = 0.0
camera_rotation_speed = cfg.DEFAULT_CAMERA_ROTATION_SPEED

# Botones de la interfaz
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
    
    def contiene_punto(self, x, y):
        return (self.x <= x <= self.x + self.ancho and 
                self.y <= y <= self.y + self.alto)
    
    def dibujar(self):
        # Cambiar a proyección 2D usando dimensiones actuales de la ventana
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT, 0, -1, 1)  # Y invertida para coincidir con coordenadas de mouse
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        
        # Color del botón
        if self.activo:
            glColor3f(self.color[0] + 0.3, self.color[1] + 0.3, self.color[2] + 0.3)
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
        
        # Texto del botón
        glColor3f(1, 1, 1)
        texto_x = self.x + 10
        texto_y = self.y + self.alto // 2 + 5
        glRasterPos2f(texto_x, texto_y)
        for char in self.texto:
            glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord(char))
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # Restaurar matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

# Crear botones adaptables
def crear_botones(interfaz):
    """Crea botones usando la interfaz adaptable"""
    botones_info = [
        ("🌳 ARBOL", "arbol", [0.2, 0.8, 0.2]),
        ("🏠 CASA", "casa", [0.8, 0.6, 0.3]),
        ("⛰️ MONTANA", "montana", [0.5, 0.5, 0.8]),
        ("💡 LUZ", "luz", [0.9, 0.9, 0.2]),
        ("👆 SELECT", "seleccionar", [0.8, 0.2, 0.8])
    ]
    
    botones = []
    for i, (texto, modo, color) in enumerate(botones_info):
        x, y = interfaz.button_positions[i]
        boton = Boton(x, y, interfaz.button_width, interfaz.button_height, texto, modo, color)
        botones.append(boton)
    
    return botones

# Inicializar botones
botones = crear_botones(interfaz)

class Objeto:
    def __init__(self, tipo, posicion, color, nombre):
        self.tipo = tipo
        self.posicion = list(posicion)
        self.color = color
        self.nombre = nombre
        self.seleccionado = False
        self.figuras = []
        
        # Crear las figuras usando las funciones de la carpeta objetos
        if tipo == "arbol":
            self.figuras = crear_arbol(posicion[0], posicion[2])
        elif tipo == "casa":
            # Usar colores por defecto para la casa
            color_casa = (0.8, 0.6, 0.4, 1.0)
            color_techo = (0.7, 0.2, 0.2, 1.0)
            self.figuras = crear_casa(posicion[0], posicion[2], color_casa, color_techo)
        elif tipo == "montana":
            self.figuras = crear_montana(posicion[0], posicion[2])
        elif tipo == "luz":
            self.figuras = crear_luz(posicion[0], posicion[2])
    
    def dibujar(self):
        # Si está seleccionado, dibujar wireframe de selección
        if self.seleccionado:
            glPushMatrix()
            glTranslatef(*self.posicion)
            
            # Color amarillo brillante para selección
            glColor4f(1, 1, 0, 1)  # Amarillo
            glLineWidth(4)
            
            # Dibujar múltiples wireframes para efecto más visible
            glDisable(GL_LIGHTING)  # Desactivar iluminación para wireframe
            
            # Wireframe exterior
            glutWireCube(4.0)
            
            # Wireframe interior más pequeño
            glColor4f(1, 0.8, 0, 0.8)  # Amarillo-naranja semi-transparente
            glutWireCube(3.0)
            
            glLineWidth(1)
            glEnable(GL_LIGHTING)  # Reactivar iluminación
            glPopMatrix()
        
        # Dibujar todas las figuras del objeto
        for figura in self.figuras:
            figura.dibujar()

def configurar_luces():
    """Configura la iluminación básica"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    
    # Luz ambiente
    luz_ambiente = [0.3, 0.3, 0.3, 1.0]
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    
    # Luz difusa
    luz_difusa = [0.8, 0.8, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    
    # Posición de la luz
    posicion_luz = [0.0, 10.0, 5.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, posicion_luz)
    
    # Luces adicionales de objetos tipo "luz"
    light_num = GL_LIGHT1
    for objeto in objetos:
        if objeto.tipo == "luz" and light_num <= GL_LIGHT7:
            glEnable(light_num)
            glLightfv(light_num, GL_POSITION, [*objeto.posicion, 1.0])
            glLightfv(light_num, GL_DIFFUSE, [1.0, 1.0, 0.8, 1.0])
            glLightfv(light_num, GL_AMBIENT, [0.2, 0.2, 0.1, 1.0])
            light_num += 1

def dibujar_terreno():
    """Dibuja un terreno verde adaptable"""
    glPushMatrix()
    glTranslatef(0, -0.5, 0)
    glScalef(cfg.TERRAIN_SIZE, 0.1, cfg.TERRAIN_SIZE)
    glColor3f(*cfg.COLOR_TERRAIN)
    glutSolidCube(1)
    glPopMatrix()

def set_camera():
    """Configura la cámara con movimiento WASD y rotación QE usando interfaz adaptable"""
    interfaz.configurar_proyeccion_3d()
    
    # Calcular la dirección de la cámara basada en el ángulo
    import math
    angle_rad = math.radians(camera_angle)
    distance = cfg.CAMERA_DISTANCE
    
    # Calcular posición de la cámara en círculo alrededor del target
    camera_pos[0] = camera_target[0] + distance * math.cos(angle_rad)
    camera_pos[2] = camera_target[2] + distance * math.sin(angle_rad)
    
    # Cámara con variables dinámicas
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],  # Posición de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Hacia dónde mira
              0, 1, 0)  # Vector "arriba"

def mouse_click(button, state, x, y):
    """Maneja clics del mouse usando el nuevo sistema"""
    global modo_actual, contador_objetos
    
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            # Verificar si se hizo clic en algún botón
            boton_clickeado = False
            for boton in botones:
                if boton.contiene_punto(x, y):
                    # Desactivar todos los botones
                    for b in botones:
                        b.activo = False
                    
                    # Activar el botón clickeado
                    boton.activo = True
                    modo_actual = boton.modo
                    print(f"Modo cambiado a: {modo_actual}")
                    
                    # Si cambiamos a modo seleccionar, deseleccionar todo
                    if modo_actual == "seleccionar":
                        sistema_seleccion.deseleccionar_todos(objetos)
                    
                    boton_clickeado = True
                    break
            
            # Si no se hizo clic en un botón
            if not boton_clickeado:
                pos_3d = convertir_mouse_a_3d(x, y)
                
                if modo_actual == "seleccionar":
                    # Modo selección
                    objeto_bajo_cursor = sistema_seleccion.detectar_objeto_bajo_cursor(objetos, pos_3d)
                    if objeto_bajo_cursor:
                        if objeto_bajo_cursor == sistema_seleccion.objeto_seleccionado:
                            # Si ya está seleccionado, comenzar a arrastrar
                            sistema_seleccion.iniciar_arrastre(pos_3d)
                        else:
                            # Seleccionar nuevo objeto
                            sistema_seleccion.deseleccionar_todos(objetos)
                            sistema_seleccion.seleccionar_objeto(objeto_bajo_cursor)
                    else:
                        # No hay objeto bajo cursor, deseleccionar
                        sistema_seleccion.deseleccionar_todos(objetos)
                        
                elif modo_actual != "navegacion":
                    # Modo agregar objeto
                    agregar_objeto(modo_actual, pos_3d)
        
        elif state == GLUT_UP:
            # Terminar arrastre
            sistema_seleccion.terminar_arrastre()
        
        glutPostRedisplay()

def mouse_motion(x, y):
    """Maneja el movimiento del mouse usando el nuevo sistema"""
    global mouse_pos_3d
    
    pos_3d = convertir_mouse_a_3d(x, y)
    
    if sistema_seleccion.arrastrando_objeto:
        # Actualizar arrastre
        sistema_seleccion.actualizar_arrastre(pos_3d)
        glutPostRedisplay()
    elif modo_actual != "navegacion" and modo_actual != "seleccionar":
        # Vista previa para agregar objetos
        mouse_pos_3d = pos_3d
        glutPostRedisplay()
    elif modo_actual == "seleccionar":
        # Actualizar posición del mouse para indicadores
        mouse_pos_3d = pos_3d
        glutPostRedisplay()

def convertir_mouse_a_3d(mouse_x, mouse_y):
    """Convierte coordenadas del mouse a coordenadas 3D en el plano Y=0"""
    global camera_pos, camera_target, camera_angle
    import math
    
    # Configurar las mismas matrices que usa la cámara actual
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Usar las mismas coordenadas de cámara que en set_camera()
    angle_rad = math.radians(camera_angle)
    distance = 15.0
    cam_x = camera_target[0] + distance * math.cos(angle_rad)
    cam_y = camera_pos[1]  # Mantener altura Y
    cam_z = camera_target[2] + distance * math.sin(angle_rad)
    
    gluLookAt(cam_x, cam_y, cam_z,  # Posición actual de la cámara
              camera_target[0], camera_target[1], camera_target[2],  # Target actual
              0, 1, 0)    # Vector "arriba"
    
    # Obtener matrices actuales
    try:
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        # Coordenadas del mouse en el sistema de ventana
        win_x = float(mouse_x)
        win_y = float(viewport[3] - mouse_y)  # Invertir Y
        
        # Hacer ray casting desde el mouse hacia la escena
        # Obtener dos puntos en el rayo (cerca y lejos)
        try:
            # Punto cercano en el rayo
            obj_x1, obj_y1, obj_z1 = gluUnProject(
                win_x, win_y, 0.0,  # z=0 (plano cercano)
                modelview, projection, viewport
            )
            
            # Punto lejano en el rayo
            obj_x2, obj_y2, obj_z2 = gluUnProject(
                win_x, win_y, 1.0,  # z=1 (plano lejano)
                modelview, projection, viewport
            )
            
            # Calcular la intersección del rayo con el plano Y=0
            # Dirección del rayo
            dir_x = obj_x2 - obj_x1
            dir_y = obj_y2 - obj_y1
            dir_z = obj_z2 - obj_z1
            
            # Evitar división por cero
            if abs(dir_y) < 0.0001:
                # El rayo es paralelo al plano Y=0, usar una posición por defecto
                world_x = (mouse_x - 400) / 40.0
                world_z = (mouse_y - 300) / 40.0
                world_y = 0
            else:
                # Calcular el parámetro t donde el rayo intersecta Y=0
                t = -obj_y1 / dir_y
                
                # Calcular la posición de intersección
                world_x = obj_x1 + t * dir_x
                world_y = 0  # En el plano del suelo
                world_z = obj_z1 + t * dir_z
        
        except Exception as e:
            # Si falla el unprojection, usar método simplificado
            print(f"Error en unprojection: {e}")
            norm_x = (mouse_x - 400) / 400.0
            norm_y = (mouse_y - 300) / 300.0
            world_x = norm_x * 20
            world_z = norm_y * 20
            world_y = 0
    
    except Exception as e:
        print(f"Error en conversión de coordenadas: {e}")
        # Método de respaldo
        norm_x = (mouse_x - 400) / 400.0
        norm_y = (mouse_y - 300) / 300.0
        world_x = norm_x * 20
        world_z = norm_y * 20
        world_y = 0
    
    finally:
        # Restaurar matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()
    
    return (world_x, world_y, world_z)

def agregar_objeto(tipo, posicion):
    """Agrega un objeto a la escena"""
    global contador_objetos
    
    contador_objetos += 1
    nombre = f"{tipo.capitalize()} {contador_objetos}"
    
    x, y, z = posicion
    
    # Limitar el área de colocación para evitar objetos muy lejos
    x = max(-40, min(40, x))  # Limitar X entre -40 y 40
    z = max(-40, min(40, z))  # Limitar Z entre -40 y 40
    
    # Ajustar la posición Y según el tipo de objeto
    if tipo in ["arbol", "casa", "montana"]:
        y = 0  # En el suelo
    elif tipo == "luz":
        y = 0  # En el suelo también
    
    nuevo_objeto = Objeto(
        tipo=tipo,
        posicion=(x, y, z),
        color=color_actual.copy(),
        nombre=nombre
    )
    
    objetos.append(nuevo_objeto)
    print(f"Agregado: {nombre} en ({x:.1f}, {y:.1f}, {z:.1f})")

def dibujar_info():
    """Dibuja información en pantalla"""
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT, 0, -1, 1)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    # Información en la parte inferior
    glColor3f(1, 1, 1)
    
    info = [
        f"Mini CAD Simple - Modo: {modo_actual.upper()}",
        f"Objetos en escena: {len(objetos)}",
        f"Posición del cursor: ({mouse_pos_3d[0]:.1f}, {mouse_pos_3d[1]:.1f}, {mouse_pos_3d[2]:.1f})",
        f"Cámara: ({camera_pos[0]:.1f}, {camera_pos[1]:.1f}, {camera_pos[2]:.1f})",
    ]
    
    # Agregar información del objeto seleccionado
    if sistema_seleccion.objeto_seleccionado:
        info.extend([
            f"📍 Seleccionado: {sistema_seleccion.objeto_seleccionado.nombre}",
            f"   Posición: ({sistema_seleccion.objeto_seleccionado.posicion[0]:.1f}, {sistema_seleccion.objeto_seleccionado.posicion[1]:.1f}, {sistema_seleccion.objeto_seleccionado.posicion[2]:.1f})",
            f"   {'🔄 Arrastrando...' if sistema_seleccion.arrastrando_objeto else '👆 Haz clic y arrastra para mover'}"
        ])
    
    info.extend([
        "Instrucciones:",
        "1. Haz clic en un botón para seleccionar herramienta",
        "2. Mueve el mouse para ver vista previa",
        "3. Haz clic en el terreno para agregar objeto",
        "4. Usa SELECCIONAR para elegir y mover objetos",
        "5. Usa WASD para mover la cámara",
        "6. Usa Q/E para rotar la cámara",
        "7. ESC para limpiar escena"
    ])
    
    y_start = 100
    for i, linea in enumerate(info):
        glRasterPos2f(20, y_start + i * 20)
        for char in linea:
            glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord(char))
    
    # Mostrar modo actual en grande
    if modo_actual != "navegacion":
        glColor3f(1, 1, 0)  # Amarillo
        glRasterPos2f(300, 80)
        texto_modo = f"MODO: {modo_actual.upper()}"
        for char in texto_modo:
            glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_18, ord(char))
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def dibujar_vista_previa():
    """Dibuja una vista previa del objeto que se va a colocar"""
    if modo_actual != "navegacion":
        glPushMatrix()
        glTranslatef(*mouse_pos_3d)
        
        # Dibujar wireframe semitransparente
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1, 1, 1, 0.5)  # Blanco semitransparente
        glLineWidth(2)
        
        if modo_actual == "arbol":
            glutWireCube(2.0)
        elif modo_actual == "casa":
            glutWireCube(2.5)
        elif modo_actual == "montana":
            glutWireCube(4.0)
        elif modo_actual == "luz":
            glutWireCube(1.5)
            
        glLineWidth(1)
        glDisable(GL_BLEND)
        glPopMatrix()

def dibujar_indicador_seleccion():
    """Dibuja un indicador cuando el mouse está sobre un objeto seleccionable"""
    if modo_actual == "seleccionar":
        # Buscar si hay un objeto bajo el cursor actual (aproximado)
        for objeto in objetos:
            # Calcular distancia aproximada al cursor
            dx = mouse_pos_3d[0] - objeto.posicion[0]
            dz = mouse_pos_3d[2] - objeto.posicion[2]
            distancia = (dx**2 + dz**2)**0.5
            
            # Si está cerca, mostrar indicador
            if distancia < 2.5:
                glPushMatrix()
                glTranslatef(*objeto.posicion)
                glDisable(GL_LIGHTING)
                glColor4f(0, 1, 1, 0.5)  # Cian semi-transparente
                glLineWidth(2)
                glutWireCube(3.5)
                glLineWidth(1)
                glEnable(GL_LIGHTING)
                glPopMatrix()
                break  # Solo mostrar para el más cercano

def display():
    """Función principal de dibujado"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    set_camera()
    configurar_luces()
    
    # Dibujar terreno
    dibujar_terreno()
    
    # Dibujar todos los objetos
    for objeto in objetos:
        objeto.dibujar()
    
    # Dibujar indicador de selección usando el sistema
    sistema_seleccion.dibujar_indicador_seleccion(objetos, mouse_pos_3d, modo_actual)
    
    # Dibujar vista previa
    dibujar_vista_previa()
    
    # Dibujar botones usando la interfaz adaptable
    for boton in botones:
        boton.dibujar()
    
    # Dibujar información
    dibujar_info()
    
    # Dibujar indicador de selección
    dibujar_indicador_seleccion()
    
    glutSwapBuffers()

def keyboard(key, x, y):
    """Maneja teclas del teclado"""
    global objetos, camera_pos, camera_target, camera_angle
    
    # Limpiar escena con ESC
    if key == b'\x1b':  # ESC
        objetos.clear()
        print("Escena limpiada")
        glutPostRedisplay()
    
    # Movimiento de cámara con WASD
    elif key == b'w' or key == b'W':  # Mover hacia adelante
        # Calcular dirección hacia adelante
        dx = camera_target[0] - camera_pos[0]
        dz = camera_target[2] - camera_pos[2]
        # Normalizar
        length = (dx**2 + dz**2)**0.5
        if length > 0:
            dx /= length
            dz /= length
        # Mover cámara y target
        camera_pos[0] += dx * camera_speed
        camera_pos[2] += dz * camera_speed
        camera_target[0] += dx * camera_speed
        camera_target[2] += dz * camera_speed
        glutPostRedisplay()
        
    elif key == b's' or key == b'S':  # Mover hacia atrás
        # Calcular dirección hacia atrás
        dx = camera_target[0] - camera_pos[0]
        dz = camera_target[2] - camera_pos[2]
        # Normalizar
        length = (dx**2 + dz**2)**0.5
        if length > 0:
            dx /= length
            dz /= length
        # Mover cámara y target
        camera_pos[0] -= dx * camera_speed
        camera_pos[2] -= dz * camera_speed
        camera_target[0] -= dx * camera_speed
        camera_target[2] -= dz * camera_speed
        glutPostRedisplay()
        
    elif key == b'a' or key == b'A':  # Mover hacia la izquierda
        # Calcular dirección hacia adelante
        dx = camera_target[0] - camera_pos[0]
        dz = camera_target[2] - camera_pos[2]
        # Calcular dirección perpendicular (izquierda)
        left_dx = -dz
        left_dz = dx
        # Normalizar
        length = (left_dx**2 + left_dz**2)**0.5
        if length > 0:
            left_dx /= length
            left_dz /= length
        # Mover cámara y target
        camera_pos[0] += left_dx * camera_speed
        camera_pos[2] += left_dz * camera_speed
        camera_target[0] += left_dx * camera_speed
        camera_target[2] += left_dz * camera_speed
        glutPostRedisplay()
        
    elif key == b'd' or key == b'D':  # Mover hacia la derecha
        # Calcular dirección hacia adelante
        dx = camera_target[0] - camera_pos[0]
        dz = camera_target[2] - camera_pos[2]
        # Calcular dirección perpendicular (derecha)
        right_dx = dz
        right_dz = -dx
        # Normalizar
        length = (right_dx**2 + right_dz**2)**0.5
        if length > 0:
            right_dx /= length
            right_dz /= length
        # Mover cámara y target
        camera_pos[0] += right_dx * camera_speed
        camera_pos[2] += right_dz * camera_speed
        camera_target[0] += right_dx * camera_speed
        camera_target[2] += right_dz * camera_speed
        glutPostRedisplay()
    
    # Rotación de cámara con Q y E
    elif key == b'q' or key == b'Q':  # Rotar hacia la izquierda
        camera_angle -= camera_rotation_speed
        glutPostRedisplay()
        
    elif key == b'e' or key == b'E':  # Rotar hacia la derecha
        camera_angle += camera_rotation_speed
        glutPostRedisplay()
    
    # Mostrar posición actual de la cámara
    print(f"Cámara en: ({camera_pos[0]:.1f}, {camera_pos[1]:.1f}, {camera_pos[2]:.1f}) - Ángulo: {camera_angle:.1f}°")

def detectar_objeto_bajo_cursor(mouse_x, mouse_y):
    """Detecta qué objeto está bajo el cursor del mouse"""
    global camera_pos, camera_target, camera_angle
    
    # Convertir coordenadas del mouse a 3D
    pos_3d = convertir_mouse_a_3d(mouse_x, mouse_y)
    
    # Buscar el objeto más cercano al cursor
    objeto_cercano = None
    distancia_minima = float('inf')
    
    for objeto in objetos:
        # Calcular distancia entre cursor y objeto
        dx = pos_3d[0] - objeto.posicion[0]
        dz = pos_3d[2] - objeto.posicion[2]
        distancia = (dx**2 + dz**2)**0.5
        
        # Si está dentro del radio de selección y es más cercano
        radio_seleccion = 2.0  # Radio de selección
        if distancia < radio_seleccion and distancia < distancia_minima:
            distancia_minima = distancia
            objeto_cercano = objeto
    
    return objeto_cercano

def deseleccionar_todos():
    """Deselecciona todos los objetos"""
    global objeto_seleccionado
    for objeto in objetos:
        objeto.seleccionado = False
    objeto_seleccionado = None

def seleccionar_objeto(objeto):
    """Selecciona un objeto específico"""
    global objeto_seleccionado
    deseleccionar_todos()
    if objeto:
        objeto.seleccionado = True
        objeto_seleccionado = objeto
        print(f"Objeto seleccionado: {objeto.nombre}")

def main():
    """Función principal"""
    # Configurar OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(*cfg.COLOR_SKY)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Configurar callbacks
    glutMouseFunc(mouse_click)
    glutPassiveMotionFunc(mouse_motion)  # Para movimiento del mouse sin clic
    glutMotionFunc(mouse_motion)  # Para movimiento del mouse con botón presionado (arrastre)
    glutKeyboardFunc(keyboard)
    glutDisplayFunc(display)
    glutReshapeFunc(callback_redimensionar)  # Para redimensionado de ventana
    
    print("=== Mini CAD Adaptable - Seleccionar y Mover ===")
    print()
    print("🎮 Instrucciones:")
    print("1. Haz clic en uno de los 5 botones superiores")
    print("2. Haz clic en el terreno verde donde quieras el objeto")
    print("3. ¡El objeto aparece automáticamente!")
    print()
    print("🔧 Controles:")
    print("- Click en botones: Seleccionar herramienta")
    print("- Click en terreno: Agregar objeto")
    print("- Modo SELECCIONAR: Click en objeto para seleccionar, arrastra para mover")
    print("- WASD: Mover cámara (W=adelante, S=atrás, A=izquierda, D=derecha)")
    print("- Q/E: Rotar cámara (Q=izquierda, E=derecha)")
    print("- ESC: Limpiar toda la escena")
    print()
    print("🎯 Herramientas disponibles:")
    print("- 🌳 Árbol")
    print("- 🏠 Casa") 
    print("- ⛰️ Montaña")
    print("- 💡 Luz (ilumina la escena)")
    print("- 👆 Seleccionar y mover objetos")
    print()
    print("¡Diviértete construyendo tu mundo! 🌟")
    
    glutMainLoop()

if __name__ == "__main__":
    main()
