'''
Archivo aún no terminado.

AMM = Área Metropolitana de Monterrey
'''

import json

import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# municipios del AMM
amm_munics = pd.read_csv(
    'resources/AMM_MUNICS.csv',
    dtype={'MUNIC': str},
    encoding='utf-8'
)

columns = ['INGRE', 'EDAD', 'ENTIDAD', 'MUNIC', 'DIAG_INI']
entries = pd.read_csv(
    'resources/EGRESO_2018.csv',
    usecols=columns,
    dtype={'ENTIDAD': str, 'MUNIC': str}
).dropna()
# filtrar registros del AMM
entries_amm = entries[
    (entries.ENTIDAD == '19') & entries.MUNIC.isin(amm_munics.MUNIC)
].drop(columns=['ENTIDAD'])

entries_amm.INGRE = pd.to_datetime(entries_amm.INGRE)

# avg_ages = entries_amm.groupby(['MUNIC']).mean()
# avg_ages = amm_munics.merge(avg_ages, on='MUNIC')
entries_amm = amm_munics.merge(entries_amm, on='MUNIC')

# munics = pd.read_json('resources/mun2019gw.json', encoding='UTF-8')
# leer GeoJSON de municipios del AMM
with open('resources/amm_mun2019gw.json', 'r', encoding='UTF-8') as jsonfile:
    munics = json.load(jsonfile)

# crear mapa coroplético
figure = px.choropleth_mapbox(
    entries_amm,
    geojson=munics,
    locations='MUNIC',
    color='EDAD',
    color_continuous_scale='Viridis',
    mapbox_style='carto-positron',
    zoom=9,
    center = {'lat': 25.668, 'lon': -100.249},
    opacity=0.5,
    hover_name='NOM_MUN',
    hover_data=['EDAD'],
)

# guardar mapa interactivo en formato HTML
plotly.offline.plot(figure, filename='results/entries/choropleth_test.html')
# figure.show()
