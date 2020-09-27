'''
Genera un mapa de calor basado en datos de contaminantes,
viento y coordenadas de estaciones de calidad del aire.
'''

import pandas as pd
import plotly
import plotly.graph_objects as go

from kriging import interpolate

def plot_heatmap(pollutant: str, day: str) -> None:
    '''
    Muestra el mapa de calor del contaminante (pollutant) el día (day) en el navegador.
    '''

    # columnas a extraer del CSV
    columns = ['timestamp', 'station', pollutant, 'velocity', 'direction']
    dataframe = pd.read_csv('filled.csv', usecols=columns).dropna()
    # leer coordenadas de estaciones
    coords = pd.read_csv('coords.csv')

    # filtrar registros del día elegido
    dataset = coords.merge(dataframe.loc[dataframe['timestamp'].str.startswith(day)], on='station')
    # convertir strings a objeto datetime
    strfdt = '%d-%b-%y %H'
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'], format=strfdt)
    # escala de densidad
    zmin, zmax = min(dataset[pollutant]), max(dataset[pollutant])

    frames, steps = [], []
    # filtrar horas del día elegido
    hours = dataset.timestamp.unique()
    hours.sort()
    for hour in hours:
        # datos leídos en la hora epecífica
        data = dataset.loc[dataset['timestamp'] == hour]

        ## método de kringing
        # interpolar contaminante
        xcoords, ycoords, zpollution = interpolate(data.lon, data.lat, data[pollutant])
        # interpolar velocidad de viento
        _, _, zvelocity = interpolate(data.lon, data.lat, data['velocity'])
        # interpolar dirección de viento
        _, _, zdirection = interpolate(data.lon, data.lat, data['direction'])

        strhour = pd.to_datetime(hour).strftime(strfdt)
        from random import random
        frames.append({
            'name': f'frame_{strhour}',
            'data': [
                # mapa de vectores de viento
                dict(
                    type='scattermapbox',
                    lon=xcoords,
                    lat=ycoords,
                    mode='markers',
                    marker=dict(
                        opacity=0.7,
                        # size=zvelocity,
                        # allowoverlap=True,
                        symbol='marker',
                        angle=[angle + 180 for angle in zdirection]
                    ),
                    text=coords.station
                ),
                # mapa de calor de densidad de contaminante
                dict(
                    type='densitymapbox',
                    lon=xcoords,
                    lat=ycoords,
                    z=zpollution,
                    opacity=0.5,
                    zmin=zmin,
                    zmax=zmax
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
                        'duration': 200,
                        'redraw': True
                    },
                    'transition': {'duration': 100}
                }
            ]
        })

    sliders = [{
        'transition': {'duration': 0},
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
                        'duration': 200,
                        'redraw': True
                    },
                    'transition': {'duration': 100},
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
        # mapbox_style='stamen-terrain',
        autosize=True,
        mapbox=dict(
            accesstoken=token,
            center=dict(lat=25.67, lon=-100.338),
            zoom=9.3
        )
    )

    data = frames[0]['data']
    figure = go.Figure(data=data, layout=layout, frames=frames)
    plotly.offline.plot(figure, filename=f'results/{pollutant}_{day}.html')
    # figure.show()
