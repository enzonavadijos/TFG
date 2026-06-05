import pandas as pd
import os
import re
from io import StringIO

# --- CONFIGURACIÓN DE RUTAS Y ARCHIVOS ---
DIR_ENTRADA = r"C:\Users\enson\Desktop\TFG\HTML_Champions"
DIR_SALIDA = r"C:\Users\enson\Desktop\TFG\ETL"

# Nomenclatura estricta para los datasets resultantes
ARCHIVO_SCORES = "scores_and_fixtures_champions.csv"
ARCHIVO_STATS = "stats_champions.csv"

def inferir_temporada(nombre_archivo):
    """
    Aplica Expresiones Regulares (Regex) sobre la nomenclatura del archivo 
    para extraer el identificador temporal (ej. '2010-2011').
    """
    coincidencia = re.search(r'(\d{4}-\d{4})', nombre_archivo)
    if coincidencia:
        return coincidencia.group(1)
    return "Desconocida"

def normalizar_columnas_dataframe(df):
    """
    Procesa las cabeceras del DataFrame. Aplica un aplanamiento (flattening) 
    a las estructuras MultiIndex jerárquicas comunes en FBref y estandariza 
    la sintaxis de las variables (minúsculas, guiones bajos).
    """
    # 1. Aplanamiento de estructuras MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        nuevas_columnas = []
        for col in df.columns.values:
            # Resolución de jerarquía: Prioriza el subnivel (nivel 1) si contiene información descriptiva
            if str(col[1]).strip() != "" and "Unnamed" not in str(col[1]):
                nuevas_columnas.append(str(col[1]))
            else:
                nuevas_columnas.append(str(col[0]))
        df.columns = nuevas_columnas

    # 2. Normalización sintáctica (Snake Case)
    df.columns = [str(c).lower().strip().replace(" ", "_").replace("/", "_") for c in df.columns]
    return df

def clasificar_y_parsear_html(ruta_archivo):
    """
    Lee el documento HTML, extrae las tablas tabulares en memoria y emplea un 
    algoritmo heurístico para clasificar su tipología ('Scores & Fixtures' vs 'Standard Stats').
    Aplica transformaciones de limpieza estructural dependiendo del dominio de datos.
    """
    nombre_archivo = os.path.basename(ruta_archivo)
    temporada = inferir_temporada(nombre_archivo)
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Ingesta mediante StringIO para optimizar memoria y evitar avisos de deprecación en Pandas
        dataframes_html = pd.read_html(StringIO(html_content))
        
        # --- CLASIFICACIÓN HEURÍSTICA DE ESTRUCTURAS TABULARES ---
        df_resultados = None
        df_estadisticas = None
        
        for df in dataframes_html:
            df_temporal = normalizar_columnas_dataframe(df.copy())
            firma_columnas = " ".join(df_temporal.columns)
            
            # CRITERIO 1: Inferencia de tabla de calendario y resultados (Scores & Fixtures)
            if "date" in firma_columnas and "opponent" in firma_columnas and "result" in firma_columnas and "player" not in firma_columnas:
                df_resultados = df 
            
            # CRITERIO 2: Inferencia de tabla de rendimiento individual (Standard Stats)
            if "player" in firma_columnas and "pos" in firma_columnas and ("mp" in firma_columnas or "matches" in firma_columnas):
                # Umbral mínimo de registros para omitir tablas residuales
                if len(df) > 5: 
                    df_estadisticas = df
        
        # --- TRANSFORMACIÓN Y CONSOLIDACIÓN ---
        diccionario_retorno = {}
        
        # 1. Pipeline para tabla de Resultados (Scores)
        if df_resultados is not None:
            df_norm = normalizar_columnas_dataframe(df_resultados)
            
            # Mapeo dinámico de atributos mediante generadores 
            mapa_columnas = {
                'date': next((c for c in df_norm.columns if 'date' in c), 'date'),
                'round': next((c for c in df_norm.columns if 'round' in c), 'round'),
                'opponent': next((c for c in df_norm.columns if 'opponent' in c), 'opponent'),
                'result': next((c for c in df_norm.columns if 'result' in c), 'result'),
                'gf': next((c for c in df_norm.columns if 'gf' in c), 'gf'),
                'ga': next((c for c in df_norm.columns if 'ga' in c), 'ga'),
                'venue': next((c for c in df_norm.columns if 'venue' in c), 'venue'),
                'xg_favor': next((c for c in df_norm.columns if 'xg' in c and 'expected' in c and 'allow' not in c), 'xg'),
                'xg_contra': next((c for c in df_norm.columns if 'xga' in c), 'xga'),
                'poss': next((c for c in df_norm.columns if 'poss' in c), 'poss')
            }
            
            # Depuración de registros nulos y filas de separación
            df_norm = df_norm[df_norm[mapa_columnas['date']].notna()]
            df_norm = df_norm[df_norm[mapa_columnas['date']] != 'Date']
            df_norm = df_norm[df_norm[mapa_columnas['result']].notna()] 
            
            # Inyección de dimensionalidad contextual
            df_norm['season'] = temporada
            df_norm['competition'] = 'Champions League'
            
            # Traducción y estandarización del esquema
            df_norm = df_norm.rename(columns={
                mapa_columnas['xg_favor']: 'xg_favor',
                mapa_columnas['xg_contra']: 'xg_contra',
                mapa_columnas['poss']: 'posesion'
            })
            
            diccionario_retorno['type'] = 'scores'
            diccionario_retorno['df'] = df_norm

        # 2. Pipeline para tabla de Estadísticas (Stats)
        elif df_estadisticas is not None:
            df_norm = normalizar_columnas_dataframe(df_estadisticas)
            
            # Aislamiento de clave primaria del jugador
            col_jugador = next((c for c in df_norm.columns if 'player' in c), 'player')
            df_norm = df_norm[df_norm[col_jugador] != 'Player']
            df_norm = df_norm[df_norm[col_jugador].notna()]
            
            # Purga de filas de agregación (Totales de equipo u oponente)
            df_norm = df_norm[~df_norm[col_jugador].astype(str).str.contains("Total", case=False)]
            
            df_norm['season'] = temporada
            df_norm['competition'] = 'Champions League'
            
            diccionario_retorno['type'] = 'stats'
            diccionario_retorno['df'] = df_norm

        return diccionario_retorno

    except Exception as e:
        print(f"Error crítico durante el procesamiento de {nombre_archivo}: {e}")
        return {}

def ejecutar_etl_champions_historico():
    """
    Orquesta la ingestión masiva de documentos HTML de la Champions League.
    Clasifica los archivos en dominios de 'Resultados' o 'Estadísticas Individuales',
    los procesa, y consolida dos tablas maestras (Fact Tables) en formato CSV.
    """
    print("--- INICIANDO CONSOLIDACIÓN ESTRUCTURAL (CHAMPIONS LEAGUE) ---")
    
    if not os.path.exists(DIR_ENTRADA):
        print(f"Error de origen: El directorio especificado no existe ({DIR_ENTRADA})")
        return
        
    os.makedirs(DIR_SALIDA, exist_ok=True)

    archivos_objetivo = [f for f in os.listdir(DIR_ENTRADA) if f.endswith(".html")]
    print(f"Info: Detectados {len(archivos_objetivo)} documentos HTML para análisis de tipología.")
    
    coleccion_resultados = []
    coleccion_estadisticas = []
    
    for archivo in archivos_objetivo:
        ruta_completa = os.path.join(DIR_ENTRADA, archivo)
        resultado_proceso = clasificar_y_parsear_html(ruta_completa)
        
        tipo_extraccion = resultado_proceso.get('type')
        if tipo_extraccion == 'scores':
            coleccion_resultados.append(resultado_proceso['df'])
            print(f"Clasificado: {archivo} -> [Tabla de Hechos: Resultados]")
        elif tipo_extraccion == 'stats':
            coleccion_estadisticas.append(resultado_proceso['df'])
            print(f"Clasificado: {archivo} -> [Tabla de Hechos: Rendimiento Individual]")
        else:
            print(f"Aviso: {archivo} -> [Tipología no identificada / Omitido]")

    # --- FASE DE CARGA (LOAD): RESULTADOS DE EQUIPO ---
    if coleccion_resultados:
        df_consolidado_scores = pd.concat(coleccion_resultados, ignore_index=True)
        
        # Coerción temporal explícita para asegurar un ordenamiento cronológico preciso
        if 'date' in df_consolidado_scores.columns:
            df_consolidado_scores['date'] = pd.to_datetime(df_consolidado_scores['date'], errors='coerce')
            df_consolidado_scores = df_consolidado_scores.sort_values('date')
            
        ruta_salida_scores = os.path.join(DIR_SALIDA, ARCHIVO_SCORES)
        df_consolidado_scores.to_csv(ruta_salida_scores, index=False, encoding='utf-8-sig')
        print(f"\nPersistencia exitosa: {ARCHIVO_SCORES} ({len(df_consolidado_scores)} registros de partido integrados).")
    
    # --- FASE DE CARGA (LOAD): ESTADÍSTICAS INDIVIDUALES ---
    if coleccion_estadisticas:
        df_consolidado_stats = pd.concat(coleccion_estadisticas, ignore_index=True)
        
        # Ordenamiento jerárquico por temporada y jugador
        df_consolidado_stats = df_consolidado_stats.sort_values(['season', 'player'])
        
        ruta_salida_stats = os.path.join(DIR_SALIDA, ARCHIVO_STATS)
        df_consolidado_stats.to_csv(ruta_salida_stats, index=False, encoding='utf-8-sig')
        print(f"Persistencia exitosa: {ARCHIVO_STATS} ({len(df_consolidado_stats)} registros individuales integrados).")

    print("\nProceso ETL completado en su totalidad.")

if __name__ == "__main__":
    ejecutar_etl_champions_historico()