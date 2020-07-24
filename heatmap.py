'''
Genera un mapa de calor basado en datos de contaminantes y coordenadas
de estaciones de calidad del aire.
'''

import pandas as pd
import plotly.graph_objects as go

from kriging import interpolate

def plot_heatmap(pollutant: str, day: str) -> None:
    '''
    Muestra el mapa de calor del contaminante (pollutant) el día (day) en el navegador.
    '''
    dataframe = pd.read_csv('filled.csv', usecols=['timestamp', 'station', pollutant]).dropna()
    coords = pd.read_csv('coords.csv')

    dates = dataframe.timestamp.unique()
    # filtrar horas del día elegido
    hours = (d for d in dates if d.startswith(day))

    frames, steps = [], []
    for hour in hours:
        # coordenadas de las estaciones y el contaminante que leyeron en la hora epecífica
        dataset = coords.merge(dataframe.loc[dataframe['timestamp'] == hour], on='station')
        # método de kringing
        xcoords, ycoords, zvalues = interpolate(dataset.lon, dataset.lat, dataset[pollutant])

        frames.append({
            'name': f'frame_{hour}',
            'data': [{
                'type': 'densitymapbox',
                'lon': xcoords,
                'lat': ycoords,
                'z': zvalues,
                'opacity': 0.5
            }],
        })
        steps.append({
            'label': hour,
            'method': 'animate',
            'args': [
                [f'frame_{hour}'],
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
            zoom=10.4
        )
    )

    figure = go.Figure(data=data, layout=layout, frames=frames)
    figure.show()
