import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_CALENDARIO = os.path.join(BASE_DIR, "LaLiga", "scores_and_fixtures_laliga.csv")
PATH_TACTICAS = os.path.join(BASE_DIR, "Fact_Tacticas_Oficiales_SB.csv")
PATH_OUTPUT = os.path.join(BASE_DIR, "Dim_Partidos.csv")

def generar_dimension_partidos():
    """
    Construye la dimensión central de partidos, consolidando calendarios, 
    limpiando cadenas de texto mediante expresiones regulares (separación de 
    penaltis y códigos de país) y asignando identificadores únicos y foráneos.
    """
    print("--- INICIANDO CONSTRUCCIÓN DE LA DIMENSIÓN DE PARTIDOS ---")
    
    # 1. Carga del calendario maestro y filtrado inicial de registros inválidos
    try:
        df_calendario = pd.read_csv(PATH_CALENDARIO)
    except FileNotFoundError:
        print(f"Error crítico: No se encuentra el archivo en la ruta especificada: {PATH_CALENDARIO}")
        return
        
    df_calendario = df_calendario.dropna(subset=['date', 'opponent']).copy()
    
    # Estandarización de la columna de competición, priorizando 'comp' sobre 'competition'
    if 'comp' in df_calendario.columns:
        df_calendario['competicion_real'] = df_calendario['comp'].fillna(df_calendario['competition'])
    else:
        df_calendario['competicion_real'] = df_calendario['competition']

    # 2. Selección de columnas estructurales y normalización de cabeceras
    df_dim_partidos = df_calendario[['date', 'season', 'competicion_real', 'opponent', 'venue', 'result', 'gf', 'ga']].copy()
    df_dim_partidos.rename(columns={
        'date': 'Fecha',
        'season': 'Temporada',
        'competicion_real': 'Competicion',
        'opponent': 'Rival',
        'venue': 'Localia',
        'result': 'Resultado',
        'gf': 'Goles_Barca',
        'ga': 'Goles_Rival'
    }, inplace=True)
    
    # 3. Limpieza de las nomenclaturas de equipos rivales
    print("Info: Normalizando nombres de equipos rivales mediante expresiones regulares...")
    # Eliminación de espacios periféricos
    df_dim_partidos['Rival'] = df_dim_partidos['Rival'].str.strip()
    # Mediante Regex, se detectan y eliminan los prefijos de país en minúsculas (ej. 'es ', 'eng ') insertados por la fuente
    df_dim_partidos['Rival'] = df_dim_partidos['Rival'].str.replace(r'^[a-z]{2,3}\s', '', regex=True)

    # Ordenamiento cronológico y deduplicación para asegurar la integridad de la entidad "Partido"
    df_dim_partidos = df_dim_partidos.drop_duplicates(subset=['Fecha', 'Rival'])
    df_dim_partidos = df_dim_partidos.sort_values(by='Fecha').reset_index(drop=True)
    
    # 4. Extracción de métricas anidadas (Goles vs Penaltis)
    print("Info: Segmentando registros de goles y tandas de penaltis...")
    # Extracción de valores numéricos contenidos entre paréntesis (representan los penaltis)
    df_dim_partidos['Penaltis_Barca'] = df_dim_partidos['Goles_Barca'].astype(str).str.extract(r'\((\d+)\)', expand=False)
    df_dim_partidos['Penaltis_Rival'] = df_dim_partidos['Goles_Rival'].astype(str).str.extract(r'\((\d+)\)', expand=False)
    
    # Extracción del primer conjunto numérico de la cadena (representa los goles en tiempo reglamentario)
    df_dim_partidos['Goles_Barca_Real'] = df_dim_partidos['Goles_Barca'].astype(str).str.extract(r'^(\d+)', expand=False)
    df_dim_partidos['Goles_Rival_Real'] = df_dim_partidos['Goles_Rival'].astype(str).str.extract(r'^(\d+)', expand=False)

    # Conversión al formato Int64 nativo de Pandas (soporta valores enteros y nulos simultáneamente)
    df_dim_partidos['Goles_Barca'] = pd.to_numeric(df_dim_partidos['Goles_Barca_Real'], errors='coerce').astype('Int64')
    df_dim_partidos['Goles_Rival'] = pd.to_numeric(df_dim_partidos['Goles_Rival_Real'], errors='coerce').astype('Int64')
    df_dim_partidos['Penaltis_Barca'] = pd.to_numeric(df_dim_partidos['Penaltis_Barca'], errors='coerce').astype('Int64')
    df_dim_partidos['Penaltis_Rival'] = pd.to_numeric(df_dim_partidos['Penaltis_Rival'], errors='coerce').astype('Int64')

    # Eliminación de columnas temporales de procesamiento
    df_dim_partidos = df_dim_partidos.drop(columns=['Goles_Barca_Real', 'Goles_Rival_Real'])

    # 5. Generación de clave primaria (Primary Key) secuencial
    df_dim_partidos.insert(0, 'ID_Partido', df_dim_partidos.index + 1)
    
    # 6. Integración de claves foráneas de StatsBomb (Left Merge)
    try:
        df_statsbomb = pd.read_csv(PATH_TACTICAS)
        df_statsbomb = df_statsbomb[['fecha', 'id_partido_sb']].rename(columns={'fecha': 'Fecha', 'id_partido_sb': 'ID_StatsBomb'})
        df_dim_partidos = pd.merge(df_dim_partidos, df_statsbomb, on='Fecha', how='left')
    except Exception as e:
        print(f"Aviso: No se pudo enlazar con los identificadores de StatsBomb. Procediendo con asignación nula. Detalle: {e}")
        df_dim_partidos['ID_StatsBomb'] = None

    # 7. Reordenación final de atributos y exportación
    columnas_ordenadas = [
        'ID_Partido', 'ID_StatsBomb', 'Fecha', 'Temporada', 'Competicion', 'Rival', 'Localia', 
        'Resultado', 'Goles_Barca', 'Goles_Rival', 'Penaltis_Barca', 'Penaltis_Rival'
    ]
    df_dim_partidos = df_dim_partidos[columnas_ordenadas]

    df_dim_partidos.to_csv(PATH_OUTPUT, index=False)
    
    print("\nProceso completado: Dimensión de partidos estructurada y variables de texto normalizadas.")
    print(f"Archivo maestro exportado en: {PATH_OUTPUT}")

if __name__ == "__main__":
    generar_dimension_partidos()