import os
import time
import pandas as pd
from statsbombpy import sb

# --- CONFIGURACIÓN DEL ENTORNO DE TRABAJO ---
# Definición del directorio de destino para el particionado físico de los archivos.
# El parámetro exist_ok=True garantiza la idempotencia en la creación de la jerarquía de directorios.
DIR_EXPORTACION = r"C:\Users\Enzo\OneDrive\Escritorio\Universidad\TFG\StatsBombMessi"
os.makedirs(DIR_EXPORTACION, exist_ok=True)

print("--- INICIANDO EXTRACCIÓN DE DATOS MEDIANTE API STATSBOMB ---")

# 1. Definición del dominio analítico (Catálogo de competiciones)
# Se consulta el índice global y se aplica un filtro restrictivo para aislar la competición de interés (LaLiga, ID=11).
df_competiciones_global = sb.competitions()
df_competiciones_laliga = df_competiciones_global[df_competiciones_global['competition_id'] == 11]

# 2. Iteración sobre el horizonte temporal definido
for indice, registro_temporada in df_competiciones_laliga.iterrows():
    id_temporada = registro_temporada['season_id']
    nombre_temporada = registro_temporada['season_name']
    print(f"\nInfo: Procesando metadatos correspondientes a la temporada {nombre_temporada}")
    
    try:
        # Extracción del catálogo de encuentros para la temporada instanciada
        df_partidos_temporada = sb.matches(competition_id=11, season_id=id_temporada)
        
        # Filtrado relacional: Aislamiento de encuentros con participación del equipo objetivo
        df_partidos_objetivo = df_partidos_temporada[
            (df_partidos_temporada['home_team'] == 'Barcelona') | 
            (df_partidos_temporada['away_team'] == 'Barcelona')
        ]
        
        # 3. Descarga granular y particionamiento físico
        for id_partido in df_partidos_objetivo['match_id']:
            ruta_archivo_salida = os.path.join(DIR_EXPORTACION, f"Eventos_{id_partido}.csv")
            
            # Control de contingencia e idempotencia: 
            # Omisión de descargas redundantes para optimizar la carga de red y permitir la reanudación de ejecuciones interrumpidas.
            if os.path.exists(ruta_archivo_salida):
                continue
                
            print(f" -> Descargando registro de eventos para el identificador de partido: {id_partido}...")
            try:
                # Ingesta de telemetría atómica mediante la interfaz de statsbombpy
                df_eventos_partido = sb.events(match_id=id_partido)
                
                # Enriquecimiento del modelo de datos con variables dimensionales de contexto
                df_eventos_partido['match_id'] = id_partido
                df_eventos_partido['season_name'] = nombre_temporada
                
                # Persistencia en disco: Guardado atómico para cumplir con las restricciones de almacenamiento del repositorio.
                df_eventos_partido.to_csv(ruta_archivo_salida, index=False)
                
                # Mecanismo de control de tasa de peticiones (Rate Limiting)
                time.sleep(1.5)
                
            except Exception as excepcion_granular:
                print(f"Error técnico durante la extracción del identificador {id_partido}: {excepcion_granular}")
                time.sleep(3) # Introducción de latencia de recuperación ante intermitencias de red
                
    except Exception as excepcion_temporada:
        print(f"Error crítico en el bloque de procesamiento de la temporada {nombre_temporada}. Detalle: {excepcion_temporada}")

print("\nProceso ETL de extracción granular y particionado finalizado con éxito.")