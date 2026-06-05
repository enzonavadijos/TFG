import os
import pandas as pd
from statsbombpy import sb
import warnings

# --- CONFIGURACIÓN DE PARÁMETROS Y RUTAS ---
DIR_SALIDA = r"C:\Users\enson\Desktop\TFG\ETL"
NOMBRE_ARCHIVO_SALIDA = "DatosLaLiga2003_2021.csv"
RUTA_COMPLETA = os.path.join(DIR_SALIDA, NOMBRE_ARCHIVO_SALIDA)

# Configuración del dominio de extracción temporal y contextual
ID_LIGA = 11  # Identificador interno de La Liga en la API de StatsBomb
ANIO_INICIO = 2003
ANIO_FIN = 2021

def extraer_catalogo_partidos_statsbomb():
    """
    Consume la API de StatsBomb para obtener el catálogo de competiciones,
    filtra las temporadas de La Liga según un rango cronológico predefinido,
    y descarga los metadatos de todos los partidos disputados en ese periodo.
    """
    print("--- INICIANDO EXTRACCIÓN DEL CATÁLOGO DE PARTIDOS (STATSBOMB API) ---")
    
    # 1. Verificación y creación del directorio de almacenamiento local
    if not os.path.exists(DIR_SALIDA):
        print(f"Info: Creando directorio de salida en {DIR_SALIDA}")
        os.makedirs(DIR_SALIDA)

    # 2. Obtención del catálogo global de competiciones disponibles
    print("Info: Consultando el índice de competiciones en StatsBomb Open Data...")
    df_competiciones = sb.competitions()
    
    # Filtrado estructural para aislar los registros pertenecientes a La Liga
    df_laliga = df_competiciones[df_competiciones['competition_id'] == ID_LIGA]
    
    if df_laliga.empty:
        print(f"Error crítico: No se han localizado registros para la competición con ID {ID_LIGA}.")
        return

    # 3. Filtrado cronológico de temporadas
    temporadas_objetivo = []
    
    for index, row in df_laliga.iterrows():
        nombre_temporada = row['season_name'] # Formato esperado: "YYYY/YYYY"
        id_temporada = row['season_id']
        
        try:
            # Parseo de la cadena de texto para extraer los años de inicio y fin
            anio_inicio_temp = int(nombre_temporada.split('/')[0])
            anio_fin_temp = int(nombre_temporada.split('/')[1])
            
            # Evaluación de la condición de contorno temporal
            if anio_inicio_temp >= ANIO_INICIO and anio_fin_temp <= ANIO_FIN:
                temporadas_objetivo.append((id_temporada, nombre_temporada))
                
        except ValueError:
            # Omisión de registros con formatos de fecha anómalos
            continue

    # Ordenamiento cronológico ascendente basado en el nombre de la temporada
    temporadas_objetivo.sort(key=lambda x: x[1])

    print(f"Info: Identificadas {len(temporadas_objetivo)} temporadas válidas en el rango {ANIO_INICIO}-{ANIO_FIN}.")

    # 4. Descarga iterativa de metadatos de partidos por temporada
    lista_partidos = []
    
    for id_temporada, nombre_temporada in temporadas_objetivo:
        print(f"Extrayendo metadatos de partidos para la temporada {nombre_temporada}...")
        
        try:
            # Petición a la API para recuperar los encuentros de la temporada específica
            df_matches = sb.matches(competition_id=ID_LIGA, season_id=id_temporada)
            
            # Inserción de la variable temporal 'season' si no está presente en el esquema original
            if 'season' not in df_matches.columns:
                df_matches['season'] = nombre_temporada
                
            lista_partidos.append(df_matches)
            
        except Exception as e:
            print(f"Error de conexión o extracción durante la temporada {nombre_temporada}: {e}")

    # 5. Consolidación y exportación del conjunto de datos
    if lista_partidos:
        print("Consolidando DataFrames temporales...")
        df_maestro_partidos = pd.concat(lista_partidos, ignore_index=True)
        
        df_maestro_partidos.to_csv(RUTA_COMPLETA, index=False)
        
        print("Operación completada exitosamente.")
        print(f"Total de registros (partidos) exportados: {len(df_maestro_partidos)}")
        print(f"Archivo persistido en: {RUTA_COMPLETA}")
    else:
        print("Aviso: El conjunto de datos resultante está vacío. Revise la conexión o los parámetros de filtrado.")

if __name__ == "__main__":
    # Supresión de advertencias no críticas relativas a credenciales de la API Open Data
    warnings.filterwarnings("ignore")
    extraer_catalogo_partidos_statsbomb()