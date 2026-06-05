from statsbombpy import sb
import pandas as pd
import os
import time
import warnings

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
DIR_CSV = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_OUTPUT_MASTER = os.path.join(DIR_CSV, "Catalogo_Partidos_StatsBomb.csv")
TARGET_TEAM = "Barcelona"

# Identificadores de las competiciones objetivo en la API de StatsBomb
COMPETICIONES_OBJETIVO = {
    11: "La Liga",
    16: "Champions League",
    37: "Copa del Rey"
}

def extraer_catalogo_maestro_statsbomb():
    """
    Motor de ingesta de metadatos. Consulta el endpoint global de competiciones 
    de StatsBomb Open Data, itera sobre los torneos objetivo e ingiere los registros
    estructurados de todos los encuentros donde participa el equipo objetivo.
    """
    print("--- INICIANDO EXTRACCIÓN MASIVA DEL CATÁLOGO DE PARTIDOS (STATSBOMB) ---")
    
    coleccion_partidos_historicos = []
    total_registros_extraidos = 0

    # 1. Recuperación del índice global de competiciones y temporadas disponibles
    print("Info: Consultando el catálogo general de la API de StatsBomb...")
    try:
        df_competiciones = sb.competitions()
    except Exception as e:
        print(f"Error crítico de conexión con la API: {e}")
        return

    # 2. Iteración secuencial sobre el subconjunto de competiciones de interés
    for id_competicion, nombre_competicion in COMPETICIONES_OBJETIVO.items():
        print(f"\nProcesando dominio analítico: {nombre_competicion}")
        
        # Aislamiento de las temporadas disponibles para la competición actual
        df_temporadas = df_competiciones[df_competiciones['competition_id'] == id_competicion]
        
        if df_temporadas.empty:
            print(f"Aviso: Ausencia de registros Open Data para {nombre_competicion}.")
            continue

        # Recorrido cronológico de las temporadas registradas
        for index, row in df_temporadas.iterrows():
            id_temporada = row['season_id']
            nombre_temporada = row['season_name']
            
            try:
                print(f"[{nombre_competicion}] Extrayendo metadatos de la temporada {nombre_temporada}...", end=" ")
                
                # Petición a la API para recuperar el volumen total de partidos del año
                df_partidos = sb.matches(competition_id=id_competicion, season_id=id_temporada)
                
                # Evaluación dinámica de nomenclatura de columnas
                # Justificación: El esquema de StatsBomb presenta variaciones nominales dependiendo 
                # de la versión del dataset (ej. 'home_team' vs 'home_team_name').
                col_local = 'home_team' if 'home_team' in df_partidos.columns else 'home_team_name'
                col_visitante = 'away_team' if 'away_team' in df_partidos.columns else 'away_team_name'

                # Filtrado de la tabla de hechos: Conservación exclusiva de registros del equipo objetivo
                df_partidos_equipo = df_partidos[
                    (df_partidos[col_local] == TARGET_TEAM) | 
                    (df_partidos[col_visitante] == TARGET_TEAM)
                ].copy() # Uso de .copy() para prevenir SettingWithCopyWarning en memoria
                
                if not df_partidos_equipo.empty:
                    # Inyección del nombre de la competición para trazabilidad dimensional
                    df_partidos_equipo['competicion_nombre'] = nombre_competicion
                    
                    coleccion_partidos_historicos.append(df_partidos_equipo)
                    volumen_parcial = len(df_partidos_equipo)
                    total_registros_extraidos += volumen_parcial
                    print(f"Completado ({volumen_parcial} registros)")
                else:
                    print("Aviso: Equipo objetivo no detectado en la muestra de datos.")
                    
                # Estrategia de Control de Tasa (Rate Limiting)
                # Retardo introducido deliberadamente para prevenir bloqueos por exceso de peticiones a la API
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error durante el procesamiento de la temporada {nombre_temporada}: {e}")

    # 3. Consolidación del modelo relacional y persistencia
    print("\n" + "="*60)
    if coleccion_partidos_historicos:
        print("Consolidando el Dataframe maestro...")
        df_maestro_final = pd.concat(coleccion_partidos_historicos, ignore_index=True)
        
        # Verificación del directorio de salida local
        os.makedirs(DIR_CSV, exist_ok=True)
        
        df_maestro_final.to_csv(PATH_OUTPUT_MASTER, index=False, encoding='utf-8-sig')
        
        print(f"PROCESO FINALIZADO EXITOSAMENTE.")
        print(f"Ruta de persistencia: {PATH_OUTPUT_MASTER}")
        print(f"Volumen total de encuentros consolidados: {len(df_maestro_final)}")
        print("="*60)
        print("Nota de Integración: Debido a los límites de disponibilidad del catálogo Open Data de StatsBomb,")
        print("el volumen restante (ej. ediciones recientes de UCL) se integrará mediante Web Scraping (FBref).")
    else:
        print("Alerta: El proceso ha concluido sin datos. Se recomienda verificar los filtros o la conectividad de red.")

if __name__ == "__main__":
    # Supresión de avisos de sistema en la consola para una lectura limpia de los logs
    warnings.filterwarnings("ignore")
    extraer_catalogo_maestro_statsbomb()