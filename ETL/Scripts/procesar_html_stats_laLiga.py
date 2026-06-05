import pandas as pd
import os
import re
from io import StringIO

# --- CONFIGURACIÓN DE RUTAS ---
DIR_ENTRADA = r"C:\Users\enson\Desktop\TFG\HTML_LaLiga"
PATH_OUTPUT = r"C:\Users\enson\Desktop\TFG\ETL\stats_laliga.csv"

def inferir_temporada(nombre_archivo):
    """
    Extrae el identificador temporal de la nomenclatura del archivo mediante Expresiones Regulares.
    """
    coincidencia = re.search(r'(\d{4}-\d{4})', nombre_archivo)
    if coincidencia:
        return coincidencia.group(1)
    return "Desconocida"

def preprocesar_html_comentarios(contenido_html):
    """
    Elimina los bloques de comentarios HTML para exponer las estructuras tabulares 
    secundarias inyectadas estáticamente en el código fuente.
    """
    return contenido_html.replace("<!--", "").replace("-->", "")

def aplanar_esquema_columnas(df):
    """
    Reduce la dimensionalidad jerárquica (MultiIndex) de las cabeceras a un vector plano.
    Estandariza la nomenclatura aplicando convención 'snake_case'.
    """
    nuevas_columnas = []
    if isinstance(df.columns, pd.MultiIndex):
        for col in df.columns.values:
            nivel_superior = str(col[0])
            nivel_inferior = str(col[1])
            
            # Resolución de nombres: Omisión de niveles sin etiqueta explícita
            if "Unnamed" in nivel_superior:
                nombre_limpio = nivel_inferior
            else:
                nombre_limpio = f"{nivel_superior}_{nivel_inferior}"
            nuevas_columnas.append(nombre_limpio)
    else:
        nuevas_columnas = [str(c) for c in df.columns]

    return [c.lower().strip().replace(" ", "_").replace("/", "_") for c in nuevas_columnas]

def extraer_metricas_individuales_laliga(ruta_archivo):
    """
    Motor de parseo y transformación para las estadísticas individuales (Standard Stats).
    Identifica heurísticamente la tabla objetivo, filtra agregaciones (Totales) y 
    aísla métricas absolutas (excluyendo normalizaciones como 'per 90 minutes').
    """
    nombre_archivo = os.path.basename(ruta_archivo)
    temporada = inferir_temporada(nombre_archivo)
    
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            html_crudo = f.read()
        
        # 1. Preprocesamiento e Ingesta
        html_limpio = preprocesar_html_comentarios(html_crudo)
        dataframes_html = pd.read_html(StringIO(html_limpio))
        
        df_objetivo = None
        
        # 2. Tipificación Heurística de la Tabla
        for df in dataframes_html:
            columnas_temporales = aplanar_esquema_columnas(df)
            
            # Criterio Primario: Presencia de Jugador, Partidos Jugados y Goles Absolutos (no /90)
            if any('player' == c for c in columnas_temporales) and any('mp' == c for c in columnas_temporales):
                 if any('gls' in c and '90' not in c for c in columnas_temporales):
                    df_objetivo = df
                    df_objetivo.columns = columnas_temporales
                    break
        
        if df_objetivo is None:
            # Criterio Secundario (Fallback histórico): Presencia de Jugador y Minutos
            for df in dataframes_html:
                columnas_temporales = aplanar_esquema_columnas(df)
                if any('player' == c for c in columnas_temporales) and any('min' in c for c in columnas_temporales):
                    df_objetivo = df
                    df_objetivo.columns = columnas_temporales
                    break

        if df_objetivo is None:
            return None

        # 3. Limpieza Estructural (Prevención de Index Misalignment)
        df_procesado = df_objetivo.copy()
        columna_jugador = 'player'
        
        # Depuración de registros pre-extracción
        df_procesado = df_procesado[df_procesado[columna_jugador].notna()]
        df_procesado = df_procesado[df_procesado[columna_jugador] != 'player']
        df_procesado = df_procesado[~df_procesado[columna_jugador].astype(str).str.lower().str.contains("total")]
        df_procesado = df_procesado[~df_procesado[columna_jugador].astype(str).str.lower().str.contains("opponent")]
        
        # 4. Construcción del Modelo Analítico Limpio
        df_limpio = pd.DataFrame()
        df_limpio['season'] = [temporada] * len(df_procesado)
        df_limpio['player'] = df_procesado[columna_jugador].values
        
        def extraer_datos_seguro(palabras_clave):
            """Función auxiliar para extracción tolerante a fallos mediante coincidencia parcial."""
            for kw in palabras_clave:
                coincidencia = next((c for c in df_procesado.columns if kw in c), None)
                if coincidencia:
                    return df_procesado[coincidencia].values
            return 0

        # Inyección de atributos demográficos y posicionales
        df_limpio['nation'] = extraer_datos_seguro(['nation'])
        df_limpio['pos'] = extraer_datos_seguro(['pos'])
        df_limpio['age'] = extraer_datos_seguro(['age'])
        
        # Inyección de métricas de participación
        df_limpio['mp'] = extraer_datos_seguro(['mp', 'matches'])
        df_limpio['starts'] = extraer_datos_seguro(['starts'])
        df_limpio['min'] = extraer_datos_seguro(['min', 'minutes'])
        
        # Inyección de métricas de rendimiento (Filtro explícito anti 'per 90')
        columna_goles = next((c for c in df_procesado.columns if ('gls' in c or 'goals' in c) and '90' not in c), None)
        df_limpio['goals'] = df_procesado[columna_goles].values if columna_goles else 0
        
        columna_asistencias = next((c for c in df_procesado.columns if ('ast' in c or 'assists' in c) and '90' not in c), None)
        df_limpio['assists'] = df_procesado[columna_asistencias].values if columna_asistencias else 0

        # 5. Coerción de Tipos (Type Casting)
        columnas_numericas = ['mp', 'starts', 'min', 'goals', 'assists']
        for col in columnas_numericas:
            df_limpio[col] = pd.to_numeric(df_limpio[col], errors='coerce').fillna(0).astype(int)

        return df_limpio

    except Exception as e:
        # Silenciado intencionalmente para evitar ruido en la consola por archivos incompatibles
        return None

def ejecutar_etl_stats_laliga():
    """
    Orquesta el flujo de extracción y normalización de estadísticas individuales
    para los encuentros de LaLiga. Consolida un modelo tabular único.
    """
    print("--- INICIANDO CONSOLIDACIÓN DE ESTADÍSTICAS INDIVIDUALES (LALIGA) ---")
    
    if not os.path.exists(DIR_ENTRADA):
        print(f"Error de origen: Directorio no localizado en {DIR_ENTRADA}")
        return

    archivos_objetivo = [f for f in os.listdir(DIR_ENTRADA) if f.endswith(".html")]
    coleccion_dataframes = []
    
    print(f"Info: Procesando lote de {len(archivos_objetivo)} documentos HTML...")
    
    for archivo in archivos_objetivo:
        ruta_completa = os.path.join(DIR_ENTRADA, archivo)
        df_procesado = extraer_metricas_individuales_laliga(ruta_completa)
        
        if df_procesado is not None and not df_procesado.empty:
            coleccion_dataframes.append(df_procesado)
            print(f"Completado: {archivo} ({len(df_procesado)} entidades analizadas).")

    # Integración global de la tabla de hechos
    if coleccion_dataframes:
        df_consolidado_final = pd.concat(coleccion_dataframes, ignore_index=True)
        
        # Ordenamiento jerárquico: Cronológico y por rendimiento relativo (Goles descendente)
        df_consolidado_final = df_consolidado_final.sort_values(['season', 'goals'], ascending=[True, False])
        
        os.makedirs(os.path.dirname(PATH_OUTPUT), exist_ok=True)
        df_consolidado_final.to_csv(PATH_OUTPUT, index=False, encoding='utf-8-sig')
        
        print("\nProceso ETL finalizado exitosamente.")
        print(f"Dataset maestro exportado a: {PATH_OUTPUT}")
        print(f"Volumen de registros individuales consolidados: {len(df_consolidado_final)}")
    else:
        print("Aviso: Ejecución abortada. Ausencia de datos estadísticos estructurados.")

if __name__ == "__main__":
    ejecutar_etl_stats_laliga()