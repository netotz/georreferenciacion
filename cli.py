'''
Funciones para la consola de comandos (CLI).

#! No terminado aún.
'''

import sys
from argparse import ArgumentParser

def parse_arguments() -> None:
    '''
    Lee argumentos de la consola al usar el comando instalado.
    '''
    # parser principal
    parser = ArgumentParser(
        description='''
            Genera un archivo HTML de un tipo de mapa especificado por
            los siguientes argumentos.
            Todos los mapas se grafican sobre el Área Metropolitana de Monterrey (AMM).
            '''
    )
    # subcomandos para definir el tipo de mapa (coroplético o de calor)
    maptypes = parser.add_subparsers(
        title='tipo de mapa',
        description='''
            Define el tipo de mapa a generar.
            Cada tipo tiene argumentos específicos:''',
        dest='maptype',
        required=True
    )

    # subparser de argumentos para mapa coroplético
    choropleth_parser = maptypes.add_parser(
        'choroplethmap',
        aliases=['cm'],
        help='''
            Mapa coroplético que muestra el conteo de casos de ingresos
            agrupados por municipio, CIE y semana epidemiológica
            de un año específico.'''
    )
    choropleth_parser.add_argument(
        'year',
        type=int,
        help='Año del archivo de egresos a leer: EGRESOS_{year}.csv'
    )

    # subparser de argumentos para mapa de calor
    heat_parser = maptypes.add_parser(
        'heatmap',
        aliases=['hm'],
        help='''
            Mapa de calor que muestra la densidad de un contaminante
            junto con marcadores que representan la velocidad y dirección
            del viento de una fecha específica.'''
    )
    heat_parser.add_argument(
        'pollutant',
        choices='CO,NO,NO2,NOX,O3,PM10,PM2_5'.split(','),
        help='Nombre del contaminante'
    )
    heat_parser.add_argument(
        'date',
        type=str,
        help='''
            Fecha en formato '<día>-<mes corto>-<año corto>',
            ejemplo: '1-Dec-18'
            '''
    )

    # si el comando no recibe argumentos
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # leer argumentos de consola
    arguments = parser.parse_args()
