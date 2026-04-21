import pandas as pd
import numpy as np
import os

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ruta_jugadores_raw = os.path.join(CARPETA_BASE, "Fact_Estadisticas_Jugadores_RAW.csv")
ruta_diccionario = os.path.join(CARPETA_BASE, "LaLiga", "stats_laliga.csv") 
ruta_salida = os.path.join(CARPETA_BASE, "Fact_Estadisticas_Jugadores.csv") 

def reparar_posiciones():
    print("--- 🛠️ INICIANDO REPARACIÓN DE POSICIONES ---")
    
    # 1. Leer archivos
    df_jugadores = pd.read_csv(ruta_jugadores_raw)
    
    try:
        df_dicc = pd.read_csv(ruta_diccionario)
        col_jugador = next((col for col in df_dicc.columns if 'player' in str(col).lower() or 'jugador' in str(col).lower()), None)
        col_posicion = next((col for col in df_dicc.columns if 'pos' in str(col).lower()), None)

        if not col_jugador or not col_posicion:
            df_dicc = pd.read_csv(ruta_diccionario, header=1)
            col_jugador = next((col for col in df_dicc.columns if 'player' in str(col).lower() or 'jugador' in str(col).lower()), None)
            col_posicion = next((col for col in df_dicc.columns if 'pos' in str(col).lower()), None)
            
    except Exception as e:
        print(f"❌ Error leyendo el diccionario: {e}")
        return

    # 2. Limpiar el diccionario a fondo
    df_dicc = df_dicc[[col_jugador, col_posicion]].drop_duplicates(subset=[col_jugador]).copy()
    df_dicc.columns = ['Jugador', 'Posicion_Global']

    # Cortar a 2 letras Y PASAR A MAYÚSCULAS para que quede FW, MF, DF limpios
    df_dicc['Posicion_Global'] = df_dicc['Posicion_Global'].astype(str).str.replace(' ', '').str[:2].str.upper()
    df_dicc['Posicion_Global'] = df_dicc['Posicion_Global'].replace('NA', '')
    df_dicc['Posicion_Global'] = df_dicc['Posicion_Global'].replace('NA', '')

    # 3. El Cruce
    df_final = df_jugadores.merge(df_dicc, on='Jugador', how='left')
    
    # 🚨 LA REGLA CORREGIDA: IGNORAMOS LA COLUMNA ROTA Y COGEMOS SOLO EL DICCIONARIO
    df_final['Posicion_Global'] = df_final['Posicion_Global'].replace('', 'Desconocida').fillna('Desconocida')
    df_final['Posicion'] = df_final['Posicion_Global']
    
    # 4. Limpieza de las columnas basura
    columnas_finales = ['ID_Partido', 'Jugador', 'Posicion', 'Titular', 'Minutos', 'Goles', 'Asistencias', 'Amarillas', 'Rojas', 'xG']
    df_final = df_final[columnas_finales]
    
    # 5. Sobrescribir
    df_final.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ ¡ERROR ARREGLADO! Se acabaron los 'Pe' y los 'Ou'.")
    print("📍 Abre tu Fact_Estadisticas_Jugadores.csv y comprueba que ahora pone FW, MF, DF.")

if __name__ == "__main__":
    reparar_posiciones()