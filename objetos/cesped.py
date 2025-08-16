import os
directorio = os.path.dirname(os.path.abspath(__file__))

import figuras as fg

def crear_cesped_infinito():
    """Crea múltiples planos de césped para cubrir todo el terreno"""
    planos_cesped = []
    
    # Crear una cuadrícula de planos de césped
    tamano_plano = 80
    num_planos_x = 5  # 5 planos en X
    num_planos_z = 15  # 15 planos en Z para cubrir más distancia
    
    for i in range(num_planos_x):
        for j in range(num_planos_z):
            # Calcular posición de cada plano
            pos_x = (i - num_planos_x//2) * tamano_plano
            pos_z = (j - num_planos_z//2) * tamano_plano
            
            plano_cesped = fg.Figura(
                tipo='cubo',
                posicion=(pos_x, -0.5, pos_z),
                escala=(tamano_plano, 0.05, tamano_plano),
                color=(0.1, 0.7, 0.1, 1.0),  # Verde césped
                textura=fg.cargarTextura(os.path.join(directorio, "cesped.jpg")),
                sombra=False
            )
            planos_cesped.append(plano_cesped)
    
    return planos_cesped

# Variables globales para los planos de césped (se inicializarán después)
planos_cesped = []
plano = None

def inicializar_cesped():
    """Inicializa el césped después de que OpenGL esté listo"""
    global planos_cesped, plano
    planos_cesped = crear_cesped_infinito()
    plano = planos_cesped[0] if planos_cesped else None
    return planos_cesped


