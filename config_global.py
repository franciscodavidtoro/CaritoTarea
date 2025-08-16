"""
Configuración global para el Mini CAD
Variables compartidas para evitar importaciones circulares
"""

# Variables de ventana y pantalla
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT

# Variables de interfaz adaptable
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
BUTTON_COUNT = 5
BUTTON_WIDTH = (WINDOW_WIDTH - (BUTTON_COUNT + 1) * BUTTON_MARGIN) // BUTTON_COUNT

# Variables de selección
SELECTION_RADIUS = 2.0
SELECTION_LINE_WIDTH = 3
HOVER_LINE_WIDTH = 2

# Variables de cámara
DEFAULT_CAMERA_POS = [15.0, 8.0, 15.0]
DEFAULT_CAMERA_TARGET = [0.0, 0.0, 0.0]
DEFAULT_CAMERA_SPEED = 0.5
DEFAULT_CAMERA_ROTATION_SPEED = 5.0
CAMERA_DISTANCE = 15.0

# Variables de terreno
TERRAIN_SIZE = 100
TERRAIN_LIMIT = 40  # Límite para colocar objetos

# Colores
COLOR_SELECTION = (1.0, 1.0, 0.0, 1.0)  # Amarillo para selección
COLOR_HOVER = (0.0, 1.0, 1.0, 0.5)      # Cian para hover
COLOR_TERRAIN = (0.2, 0.8, 0.3)         # Verde césped
COLOR_SKY = (0.5, 0.7, 1.0, 1.0)        # Azul cielo

# Variables de modo
MODOS = ["navegacion", "arbol", "casa", "montana", "luz", "seleccionar"]

# Variables globales de estado (se inicializarán en el programa principal)
window_width = WINDOW_WIDTH
window_height = WINDOW_HEIGHT
aspect_ratio = ASPECT_RATIO
