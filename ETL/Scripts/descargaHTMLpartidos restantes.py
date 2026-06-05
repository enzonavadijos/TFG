import pandas as pd
import os
import glob

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
DIR_ENLACES = os.path.join(BASE_DIR, "Enlaces FBref")
PATH_DIM_PARTIDOS = os.path.join(BASE_DIR, "Dim_Partidos.csv")
PATH_OUTPUT = os.path.join(BASE_DIR, "Lista_Links_Restantes.csv")

def generar_enlaces_restantes():
    """
    Consolida los archivos de enlaces extraídos previamente y realiza un cruce relacional 
    con la dimensión de partidos. Filtra exclusivamente aquellos encuentros 
    que poseen un identificador válido en StatsBomb para completar el dataset.
    """
    print("--- INICIANDO IDENTIFICACIÓN DE ENLACES RESTANTES ---")
    
    # 1. Exploración y consolidación de los archivos CSV locales
    archivos_csv = glob.glob(os.path.join(DIR_ENLACES, "*.csv"))
    
    if not archivos_csv:
        print(f"Error: No se ha encontrado ningún archivo CSV en la ruta: {DIR_ENLACES}")
        return
        
    lista_dataframes = [pd.read_csv(archivo) for archivo in archivos_csv]
    
    # Concatenación estructural y deduplicación basada en la fecha del encuentro
    df_enlaces_consolidados = pd.concat(lista_dataframes, ignore_index=True).drop_duplicates(subset=['Fecha'])
    
    # 2. Lectura de la tabla dimensional y filtrado condicional
    # Se seleccionan únicamente los registros que cuentan con ID válido de StatsBomb
    df_dim_partidos = pd.read_csv(PATH_DIM_PARTIDOS)
    df_partidos_objetivo = df_dim_partidos[df_dim_partidos['ID_StatsBomb'].notna()][['ID_Partido', 'Fecha', 'Temporada', 'Rival']].copy()
    
    # 3. Cruce relacional (Left Merge) para asignar la URL correspondiente a cada partido
    df_resultado = pd.merge(df_partidos_objetivo, df_enlaces_consolidados, on='Fecha', how='left')
    
    # Depuración de registros sin correspondencia de URL en el conjunto consolidado
    df_encontrados = df_resultado.dropna(subset=['URL_FBref'])
    
    # 4. Exportación del subconjunto resultante
    df_encontrados.to_csv(PATH_OUTPUT, index=False)
    
    print(f"Operación completada: Se han identificado y consolidado {len(df_encontrados)} enlaces válidos para su posterior extracción.")
    print(f"Archivo exportado en: {PATH_OUTPUT}")

if __name__ == "__main__":
    generar_enlaces_restantes()