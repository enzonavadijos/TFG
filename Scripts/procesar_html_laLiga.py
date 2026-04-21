import pandas as pd
import os
import re
from io import StringIO

# --- CONFIGURACIÓN ---
INPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\HTML_LaLiga"
# Ruta actualizada según tu indicación:
OUTPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga\scores_and_fixtures_laliga.csv"

def extraer_temporada(filename):
    match = re.search(r'(\d{4}-\d{4})', filename)
    if match:
        return match.group(1)
    return "Desconocida"

def limpiar_columnas(df):
    """Estandariza nombres de columnas."""
    if isinstance(df.columns, pd.MultiIndex):
        new_cols = []
        for col in df.columns.values:
            # Preferimos el nivel inferior
            if str(col[1]).strip() != "" and "Unnamed" not in str(col[1]):
                new_cols.append(str(col[1]))
            else:
                new_cols.append(str(col[0]))
        df.columns = new_cols
    
    # Minúsculas y guiones bajos
    df.columns = [str(c).lower().strip().replace(" ", "_").replace("/", "_") for c in df.columns]
    return df

def procesar_scores(filepath):
    filename = os.path.basename(filepath)
    season = extraer_temporada(filename)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        
        dfs = pd.read_html(StringIO(html))
        df_scores = None
        
        # BUSCAR TABLA DE PARTIDOS
        for df in dfs:
            df_temp = limpiar_columnas(df.copy())
            cols = " ".join(df_temp.columns)
            
            # Criterio: Date + Opponent + Result (y que no sea tabla de jugadores)
            if "date" in cols and "opponent" in cols and "result" in cols and "player" not in cols:
                df_scores = df
                break
        
        if df_scores is None:
            return None

        # --- PROCESAMIENTO ---
        df = limpiar_columnas(df_scores)
        
        # Mapeo de columnas esenciales
        cols_map = {
            'date': next((c for c in df.columns if 'date' in c), 'date'),
            'round': next((c for c in df.columns if 'round' in c), 'round'),
            'opponent': next((c for c in df.columns if 'opponent' in c), 'opponent'),
            'result': next((c for c in df.columns if 'result' in c), 'result'),
            'gf': next((c for c in df.columns if 'gf' in c), 'gf'),
            'ga': next((c for c in df.columns if 'ga' in c), 'ga'),
            'venue': next((c for c in df.columns if 'venue' in c), 'venue'),
            # Métricas avanzadas (xG)
            'xg_favor': next((c for c in df.columns if 'xg' in c and 'expected' in c and 'allow' not in c), 'xg_favor'),
            'xg_contra': next((c for c in df.columns if 'xga' in c), 'xg_contra'),
            'poss': next((c for c in df.columns if 'poss' in c), 'poss')
        }
        
        # Filtros de validez (eliminar filas vacías o cabeceras repetidas)
        df = df[df[cols_map['date']].notna()]
        df = df[df[cols_map['date']] != 'Date']
        df = df[df[cols_map['result']].notna()] # Solo partidos jugados (con resultado)
        
        # Añadir metadatos
        df['season'] = season
        df['competition'] = 'La Liga'
        
        # Renombrar para estandarizar
        df = df.rename(columns={
            cols_map['xg_favor']: 'xg_favor',
            cols_map['xg_contra']: 'xg_contra',
            cols_map['poss']: 'posesion'
        })
        
        # Rellenar valores numéricos faltantes con 0 (para años antiguos)
        if 'xg_favor' not in df.columns: df['xg_favor'] = 0
        if 'xg_contra' not in df.columns: df['xg_contra'] = 0
        if 'posesion' not in df.columns: df['posesion'] = 0
            
        return df

    except Exception as e:
        print(f"❌ Error leyendo {filename}: {e}")
        return None

def main():
    print("--- 🇪🇸 GENERADOR DE LA LIGA (CON FILTRO ANTIDUPLICADOS) ---")
    
    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ No existe la carpeta de entrada: {INPUT_FOLDER}")
        return
    
    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    archivos = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".html")]
    print(f"📂 Procesando {len(archivos)} archivos...")
    
    data = []
    for archivo in archivos:
        df = procesar_scores(os.path.join(INPUT_FOLDER, archivo))
        if df is not None:
            data.append(df)
            print(f"   ✅ {archivo}")
    
    if data:
        # 1. UNIR TODO
        df_final = pd.concat(data, ignore_index=True)
        
        # 2. LIMPIEZA DE FORMATOS
        if 'date' in df_final.columns:
            df_final['date'] = pd.to_datetime(df_final['date'], errors='coerce')
        
        # 3. EL GRAN FILTRO (Eliminar duplicados aquí mismo)
        print(f"📊 Partidos brutos extraídos: {len(df_final)}")
        
        # Usamos Fecha + Rival + Temporada como 'DNI' del partido
        df_final = df_final.drop_duplicates(subset=['date', 'opponent', 'season'], keep='first')
        
        # Ordenar cronológicamente
        df_final = df_final.sort_values('date')
        
        # 4. GUARDAR
        df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n🎉 ¡ÉXITO! Archivo limpio generado en:\n   -> {OUTPUT_FILE}")
        print(f"✅ Partidos únicos finales: {len(df_final)}")
    else:
        print("❌ No se encontraron datos de partidos.")

if __name__ == "__main__":
    main()