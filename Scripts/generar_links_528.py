import pandas as pd
import os
import glob

# --- CONFIGURACIÓN DE RUTAS ---
DIR_CSV = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
# Ruta corregida apuntando directamente al repositorio maestro de enlaces extraídos
DIR_ENLACES = r"C:\Users\enson\Desktop\TFG\Enlaces FBref" 
PATH_DIM_PARTIDOS = os.path.join(DIR_CSV, "Dim_Partidos.csv")
PATH_OUTPUT = os.path.join(DIR_CSV, "Lista_Links_StatsBomb_Para_FBref.csv")

def consolidar_enlaces_statsbomb():
    """
    Consolida los archivos CSV de enlaces extraídos históricamente y realiza un 
    cruce relacional (Merge) con la dimensión maestra de partidos. Filtra 
    exclusivamente los encuentros pertenecientes a la era StatsBomb para recuperar 
    su URL correspondiente y posibilitar la descarga de sus informes en FBref.
    """
    print("--- INICIANDO CONSOLIDACIÓN DE ENLACES (ERA STATSBOMB) ---")
    
    # 1. Exploración y lectura del lote de archivos de enlaces en el directorio corregido
    archivos_csv = glob.glob(os.path.join(DIR_ENLACES, "*.csv"))
    
    if len(archivos_csv) == 0:
        print(f"Error crítico: No se ha localizado ningún archivo de enlaces en el directorio: {DIR_ENLACES}")
        return

    print(f"Info: Detectados {len(archivos_csv)} archivos históricos de temporadas. Iniciando consolidación...")
    
    # Lectura en bloque y concatenación estructural
    lista_dataframes = [pd.read_csv(archivo) for archivo in archivos_csv]
    
    # Deduplicación basada en la fecha para evitar multiplicidad en el cruce relacional (cross-join accidental)
    df_enlaces_consolidados = pd.concat(lista_dataframes, ignore_index=True).drop_duplicates(subset=['Fecha'])
    
    # 2. Lectura de la Dimensión de Partidos y filtrado de la muestra objetivo
    # Se seleccionan únicamente los registros que poseen un ID válido en StatsBomb
    df_dim_partidos = pd.read_csv(PATH_DIM_PARTIDOS)
    df_partidos_statsbomb = df_dim_partidos[df_dim_partidos['ID_StatsBomb'].notna()][['ID_Partido', 'Fecha', 'Temporada', 'Rival']].copy()
    
    # 3. Cruce relacional (Left Join) para la inyección de la URL de FBref
    # La fecha actúa como clave natural de cruce entre ambos modelos de datos
    df_cruce_final = pd.merge(df_partidos_statsbomb, df_enlaces_consolidados, on='Fecha', how='left')
    
    # Purga de registros huérfanos (partidos sin URL asociada en el catálogo histórico)
    df_enlaces_validados = df_cruce_final.dropna(subset=['URL_FBref'])
    
    # 4. Exportación del modelo resultante con codificación segura
    df_enlaces_validados.to_csv(PATH_OUTPUT, index=False, encoding='utf-8-sig')
    
    print(f"Proceso finalizado exitosamente. Catálogo generado con {len(df_enlaces_validados)} enlaces validados.")
    print(f"Ruta de persistencia: {PATH_OUTPUT}")

if __name__ == "__main__":
    consolidar_enlaces_statsbomb()