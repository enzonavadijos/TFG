import pandas as pd
import numpy as np
import os

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_JUGADORES_RAW = os.path.join(BASE_DIR, "Fact_Estadisticas_Jugadores_RAW.csv")
PATH_DICCIONARIO = os.path.join(BASE_DIR, "LaLiga", "stats_laliga.csv") 
PATH_OUTPUT = os.path.join(BASE_DIR, "Fact_Estadisticas_Jugadores.csv") 

def estandarizar_posiciones():
    """
    Lee los datos crudos de las estadísticas de los jugadores y aplica un cruce
    con un diccionario de posiciones para estandarizar la nomenclatura 
    (ej. limitando a 2 caracteres: FW, MF, DF) y corrigiendo defectos de extracción.
    """
    print("--- INICIANDO ESTANDARIZACIÓN DE POSICIONES ---")
    
    # 1. Lectura del archivo de hechos en crudo
    df_jugadores = pd.read_csv(PATH_JUGADORES_RAW)
    
    # 2. Carga y validación del diccionario de posiciones
    try:
        df_diccionario = pd.read_csv(PATH_DICCIONARIO)
        
        # Identificación dinámica de las columnas relevantes
        col_nombre_jugador = next((col for col in df_diccionario.columns if 'player' in str(col).lower() or 'jugador' in str(col).lower()), None)
        col_posicion_original = next((col for col in df_diccionario.columns if 'pos' in str(col).lower()), None)

        # Mecanismo de contingencia: Si no se detectan las columnas, se asume 
        # que la cabecera real se encuentra en la segunda fila (header=1)
        if not col_nombre_jugador or not col_posicion_original:
            df_diccionario = pd.read_csv(PATH_DICCIONARIO, header=1)
            col_nombre_jugador = next((col for col in df_diccionario.columns if 'player' in str(col).lower() or 'jugador' in str(col).lower()), None)
            col_posicion_original = next((col for col in df_diccionario.columns if 'pos' in str(col).lower()), None)
            
    except Exception as e:
        print(f"Error durante la lectura del diccionario de posiciones: {e}")
        return

    # 3. Limpieza y preparación del diccionario de posiciones
    df_diccionario = df_diccionario[[col_nombre_jugador, col_posicion_original]].drop_duplicates(subset=[col_nombre_jugador]).copy()
    df_diccionario.columns = ['Jugador', 'Posicion_Global']

    # Normalización: eliminación de espacios, extracción de los primeros 2 caracteres y conversión a mayúsculas
    df_diccionario['Posicion_Global'] = df_diccionario['Posicion_Global'].astype(str).str.replace(' ', '').str[:2].str.upper()
    
    # Limpieza de nulos literales (se respeta la doble asignación estructural del script original)
    df_diccionario['Posicion_Global'] = df_diccionario['Posicion_Global'].replace('NA', '')
    df_diccionario['Posicion_Global'] = df_diccionario['Posicion_Global'].replace('NA', '')

    # 4. Cruce de datos (Left Merge) para incorporar las posiciones corregidas a la tabla de hechos
    df_resultado = df_jugadores.merge(df_diccionario, on='Jugador', how='left')
    
    # Tratamiento de valores no mapeados: sustitución de vacíos y nulos por "Desconocida"
    df_resultado['Posicion_Global'] = df_resultado['Posicion_Global'].replace('', 'Desconocida').fillna('Desconocida')
    df_resultado['Posicion'] = df_resultado['Posicion_Global']
    
    # 5. Selección final de atributos para la tabla de hechos
    columnas_finales = [
        'ID_Partido', 'Jugador', 'Posicion', 'Titular', 'Minutos', 
        'Goles', 'Asistencias', 'Amarillas', 'Rojas', 'xG'
    ]
    df_resultado = df_resultado[columnas_finales]
    
    # 6. Exportación de los datos transformados
    df_resultado.to_csv(PATH_OUTPUT, index=False, encoding='utf-8-sig')
    
    print("\nProceso completado: Nomenclatura de posiciones estandarizada al formato internacional (FW, MF, DF).")
    print(f"Archivo exportado exitosamente en: {PATH_OUTPUT}")

if __name__ == "__main__":
    estandarizar_posiciones()