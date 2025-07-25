

import figuras as fg

base = fg.Figura(tipo='cubo', posicion=(0, 0, 0), escala=(2, 0.3, 1), color=(0.2, 0.6, 0.9, 1.0))  # Azul celeste

    # Techo del carro (cubo más pequeño)
techo = fg.Figura(tipo='cubo', posicion=(0, .85, 0), escala=(1.2, 0.1, 0.8), color=(1.0, 0.85, 0.2, 1.0))  # Amarillo dorado

    # 4 pilares (cubos delgados)
pilar1 = fg.Figura(tipo='cubo', posicion=(-0.5, 0.3, 0.35), escala=(0.1, 1, 0.1), color=(0.7, 0.2, 0.2, 1.0))  # Rojo oscuro
pilar2 = fg.Figura(tipo='cubo', posicion=(0.5, 0.3, 0.35), escala=(0.1, 1, 0.1), color=(0.2, 0.7, 0.2, 1.0))   # Verde intenso
pilar3 = fg.Figura(tipo='cubo', posicion=(-0.5, 0.3, -0.35), escala=(0.1, 1, 0.1), color=(0.2, 0.2, 0.7, 1.0)) # Azul intenso
pilar4 = fg.Figura(tipo='cubo', posicion=(0.5, 0.3, -0.35), escala=(0.1, 1, 0.1), color=(0.8, 0.4, 0.1, 1.0))  # Naranja

    # 4 ruedas (toroides)
rueda1 = fg.Figura(tipo='toroide', posicion=(-0.8, -0.2, 0.5), escala=(0.4, 0.4, 0.4), color=(0.1, 0.1, 0.1, 1.0), argumentos=(0.08, 0.18))  # Negro
rueda2 = fg.Figura(tipo='toroide', posicion=(0.8, -0.2, 0.5), escala=(0.4, 0.4, 0.4), color=(0.3, 0.3, 0.3, 1.0), argumentos=(0.08, 0.18))   # Gris oscuro
rueda3 = fg.Figura(tipo='toroide', posicion=(-0.8, -0.2, -0.5), escala=(0.4, 0.4, 0.4), color=(0.9, 0.7, 0.1, 1.0), argumentos=(0.08, 0.18)) # Amarillo mostaza
rueda4 = fg.Figura(tipo='toroide', posicion=(0.8, -0.2, -0.5), escala=(0.4, 0.4, 0.4), color=(0.2, 0.8, 0.8, 1.0), argumentos=(0.08, 0.18))  # Turquesa
    # Ventana (cubo achatado y más transparente)
ventana1 = fg.Figura(
        tipo='cubo',
        posicion=(0, 0.45, 0.36),
        escala=(1, 0.68, 0.005),
        color=(0.7, 0.9, 1.0, 0.2)  # Más transparente
    )
ventana2 = fg.Figura(
        tipo='cubo',
        posicion=(0, 0.45, -0.36),
        escala=(1, 0.68, 0.005),
        color=(0.7, 0.9, 1.0, 0.2)  # Más transparente
    )
ventana3 = fg.Figura(
        tipo='cubo',
        posicion=(0.51, 0.45, 0),
        escala=(0.005, 0.68, 0.7),
        color=(0.7, 0.9, 1.0, 0.2)  # Más transparente
    )
ventana4 = fg.Figura(
        tipo='cubo',
        posicion=(-0.51, 0.45, 0),
        escala=(0.005, 0.68, 0.7),
        color=(0.7, 0.9, 1.0, 0.2)  # Más transparente
    )
    
    # Asiento del carro mejorado (posicionado mejor dentro del carro)
asiento_base = fg.Figura(
        tipo='cubo',
        posicion=(-0.2, 0.05, 0),
        escala=(0.4, 0.15, 0.5),
        color=(0.4, 0.2, 0.2, 1.0)  # Marrón cuero
    )
    
asiento_respaldo = fg.Figura(
        tipo='cubo',
        posicion=(-0.2, 0.25, -0.12),
        escala=(0.4, 0.4, 0.08),
        color=(0.35, 0.15, 0.15, 1.0)  # Marrón más oscuro
    )
    
    # Volante mejorado con soporte (más visible)
volante_soporte = fg.Figura(
        tipo='cubo',
        posicion=(0.3, 0.2, 0),
        escala=(0.03, 0.25, 0.03),
        color=(0.1, 0.1, 0.1, 1.0)  # Negro
    )
    
volante = fg.Figura(
        tipo='toroide', 
        posicion=(0.3, 0.32, 0), 
        escala=(0.25, 0.25, 0.25), 
        color=(0.1, 0.1, 0.1, 1.0), 
        argumentos=(0.04, 0.12)
    )  # Negro
    
    # Panel de control más visible
panel_control = fg.Figura(
        tipo='cubo',
        posicion=(0.4, 0.25, 0),
        escala=(0.08, 0.15, 0.3),
        color=(0.2, 0.2, 0.2, 1.0)  # Gris oscuro
    )
    
    # Agregar algunos detalles del interior
    # Espejo retrovisor
espejo = fg.Figura(
        tipo='cubo',
        posicion=(0, 0.7, 0),
        escala=(0.15, 0.05, 0.02),
        color=(0.8, 0.8, 0.8, 1.0)  # Plateado
    )
    
    # Palanca de cambios
palanca_base = fg.Figura(
        tipo='cubo',
        posicion=(0.1, 0.12, 0),
        escala=(0.08, 0.08, 0.08),
        color=(0.2, 0.2, 0.2, 1.0)
    )
    
palanca = fg.Figura(
        tipo='cubo',
        posicion=(0.1, 0.2, 0),
        escala=(0.02, 0.15, 0.02),
        color=(0.1, 0.1, 0.1, 1.0)
    )
    
carro = fg.Objeto3D(rotacion=(0,270,0))
carro.figuras.extend([base, techo, pilar1, pilar2, pilar3, pilar4, rueda1, rueda2, rueda3, rueda4, asiento_base, asiento_respaldo, volante_soporte, volante, panel_control, espejo, palanca_base, palanca, ventana1, ventana2, ventana3, ventana4])
   