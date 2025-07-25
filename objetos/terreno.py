import figuras as fg
from .arboles import arboles
from .caretera import carretera
from .casas import casas
from .cesped import plano
from .gupoMontannas import grupoMontannas

terreno = fg.Objeto3D()
terreno.figuras.append(plano)
terreno.figuras.append(carretera)
terreno.figuras.extend(arboles)

terreno.figuras.extend(grupoMontannas)
terreno.figuras.extend(casas)
