
import figuras as fg
import copy
import numpy as np

def obtener_posicion_carretera(z):
    """Función para obtener la posición X de la carretera en cualquier Z"""
    amplitud_curva = 50
    factor_z = z / 60
    return amplitud_curva * np.sin(factor_z) * (1 + 0.5 * np.sin(factor_z * 3))

# Crear montañas que siguen la carretera a lo lejos
grupoMontannas = []

# Montañas en el fondo siguiendo la carretera
for z in range(-100, 101, 25):
    x_carretera = obtener_posicion_carretera(z)
    
    # Montañas en el lado derecho de la carretera (lejos)
    montana_der = fg.Figura(
        tipo='cono',
        posicion=(x_carretera + 35, -0.5, z),
        rotacion=(-90, 0, 0),
        escala=(2.5, 3, 2.5),
        color=(0.3, 0.6, 0.2, 1.0),
        argumentos=(1.0, 1.5)
    )
    grupoMontannas.append(montana_der)
    
    # Montañas en el lado izquierdo de la carretera (lejos)
    if z % 50 == 0:  # Menos montañas en el lado izquierdo
        montana_izq = fg.Figura(
            tipo='cono',
            posicion=(x_carretera - 35, -0.5, z),
            rotacion=(-90, 0, 0),
            escala=(2.2, 2.8, 2.2),
            color=(0.2, 0.5, 0.1, 1.0),
            argumentos=(1.0, 1.5)
        )
        grupoMontannas.append(montana_izq)