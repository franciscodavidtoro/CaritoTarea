import figuras as fg
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
    
arboles=[]  
for i in range(-15, 16, 2):  # De -15 a 15 con intervalos de 2 (más casas)
        if abs(i) > 1:  # No colocar muy cerca del centro donde está el carro
            # Lado derecho de la carretera
            if i % 4 != 0:  
                arboles.extend(crear_arbol(i, 3.5))
                arboles.extend(crear_arbol(i, -3.5))