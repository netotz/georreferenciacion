'''
Genera un mapa de calor basado en datos de contaminantes,
viento y coordenadas de estaciones de calidad del aire.
'''

import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go

from kriging import interpolate

def plot_heatmap(pollutant: str, date: str) -> None:
    '''
    Genera un mapa de calor de un contaminante con marcadores
    de dirección y velocidad del viento del día especificado.

    :pollutant: Nombre del contaminante.

    :date: Fecha en formato `<día>-<mes corto>-<año corto>` (`'d-b-y'`), ejemplo:
        '1-Dec-18'
    '''
    # columnas a extraer del CSV
    columns = ['timestamp', 'station', pollutant, 'velocity', 'direction']
    dataframe = pd.read_csv('resources/filled.csv', usecols=columns).dropna()
    # leer coordenadas de estaciones
    coords = pd.read_csv('resources/coords.csv')

    # filtrar registros del día elegido
    dataset = coords.merge(dataframe.loc[dataframe['timestamp'].str.startswith(date)], on='station')
    # convertir strings a objeto datetime
    strfdt = '%d-%b-%y %H'
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'], format=strfdt)

    # escala de densidad
    pollutionmin, pollutionmax = min(dataset[pollutant]), max(dataset[pollutant])

    velocitymin, velocitymax = min(dataset['velocity']), max(dataset['velocity'])

    frames, steps = [], []
    # filtrar horas del día elegido
    hours = dataset.timestamp.unique()
    hours.sort()
    for hour in hours:
        # datos leídos en la hora epecífica
        data = dataset.loc[dataset['timestamp'] == hour]

        ## método de kringing
        # interpolar contaminante
        xpollution, ypollution, zpollution = interpolate(data.lon, data.lat, data[pollutant], range(5, 41, 5))

        # rango para interpolación recursiva para valores de viento (20x20 puntos)
        grid = range(5, 21, 5)
        # interpolar velocidad de viento
        xvelocity, yvelocity, zvelocity = interpolate(data.lon, data.lat, data['velocity'], grid)
        # interpolar dirección de viento
        xdirection, ydirection, zdirection = interpolate(data.lon, data.lat, data['direction'], grid)

        strhour = pd.to_datetime(hour).strftime(strfdt)

        frames.append({
            'name': f'frame_{strhour}',
            'data': [
                # mapa de dirección de viento
                dict(
                    type='scattermapbox',
                    lon=xdirection,
                    lat=ydirection,
                    mode='markers',
                    marker=dict(
                        symbol='marker',
                        size=12,
                        allowoverlap=True,
                        angle=[angle + 180 for angle in zdirection]
                    ),
                    text=zdirection
                ),
                # mapa de velocidad de viento
                dict(
                    type='scattermapbox',
                    lon=xvelocity,
                    lat=yvelocity,
                    mode='markers',
                    marker=dict(
                        symbol='circle',
                        size=12,
                        allowoverlap=True,
                        color='white',
                        opacity=np.interp(zvelocity, (velocitymin, velocitymax), (0, 1)),
                    ),
                    text=zvelocity
                ),
                # mapa de calor de densidad de contaminante
                dict(
                    type='densitymapbox',
                    lon=xpollution,
                    lat=ypollution,
                    z=zpollution,
                    opacity=0.5,
                    zmin=pollutionmin,
                    zmax=pollutionmax
                )
            ]
        })
        steps.append({
            'label': strhour,
            'method': 'animate',
            'args': [
                [f'frame_{strhour}'],
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

    with open('.token', 'r') as file:
        token = file.read()

    layout = go.Layout(
        sliders=sliders,
        updatemenus=playbtn,
        autosize=True,
        mapbox=dict(
            accesstoken=token,
            center=dict(lat=25.67, lon=-100.338),
            zoom=9.3
        )
    )

    data = frames[0]['data']
    figure = go.Figure(data=data, layout=layout, frames=frames)

    # plotly.offline.plot(figure, filename=f'results/pollution/{pollutant}_{date}.html')
    # obtener mapa en HTML como string
    graph = plotly.offline.plot(figure, output_type='div')
    # guardar string en archivo
    print(graph)
    # figure.show()
