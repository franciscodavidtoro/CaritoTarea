import os
directorio = os.path.dirname(os.path.abspath(__file__))

import figuras as fg

def crear_cesped_infinito():
    """Crea múltiples planos de césped para cubrir todo el terreno"""
    global textura_actual
    return crear_cesped_infinito_con_textura(textura_actual)

# Variables globales para los planos de césped (se inicializarán después)
planos_cesped = []
plano = None

def inicializar_cesped():
    """Inicializa el césped después de que OpenGL esté listo"""
    global planos_cesped, plano
    planos_cesped = crear_cesped_infinito()
    plano = planos_cesped[0] if planos_cesped else None
    return planos_cesped

# Variable global para la ruta de textura actual
textura_actual = "cesped.jpg"

def cambiar_textura_cesped_global(nueva_ruta_textura):
    """Cambia la textura global del césped"""
    global textura_actual
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(nueva_ruta_textura):
            print(f"Error: El archivo {nueva_ruta_textura} no existe")
            return False
        
        # Actualizar la ruta de textura global
        textura_actual = nueva_ruta_textura
        print(f"Textura actualizada a: {textura_actual}")
        return True
        
    except Exception as e:
        print(f"Error al cambiar textura: {e}")
        return False

def crear_cesped_infinito_con_textura(ruta_textura=None):
    """Crea múltiples planos de césped con textura específica"""
    if ruta_textura is None:
        ruta_textura = textura_actual
    
    # Obtener directorio actual del script
    directorio = os.path.dirname(os.path.abspath(__file__))
    
    # Si la ruta no es absoluta, combinarla con el directorio
    if not os.path.isabs(ruta_textura):
        ruta_textura = os.path.join(directorio, ruta_textura)
    
    planos_cesped = []
    
    # Crear una cuadrícula de planos de césped (igual que la función original)
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
                textura=fg.cargarTextura(ruta_textura),
                sombra=False
            )
            planos_cesped.append(plano_cesped)
    
    return planos_cesped


