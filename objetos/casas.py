import figuras as fg
import numpy as np

def obtener_posicion_carretera(z):
    """Función para obtener la posición X de la carretera en cualquier Z"""
    amplitud_curva = 50
    factor_z = z / 60
    return amplitud_curva * np.sin(factor_z) * (1 + 0.5 * np.sin(factor_z * 3))

def crear_casa(pos_x, pos_z, color_casa, color_techo):
    # Paredes de la casa
    casa_base = fg.Figura(
        tipo='cubo',
        posicion=(pos_x, 0.1, pos_z),
        escala=(1.2, 1.2, 1.2),
        color=color_casa
    )
    # Techo de la casa
    techo_casa = fg.Figura(
        tipo='cono',
        posicion=(pos_x, 0.7, pos_z),
        rotacion=(-90, 0, 0),
        escala=(1, 0.8, 1),
        color=color_techo,
        argumentos=(1, 0.6)
    )
    return [casa_base, techo_casa]

casas = []  
# Crear casas que siguen la trayectoria de la carretera
for z in range(-50, 51, 20):  # Más cerca del centro, cada 20 unidades
    x_carretera = obtener_posicion_carretera(z)
    
    # Casas a ambos lados de la carretera
    if z % 20 == 0:  # Casas más frecuentes
        # Lado derecho de la carretera
        color_casa_der = (0.8, 0.6, 0.4, 1.0) if z > 0 else (0.6, 0.8, 0.9, 1.0)
        color_techo_der = (0.7, 0.2, 0.2, 1.0) if z > 0 else (0.2, 0.7, 0.2, 1.0)
        casas.extend(crear_casa(x_carretera + 12, z, color_casa_der, color_techo_der))
        
        # Lado izquierdo de la carretera
        color_casa_izq = (0.9, 0.7, 0.5, 1.0) if z > 0 else (0.7, 0.6, 0.8, 1.0)
        color_techo_izq = (0.2, 0.2, 0.7, 1.0) if z > 0 else (0.8, 0.4, 0.1, 1.0)
        casas.extend(crear_casa(x_carretera - 12, z, color_casa_izq, color_techo_izq))

# Agregar más casas en el área donde están las montañas
for z in range(-80, 81, 30):
    x_carretera = obtener_posicion_carretera(z)
    if z % 30 == 0:
        color_casa = (0.7, 0.5, 0.3, 1.0)
        color_techo = (0.5, 0.3, 0.1, 1.0)
        casas.extend(crear_casa(x_carretera + 18, z, color_casa, color_techo))
        casas.extend(crear_casa(x_carretera - 18, z, color_casa, color_techo))

# Agregar casas al lado de donde están los árboles (misma distribución que los árboles)
for z in range(-200, 201, 15):  # Misma distribución que los árboles
    x_carretera = obtener_posicion_carretera(z)
    
    if z % 30 != 0:  # No todos los puntos para variedad, igual que los árboles
        # Casas cerca de donde están los árboles del lado izquierdo
        color_casa_1 = (0.6, 0.4, 0.2, 1.0)
        color_techo_1 = (0.8, 0.2, 0.1, 1.0)
        casas.extend(crear_casa(x_carretera - 10, z, color_casa_1, color_techo_1))
        
        # Casas cerca de donde están los árboles del lado derecho
        color_casa_2 = (0.5, 0.7, 0.4, 1.0)
        color_techo_2 = (0.3, 0.1, 0.6, 1.0)
        casas.extend(crear_casa(x_carretera + 10, z, color_casa_2, color_techo_2))
        
        # Casas adicionales más lejas para más densidad
        if z % 45 == 0:
            color_casa_3 = (0.8, 0.5, 0.6, 1.0)
            color_techo_3 = (0.4, 0.2, 0.3, 1.0)
            casas.extend(crear_casa(x_carretera - 20, z, color_casa_3, color_techo_3))
            casas.extend(crear_casa(x_carretera + 20, z, color_casa_3, color_techo_3))

