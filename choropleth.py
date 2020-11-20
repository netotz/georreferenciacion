'''
Archivo aún no terminado.

AMM = Área Metropolitana de Monterrey
'''

import json

import plotly
import plotly.graph_objects as go
import pandas as pd

## las columnas de IDs de los CSV se leen como string
## porque el archivo GeoJSON así los tiene

# municipios del AMM
amm_munics = pd.read_csv(
    'resources/AMM_MUNICS.csv',
    dtype={'MUNIC': str},
    encoding='utf-8'
)

columns = ['INGRE', 'ENTIDAD', 'MUNIC', 'DIAG_INI']
entries = pd.read_csv(
    'resources/EGRESO_2018.csv',
    usecols=columns,
    dtype={'ENTIDAD': str, 'MUNIC': str, 'INGRE': str}
).dropna()

# filtrar registros del AMM
entries_amm = entries[
    (entries.ENTIDAD == '19') &
    entries.MUNIC.isin(amm_munics.MUNIC)
].drop(columns=['ENTIDAD'])

entries_amm.INGRE = pd.to_datetime(entries_amm.INGRE)

# agregar columna con primera letra de CIE
entries_amm['LETRA_CIE'] = entries_amm.DIAG_INI.str[0]
# agregar columna de conteos de casos
# agrupados por municipio y letra de CIE
entries_amm['CONT'] = 0

dates = entries_amm['INGRE']

# contar casos
entries_amm = (entries_amm
    .groupby(['LETRA_CIE', 'MUNIC'])
    .count()
    .reset_index()
    #)
    .drop(columns=['INGRE', 'DIAG_INI']))

entries_amm['INGRE'] = dates

# agregar columna con nombres de municipios
entries_amm = amm_munics.merge(entries_amm, on='MUNIC')

# munics = pd.read_json('resources/mun2019gw.json', encoding='UTF-8')
# leer GeoJSON de municipios del AMM
with open('resources/amm_mun2019gw.json', 'r', encoding='utf-8') as jsonfile:
    munics = json.load(jsonfile)

# límites por año
maxcount, mincount = max(entries_amm.CONT), min(entries_amm.CONT)

# por cada letra inicial de los CIE
for cie_letter in entries_amm.LETRA_CIE.unique()[:1]:
    dataset = entries_amm[entries_amm.LETRA_CIE == cie_letter]

    # crear mapa coroplético
    choropleth = go.Choroplethmapbox(
        geojson=munics,
        locations=dataset['MUNIC'],
        z=dataset['CONT'],
        zmin=mincount,
        zmax=maxcount,
        hoverinfo='z+text+name',
        text=dataset['NOM_MUN'],
        name='Casos en',
        colorscale='Viridis',
        marker_opacity=0.5,
        marker_line_width=0,
    )

    layout = go.Layout(
        title=f'2018, CIE: {cie_letter}',
        mapbox_style='carto-positron',
        mapbox_zoom=9.5,
        mapbox_center = {'lat': 25.680, 'lon': -100.249},
    )

    figure = go.Figure(choropleth, layout)
    # guardar mapa interactivo en formato HTML
    plotly.offline.plot(figure, filename=f'results/entries/choropleth_{cie_letter}.html')
    # figure.show()
