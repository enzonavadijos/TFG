import pandas as pd
import os
import glob

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ENLACES_DIR = os.path.join(BASE_DIR, "Enlaces FBref")
PATH_DIM_PARTIDOS = os.path.join(BASE_DIR, "Dim_Partidos.csv")
PATH_OUTPUT = os.path.join(BASE_DIR, "Lista_Links_Faltantes_Corregida.csv")

def consolidar_enlaces_fbref():
    """
    Lee múltiples archivos CSV con enlaces de FBref, los unifica y realiza 
    un cruce relacional con la dimensión de partidos para identificar 
    aquellos registros que carecen de identificador de StatsBomb.
    """
    print("--- INICIANDO CONSOLIDACIÓN DE ENLACES DE FBREF ---")
    
    # 1. Exploración y carga de los archivos CSV locales
    archivos_csv = glob.glob(os.path.join(ENLACES_DIR, "*.csv"))
    
    if not archivos_csv:
        print(f"Error: No se ha encontrado ningún archivo CSV en la ruta: {ENLACES_DIR}")
        return
        
    print(f"Info: Se han localizado {len(archivos_csv)} archivos. Procediendo a la unificación...")
    
    lista_dataframes = []
    for archivo in archivos_csv:
        try:
            df_temporal = pd.read_csv(archivo)
            lista_dataframes.append(df_temporal)
        except Exception as e:
            print(f"Error de lectura en el archivo {os.path.basename(archivo)}: {e}")
            
    # Consolidación estructural y eliminación de registros duplicados basados en la fecha
    df_enlaces_consolidados = pd.concat(lista_dataframes, ignore_index=True)
    df_enlaces_consolidados = df_enlaces_consolidados.drop_duplicates(subset=['Fecha'])
    
    # 2. Lectura de la tabla dimensional y filtrado de registros sin ID de StatsBomb
    df_dim_partidos = pd.read_csv(PATH_DIM_PARTIDOS)
    df_partidos_faltantes = df_dim_partidos[df_dim_partidos['ID_StatsBomb'].isna()][['ID_Partido', 'Fecha', 'Temporada', 'Rival']].copy()
    
    # 3. Cruce relacional (Left Merge) utilizando la fecha como clave temporal
    df_resultado = pd.merge(df_partidos_faltantes, df_enlaces_consolidados, on='Fecha', how='left')
    
    # Separación de registros cruzados con éxito y valores nulos
    df_encontrados = df_resultado.dropna(subset=['URL_FBref'])
    df_no_encontrados = df_resultado[df_resultado['URL_FBref'].isna()]
    
    # Exportación del subconjunto consolidado
    df_encontrados.to_csv(PATH_OUTPUT, index=False)
    
    print(f"\nÉxito: Se han cruzado y unificado correctamente {len(df_encontrados)} partidos con su URL de origen.")
    
    if not df_no_encontrados.empty:
        print(f"Nota: Existen {len(df_no_encontrados)} partidos en la tabla dimensional sin correspondencia de URL (habitual en encuentros amistosos o aplazados).")
        
    print(f"Archivo exportado correctamente en: {PATH_OUTPUT}")

if __name__ == "__main__":
    consolidar_enlaces_fbref()