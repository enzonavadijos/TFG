import pandas as pd

# 1. Rutas exactas de tus archivos
ruta_laliga = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga\stats_laliga.csv"
ruta_champions = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League\stats_champions.csv"
ruta_naciones = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Nacionalidades.csv"
ruta_salida = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Dim_Jugadores.csv"

def cargar_jugadores_y_nacion(ruta):
    df_cols = pd.read_csv(ruta, nrows=0)
    columnas = df_cols.columns.tolist()
    
    col_jugador = None
    for col in columnas:
        if str(col).strip().lower() in ['jugador', 'player', 'nombre']:
            col_jugador = col
            break
            
    if not col_jugador or 'nation' not in columnas:
        print(f"⚠️ Faltan columnas en {ruta}")
        return pd.DataFrame()
        
    df = pd.read_csv(ruta, usecols=[col_jugador, 'nation'])
    df = df.rename(columns={col_jugador: 'Jugador'})
    return df

try:
    # 2. Cargar los datos crudos
    df_liga = cargar_jugadores_y_nacion(ruta_laliga)
    df_champ = cargar_jugadores_y_nacion(ruta_champions)

    # 3. Unir, quitar nulos y dejar UN SOLO registro por jugador
    df_jugadores = pd.concat([df_liga, df_champ]).dropna().drop_duplicates(subset=['Jugador'])

    # 4. Limpiar la nacionalidad
    df_jugadores['Codigo_Crudo'] = df_jugadores['nation'].astype(str).str.strip().str.split(' ').str[-1].str.upper()
    
    arreglar_cortos = {
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
    df_jugadores['Codigo'] = df_jugadores['Codigo_Crudo'].replace(arreglar_cortos)

    # 5. Leer la Dim_Nacionalidades
    df_dim_nac = pd.read_csv(ruta_naciones)
    
    # 6. Cruzar las tablas (Merge)
    df_final = pd.merge(df_jugadores, df_dim_nac[['ID_Nacion', 'Codigo']], on='Codigo', how='left')

    # 7. Limpiar columnas y FORZAR TIPO ENTERO (sin decimales)
    df_final = df_final[['Jugador', 'ID_Nacion']].sort_values(by='Jugador').reset_index(drop=True)
    
    # MAGIA AQUÍ: Convertimos a int (entero)
    df_final['ID_Nacion'] = df_final['ID_Nacion'].fillna(0).astype(int)
    
    # 8. Generar el ID_Jugador definitivo (range ya genera enteros por defecto)
    df_final.insert(0, 'ID_Jugador', range(1, len(df_final) + 1))

    # 9. Guardar la nueva dimensión maestra
    df_final.to_csv(ruta_salida, index=False, encoding='utf-8')
    
    print(f"✅ ¡Éxito! Dim_Jugadores generada con {len(df_final)} jugadores.")
    print("Muestra de los datos (Solo números enteros):")
    print(df_final.head(10))

except Exception as e:
    print("❌ Error:", e)