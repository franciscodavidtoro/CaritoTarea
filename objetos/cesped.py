import os
directorio = os.path.dirname(os.path.abspath(__file__))


import figuras as fg

plano = fg.Figura(
        tipo='cubo',
        posicion=(0, -0.5, 0),
        escala=(40, 0.05, 20),
        color=(0.1, 0.7, 0.1, 1.0),  # Verde césped
        textura=fg.cargarTextura(os.path.join(directorio, "cesped.jpg")),
        sombra=False
    )


