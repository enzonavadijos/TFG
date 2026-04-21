import pandas as pd
import os
import glob

# --- RUTAS CORREGIDAS ---
CARPETA_CSV = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
carpeta_enlaces = r"C:\Users\enson\Desktop\TFG\Enlaces FBref" # <-- ¡AQUÍ ESTABA EL FALLO!
ruta_dim_partidos = os.path.join(CARPETA_CSV, "Dim_Partidos.csv")
ruta_salida = os.path.join(CARPETA_CSV, "Lista_Links_StatsBomb_Para_FBref.csv")

def generar_links_528():
    print("--- 🔍 BUSCANDO LOS ENLACES DE LA ERA STATSBOMB ---")
    
    # 1. Leemos el historial de links en tu ruta exacta
    archivos_csv = glob.glob(os.path.join(carpeta_enlaces, "*.csv"))
    
    if len(archivos_csv) == 0:
        print(f"❌ ¡ALERTA! Sigo sin encontrar los archivos en {carpeta_enlaces}")
        return

    print(f"✅ Encontrados {len(archivos_csv)} archivos de temporadas. Uniendo...")
    
    lista_dfs = [pd.read_csv(archivo) for archivo in archivos_csv]
    df_todos_los_links = pd.concat(lista_dfs, ignore_index=True).drop_duplicates(subset=['Fecha'])
    
    # 2. Leer la Dim_Partidos y filtrar los de StatsBomb
    dim_partidos = pd.read_csv(ruta_dim_partidos)
    partidos_statsbomb = dim_partidos[dim_partidos['ID_StatsBomb'].notna()][['ID_Partido', 'Fecha', 'Temporada', 'Rival']].copy()
    
    # 3. Cruzar para coger su URL oculta
    lista_final = pd.merge(partidos_statsbomb, df_todos_los_links, on='Fecha', how='left')
    encontrados = lista_final.dropna(subset=['URL_FBref'])
    
    # 4. Guardar
    encontrados.to_csv(ruta_salida, index=False)
    
    print(f"🎉 ¡Lista generada! Hay {len(encontrados)} partidos listos para descargar.")
    print(f"📍 Guardada en: {ruta_salida}")

if __name__ == "__main__":
    generar_links_528()