import os
import pandas as pd

# --- CONFIGURACIÓN DEL ENTORNO Y RUTAS ---
DIR_HTML_TEMPORADAS = r"C:\Users\enson\Desktop\TFG\ETL\HTML_Temporadas"
DIR_CSV = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_OUTPUT_GLOBAL = os.path.join(DIR_CSV, "Fact_Estadisticas_Globales.csv")

def extraer_estadisticas_globales_temporada():
    """
    Motor de Extracción, Transformación y Carga (ETL).
    Recorre recursivamente los documentos HTML estáticos de resúmenes de temporada.
    Aplica técnicas de aplanamiento de jerarquías en dataframes, mapeo heurístico 
    para la identificación de tablas, y resolución de colisiones (merges).
    Posteriormente, aplica una coerción estricta de tipos a enteros puros (Int64)
    y estandariza los esquemas de datos al castellano.
    """
    print("--- INICIANDO TRANSFORMACIÓN Y CONSOLIDACIÓN DE ESTADÍSTICAS GLOBALES ---")
    
    lista_dataframes_temporadas = []

    for archivo in os.listdir(DIR_HTML_TEMPORADAS):
        if not archivo.endswith(".html"):
            continue
            
        id_temporada = archivo.replace("Barcelona_Stats_", "").replace(".html", "")
        ruta_absoluta = os.path.join(DIR_HTML_TEMPORADAS, archivo)
        
        try:
            # Parseo de estructuras tabulares subyacentes mediante Pandas
            tablas_html = pd.read_html(ruta_absoluta)
            
            # Inicialización de DataFrames temporales por subdominio analítico
            df_standard = pd.DataFrame()
            df_shooting = pd.DataFrame()
            df_keepers = pd.DataFrame()
            df_misc = pd.DataFrame()
            
            for tabla in tablas_html:
                # 1. Aplanamiento jerárquico de columnas MultiIndex a dimensión plana
                if isinstance(tabla.columns, pd.MultiIndex):
                    tabla.columns = tabla.columns.droplevel(0)
                
                # 2. Resolución de colisiones: Omisión de columnas duplicadas post-aplanamiento
                tabla = tabla.loc[:, ~tabla.columns.duplicated()].copy()
                
                # 3. Limpieza de filas totalizadoras y encabezados repetidos
                if 'Player' in tabla.columns:
                    tabla = tabla[~tabla['Player'].isin(['Squad Total', 'Opponent Total', 'Player'])].copy()
                    
                    # --- Mapeo heurístico para la tipificación de DataFrames ---
                    # Se evalúa la presencia de combinaciones de columnas unívocas para cada subdominio
                    
                    if df_standard.empty and 'Min' in tabla.columns and 'Ast' in tabla.columns and 'Gls' in tabla.columns:
                        cols_objetivo = ['Player', 'Min', 'Gls', 'Ast', 'CrdY', 'CrdR']
                        cols_presentes = [c for c in cols_objetivo if c in tabla.columns]
                        df_standard = tabla[cols_presentes].copy()
                    
                    elif df_shooting.empty and 'Sh' in tabla.columns and 'SoT' in tabla.columns:
                        cols_objetivo = ['Player', 'Sh', 'SoT', 'SoT%']
                        cols_presentes = [c for c in cols_objetivo if c in tabla.columns]
                        df_shooting = tabla[cols_presentes].copy()
                    
                    elif df_misc.empty and 'Fls' in tabla.columns and 'Fld' in tabla.columns:
                        cols_objetivo = ['Player', 'Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'PKwon', 'PKcon', 'OG']
                        cols_presentes = [c for c in cols_objetivo if c in tabla.columns]
                        df_misc = tabla[cols_presentes].copy()
                    
                    elif df_keepers.empty and 'CS' in tabla.columns and 'Saves' in tabla.columns:
                        cols_objetivo = ['Player', 'CS', 'CS%', 'GA', 'SoTA', 'Saves', 'Save%']
                        cols_presentes = [c for c in cols_objetivo if c in tabla.columns]
                        df_keepers = tabla[cols_presentes].copy()

            # --- Consolidación Relacional (Left Joins sobre el jugador) ---
            df_temporal = df_standard
            
            if not df_shooting.empty:
                df_temporal = pd.merge(df_temporal, df_shooting, on='Player', how='left')
            if not df_misc.empty:
                df_temporal = pd.merge(df_temporal, df_misc, on='Player', how='left')
            if not df_keepers.empty:
                df_temporal = pd.merge(df_temporal, df_keepers, on='Player', how='left')

            # --- Estandarización del esquema dimensional al castellano ---
            if not df_temporal.empty:
                # Verificación secundaria post-merge para asegurar unicidad de columnas
                df_temporal = df_temporal.loc[:, ~df_temporal.columns.duplicated()].copy()
                
                diccionario_nomenclatura = {
                    'Player': 'Jugador', 'Min': 'Minutos', 'Gls': 'Goles', 'Ast': 'Asistencias',
                    'CrdY': 'Amarillas', 'CrdR': 'Rojas', 'Sh': 'Tiros_Totales', 'SoT': 'Tiros_Puerta',
                    'SoT%': 'Porcentaje_Tiros_Puerta', 'Fls': 'Faltas_Cometidas', 'Fld': 'Faltas_Recibidas',
                    'Off': 'Fueras_Juego', 'Crs': 'Centros', 'Int': 'Intercepciones', 'TklW': 'Entradas_Ganadas',
                    'PKwon': 'Penaltis_Provocados', 'PKcon': 'Penaltis_Cometidos', 'OG': 'Goles_Propia',
                    'CS': 'Porterias_a_Cero', 'CS%': 'Porcentaje_Porterias_Cero', 'GA': 'Goles_Encajados',
                    'SoTA': 'Tiros_Puerta_Recibidos', 'Saves': 'Paradas', 'Save%': 'Porcentaje_Paradas'
                }
                
                df_temporal.rename(columns=diccionario_nomenclatura, inplace=True)
                df_temporal['temporada'] = id_temporada
                lista_dataframes_temporadas.append(df_temporal)
                print(f"Operación completada: {id_temporada} normalizada estructuralmente.")
                
        except Exception as e:
            print(f"Error de procesamiento en el archivo {archivo}: {e}")

    # --- Integración global y Coerción estricta de tipos de datos ---
    if lista_dataframes_temporadas:
        df_maestro = pd.concat(lista_dataframes_temporadas, ignore_index=True)
        
        # Coerción de tipos continuos a discretos. 
        # La notación 'Int64' nativa de Pandas permite la convivencia de valores enteros puros 
        # junto a valores nulos (NaN), evitando la transformación forzada a punto flotante (0.0).
        columnas_discretas_objetivo = [
            'Minutos', 'Goles', 'Asistencias', 'Amarillas', 'Rojas', 'Tiros_Totales', 
            'Tiros_Puerta', 'Faltas_Cometidas', 'Faltas_Recibidas', 'Fueras_Juego', 
            'Centros', 'Intercepciones', 'Entradas_Ganadas', 'Penaltis_Provocados', 
            'Penaltis_Cometidos', 'Goles_Propia', 'Porterias_a_Cero', 'Goles_Encajados', 
            'Tiros_Puerta_Recibidos', 'Paradas'
        ]
        
        for col in columnas_discretas_objetivo:
            if col in df_maestro.columns:
                df_maestro[col] = pd.to_numeric(df_maestro[col], errors='coerce').astype('Int64')

        # Exportación del archivo maestro. 
        # Se establece sep=';' y decimal=',' para asegurar la compatibilidad regional en la ingesta de Power BI.
        df_maestro.to_csv(PATH_OUTPUT_GLOBAL, index=False, encoding='utf-8-sig', sep=';', decimal=',')
        print(f"\nProceso finalizado exitosamente. Tabla de hechos consolidada en: {PATH_OUTPUT_GLOBAL}")
    else:
        print("Aviso: Ejecución abortada. No se han detectado datos tabulares estructurados.")

if __name__ == "__main__":
    extraer_estadisticas_globales_temporada()