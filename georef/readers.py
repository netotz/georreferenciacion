'''
Funciones que leen los archivos CSV de esta carpeta (recursos).
'''

import pandas as pd

## las columnas de IDs de los CSV se leen como string
## porque el archivo GeoJSON así los tiene

def read_amm_municipalities() -> pd.DataFrame:
    '''
    Lee el archivo AMM_MUNICS.csv, el cual contiene
    los nombres y claves de los municipios del AMM.

    :returns: `DataFrame` con los municipos del AMM en columnas:
        [MUNIC, NOM_MUN]
    '''
    return pd.read_csv(
        'resources/AMM_MUNICS.csv',
        dtype={'MUNIC': str},
        encoding='utf-8'
    )

def read_entries(year: int, cie_column: str = 'DIAG_INI') -> pd.DataFrame:
    '''
    Lee el archivo EGRESO_`year`.csv.

    :param year: año del nombre del archivo.

    :param cie_column: nombre de la columna de CIE, varía por archivos.

    :returns: `DataFrame` con todos los registros, en columnas:
        [INGRE, ENTIDAD, MUNIC, `cie_column`]
    '''
    columns = ['INGRE', 'ENTIDAD', 'MUNIC', cie_column]
    # leer todos los registros del año especificado
    return pd.read_csv(
        f'resources/EGRESO_{year}.csv',
        usecols=columns,
        dtype={'ENTIDAD': str, 'MUNIC': str, 'INGRE': str}
    ).dropna()
