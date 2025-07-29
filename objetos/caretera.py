# Crear carretera infinita con curvas para el juego
import figuras as fg
import numpy as np

def crear_carretera_infinita():
    """Crea una carretera infinita con curvas"""
    carretera_segmentos = []
    
    # Parámetros para la carretera
    longitud_total = 600  # Carretera muy larga
    ancho_carretera = 4   # Ancho de la carretera
    num_segmentos = 300   # Más segmentos para suavidad
    amplitud_curva = 50   # MÁS CURVA - aumenté de 40 a 50
    
    # Crear segmentos de la carretera con forma de S más curva en panza y cabeza
    for i in range(num_segmentos):
        # Posición a lo largo del eje Z
        z = (i / num_segmentos) * longitud_total - longitud_total/2
        
        # Función para crear una S con curvas más pronunciadas en panza y cabeza
        # Usando una función cúbica para hacer las curvas más cerradas
        factor_z = z / 60  # Normalizar
        x = amplitud_curva * np.sin(factor_z) * (1 + 0.5 * np.sin(factor_z * 3))  # Curvas más cerradas
        
        
        derivada = amplitud_curva * np.cos(factor_z) * (1 + 0.5 * np.sin(factor_z * 3)) / 60
        derivada += amplitud_curva * np.sin(factor_z) * 0.5 * np.cos(factor_z * 3) * 3 / 60
        angulo_radianes = np.arctan(derivada)
        angulo_grados = np.degrees(angulo_radianes)
        
        # Crear segmento de carretera
        segmento = fg.Figura(
            tipo='cubo',
            posicion=(x, -0.48, z),
            escala=(ancho_carretera, 0.02, longitud_total/num_segmentos + 1.4),
            color=(0.3, 0.3, 0.3, 1.0),  # Gris para asfalto
            rotacion=(0, angulo_grados,0), #derivadas de las posiciones
            sombra=False
        )
        carretera_segmentos.append(segmento)
    
    # Agregar líneas centrales amarillas
    for i in range(0, num_segmentos, 10):
        z = (i / num_segmentos) * longitud_total - longitud_total/2
        factor_z = z / 60
        x = amplitud_curva * np.sin(factor_z) * (1 + 0.5 * np.sin(factor_z * 3))
        
        derivada = amplitud_curva * np.cos(factor_z) * (1 + 0.5 * np.sin(factor_z * 3)) / 60
        derivada += amplitud_curva * np.sin(factor_z) * 0.5 * np.cos(factor_z * 3) * 3 / 60
        angulo_radianes = np.arctan(derivada)
        angulo_grados = np.degrees(angulo_radianes)
        
        linea_central = fg.Figura(
            tipo='cubo',
            posicion=(x, -0.465, z),
            escala=(0.3, 0.01, 3),
            color=(1.0, 1.0, 0.0, 1.0),  # Amarillo
            rotacion=(0, angulo_grados,0), #derivadas de las posiciones
            sombra=False
        )
        carretera_segmentos.append(linea_central)
    
    return carretera_segmentos

def obtener_posicion_carretera(z):
    """Obtiene la posición X de la carretera en una coordenada Z dada"""
    amplitud_curva = 50
    factor_z = z / 60
    return amplitud_curva * np.sin(factor_z) * (1 + 0.5 * np.sin(factor_z * 3))

# Crear la carretera
carretera_segmentos = crear_carretera_infinita()

# Para compatibilidad, mantener la referencia original
carretera = carretera_segmentos[0] if carretera_segmentos else None