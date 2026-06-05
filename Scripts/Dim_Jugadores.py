import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
PATH_LALIGA = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga\stats_laliga.csv"
PATH_CHAMPIONS = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League\stats_champions.csv"
PATH_NACIONES = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Nacionalidades.csv"
PATH_OUTPUT = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Jugadores.csv"

def extraer_columnas_jugador_nacion(ruta_archivo):
    """
    Función auxiliar que lee la cabecera de un archivo CSV para detectar dinámicamente 
    el nombre de la columna referente al jugador y extrae un subconjunto de datos 
    conteniendo únicamente la identidad del jugador y su nacionalidad en crudo.
    """
    try:
        # Lectura exclusiva de la cabecera para optimización de memoria
        df_cabecera = pd.read_csv(ruta_archivo, nrows=0)
        columnas = df_cabecera.columns.tolist()
        
        col_jugador = None
        for col in columnas:
            if str(col).strip().lower() in ['jugador', 'player', 'nombre']:
                col_jugador = col
                break
                
        if not col_jugador or 'nation' not in columnas:
            print(f"Aviso: No se detectaron las columnas requeridas (Jugador/Nation) en {ruta_archivo}")
            return pd.DataFrame()
            
        # Extracción del subconjunto de datos y normalización de la cabecera
        df_datos = pd.read_csv(ruta_archivo, usecols=[col_jugador, 'nation'])
        df_datos = df_datos.rename(columns={col_jugador: 'Jugador'})
        return df_datos
        
    except Exception as e:
        print(f"Error durante la lectura del archivo {ruta_archivo}: {e}")
        return pd.DataFrame()

def generar_dimension_jugadores():
    """
    Consolida los registros de jugadores de diferentes competiciones, realiza un 
    proceso de deduplicación y mapea los códigos de nacionalidad en crudo con la 
    dimensión maestra de países para generar la clave foránea (ID_Nacion).
    """
    print("--- INICIANDO CONSTRUCCIÓN DE LA DIMENSIÓN DE JUGADORES ---")
    
    try:
        # 1. Carga de los datos en crudo desde las fuentes de LaLiga y Champions
        df_liga = extraer_columnas_jugador_nacion(PATH_LALIGA)
        df_champ = extraer_columnas_jugador_nacion(PATH_CHAMPIONS)

        # 2. Consolidación estructural, eliminación de registros nulos y deduplicación por jugador
        df_jugadores = pd.concat([df_liga, df_champ]).dropna().drop_duplicates(subset=['Jugador'])

        # 3. Limpieza de la cadena de texto de nacionalidad
        # Aísla el código del país separando por espacios y extrayendo el último elemento
        df_jugadores['Codigo_Crudo'] = df_jugadores['nation'].astype(str).str.strip().str.split(' ').str[-1].str.upper()
        
        # Diccionario de estandarización: Transforma códigos de 2 letras a formato FIFA/StatsBomb (3 letras)
        mapeo_codigos_cortos = {
            'PT': 'POR', 'ES': 'ESP', 'BR': 'BRA', 'AR': 'ARG', 'FR': 'FRA', 
            'NL': 'NED', 'DE': 'GER', 'IT': 'ITA', 'EN': 'ENG', 'UY': 'URU',
            'CM': 'CMR', 'SE': 'SWE', 'CI': 'CIV', 'HR': 'CRO', 'DK': 'DEN',
            'PL': 'POL', 'CL': 'CHI', 'MX': 'MEX', 'US': 'USA', 'BE': 'BEL',
            'SN': 'SEN', 'ML': 'MLI', 'GH': 'GHA', 'MA': 'MAR', 'TR': 'TUR',
            'IS': 'ISL', 'BA': 'BIH', 'UA': 'UKR', 'AT': 'AUT', 'CO': 'COL',
            'VE': 'VEN', 'WA': 'WAL', 'SC': 'SCO', 'CH': 'SUI', 'RS': 'SRB',
            'JP': 'JPN', 'KR': 'KOR', 'GP': 'GLP', 'BY': 'BLR', 'DO': 'DOM', 
            'AL': 'ALB', 'GN': 'GUI', 'GA': 'GAB', 'ME': 'MNE', 'HU': 'HUN'
        }
        df_jugadores['Codigo'] = df_jugadores['Codigo_Crudo'].replace(mapeo_codigos_cortos)

        # 4. Lectura de la dimensión maestra de nacionalidades
        df_dim_naciones = pd.read_csv(PATH_NACIONES)
        
        # 5. Cruce relacional (Left Merge) para incorporar el ID_Nacion
        df_final = pd.merge(df_jugadores, df_dim_naciones[['ID_Nacion', 'Codigo']], on='Codigo', how='left')

        # 6. Selección de atributos y ordenamiento alfabético
        df_final = df_final[['Jugador', 'ID_Nacion']].sort_values(by='Jugador').reset_index(drop=True)
        
        # Imputación de nulos y coerción a tipo entero (int) para mantener la integridad
        # del modelo relacional en herramientas de Business Intelligence (Power BI)
        df_final['ID_Nacion'] = df_final['ID_Nacion'].fillna(0).astype(int)
        
        # 7. Asignación de clave primaria (Primary Key) secuencial
        df_final.insert(0, 'ID_Jugador', range(1, len(df_final) + 1))

        # 8. Exportación de la dimensión generada
        df_final.to_csv(PATH_OUTPUT, index=False, encoding='utf-8')
        
        print(f"Proceso completado: Dimensión de Jugadores estructurada con {len(df_final)} registros.")
        print("Muestra del conjunto de datos procesado (Validación de tipos de datos):")
        print(df_final.head(5))

    except Exception as e:
        print(f"Error crítico durante la generación de la dimensión: {e}")

if __name__ == "__main__":
    generar_dimension_jugadores()