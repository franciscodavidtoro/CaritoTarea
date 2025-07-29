import figuras as fg
import numpy as np

def obtener_posicion_carretera(z):
    """Función para obtener la posición X de la carretera en cualquier Z"""
    amplitud_curva = 50
    factor_z = z / 60
    return amplitud_curva * np.sin(factor_z) * (1 + 0.5 * np.sin(factor_z * 3))

def crear_arbol(pos_x, pos_z):
    # Tronco del árbol
    tronco = fg.Figura(
        tipo='cubo',
        posicion=(pos_x, -0.1, pos_z),
        escala=(0.2, 0.8, 0.2),
        color=(0.4, 0.2, 0.1, 1.0)  # Marrón
    )
    # Follaje del árbol
    follaje = fg.Figura(
        tipo='esfera',
        posicion=(pos_x, 0.5, pos_z),
        escala=(0.6, 0.6, 0.6),
        color=(0.2, 0.6, 0.2, 1.0),  # Verde
        argumentos=0.5
    )
    return [tronco, follaje]

arboles = []  
# Crear árboles que siguen la trayectoria de la carretera
for z in range(-200, 201, 15):  # A lo largo de la carretera
    x_carretera = obtener_posicion_carretera(z)
    
    # Árboles a ambos lados de la carretera
    if z % 30 != 0:  # No todos los puntos para variedad
        # Lado izquierdo de la carretera
        arboles.extend(crear_arbol(x_carretera - 8, z))
        # Lado derecho de la carretera  
        arboles.extend(crear_arbol(x_carretera + 8, z))
        
        # Algunos árboles más lejos para profundidad
        if z % 45 == 0:
            arboles.extend(crear_arbol(x_carretera - 15, z))
            arboles.extend(crear_arbol(x_carretera + 15, z))