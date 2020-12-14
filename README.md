# Georreferenciación

Proyecto de investigación de PROVERICYT 2020:
Georreferenciación con datos de contaminantes en el Área Metropolitana de Monterrey (AMM).

## CLI

Este proyecto cuenta con una interfaz de línea de comandos (CLI).
Para usarla basta con ejecutar el archivo [`cli.py`](/georef/cli.py) desde el directorio de este repositorio:

`python georef/cli.py --help`

### Instalar comando

También es posible instalar el programa para mandarlo a llamar desde un comando:

`python setup.py install`

Luego de instalarlo, el programa estará disponible con el comando `georef`, sin tener que usar el de Python:

`georef --help`

## Mapas de calor

Se requiere una base de datos CSV con la siguiente cabecera:

`timestamp,station,CO,NO,NO2,NOX,O3,PM10,PM2_5,pressure,rainfall,humidity,SO2,solar,temperature,velocity,direction,valid,notes`

Al ejecutar la función `plot_heatmap`
(ver [`heatmap.py`](/georef/heatmap.py))
se genera un mapa de calor animado como el siguiente:

![Mapa de calor](/results/pollution/demo.png)

En la carpeta [`results/pollution`](/results/pollution)
se encuentran los HTML de mapas completos de distintas fechas,
y enlaces para visualizarlos.

La escala de colores representa el nivel del contaminante,
la dirección de los marcadores indica la dirección del viento,
y la opacidad de los círculos sobre los marcadores representa la velocidad del viento.

## Mapas coropléticos

Se requiere uno de los archivos `EGRESO_{año}.csv` disponibles en:
<http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_egresoshosp_gobmx.html>.

También se requiere un archivo GeoJSON que contenga la división municipal del AMM:
[`resources/amm_mun2019gw.json`](/resources/amm_mun2019gw.json).

Al ejecutar la función `plot_entries_choropleth`
(ver [`choropleth.py`](/georef/choropleth.py))
se genera un mapa coroplético animado como el siguiente:

![Mapa coroplético](/results/entries/demo.png)

Muestra el número de casos de ingresos agrupados por CIE,
municipio del AMM y semana epidemiológica.

En la carpeta [`results/entries`](/results/entries)
se encuentra un HTML de un mapa, pero está incompleto,
pues no contiene todas las semanas epidemiológicas,
debido a que el límite de tamaño en GitHub son 100 MB.
Para generar un mapa completo es necesario ejecutar la función.

## Recursos

Los archivos que necesita cada mapa deben encontrarse en una carpeta de nombre `resources`, como se muestra en este repositorio.
