'''
El GeoJSON 'mun2019gw.json' contiene la división municipal de todo México.
En este proyecto solo se usan los municipios del Área Metropolitana de Monterrey (AMM),
por lo que se crea un archivo nuevo que los contiene y no el resto.

'mun2019gw.json' obtenido de CONABIO:
http://www.conabio.gob.mx/informacion/gis/
'''

import json

def write_filtered_geojson() -> None:
    '''
    Crea un nuevo archivo GeoJSON con solo los municipios del AMM.
    '''
    # leer GeoJSON de división municipal de México
    with open('mun2019gw.json', 'r', encoding='utf-8') as jsonfile:
        munics = json.load(jsonfile)

    # los municipios del AMM son del 959 al 1002
    munics['features'] = munics['features'][959:1003]
    for feature in munics['features']:
        # agregar llave 'id' con el valor del ID del municipio
        feature['id'] = feature['properties']['CVE_MUN']

    # guardar datos GeoJSON filtrados por AMM
    with open('amm_mun2019gw.json', 'w', encoding='utf-8') as newfile:
        json.dump(munics, newfile)

if __name__ == '__main__':
    write_filtered_geojson()
