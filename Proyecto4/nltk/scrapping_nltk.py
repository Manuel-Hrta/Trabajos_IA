import twint
import pandas as pd

# Configuración de twint
c = twint.Config()
c.Search = "PelonGomis"  # Búsqueda en Twitter para el usuario "PelonGomis"
c.Limit = 100            # Limitar a 100 tweets
c.Pandas = True          # Usar pandas para almacenar los resultados

# Realizar búsqueda y obtener los tweets
twint.run.Search(c)

# Obtener los tweets y guardarlos en un archivo CSV
df = twint.storage.panda.Tweets_df
df.to_csv('tweets.csv', index=False)  # Guardar los tweets en un archivo CSV
print("Tweets guardados en tweets.csv")
