import figuras as fg
from .arboles import arboles
from .caretera import carretera_segmentos
from .casas import casas
from .cesped import planos_cesped
from .gupoMontannas import grupoMontannas

terreno = fg.Objeto3D()
# Agregar todos los planos de césped
terreno.figuras.extend(planos_cesped)
# Agregar todos los segmentos de la carretera infinita
terreno.figuras.extend(carretera_segmentos)
terreno.figuras.extend(arboles)

terreno.figuras.extend(grupoMontannas)
terreno.figuras.extend(casas)
