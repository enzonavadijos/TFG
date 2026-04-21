import pandas as pd
import os
import glob

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
carpeta_enlaces = os.path.join(CARPETA_BASE, "Enlaces FBref") # Tu carpeta exacta
ruta_dim_partidos = os.path.join(CARPETA_BASE, "Dim_Partidos.csv")
ruta_salida = os.path.join(CARPETA_BASE, "Lista_Links_Faltantes_Corregida.csv")

def unir_enlaces_fbref():
    print("--- 🧩 COSIENDO LOS ENLACES MANUALES DE FBREF ---")
    
    # 1. Leer TODOS los CSVs que has descargado a mano
    archivos_csv = glob.glob(os.path.join(carpeta_enlaces, "*.csv"))
    
    if len(archivos_csv) == 0:
        print(f"❌ Error: No he encontrado ningún CSV en {carpeta_enlaces}")
        return
        
    print(f"📥 Encontrados {len(archivos_csv)} archivos. Uniendo...")
    
    lista_dfs = []
    for archivo in archivos_csv:
        try:
            df_temp = pd.read_csv(archivo)
            lista_dfs.append(df_temp)
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
            
    # Unimos todos los enlaces en una super-tabla
    df_todos_los_links = pd.concat(lista_dfs, ignore_index=True)
    df_todos_los_links = df_todos_los_links.drop_duplicates(subset=['Fecha'])
    
    # 2. Leer tu Dim_Partidos y ver cuáles nos faltan
    dim_partidos = pd.read_csv(ruta_dim_partidos)
    partidos_huerfanos = dim_partidos[dim_partidos['ID_StatsBomb'].isna()][['ID_Partido', 'Fecha', 'Temporada', 'Rival']].copy()
    
    # 3. Cruzar los datos usando la Fecha como puente
    lista_final = pd.merge(partidos_huerfanos, df_todos_los_links, on='Fecha', how='left')
    
    encontrados = lista_final.dropna(subset=['URL_FBref'])
    faltantes = lista_final[lista_final['URL_FBref'].isna()]
    
    encontrados.to_csv(ruta_salida, index=False)
    
    print(f"\n🎉 ¡ÉXITO! Hemos casado {len(encontrados)} partidos con su enlace real.")
    if len(faltantes) > 0:
        print(f"⚠️ Nota: Hay {len(faltantes)} partidos en tu Dimensión que no cruzaron con las URLs (normal en partidos amistosos o no jugados aún).")
        
    print(f"📍 Tu lista dorada está guardada en: {ruta_salida}")

if __name__ == "__main__":
    unir_enlaces_fbref()