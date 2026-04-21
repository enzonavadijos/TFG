import pandas as pd

import os

import glob



# --- RUTAS ---

CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL\CSV"

carpeta_enlaces = os.path.join(CARPETA_BASE, "Enlaces FBref")

ruta_dim_partidos = os.path.join(CARPETA_BASE, "Dim_Partidos.csv")

ruta_salida = os.path.join(CARPETA_BASE, "Lista_Links_Restantes.csv")



def generar_links_restantes():

    print("--- 🔍 BUSCANDO LOS 528 ENLACES RESTANTES ---")

    

    # 1. Unimos de nuevo los CSVs manuales que bajaste ayer de la consola

    archivos_csv = glob.glob(os.path.join(carpeta_enlaces, "*.csv"))

    lista_dfs = [pd.read_csv(archivo) for archivo in archivos_csv]

    df_todos_los_links = pd.concat(lista_dfs, ignore_index=True).drop_duplicates(subset=['Fecha'])

    

    # 2. Leer la Dim_Partidos y filtrar SOLO los que SÍ tienen ID_StatsBomb

    dim_partidos = pd.read_csv(ruta_dim_partidos)

    partidos_restantes = dim_partidos[dim_partidos['ID_StatsBomb'].notna()][['ID_Partido', 'Fecha', 'Temporada', 'Rival']].copy()

    

    # 3. Cruzar para coger su URL

    lista_final = pd.merge(partidos_restantes, df_todos_los_links, on='Fecha', how='left')

    encontrados = lista_final.dropna(subset=['URL_FBref'])

    

    # 4. Guardar

    encontrados.to_csv(ruta_salida, index=False)

    

    print(f"✅ ¡Lista generada! Hay {len(encontrados)} partidos listos para completar la historia.")

    print(f"📍 Guardada en: {ruta_salida}")



if __name__ == "__main__":

    generar_links_restantes()