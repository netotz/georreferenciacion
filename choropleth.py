'''
Archivo aún no terminado.

AMM = Área Metropolitana de Monterrey
'''

import json
import itertools

import plotly
import plotly.graph_objects as go
import pandas as pd
import epiweeks

## las columnas de IDs de los CSV se leen como string
## porque el archivo GeoJSON así los tiene

# municipios del AMM
amm_munics = pd.read_csv(
    'resources/AMM_MUNICS.csv',
    dtype={'MUNIC': str},
    encoding='utf-8'
)

YEAR = 2018
columns = ['INGRE', 'ENTIDAD', 'MUNIC', 'DIAG_INI']
# leer todos los registros del año especificado
entries = pd.read_csv(
    f'resources/EGRESO_{YEAR}.csv',
    usecols=columns,
    dtype={'ENTIDAD': str, 'MUNIC': str, 'INGRE': str}
).dropna()

# filtrar registros del AMM
entries_amm = entries[
    (entries['ENTIDAD'] == '19') &
    entries['MUNIC'].isin(amm_munics['MUNIC'])
].drop(columns=['ENTIDAD'])

# convertir columna de ingresos a tipo datetime
entries_amm['INGRE'] = pd.to_datetime(entries_amm['INGRE'])
# ordenar ascendente por ingresos
entries_amm.sort_values('INGRE', inplace=True)

# años mínimo y máximo que aparecen en el archivo
minyear, maxyear = min(entries_amm['INGRE']).year, max(entries_amm['INGRE']).year

# unir semanas de los años que aparecen en el archivo
# y uno posterior
weeks = list(itertools.chain.from_iterable(
    epiweeks.Year(year).iterweeks()
    for year in range(minyear, maxyear + 2)
))

# lista de ingresos en semana epidemiológica
dates = list()
# índice para iterar las semanas
i = 0
week = weeks[i]
for dfdate in entries_amm['INGRE'].tolist():
    while True:
        # si está dentro de la semana actual
        if week.startdate() <= dfdate <= week.enddate():
            dates.append(week)
            # siguiente ingreso
            break
        # si no, siguiente semana
        # pero mismo ingreso
        i += 1
        week = weeks[i]
entries_amm['INGRE'] = dates

# agregar columna con primera letra de CIE
entries_amm['LETRA_CIE'] = entries_amm['DIAG_INI'].str[0]
# agregar columna de conteos de casos
# agrupados por municipio y letra de CIE
entries_amm['CONT'] = 0

# contar casos
entries_amm = (entries_amm
    .groupby(['LETRA_CIE', 'MUNIC', 'INGRE'])
    .count()
    .reset_index()
    .drop(columns=['DIAG_INI'])
    .sort_values('LETRA_CIE'))

# agregar columna con nombres de municipios
entries_amm = amm_munics.merge(entries_amm, on='MUNIC')

# munics = pd.read_json('resources/mun2019gw.json', encoding='UTF-8')
# leer GeoJSON de municipios del AMM
with open('resources/amm_mun2019gw.json', 'r', encoding='utf-8') as jsonfile:
    munics = json.load(jsonfile)

# límites de casos por archivo (año)
mincount, maxcount = min(entries_amm['CONT']), max(entries_amm['CONT'])

# por cada letra inicial de los CIE
for cie_letter in entries_amm['LETRA_CIE'].unique()[14:15]:
    entries_cie = entries_amm[
        entries_amm['LETRA_CIE'] == cie_letter
    ].sort_values('INGRE')

    frames, steps = list(), list()
    for week in entries_cie['INGRE'].unique():
        entries_ingre = entries_cie[
            entries_cie['INGRE'] == week
        ].sort_values('MUNIC')

        label = f'{week}'
        name = f'frame_{label}'
        frames.append({
            'name': name,
            'data': [
                # mapa coroplético
                dict(
                    type='choroplethmapbox',
                    geojson=munics,
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
        title=f'2018, CIE: {cie_letter}',
        mapbox_style='carto-positron',
        mapbox_zoom=9.5,
        mapbox_center = {'lat': 25.680, 'lon': -100.249},
        sliders=sliders,
        updatemenus=playbtn
    )

    data = frames[0]['data']
    figure = go.Figure(data=data, layout=layout, frames=frames)
    # figure = go.Figure(choropleth, layout)
    # guardar mapa interactivo en formato HTML
    plotly.offline.plot(figure, filename=f'results/entries/choropleth_{cie_letter}.html')
    # figure.show()
