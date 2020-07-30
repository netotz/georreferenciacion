'''
Genera un mapa de calor basado en datos de contaminantes y coordenadas
de estaciones de calidad del aire.
'''

import pandas as pd
import plotly
import plotly.graph_objects as go

from kriging import interpolate

def plot_heatmap(pollutant: str, day: str) -> None:
    '''
    Muestra el mapa de calor del contaminante (pollutant) el día (day) en el navegador.
    '''
    dataframe = pd.read_csv('filled.csv', usecols=['timestamp', 'station', pollutant]).dropna()
    coords = pd.read_csv('coords.csv')

    # filtrar registros del día elegido
    dataset = coords.merge(dataframe.loc[dataframe['timestamp'].str.startswith(day)], on='station')
    # convertir strings a objeto datetime
    strfdt = '%d-%b-%y %H'
    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'], format=strfdt)
    # escala de densidad
    zmin, zmax = min(dataset.PM10), max(dataset.PM10)

    frames, steps = [], []
    # filtrar horas del día elegido
    hours = dataset.timestamp.unique()
    hours.sort()
    for hour in hours:
        # coordenadas de las estaciones y el contaminante que leyeron en la hora epecífica
        data = dataset.loc[dataset['timestamp'] == hour]

        # método de kringing
        xcoords, ycoords, zvalues = interpolate(data.lon, data.lat, data[pollutant])

        strhour = pd.to_datetime(hour).strftime(strfdt)
        frames.append({
            'name': f'frame_{strhour}',
            'data': [{
                'type': 'densitymapbox',
                'lon': xcoords,
                'lat': ycoords,
                'z': zvalues,
                'opacity': 0.5,
                'zmin': zmin,
                'zmax': zmax
            }],
        })
        steps.append({
            'label': strhour,
            'method': 'animate',
            'args': [
                [f'frame_{strhour}'],
                {
                    'mode': 'immediate',
                    'frame': {
                        'duration': 100,
                        'redraw': True
                    },
                    'transition': {'duration': 50}
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
                        'duration': 100,
                        'redraw': True
                    },
                    'transition': {'duration': 50},
                    'fromcurrent': True
                }
            ]
        }]
    }]

    data = frames[0]['data']
    layout = go.Layout(
        sliders=sliders,
        updatemenus=playbtn,
        mapbox_style='stamen-terrain',
        autosize=True,
        mapbox=dict(
            center=dict(lat=25.67, lon=-100.338),
            zoom=10
        )
    )

    figure = go.Figure(data=data, layout=layout, frames=frames)
    plotly.offline.plot(figure, filename=f'results/{pollutant}_{day}.html')
