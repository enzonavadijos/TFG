import os
import pandas as pd

print("--- 🔬 INICIANDO CIRUGÍA DEFINITIVA (LIMPIEZA DE ENTEROS Y FORMATO ESPAÑOL) ---")

CARPETA_HTML = r"C:\Users\enson\Desktop\TFG\ETL\HTML_Temporadas"
CARPETA_CSV = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ruta_salida = os.path.join(CARPETA_CSV, "Fact_Estadisticas_Globales.csv")

datos_totales = []

for archivo in os.listdir(CARPETA_HTML):
    if not archivo.endswith(".html"):
        continue
        
    temporada = archivo.replace("Barcelona_Stats_", "").replace(".html", "")
    ruta_archivo = os.path.join(CARPETA_HTML, archivo)
    
    try:
        tablas = pd.read_html(ruta_archivo)
        
        df_std = pd.DataFrame()
        df_sho = pd.DataFrame()
        df_kpr = pd.DataFrame()
        df_msc = pd.DataFrame()
        
        for tabla in tablas:
            # 1. Aplanar encabezados dobles
            if isinstance(tabla.columns, pd.MultiIndex):
                tabla.columns = tabla.columns.droplevel(0)
            
            # 2. Destruir columnas duplicadas antes de hacer nada
            tabla = tabla.loc[:, ~tabla.columns.duplicated()].copy()
            
            # 3. Limpiar filas basura
            if 'Player' in tabla.columns:
                tabla = tabla[~tabla['Player'].isin(['Squad Total', 'Opponent Total', 'Player'])].copy()
                
                # --- CAZAR TABLAS (Solo la primera de cada tipo) ---
                if df_std.empty and 'Min' in tabla.columns and 'Ast' in tabla.columns and 'Gls' in tabla.columns:
                    cols_std = ['Player', 'Min', 'Gls', 'Ast', 'CrdY', 'CrdR']
                    cols_presentes = [c for c in cols_std if c in tabla.columns]
                    df_std = tabla[cols_presentes].copy()
                
                elif df_sho.empty and 'Sh' in tabla.columns and 'SoT' in tabla.columns:
                    cols_sho = ['Player', 'Sh', 'SoT', 'SoT%']
                    cols_presentes = [c for c in cols_sho if c in tabla.columns]
                    df_sho = tabla[cols_presentes].copy()
                
                elif df_msc.empty and 'Fls' in tabla.columns and 'Fld' in tabla.columns:
                    cols_msc = ['Player', 'Fls', 'Fld', 'Off', 'Crs', 'Int', 'TklW', 'PKwon', 'PKcon', 'OG']
                    cols_presentes = [c for c in cols_msc if c in tabla.columns]
                    df_msc = tabla[cols_presentes].copy()
                
                elif df_kpr.empty and 'CS' in tabla.columns and 'Saves' in tabla.columns:
                    cols_kpr = ['Player', 'CS', 'CS%', 'GA', 'SoTA', 'Saves', 'Save%']
                    cols_presentes = [c for c in cols_kpr if c in tabla.columns]
                    df_kpr = tabla[cols_presentes].copy()

        # --- COSER LAS TABLAS (MERGE) ---
        df_temp = df_std
        
        if not df_sho.empty:
            df_temp = pd.merge(df_temp, df_sho, on='Player', how='left')
        if not df_msc.empty:
            df_temp = pd.merge(df_temp, df_msc, on='Player', how='left')
        if not df_kpr.empty:
            df_temp = pd.merge(df_temp, df_kpr, on='Player', how='left')

        # --- TRADUCCIÓN PROFESIONAL AL ESPAÑOL ---
        if not df_temp.empty:
            # Seguro anti-duplicados post-merge
            df_temp = df_temp.loc[:, ~df_temp.columns.duplicated()].copy()
            
            mapeo = {
                'Player': 'Jugador', 'Min': 'Minutos', 'Gls': 'Goles', 'Ast': 'Asistencias',
                'CrdY': 'Amarillas', 'CrdR': 'Rojas', 'Sh': 'Tiros_Totales', 'SoT': 'Tiros_Puerta',
                'SoT%': 'Porcentaje_Tiros_Puerta', 'Fls': 'Faltas_Cometidas', 'Fld': 'Faltas_Recibidas',
                'Off': 'Fueras_Juego', 'Crs': 'Centros', 'Int': 'Intercepciones', 'TklW': 'Entradas_Ganadas',
                'PKwon': 'Penaltis_Provocados', 'PKcon': 'Penaltis_Cometidos', 'OG': 'Goles_Propia',
                'CS': 'Porterias_a_Cero', 'CS%': 'Porcentaje_Porterias_Cero', 'GA': 'Goles_Encajados',
                'SoTA': 'Tiros_Puerta_Recibidos', 'Saves': 'Paradas', 'Save%': 'Porcentaje_Paradas'
            }
            
            df_temp.rename(columns=mapeo, inplace=True)
            df_temp['temporada'] = temporada
            datos_totales.append(df_temp)
            print(f"   ✅ {temporada}: Limpia y lista.")
            
    except Exception as e:
        print(f"   ❌ Error al procesar {archivo}: {e}")

# --- UNIÓN Y LIMPIEZA FINAL ---
if datos_totales:
    df_final = pd.concat(datos_totales, ignore_index=True)
    
    # 🔥 LA MAGIA: Forzar a Enteros Puros (Int64) para matar el '.0'
    columnas_enteras = [
        'Minutos', 'Goles', 'Asistencias', 'Amarillas', 'Rojas', 'Tiros_Totales', 
        'Tiros_Puerta', 'Faltas_Cometidas', 'Faltas_Recibidas', 'Fueras_Juego', 
        'Centros', 'Intercepciones', 'Entradas_Ganadas', 'Penaltis_Provocados', 
        'Penaltis_Cometidos', 'Goles_Propia', 'Porterias_a_Cero', 'Goles_Encajados', 
        'Tiros_Puerta_Recibidos', 'Paradas'
    ]
    
    for col in columnas_enteras:
        if col in df_final.columns:
            # Lo convierte a número y luego al formato Int64 (que soporta valores vacíos sin añadir decimales)
            df_final[col] = pd.to_numeric(df_final[col], errors='coerce').astype('Int64')

    # Guardado maestro: Separador ';' y decimales ',' para Power BI en español
    df_final.to_csv(ruta_salida, index=False, encoding='utf-8-sig', sep=';', decimal=',')
    print(f"\n🎉 ¡MISIÓN CUMPLIDA! Archivo maestro guardado en: {ruta_salida}")
else:
    print("No se encontraron datos.")