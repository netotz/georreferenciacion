'''
Contiene funciones para generar mapas coropléticos que muestran
conteos de ingresos agrupados por primera letra de CIE,
municipio del AMM y semana epidemiológica.

AMM = Área Metropolitana de Monterrey
'''

import itertools

import plotly
import plotly.graph_objects as go
import pandas as pd
import epiweeks

from resources.filter_geojson import read_amm_geojson
from resources.readers import read_entries, read_amm_municipalities

def group_dates_by_epiweeks(entries_dates: pd.Series) -> pd.Series:
    '''
    Agrupa fechas de ingreso for semanas epidemiológicas.

    :param entries: columna de fechas de ingreso.

    :returns: `pandas.Series` de fechas de ingreso ya agrupadas.
    '''
    # años mínimo y máximo que aparecen en el archivo
    minyear, maxyear = min(entries_dates).year, max(entries_dates).year

    # unir semanas de los años que aparecen en el archivo
    # y uno posterior
    weeks = list(itertools.chain.from_iterable(
        epiweeks.Year(year).iterweeks()
        for year in range(minyear, maxyear + 2)
    ))

    # lista de ingresos en semana epidemiológica
    epidates = list()
    # índice para iterar las semanas
    i = 0
    week = weeks[i]
    for dfdate in entries_dates.tolist():
        while True:
            # si está dentro de la semana actual
            if week.startdate() <= dfdate <= week.enddate():
                epidates.append(week)
                # siguiente ingreso
                break
            # si no, siguiente semana
            # pero mismo ingreso
            i += 1
            week = weeks[i]
    return epidates

def count_grouped_entries(entries: pd.DataFrame) -> pd.DataFrame:
    '''
    Cuenta los casos de ingresos agrupados por
    primera letra del CIE, municipio y semana epidemiológica.

    :param entries: debe contener las columnas:
        [DIAG_INI, MUNIC, INGRE]

    :returns: `entries` con una columna `CONT`, que cuenta de los casos agrupados.
    '''
    # agregar columna con primera letra de CIE
    entries['LETRA_CIE'] = entries['DIAG_INI'].str[0]
    # agregar columna de conteos de casos
    entries['CONT'] = 0

    # contar casos
    return (entries
        .groupby(['LETRA_CIE', 'MUNIC', 'INGRE'])
        .count()
        .reset_index()
        .drop(columns=['DIAG_INI'])
        .sort_values('LETRA_CIE'))

def get_amm_entries(year: int) -> pd.DataFrame:
    '''
    Filtra solamente los ingresos del AMM, agrupa las fechas
    por semana epidemiológica y cuenta los casos de CIE.

    :param year: año del archivo a leer (EGRESO_`year`.csv).

    :returns: registros de ingresos del AMM, y con columnas extras:
        [NOM_MUN, LETRA_CIE, CONT]
    '''
    entries = read_entries(year)
    amm_munics = read_amm_municipalities()

    # filtrar registros del AMM
    entries_amm = entries[
        (entries['ENTIDAD'] == '19') &
        entries['MUNIC'].isin(amm_munics['MUNIC'])
    ].drop(columns=['ENTIDAD'])

    # convertir columna de ingresos a tipo datetime
    entries_amm['INGRE'] = pd.to_datetime(entries_amm['INGRE'])
    # ordenar ascendente por ingresos
    entries_amm.sort_values('INGRE', inplace=True)
    entries_amm['INGRE'] = group_dates_by_epiweeks(entries_amm['INGRE'])

    entries_amm = count_grouped_entries(entries_amm)

    # agregar columna con nombres de municipios
    entries_amm = amm_munics.merge(entries_amm, on='MUNIC')

    return entries_amm

def plot_entries_choropleth(year: int, output: str = '') -> None:
    '''
    Genera un mapa coroplético animado sobre el conteo de
    ingresos por municipio, CIE y semana epidemiológica.

    :param year: año del archivo a leer (EGRESO_`year`.csv).

    :param output: Ruta relativa del archivo HTML para guardar el mapa coroplético.
    '''
    entries_amm = get_amm_entries(year)
    # límites de casos por archivo (año)
    mincount, maxcount = min(entries_amm['CONT']), max(entries_amm['CONT'])

    munics_geojson = read_amm_geojson()

    # por cada letra inicial de los CIE
    for cie_letter in entries_amm['LETRA_CIE'].unique():
        # filtrar ingresos por la letra CIE
        entries_cie = entries_amm[
            entries_amm['LETRA_CIE'] == cie_letter
        ].sort_values('INGRE')

        # listas para animación del mapa
        frames, steps = list(), list()
        # por cada semana en los ingresos del CIE actual
        for week in entries_cie['INGRE'].unique():
            # filtrar ingresos por la semana
            entries_ingre = entries_cie[
                entries_cie['INGRE'] == week
            ].sort_values('MUNIC')

            label = f'{week.year}, semana {week.week}'
            name = f'frame_{week}'
            frames.append({
                'name': name,
                'data': [
                    # mapa coroplético
                    dict(
                        type='choroplethmapbox',
                        geojson=munics_geojson,
                        locations=entries_ingre['MUNIC'],
                        z=entries_ingre['CONT'],
                        zmin=mincount,
                        zmax=maxcount,
                        hoverinfo='z+text+name',
                        text=entries_ingre['NOM_MUN'],
                        name='Casos en',
                        colorscale='Viridis',
                        marker_opacity=0.5,
                        marker_line_width=0,
                    )
                ]
            })
            steps.append({
                'label': label,
                'method': 'animate',
                'args': [
                    [name],
                    {
                        'mode': 'immediate',
                        'frame': {
                            'duration': 500,
                            'redraw': True
                        },
                        'transition': {'duration': 300}
                    }
                ]
            })

        sliders = [{
            'transition': {'duration': 300},
            'x': 0.08,
            'len': 0.88,
            'currentvalue': {'xanchor': 'center'},
            'steps': steps
        }]

        playbtn = [{
            'type': 'buttons',
            'showactive': True,
            'x': 0.045, 'y': -0.08,
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [
                    None,
                    {
                        'mode': 'immediate',
                        'frame': {
                            'duration': 500,
                            'redraw': True
                        },
                        'transition': {'duration': 300},
                        'fromcurrent': True
                    }
                ]
            }]
        }]

        layout = go.Layout(
            title=f'Archivo: EGRESOS_{year}     CIE: {cie_letter}',
            mapbox_style='carto-positron',
            mapbox_zoom=9.5,
            mapbox_center = {'lat': 25.680, 'lon': -100.249},
            sliders=sliders,
            updatemenus=playbtn
        )

        data = frames[0]['data']
        figure = go.Figure(data=data, layout=layout, frames=frames)

        # si no se especificó nombre de archivo, generar uno
        filepath = output if output else f'ingresos_{year}.html'
        # guardar mapa en archivo
        plotly.offline.plot(figure, filename=filepath)
