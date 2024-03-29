'''
Interpolación con método de Kringing.
'''

from typing import Iterable, Tuple, List, Sequence
from itertools import chain, product

import numpy as np
from pykrige.ok import OrdinaryKriging

def get_segments(array: Iterable, n: int) -> np.ndarray:
    '''
    Segmenta 'array' en 'n' partes.
    '''
    amin, amax = min(array), max(array)
    return np.linspace(amin, amax, n)

def interpolate(xcoords: Sequence, ycoords: Sequence, zvalues: Sequence, gridrange: range) -> Tuple[List[float], List[float], List[float]]:
    '''
    Interpola las coordenadas (`xcoords`, `ycoords`) con valores `zvalues` para estimar puntos
    usando un rango `gridrange` en forma de malla recursiva.
    '''
    for k in gridrange:
        krige = OrdinaryKriging(
            xcoords, ycoords, zvalues,
            variogram_model='spherical'
        )

        xpoints, ypoints = get_segments(xcoords, k), get_segments(ycoords, k)
        # ejecutar método de kriging
        zvalues, _ = krige.execute('grid', xpoints, ypoints)

        # usar cada celda de la malla generada como punto estimado
        xcoords = [x for y, x in product(ypoints, xpoints)]
        ycoords = [y for y, x in product(ypoints, xpoints)]
        zvalues = list(chain.from_iterable(zvalues))

    # retornar 1600 coordenadas (malla 40x40)
    return xcoords, ycoords, zvalues
