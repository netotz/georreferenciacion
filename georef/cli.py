'''
Funciones para la consola de comandos (CLI).
'''

import sys
from argparse import ArgumentParser
from typing import Optional, List
from pathlib import Path
import string

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
            Todos los mapas se grafican sobre el Área Metropolitana de Monterrey (AMM).
            En el directorio actual debe existir un carpeta de nombre 'resources'
            que contenga los archivos necesarios para generar los mapas.
            Más información: https://github.com/netotz/georreferenciacion/blob/master/README.md#georreferenciaci%C3%B3n
            '''
    )

    # subcomandos para definir el tipo de mapa (coroplético o de calor)
    maptypes = parser.add_subparsers(
        title='tipo de mapa',
        description='''Define el tipo de mapa a generar.
            Agrega el argumento '-h' o '--help' después del subcomando
            para ver los argumentos de cada uno:''',
        dest='maptype',
        required=True
    )

    # parser padre de los subparsers de maptype,
    # sirve para contener los argumentos que tienen en común
    common_args_parser = ArgumentParser(add_help=False)
    common_args_parser.add_argument(
        '-o', '--output',
        metavar='FILEPATH',
        type=Path,
        help='''Ruta relativa del archivo destino HTML para guardar el mapa.
            Si no se especifica, se genera un nombre de archivo basado en
            los argumentos posicionales y lo crea en el directorio actual.
            Si el archivo ya existe lo sobrescribe.
            La ruta debe contener carpetas existentes.
            Ejemplos: diractual.html , carpetas/existentes/mapa.html'''
    )

    cm_help = '''Mapa coroplético que muestra el conteo de casos de ingresos
        agrupados por municipio, CIE y semana epidemiológica
        de un año específico.'''
    cm_description = f'''Genera un {cm_help[0].lower()}{cm_help[1:]}
        Ejemplo: georef cm 2018 O'''
    # subparser de argumentos para mapa coroplético
    choropleth_parser = maptypes.add_parser(
        'choroplethmap',
        aliases=['cm'],
        parents=[common_args_parser],
        help=cm_help,
        description=cm_description
    )
    choropleth_parser.add_argument(
        'year',
        type=int,
        help='Año del archivo de egresos a leer: EGRESOS_{year}.csv'
    )
    choropleth_parser.add_argument(
        'cie',
        choices=string.ascii_uppercase,
        help='Primera letra del diagnóstico CIE'
    )

    hm_help = '''Mapa de calor que muestra la densidad de un contaminante
        junto con marcadores que representan la velocidad y dirección
        del viento de una fecha específica.
        Requiere tener un token de Mapbox.'''
    hm_description = f'''Genera un {hm_help[0].lower()}{hm_help[1:]}
        Ejemplo: georef hm PM10 25-Dec-18'''
    # subparser de argumentos para mapa de calor
    heat_parser = maptypes.add_parser(
        'heatmap',
        aliases=['hm'],
        parents=[common_args_parser],
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
        help='''Fecha en inglés con formato '<día>-<mes corto>-<año corto>',
            ejemplo: \'1-Dec-18\''''
    )
    heat_parser.add_argument(
        '-t', '--token',
        metavar='FILEPATH',
        type=Path,
        required=True,
        help='''Ruta relativa del archivo que contiene el token de Mapbox.
            Más información: https://docs.mapbox.com/help/tutorials/get-started-tokens-api/'''
    )

    # si el comando no recibe argumentos
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # leer argumentos de consola
    arguments = parser.parse_args(optional_args)

    # ruta del archivo, si no especificó, usar string vacío
    filepath = str(arguments.output) if arguments.output else ''

    # no es necesario checar si el subcomando 'maptype' existe porque es obligatorio
    if arguments.maptype in ('cm', 'choroplethmap'):
        year = arguments.year
        cie = arguments.cie
        plot_entries_choropleth(year, cie, filepath)
    elif arguments.maptype in ('hm', 'heatmap'):
        pollutant = arguments.pollutant
        date = arguments.date
        token = str(arguments.token)
        plot_heatmap(pollutant, date, token, filepath)

# ejecutar la aplicación de consola al correr este archivo
if __name__ == '__main__':
    parse_arguments()
