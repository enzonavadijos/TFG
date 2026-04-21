import pandas as pd
import os

# --- RUTAS EXACTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ruta_calendario = os.path.join(CARPETA_BASE, "LaLiga", "scores_and_fixtures_laliga.csv")
ruta_tacticas = os.path.join(CARPETA_BASE, "Fact_Tacticas_Oficiales_SB.csv")
ruta_salida = os.path.join(CARPETA_BASE, "Dim_Partidos.csv")

def generar_dim_partidos():
    print("--- 🏗️ CONSTRUYENDO DIM_PARTIDOS (CON LIMPIEZA DE EQUIPOS) ---")
    
    # 1. Cargar el calendario maestro
    try:
        df_cal = pd.read_csv(ruta_calendario)
    except FileNotFoundError:
        print(f"❌ Error: No encuentro el archivo en {ruta_calendario}")
        return
        
    df_cal = df_cal.dropna(subset=['date', 'opponent']).copy()
    
    if 'comp' in df_cal.columns:
        df_cal['competicion_real'] = df_cal['comp'].fillna(df_cal['competition'])
    else:
        df_cal['competicion_real'] = df_cal['competition']

    # 2. Seleccionar columnas clave y renombrar
    dim_partidos = df_cal[['date', 'season', 'competicion_real', 'opponent', 'venue', 'result', 'gf', 'ga']].copy()
    dim_partidos.rename(columns={
        'date': 'Fecha',
        'season': 'Temporada',
        'competicion_real': 'Competicion',
        'opponent': 'Rival',
        'venue': 'Localia',
        'result': 'Resultado',
        'gf': 'Goles_Barca',
        'ga': 'Goles_Rival'
    }, inplace=True)
    
    # --- ¡NUEVO!: 2.5 LIMPIEZA DE NOMBRES DE RIVALES (FBREF) ---
    print("🧼 Limpiando códigos de país en los nombres de los rivales...")
    # Primero quitamos espacios en blanco extra al principio o final
    dim_partidos['Rival'] = dim_partidos['Rival'].str.strip()
    # Buscamos 2 o 3 letras minúsculas al principio seguidas de un espacio y lo borramos
    dim_partidos['Rival'] = dim_partidos['Rival'].str.replace(r'^[a-z]{2,3}\s', '', regex=True)

    # 3. Ordenar cronológicamente y limpiar duplicados
    dim_partidos = dim_partidos.drop_duplicates(subset=['Fecha', 'Rival'])
    dim_partidos = dim_partidos.sort_values(by='Fecha').reset_index(drop=True)
    
    # 4. EXTRACCIÓN SEPARADA: GOLES Y PENALTIS
    dim_partidos['Penaltis_Barca'] = dim_partidos['Goles_Barca'].astype(str).str.extract(r'\((\d+)\)', expand=False)
    dim_partidos['Penaltis_Rival'] = dim_partidos['Goles_Rival'].astype(str).str.extract(r'\((\d+)\)', expand=False)
    
    dim_partidos['Goles_Barca_Real'] = dim_partidos['Goles_Barca'].astype(str).str.extract(r'^(\d+)', expand=False)
    dim_partidos['Goles_Rival_Real'] = dim_partidos['Goles_Rival'].astype(str).str.extract(r'^(\d+)', expand=False)

    dim_partidos['Goles_Barca'] = pd.to_numeric(dim_partidos['Goles_Barca_Real'], errors='coerce').astype('Int64')
    dim_partidos['Goles_Rival'] = pd.to_numeric(dim_partidos['Goles_Rival_Real'], errors='coerce').astype('Int64')
    dim_partidos['Penaltis_Barca'] = pd.to_numeric(dim_partidos['Penaltis_Barca'], errors='coerce').astype('Int64')
    dim_partidos['Penaltis_Rival'] = pd.to_numeric(dim_partidos['Penaltis_Rival'], errors='coerce').astype('Int64')

    dim_partidos = dim_partidos.drop(columns=['Goles_Barca_Real', 'Goles_Rival_Real'])

    # 5. CREAR EL ID NUMÉRICO ASCENDENTE
    dim_partidos.insert(0, 'ID_Partido', dim_partidos.index + 1)
    
    # 6. Traer los IDs de StatsBomb
    try:
        df_sb = pd.read_csv(ruta_tacticas)
        df_sb = df_sb[['fecha', 'id_partido_sb']].rename(columns={'fecha': 'Fecha', 'id_partido_sb': 'ID_StatsBomb'})
        dim_partidos = pd.merge(dim_partidos, df_sb, on='Fecha', how='left')
    except Exception as e:
        dim_partidos['ID_StatsBomb'] = None

    columnas_ordenadas = [
        'ID_Partido', 'ID_StatsBomb', 'Fecha', 'Temporada', 'Competicion', 'Rival', 'Localia', 
        'Resultado', 'Goles_Barca', 'Goles_Rival', 'Penaltis_Barca', 'Penaltis_Rival'
    ]
    dim_partidos = dim_partidos[columnas_ordenadas]

    # 7. Guardar el archivo maestro
    dim_partidos.to_csv(ruta_salida, index=False)
    
    print("\n✅ ¡LISTO! Rivales y Goles completamente limpios.")
    print(f"📍 Guardado en: {ruta_salida}")

if __name__ == "__main__":
    generar_dim_partidos()