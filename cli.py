'''
Funciones para la consola de comandos (CLI).

#! No terminado aún.
'''

import sys
from argparse import ArgumentParser
from typing import Optional, List

from heatmap import plot_heatmap
from choropleth import plot_entries_choropleth

def parse_arguments(optional_args: Optional[List[str]] = None) -> None:
    '''
    Lee argumentos de la consola al usar el comando instalado.

    :param optional_args: Lista de argumentos opcionales, por defecto `None`.
    Si se especifica, no se leerán los recibidos por consola.
    '''
    # parser principal
    parser = ArgumentParser(
        description='''Genera el HTML de un tipo de mapa especificado por
            los siguientes comandos y sus argumentos.
            Todos los mapas se grafican sobre el Área Metropolitana de Monterrey (AMM).'''
    )
    # subcomandos para definir el tipo de mapa (coroplético o de calor)
    maptypes = parser.add_subparsers(
        title='tipo de mapa',
        description='''Define el tipo de mapa a generar.
            Para guardar el mapa en un archivo HTML, usar el operador '>'
            y el nombre del archivo al final del comando.
            Agrega el argumento '-h' o '--help' después del subcomando
            para ver los argumentos de cada uno:''',
        dest='maptype',
        required=True
    )

    cm_help = '''Mapa coroplético que muestra el conteo de casos de ingresos
        agrupados por municipio, CIE y semana epidemiológica
        de un año específico.'''
    cm_description = f'''Genera un {cm_help[0].lower()}{cm_help[1:]}
        Ejemplo: georef cm 2018 > ingresos2018.html'''
    # subparser de argumentos para mapa coroplético
    choropleth_parser = maptypes.add_parser(
        'choroplethmap',
        aliases=['cm'],
        help=cm_help,
        description=cm_description
    )
    choropleth_parser.add_argument(
        'year',
        type=int,
        help='Año del archivo de egresos a leer: EGRESOS_{year}.csv'
    )

    hm_help = '''Mapa de calor que muestra la densidad de un contaminante
        junto con marcadores que representan la velocidad y dirección
        del viento de una fecha específica.'''
    hm_description = f'''Genera un {hm_help[0].lower()}{hm_help[1:]}
        Ejemplo: georef hm PM10 25-Dec-18 > pm10_25dec18.html'''
    # subparser de argumentos para mapa de calor
    heat_parser = maptypes.add_parser(
        'heatmap',
        aliases=['hm'],
        help=hm_help,
        description=hm_description
    )
    heat_parser.add_argument(
        'pollutant',
        choices='CO,NO,NO2,NOX,O3,PM10,PM2_5'.split(','),
        help='Nombre del contaminante'
    )
    heat_parser.add_argument(
        'date',
        type=str,
        help='''Fecha en formato '<día>-<mes corto>-<año corto>', ejemplo: \'1-Dec-18\''''
    )

    # si el comando no recibe argumentos
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # leer argumentos de consola
    arguments = parser.parse_args(optional_args)

    # no es necesario checar si el subcomando 'maptype' existe porque es obligatorio
    if arguments.maptype in ('cm', 'choroplethmap'):
        year = arguments.year
        plot_entries_choropleth(year)
    elif arguments.maptype in ('hm', 'heatmap'):
        pollutant = arguments.pollutant
        date = arguments.date
        plot_heatmap(pollutant, date)
