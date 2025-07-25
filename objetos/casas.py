import figuras as fg

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
    
casas=[]  
for i in range(-15, 16, 1):  # De -15 a 15 con intervalos de 2 (más casas)
    if abs(i) > 1:  # No colocar muy cerca del centro donde está el carro
            # Lado derecho de la carretera
        if i % 4 == 0:  # Casas cada 4 unidades
            color_casa = (0.8, 0.6, 0.4, 1.0) if i > 0 else (0.6, 0.8, 0.9, 1.0)
            color_techo = (0.7, 0.2, 0.2, 1.0) if i > 0 else (0.2, 0.7, 0.2, 1.0)
            
            casas.extend(crear_casa(i, 3.5, color_casa, color_techo))
                # Lado izquierdo de la carretera
            color_casa = (0.9, 0.7, 0.5, 1.0) if i > 0 else (0.7, 0.6, 0.8, 1.0)
            color_techo = (0.2, 0.2, 0.7, 1.0) if i > 0 else (0.8, 0.4, 0.1, 1.0)
            casas.extend(crear_casa(i, -3.5, color_casa, color_techo))

