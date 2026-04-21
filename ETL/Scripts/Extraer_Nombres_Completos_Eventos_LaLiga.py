import pandas as pd
import os

# Definimos la ruta exacta de tu carpeta (la 'r' delante es para que Windows lea bien las barras '\')
ruta_carpeta = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga"

# Archivos de entrada y salida
ruta_entrada = os.path.join(ruta_carpeta, "Detalle_Eventos_LaLiga_Total.csv")
ruta_salida = os.path.join(ruta_carpeta, "Nombres_Unicos_LaLiga.csv")

print("Leyendo el archivo de eventos...")
# 1. Cargamos tu tabla de eventos de LaLiga
df_eventos = pd.read_csv(ruta_entrada) 

# 2. Extraemos los nombres únicos largos (quitando los nulos)
nombres_unicos = pd.DataFrame(df_eventos['jugador'].dropna().unique(), columns=['Nombre_Largo_LaLiga'])

# 3. Exportamos el CSV limpio a esa misma carpeta
nombres_unicos.to_csv(ruta_salida, index=False, sep=';')

print(f"¡Listo! Se han guardado {len(nombres_unicos)} nombres únicos en: {ruta_salida}")