# Georreferenciación

Proyecto de investigación de PROVERICYT 2020:
Georreferenciación con datos de contaminantes en el Área Metropolitana de Monterrey (AMM).

## Mapas de calor

Se requiere una base de datos CSV con la siguiente cabecera:

`timestamp,station,CO,NO,NO2,NOX,O3,PM10,PM2_5,pressure,rainfall,humidity,SO2,solar,temperature,velocity,direction,valid,notes`

Al ejecutar la función `plot_heatmap`
(ver [`heatmap.py`](/heatmap.py))
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
<http://www.dgis.salud.gob.mx/contenidos/basesdedatos/da_egresoshosp_gobmx.html>

Al ejecutar la función `plot_entries_choropleth`
(ver [`choropleth.py`](/choropleth.py))
se genera un mapa coroplético animado como el siguiente:

![Mapa coroplético](/results/entries/demo.png)

Muestra el número de casos de ingresos agrupados por CIE,
municipio del AMM y semana epidemiológica.

En la carpeta [`results/entries`](/results/entries)
se encuentra un HTML de un mapa, pero está incompleto,
pues no contiene todas las semanas epidemiológicas,
debido a que el límite de tamaño en GitHub son 100 MB.
Para generar un mapa completo es necesario ejecutar la función.