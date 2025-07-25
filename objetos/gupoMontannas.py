


import figuras as fg
import copy
    # Crear una montaña usando un cono grande y verde
montanna1 = fg.Figura(
        tipo='cono',
        posicion=(5, -0.5, -8),
        rotacion=(-90, 0, 0),  # Apuntar hacia arriba
        escala=(2.5, 3, 2.5),
        color=(0.3, 0.6, 0.2, 1.0),
        argumentos=(1.0, 1.5)  # base, altura
    )
montanna2 = copy.deepcopy(montanna1)
montanna2.posicion = (3, -0.5, -8)

montanna3 = copy.deepcopy(montanna1)
montanna3.posicion = (7, -0.5, -10)
montanna3.escala = (2, 2.5, 2)

montanna4 = copy.deepcopy(montanna1)
montanna4.posicion = (6, -0.5, -6)
montanna4.escala = (1.5, 2, 1.5)

montanna5 = copy.deepcopy(montanna1)
montanna5.posicion = (4, -0.5, -12)
montanna5.escala = (2.2, 2.8, 2.2)

montanna6 = copy.deepcopy(montanna1)
montanna6.posicion = (8, -0.5, -7)
montanna6.escala = (1.8, 2.2, 1.8)

grupoMontannas = [
    montanna1,
    montanna2,
    montanna3,
    montanna4,
    montanna5,
    montanna6
]