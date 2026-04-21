import pandas as pd
import os
import re
from io import StringIO

# --- CONFIGURACIÓN ---
INPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\HTML_Champions"
OUTPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\ETL"

# Nombres de los archivos de salida
FILE_SCORES = "scores_and_fixtures_champions.csv"
FILE_STATS = "stats_champions.csv"

def extraer_temporada(filename):
    match = re.search(r'(\d{4}-\d{4})', filename)
    if match:
        return match.group(1)
    return "Desconocida"

def limpiar_columnas(df):
    # 1. Aplanar MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        new_cols = []
        for col in df.columns.values:
            # Si el nivel 1 tiene texto, úsalo. Si no, usa el nivel 0.
            if str(col[1]).strip() != "" and "Unnamed" not in str(col[1]):
                new_cols.append(str(col[1]))
            else:
                new_cols.append(str(col[0]))
        df.columns = new_cols

    # 2. Limpieza estándar
    df.columns = [str(c).lower().strip().replace(" ", "_").replace("/", "_") for c in df.columns]
    return df

def clasificar_y_procesar(filepath):
    filename = os.path.basename(filepath)
    season = extraer_temporada(filename)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        
        dfs = pd.read_html(StringIO(html))
        
        # --- DETECTIVES DE TABLAS ---
        df_scores = None
        df_stats = None
        
        for df in dfs:
            df_temp = limpiar_columnas(df.copy())
            cols = " ".join(df_temp.columns)
            
            # CRITERIO 1: Es tabla de PARTIDOS? (Scores & Fixtures)
            # Debe tener Date, Opponent y Result
            if "date" in cols and "opponent" in cols and "result" in cols and "player" not in cols:
                df_scores = df # Guardamos la original
            
            # CRITERIO 2: Es tabla de JUGADORES? (Standard Stats)
            # Debe tener Player, Pos, Age, MP (Matches Played)
            # Buscamos 'mp' o 'matches_played' y 'starts'
            if "player" in cols and "pos" in cols and ("mp" in cols or "matches" in cols):
                # A veces hay varias tablas de stats (Porteros, Shoots...), nos quedamos la primera grande (Standard)
                if len(df) > 5: # Filtro simple para evitar tablitas pequeñas
                    df_stats = df
                    # Si encontramos Standard Stats, a veces es suficiente, pero seguimos por si acaso el loop
                    # Prioridad: Standard Stats suele ser la primera grande.
        
        # --- RETORNO DE RESULTADOS ---
        results = {}
        
        # 1. PROCESAR SCORES (Si encontró)
        if df_scores is not None:
            df = limpiar_columnas(df_scores)
            # Columnas clave
            cols_map = {
                'date': next((c for c in df.columns if 'date' in c), 'date'),
                'round': next((c for c in df.columns if 'round' in c), 'round'),
                'opponent': next((c for c in df.columns if 'opponent' in c), 'opponent'),
                'result': next((c for c in df.columns if 'result' in c), 'result'),
                'gf': next((c for c in df.columns if 'gf' in c), 'gf'),
                'ga': next((c for c in df.columns if 'ga' in c), 'ga'),
                'venue': next((c for c in df.columns if 'venue' in c), 'venue'),
                'xg_favor': next((c for c in df.columns if 'xg' in c and 'expected' in c and 'allow' not in c), 'xg'),
                'xg_contra': next((c for c in df.columns if 'xga' in c), 'xga'),
                'poss': next((c for c in df.columns if 'poss' in c), 'poss')
            }
            
            # Limpieza filas
            df = df[df[cols_map['date']].notna()]
            df = df[df[cols_map['date']] != 'Date']
            df = df[df[cols_map['result']].notna()] # Solo partidos jugados
            
            # Añadir metadatos
            df['season'] = season
            df['competition'] = 'Champions League'
            
            # Estandarizar nombres clave
            df = df.rename(columns={
                cols_map['xg_favor']: 'xg_favor',
                cols_map['xg_contra']: 'xg_contra',
                cols_map['poss']: 'posesion'
            })
            
            results['type'] = 'scores'
            results['df'] = df

        # 2. PROCESAR STATS (Si encontró y NO es scores)
        elif df_stats is not None:
            df = limpiar_columnas(df_stats)
            
            # Limpieza básica
            col_player = next((c for c in df.columns if 'player' in c), 'player')
            df = df[df[col_player] != 'Player']
            df = df[df[col_player].notna()]
            
            # Filtro: Eliminar filas de "Squad Total" o "Opponent Total"
            df = df[~df[col_player].astype(str).str.contains("Total", case=False)]
            
            df['season'] = season
            df['competition'] = 'Champions League'
            
            results['type'] = 'stats'
            results['df'] = df

        return results

    except Exception as e:
        print(f"❌ Error en {filename}: {e}")
        return {}

def main():
    print("--- 🏭 UNIFICADOR DE CHAMPIONS (SCORES + STATS) ---")
    
    if not os.path.exists(INPUT_FOLDER):
        print(f"❌ No existe la carpeta {INPUT_FOLDER}")
        return
        
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    archivos = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".html")]
    print(f"📂 Escaneando {len(archivos)} archivos...")
    
    list_scores = []
    list_stats = []
    
    for archivo in archivos:
        path = os.path.join(INPUT_FOLDER, archivo)
        res = clasificar_y_procesar(path)
        
        if res.get('type') == 'scores':
            list_scores.append(res['df'])
            print(f"   ⚽ {archivo} -> Scores")
        elif res.get('type') == 'stats':
            list_stats.append(res['df'])
            print(f"   📊 {archivo} -> Stats")
        else:
            print(f"   ⚠️ {archivo} -> No identificado / Saltado")

    # --- GUARDAR SCORES ---
    if list_scores:
        df_scores = pd.concat(list_scores, ignore_index=True)
        # Ordenar por fecha
        if 'date' in df_scores.columns:
            df_scores['date'] = pd.to_datetime(df_scores['date'], errors='coerce')
            df_scores = df_scores.sort_values('date')
            
        path_scores = os.path.join(OUTPUT_FOLDER, FILE_SCORES)
        df_scores.to_csv(path_scores, index=False, encoding='utf-8-sig')
        print(f"\n✅ GENERADO: {FILE_SCORES} ({len(df_scores)} partidos)")
    
    # --- GUARDAR STATS ---
    if list_stats:
        df_stats = pd.concat(list_stats, ignore_index=True)
        # Ordenar por temporada y jugador
        df_stats = df_stats.sort_values(['season', 'player'])
        
        path_stats = os.path.join(OUTPUT_FOLDER, FILE_STATS)
        df_stats.to_csv(path_stats, index=False, encoding='utf-8-sig')
        print(f"✅ GENERADO: {FILE_STATS} ({len(df_stats)} registros de jugadores)")

    print("\n🚀 ¡Proceso completado!")

if __name__ == "__main__":
    main()