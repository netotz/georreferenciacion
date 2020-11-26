'''
Archivo para ya sea generar mapas de calor de contaminantes
o mapas coropléticos de ingresos por CIE.
'''

# from heatmap import plot_heatmap

# POLLUTANT = 'PM10'
# DAY = '1-Dec-18'

# plot_heatmap(POLLUTANT, DAY)

from choropleth import plot_entries_choropleth

YEAR = 2018
plot_entries_choropleth(YEAR)
