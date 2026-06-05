import pandas as pd
import os
import re
from io import StringIO

# --- CONFIGURACIÓN DE RUTAS ---
DIR_ENTRADA = r"C:\Users\enson\Desktop\TFG\HTML_LaLiga"
PATH_OUTPUT = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga\scores_and_fixtures_laliga.csv"

def inferir_temporada(nombre_archivo):
    """
    Aplica Expresiones Regulares (Regex) sobre la nomenclatura del documento 
    para extraer el identificador cronológico (ej. '2010-2011').
    """
    coincidencia = re.search(r'(\d{4}-\d{4})', nombre_archivo)
    if coincidencia:
        return coincidencia.group(1)
    return "Desconocida"

def normalizar_columnas_dataframe(df):
    """
    Estandariza el esquema de atributos del DataFrame. Aplica un aplanamiento 
    a las estructuras MultiIndex jerárquicas y formatea la sintaxis a 'snake_case'.
    """
    if isinstance(df.columns, pd.MultiIndex):
        nuevas_columnas = []
        for col in df.columns.values:
            # Resolución de jerarquía: Prioriza el subnivel descriptivo (nivel 1)
            if str(col[1]).strip() != "" and "Unnamed" not in str(col[1]):
                nuevas_columnas.append(str(col[1]))
            else:
                nuevas_columnas.append(str(col[0]))
        df.columns = nuevas_columnas
    
    # Normalización sintáctica
    df.columns = [str(c).lower().strip().replace(" ", "_").replace("/", "_") for c in df.columns]
    return df

def parsear_tabla_resultados(ruta_archivo):
    """
    Parsea el documento HTML en memoria y localiza heurísticamente la tabla 
    de calendario y resultados. Realiza la limpieza de registros nulos y la 
    imputación de métricas avanzadas ausentes en temporadas históricas.
    """
    nombre_archivo = os.path.basename(ruta_archivo)
    temporada = inferir_temporada(nombre_archivo)
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Ingesta mediante StringIO para optimizar el consumo de memoria
        dataframes_html = pd.read_html(StringIO(html_content))
        df_resultados = None
        
        # --- TIPOLOGIZACIÓN HEURÍSTICA DE LA TABLA ---
        for df in dataframes_html:
            df_temporal = normalizar_columnas_dataframe(df.copy())
            firma_columnas = " ".join(df_temporal.columns)
            
            # Criterio de validación: Presencia de entidades de partido excluyendo métricas individuales
            if "date" in firma_columnas and "opponent" in firma_columnas and "result" in firma_columnas and "player" not in firma_columnas:
                df_resultados = df
                break
        
        if df_resultados is None:
            return None

        # --- TRANSFORMACIÓN Y LIMPIEZA ESTRUCTURAL ---
        df_norm = normalizar_columnas_dataframe(df_resultados)
        
        # Mapeo dinámico de dimensiones y métricas
        mapa_columnas = {
            'date': next((c for c in df_norm.columns if 'date' in c), 'date'),
            'round': next((c for c in df_norm.columns if 'round' in c), 'round'),
            'opponent': next((c for c in df_norm.columns if 'opponent' in c), 'opponent'),
            'result': next((c for c in df_norm.columns if 'result' in c), 'result'),
            'gf': next((c for c in df_norm.columns if 'gf' in c), 'gf'),
            'ga': next((c for c in df_norm.columns if 'ga' in c), 'ga'),
            'venue': next((c for c in df_norm.columns if 'venue' in c), 'venue'),
            'xg_favor': next((c for c in df_norm.columns if 'xg' in c and 'expected' in c and 'allow' not in c), 'xg_favor'),
            'xg_contra': next((c for c in df_norm.columns if 'xga' in c), 'xg_contra'),
            'poss': next((c for c in df_norm.columns if 'poss' in c), 'poss')
        }
        
        # Depuración de registros nulos y encabezados intercalados
        df_norm = df_norm[df_norm[mapa_columnas['date']].notna()]
        df_norm = df_norm[df_norm[mapa_columnas['date']] != 'Date']
        df_norm = df_norm[df_norm[mapa_columnas['result']].notna()] # Omisión de partidos no disputados
        
        # Inyección de contexto dimensional
        df_norm['season'] = temporada
        df_norm['competition'] = 'La Liga'
        
        # Estandarización del esquema final
        df_norm = df_norm.rename(columns={
            mapa_columnas['xg_favor']: 'xg_favor',
            mapa_columnas['xg_contra']: 'xg_contra',
            mapa_columnas['poss']: 'posesion'
        })
        
        # Imputación de variables históricas: Asignación de 0 a métricas avanzadas
        # inexistentes en las fuentes de datos de las temporadas más antiguas.
        if 'xg_favor' not in df_norm.columns: df_norm['xg_favor'] = 0
        if 'xg_contra' not in df_norm.columns: df_norm['xg_contra'] = 0
        if 'posesion' not in df_norm.columns: df_norm['posesion'] = 0
            
        return df_norm

    except Exception as e:
        print(f"Error crítico durante el parseo de {nombre_archivo}: {e}")
        return None

def ejecutar_etl_laliga_resultados():
    """
    Orquesta el flujo ETL para consolidar los resultados históricos de LaLiga.
    Aplica una deduplicación final basada en una clave primaria compuesta para 
    garantizar la integridad referencial del conjunto de datos resultante.
    """
    print("--- INICIANDO CONSOLIDACIÓN ESTRUCTURAL (LALIGA - SCORES & FIXTURES) ---")
    
    if not os.path.exists(DIR_ENTRADA):
        print(f"Error de origen: Directorio inexistente en {DIR_ENTRADA}")
        return
    
    # Aprovisionamiento del directorio de persistencia
    os.makedirs(os.path.dirname(PATH_OUTPUT), exist_ok=True)

    archivos_objetivo = [f for f in os.listdir(DIR_ENTRADA) if f.endswith(".html")]
    print(f"Info: Procesando un lote de {len(archivos_objetivo)} documentos HTML...")
    
    coleccion_dataframes = []
    for archivo in archivos_objetivo:
        df_procesado = parsear_tabla_resultados(os.path.join(DIR_ENTRADA, archivo))
        if df_procesado is not None:
            coleccion_dataframes.append(df_procesado)
            print(f"Completado: {archivo}")
    
    if coleccion_dataframes:
        # 1. Integración de la tabla de hechos
        df_consolidado = pd.concat(coleccion_dataframes, ignore_index=True)
        
        # 2. Coerción de tipos: Formateo de fechas para ordenamiento cronológico estricto
        if 'date' in df_consolidado.columns:
            df_consolidado['date'] = pd.to_datetime(df_consolidado['date'], errors='coerce')
        
        print(f"\nInfo: Volumen bruto de registros extraídos: {len(df_consolidado)}")
        
        # 3. Deduplicación Estructural mediante Clave Compuesta (Composite Key)
        # La tupla (Fecha, Rival, Temporada) actúa como identificador único natural del partido.
        df_consolidado = df_consolidado.drop_duplicates(subset=['date', 'opponent', 'season'], keep='first')
        
        # 4. Ordenamiento absoluto
        df_consolidado = df_consolidado.sort_values('date')
        
        # 5. Persistencia del modelo
        df_consolidado.to_csv(PATH_OUTPUT, index=False, encoding='utf-8-sig')
        print(f"\nProceso finalizado exitosamente. Tabla de hechos consolidada en: \n -> {PATH_OUTPUT}")
        print(f"Volumen neto tras deduplicación: {len(df_consolidado)} registros únicos.")
    else:
        print("Aviso: Ejecución abortada. No se han detectado datos de resultados en la muestra.")

if __name__ == "__main__":
    ejecutar_etl_laliga_resultados()