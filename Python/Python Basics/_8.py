import numpy as np

utilidad = [0.60, 0.10, 0.09]
capacidad = [6*30, 7*25]
demanda  =[100, 1400, 1000]

restriciones = np.array(demanda + capacidad)
print(restriciones)

requerimiento = [[1, 0, 0],
                 [0, 1, 0],
                 [0, 0, 1]]

maquinas = [[0.75*0.5, 0.5*0.1, 0.15*0.03],
            [2.00*0.5, 1.5*0.1, 1.5*0.03]]

_1 = requerimiento + maquinas

print(np.array(_1))
print(_1)

import lp
import pulp
from cvxopt.glpk import ilp

plan, objetivo = ilp(utilidad, _1, restriciones, "", "max")
print("x variables: {}" .format(plan))

