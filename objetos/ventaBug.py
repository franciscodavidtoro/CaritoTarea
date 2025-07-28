import figuras as fg

ventana=fg.Figura(posicion=(0,2.5,0),escala=(5,5,0.1), color=(1,1,1,0.1))
objeto=fg.Figura(posicion=(0,2.5,3), color=(0,0,0.4,1))
objetoVisible=fg.Figura(posicion=(0,2.5,-3), color=(0,0.4,0,1))


test=fg.Objeto3D()
test.figuras.append(objetoVisible)
test.figuras.append(ventana)
test.figuras.append(objeto)