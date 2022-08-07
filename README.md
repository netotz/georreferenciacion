# Georreferenciación

Verano Científico de la UANL 2020:
Georreferenciación con datos de contaminantes en el Área Metropolitana de Monterrey (AMM).

Ver póster en español [aquí](https://uanledu-my.sharepoint.com/:b:/g/personal/andres_ortizlpz_uanl_edu_mx/EWu9182vF_BGgz2Ai2FZDVQBURQJADUHYJ_OZv_6INo-TA?e=Vfn6gq).

---

2020 University Scientific Summer:
Geostatistical analysis of pollution in the city of Monterrey, México.

See Spanish poster [here](https://uanledu-my.sharepoint.com/:b:/g/personal/andres_ortizlpz_uanl_edu_mx/EWu9182vF_BGgz2Ai2FZDVQBURQJADUHYJ_OZv_6INo-TA?e=Vfn6gq).

## CLI

Este proyecto cuenta con una interfaz de línea de comandos (CLI).
Para usarla basta con ejecutar el archivo [`cli.py`](/georef/cli.py) desde el directorio de este repositorio:

`python georef/cli.py --help`

### Instalar comando

También es posible instalar el programa para mandarlo a llamar desde un comando:

`python setup.py install`

Luego de instalarlo, el programa estará disponible con el comando `georef`, sin tener que usar el de Python:

`georef --help`

## Mapas de calor / Heat maps

Translated from publication (not revised):

> Meteorological stations monitor air quality only in the microenvironment around them, so spatial interpolation methods are used, which are used to estimate or predict new levels of pollutants at points without information, based on the locations of the stations. stations and their known values.
> 
> Kriging is a spatial interpolation method that provides the best unbiased linear estimator of a point and minimizes the variance of the estimate. In the present work, the ordinary kriging method is used.
> 
> Starting from the known locations, that is, the thirteen monitoring stations, the points with calculated values ​​of the pollutant are predicted using a recursive calculation method by grids: it begins by executing the kriging method with a 5 × 5 grid, which is used to calculate another by adding five rows and five columns, 10 × 10. The procedure ends when there is a 40 × 40 coordinate grid, within which each cell has an estimated value on the pollutant, which results in a total of 1600 estimated points. These new points are used to plot a heat map for a pollutant on the MMA.

Se requiere una base de datos CSV con la siguiente cabecera:

`timestamp,station,CO,NO,NO2,NOX,O3,PM10,PM2_5,pressure,rainfall,humidity,SO2,solar,temperature,velocity,direction,valid,notes`

También se necesita un token de Mapbox para poder generar estos mapas. Para los detalles, consultar [ayuda de Mapbox](https://docs.mapbox.com/help/tutorials/get-started-tokens-api/) (en inglés).

Al ejecutar la función `plot_heatmap`
(ver [`heatmap.py`](/georef/heatmap.py))
se genera un mapa de calor animado como el siguiente:

![Mapa de calor](/results/pollution/demo.png)

En la carpeta [`results/pollution`](/results/pollution)
se encuentran los HTML de mapas completos de distintas fechas,
y enlaces para visualizarlos.

- La escala de colores representa el nivel del contaminante.
- La dirección de los marcadores indica la dirección del viento.
- La opacidad de los círculos sobre los marcadores representa la velocidad del viento.

## Mapas coropléticos / Choropleth maps

Se requiere uno de los archivos `EGRESO_{año}.csv` disponibles en el
[sitio web de la Secretaría de Salud](http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_egresoshosp_gobmx.html).

También se requiere un archivo GeoJSON que contenga la división municipal del AMM:
[`resources/amm_mun2019gw.json`](/resources/amm_mun2019gw.json) (archivo local).

Al ejecutar la función `plot_entries_choropleth`
(ver [`choropleth.py`](/georef/choropleth.py))
se genera un mapa coroplético animado como el siguiente:

![Mapa coroplético](/results/entries/demo.png)

Muestra el número de casos de ingresos hospitalarios agrupados por CIE,
municipio del AMM y semana epidemiológica.

En la carpeta [`results/entries`](/results/entries)
se encuentra un HTML de un mapa, pero está incompleto,
pues no contiene todas las semanas epidemiológicas,
debido a que el límite de tamaño en GitHub son 100 MB.
Para generar un mapa completo es necesario ejecutar la función.

## Recursos

Los archivos que necesita cada mapa deben encontrarse en una carpeta de nombre `resources`, como se muestra en este repositorio.
