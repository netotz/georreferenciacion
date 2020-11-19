'''
Archivo aún no terminado.
'''

import json

import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# municipios del AMM
mam_munics = pd.read_csv(
    'resources/mam_munics.csv',
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
entries_mam = entries[
    (entries.ENTIDAD == '19') & entries.MUNIC.isin(mam_munics.MUNIC)
].drop(columns=['ENTIDAD'])

entries_mam.INGRE = pd.to_datetime(entries_mam.INGRE)


# avg_ages = entries_mam.groupby(['MUNIC']).mean()
# avg_ages = mam_munics.merge(avg_ages, on='MUNIC')
# entries_mam = mam_munics.merge(entries_mam, on='MUNIC')


# munics = pd.read_json('resources/mun2019gw.json', encoding='UTF-8')
# leer GeoJSON de división municipal de México
with open('resources/mun2019gw.json', 'r', encoding='UTF-8') as jsonfile:
    munics = json.load(jsonfile)

# los municipios del AMM son del 959 al 1002
munics['features'] = munics['features'][959:1003]
for feature in munics['features']:
    # agregar llave 'id' con el valor del ID del municipio
    feature['id'] = feature['properties']['CVE_MUN']

# crear mapa coroplético
figure = px.choropleth_mapbox(
    entries_mam,
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
