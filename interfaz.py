from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import OpenGL.GLUT as GLUT  # Importación explícita para constantes de GLUT
import numpy as np
import figuras as fg
from objetos.arboles import crear_arbol
from objetos.casas import crear_casa
from objetos.gupoMontannas import obtener_posicion_carretera

class Boton:
    """Clase para crear y gestionar botones en la interfaz"""
    
    def __init__(self, x, y, ancho, alto, texto, color=(0.7, 0.7, 0.7, 1.0), color_texto=(0.0, 0.0, 0.0, 1.0)):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.texto = texto
        self.color = color
        self.color_texto = color_texto
        self.activo = False
        self.hover = False  # Estado cuando el mouse está sobre el botón
    
    def esta_dentro(self, x, y):
        """Verifica si las coordenadas (x, y) están dentro del botón"""
        return (self.x <= x <= self.x + self.ancho and 
                self.y <= y <= self.y + self.alto)
    
    def dibujar(self):
        """Dibuja el botón en la pantalla con efectos visuales mejorados"""
        # Guardar la matriz de proyección actual
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, 800, 0, 600, -1, 1)  # Cambiar a una proyección ortográfica para HUD
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        # Desactivar iluminación y prueba de profundidad para HUD
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        
        # Efecto de sombra debajo del botón
        if not self.activo:
            glColor4f(0.0, 0.0, 0.0, 0.3)
            glBegin(GL_QUADS)
            glVertex2f(self.x + 3, self.y - 3)
            glVertex2f(self.x + self.ancho + 3, self.y - 3)
            glVertex2f(self.x + self.ancho + 3, self.y + self.alto - 3)
            glVertex2f(self.x + 3, self.y + self.alto - 3)
            glEnd()
        
        # Determinar el color del botón basado en su estado
        if self.activo:
            # Color más brillante cuando está activo
            color = (
                min(self.color[0] + 0.2, 1.0),
                min(self.color[1] + 0.2, 1.0),
                min(self.color[2] + 0.2, 1.0),
                self.color[3]
            )
        else:
            color = self.color
        
        # Dibujar fondo del botón (con gradiente)
        glBegin(GL_QUADS)
        # Parte superior (más clara)
        glColor4f(min(color[0] + 0.1, 1.0), min(color[1] + 0.1, 1.0), min(color[2] + 0.1, 1.0), color[3])
        glVertex2f(self.x, self.y + self.alto)
        glVertex2f(self.x + self.ancho, self.y + self.alto)
        
        # Parte inferior (más oscura)
        glColor4f(max(color[0] - 0.1, 0.0), max(color[1] - 0.1, 0.0), max(color[2] - 0.1, 0.0), color[3])
        glVertex2f(self.x + self.ancho, self.y)
        glVertex2f(self.x, self.y)
        glEnd()
        
        # Borde del botón con efecto 3D
        if self.activo:
            # Borde hundido cuando está activo
            # Borde inferior y derecho (claro)
            glColor4f(0.9, 0.9, 0.9, 1.0)
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.ancho, self.y)
            glVertex2f(self.x + self.ancho, self.y)
            glVertex2f(self.x + self.ancho, self.y + self.alto)
            glEnd()
            
            # Borde superior e izquierdo (oscuro)
            glColor4f(0.2, 0.2, 0.2, 1.0)
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y + self.alto)
            glVertex2f(self.x + self.ancho, self.y + self.alto)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x, self.y + self.alto)
            glEnd()
        else:
            # Borde elevado cuando no está activo
            # Borde superior e izquierdo (claro)
            glColor4f(0.9, 0.9, 0.9, 1.0)
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y + self.alto)
            glVertex2f(self.x + self.ancho, self.y + self.alto)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x, self.y + self.alto)
            glEnd()
            
            # Borde inferior y derecho (oscuro)
            glColor4f(0.2, 0.2, 0.2, 1.0)
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.ancho, self.y)
            glVertex2f(self.x + self.ancho, self.y)
            glVertex2f(self.x + self.ancho, self.y + self.alto)
            glEnd()
        
        # Dibujar texto del botón con sombra para mejor legibilidad
        # Primero la sombra
        glColor4f(0.0, 0.0, 0.0, 0.5)
        texto_x = self.x + (self.ancho - len(self.texto) * 9) / 2 + 1  # +1 para offset de sombra
        texto_y = self.y + (self.alto - 12) / 2 - 1  # -1 para offset de sombra
        
        glRasterPos2f(texto_x, texto_y)
        for caracter in self.texto:
            glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord(caracter))
        
        # Luego el texto real
        if self.activo:
            # Texto en blanco brillante cuando está activo
            glColor4f(1.0, 1.0, 1.0, 1.0)
        else:
            glColor4f(*self.color_texto)
            
        texto_x = self.x + (self.ancho - len(self.texto) * 9) / 2
        texto_y = self.y + (self.alto - 12) / 2
        
        glRasterPos2f(texto_x, texto_y)
        for caracter in self.texto:
            glutBitmapCharacter(GLUT.GLUT_BITMAP_HELVETICA_12, ord(caracter))        # Restaurar estados
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        # Restaurar matrices
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

class InterfazGUI:
    """Clase para gestionar toda la interfaz de usuario"""
    
    def __init__(self, ancho_ventana=800, alto_ventana=600):
        self.ancho_ventana = ancho_ventana
        self.alto_ventana = alto_ventana
        self.modo_seleccion = None  # 'arbol', 'casa', 'montana' o None
        
        # Crear botones más grandes y visibles en la parte superior
        tamano_boton = 120
        altura_boton = 50
        separacion = 20
        inicio_x = (ancho_ventana - (3 * tamano_boton + 2 * separacion)) / 2
        y_pos = alto_ventana - altura_boton - 10  # 10 pixels del borde superior
        
        self.botones = [
            Boton(inicio_x, y_pos, tamano_boton, altura_boton, 
                 "ÁRBOLES", color=(0.2, 0.8, 0.3, 0.9)),
            Boton(inicio_x + tamano_boton + separacion, y_pos, tamano_boton, altura_boton, 
                 "CASAS", color=(0.9, 0.6, 0.3, 0.9)),
            Boton(inicio_x + 2 * (tamano_boton + separacion), y_pos, tamano_boton, altura_boton, 
                 "MONTAÑAS", color=(0.5, 0.5, 0.8, 0.9))
        ]
        self.objetos_nuevos = []  # Lista para almacenar los nuevos objetos añadidos
    
    def dibujar(self):
        """Dibuja todos los elementos de la interfaz"""
        for boton in self.botones:
            boton.dibujar()
    
    def procesar_click(self, x, y):
        """Procesa un click de ratón en coordenadas (x, y) de ventana"""
        # Convertir coordenadas de ventana a coordenadas de interfaz
        y = self.alto_ventana - y  # Invertir Y ya que OpenGL cuenta desde abajo
        
        # Verificar si se hizo clic en alguno de los botones
        for i, boton in enumerate(self.botones):
            if boton.esta_dentro(x, y):
                # Desactivar todos los botones
                for b in self.botones:
                    b.activo = False
                
                # Si el botón ya estaba seleccionado, desactivarlo
                if self.modo_seleccion == ['arbol', 'casa', 'montana'][i]:
                    self.modo_seleccion = None
                else:
                    # Activar este botón
                    boton.activo = True
                    self.modo_seleccion = ['arbol', 'casa', 'montana'][i]
                return True
        
        # Si no se hizo clic en un botón y hay un modo de selección activo,
        # procesar el clic en el terreno
        if self.modo_seleccion:
            return False  # Indica que se debe procesar el clic para añadir un objeto
        
        return False

def convertir_coord_ventana_a_3d(x, y, carro_posicion, carro_direccion, camara_distancia):
    """
    Método simplificado para colocar objetos exactamente donde el usuario hace clic
    basado en un enfoque más directo de mapeo de pantalla al terreno
    """
    # Variables de la ventana
    ancho_ventana = 800
    alto_ventana = 600
    
    # Obtener posición y orientación de la cámara
    angulo_rad = np.radians(carro_direccion)
    cam_x = carro_posicion[0] - camara_distancia * np.sin(angulo_rad)
    cam_y = carro_posicion[1] + 5  # Altura de la cámara (5 unidades sobre el carro)
    cam_z = carro_posicion[2] - camara_distancia * np.cos(angulo_rad)
    
    # Normalizar las coordenadas de pantalla al rango [-1, 1]
    x_pantalla = (2.0 * x / ancho_ventana) - 1.0
    y_pantalla = 1.0 - (2.0 * y / alto_ventana)  # Invertido para coordenadas OpenGL
    
    # Ajustar mapeo directo basado en la posición del clic en pantalla
    # El mapa es dividido en regiones:
    # - Centro: Objetos se colocan frente al carro
    # - Lados: Objetos se colocan hacia los lados del carro
    # - Arriba/abajo: Objetos se colocan más lejos/cerca del carro
    
    # Distancia base desde el carro (ajustada por posición vertical del clic)
    distancia_base = 10.0  # Distancia base desde el carro
    # Más abajo en la pantalla = más cerca, más arriba = más lejos
    distancia = distancia_base + (y_pantalla * 15.0)
    
    # Desplazamiento lateral basado en la posición horizontal del clic
    # Centro = 0, izquierda = negativo, derecha = positivo
    desplazamiento = x_pantalla * 20.0  # Factor de escala para el desplazamiento lateral
    
    # Calcular la dirección hacia adelante del carro (vector dirección)
    frente_x = np.sin(angulo_rad)
    frente_z = np.cos(angulo_rad)
    
    # Calcular la dirección perpendicular (vector lateral)
    lateral_x = -frente_z  # Perpendicular a la dirección frontal
    lateral_z = frente_x
    
    # Posición del objeto relativa al carro
    objeto_x = carro_posicion[0] + (frente_x * distancia) + (lateral_x * desplazamiento)
    objeto_z = carro_posicion[2] + (frente_z * distancia) + (lateral_z * desplazamiento)
    
    # Factor de corrección adicional basado en pruebas
    # Este factor ajusta la posición final para que coincida mejor con el clic
    factor_correccion_x = -x_pantalla * 5.0  # Ajuste fino para X
    factor_correccion_z = -y_pantalla * 5.0  # Ajuste fino para Z
    
    objeto_x += factor_correccion_x
    objeto_z += factor_correccion_z
    
    # Altura fija para el terreno
    objeto_y = -0.5
    
    # Imprimir valores de depuración para ajuste
    print(f"Pantalla: ({x_pantalla:.2f}, {y_pantalla:.2f})")
    print(f"Distancia: {distancia:.2f}, Desplazamiento: {desplazamiento:.2f}")
    
    return (objeto_x, objeto_y, objeto_z)

def agregar_objeto(tipo, posicion):
    """
    Agrega un nuevo objeto al terreno exactamente donde se hizo clic
    - tipo: 'arbol', 'casa', 'montana'
    - posicion: (x, y, z) donde se colocará el objeto
    """
    nuevos_objetos = []
    
    # Extraer coordenadas exactas
    x, y, z = posicion
    y_terreno = -0.5  # Altura fija del terreno
    
    # Calcular escala según la distancia (objetos más lejanos aparecen más pequeños)
    escala_base = 1.0
    
    if tipo == 'arbol':
        # Crear árbol directamente en la posición exacta del clic
        tronco = fg.Figura(
            tipo='cubo',
            posicion=(x, y_terreno + 0.4, z),  # Ajustar altura para que esté sobre el terreno
            escala=(0.2 * escala_base, 0.8 * escala_base, 0.2 * escala_base),
            color=(0.4, 0.2, 0.1, 1.0)  # Marrón
        )
        follaje = fg.Figura(
            tipo='esfera',
            posicion=(x, y_terreno + 1.0, z),  # Ajustar altura para que esté sobre el terreno
            escala=(0.6 * escala_base, 0.6 * escala_base, 0.6 * escala_base),
            color=(0.2, 0.6, 0.2, 1.0),  # Verde
            argumentos=0.5
        )
        nuevos_objetos = [tronco, follaje]
        print(f"Árbol creado en: ({x:.2f}, {y_terreno:.2f}, {z:.2f})")
        
    elif tipo == 'casa':
        # Color aleatorio para casas
        color_casa = (np.random.uniform(0.4, 0.9), np.random.uniform(0.4, 0.7), np.random.uniform(0.3, 0.6), 1.0)
        color_techo = (np.random.uniform(0.5, 0.9), np.random.uniform(0.2, 0.5), np.random.uniform(0.1, 0.4), 1.0)
        
        # Crear casa directamente en la posición exacta del clic
        casa_base = fg.Figura(
            tipo='cubo',
            posicion=(x, y_terreno + 0.6, z),  # Ajustar altura para que esté sobre el terreno
            escala=(1.2 * escala_base, 1.2 * escala_base, 1.2 * escala_base),
            color=color_casa
        )
        techo_casa = fg.Figura(
            tipo='cono',
            posicion=(x, y_terreno + 1.2, z),  # Ajustar altura para que esté sobre el terreno
            rotacion=(-90, 0, 0),
            escala=(1 * escala_base, 0.8 * escala_base, 1 * escala_base),
            color=color_techo,
            argumentos=(1, 0.6)
        )
        nuevos_objetos = [casa_base, techo_casa]
        print(f"Casa creada en: ({x:.2f}, {y_terreno:.2f}, {z:.2f})")
        
    elif tipo == 'montana':
        # Crear montaña simple en la posición exacta del clic
        montana = fg.Figura(
            tipo='cono',
            posicion=(x, y_terreno, z),  # Posición exacta en el terreno
            rotacion=(-90, 0, 0),
            escala=(2.0 * escala_base, 2.5 * escala_base, 2.0 * escala_base),
            color=(0.3, 0.6, 0.2, 1.0),
            argumentos=(1.0, 1.5)
        )
        nuevos_objetos = [montana]
        print(f"Montaña creada en: ({x:.2f}, {y_terreno:.2f}, {z:.2f})")
    
    return nuevos_objetos
