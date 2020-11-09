from numpy.lib.shape_base import apply_over_axes
import pandas as pd

# Importar CSV
data = pd.read_csv("athlete_events.csv")

# Seleccionar datos deporte
deporte = data[data["Sport"] == "Wrestling"]

# filtrar medallas de oro
medalla = deporte[deporte["Medal"] == "Gold"]

# Crear un LOOP analisis anual - Iterable por Año
years = medalla["Year"].unique()

for year in years:
    # Filtrar para ese año
    x = medalla[medalla["Year"] == year]

    # crear loop para cada país - iterable país
    paises = x[""]

# Filtrar para ese país

# Mayor de 15 medallas de oro
