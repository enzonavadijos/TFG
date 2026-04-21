import pandas as pd
import os
import re
from io import StringIO

# --- CONFIGURACIÓN ---
INPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\HTML_LaLiga"
OUTPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\stats_laliga.csv"

def extraer_temporada(filename):
    match = re.search(r'(\d{4}-\d{4})', filename)
    if match:
        return match.group(1)
    return "Desconocida"

def limpiar_comentarios_html(html_content):
    """Elimina comentarios para exponer tablas ocultas."""
    return html_content.replace("", "")

def aplanar_columnas_cirujano(df):
    new_cols = []
    if isinstance(df.columns, pd.MultiIndex):
        for col in df.columns.values:
            top = str(col[0])
            bot = str(col[1])
            if "Unnamed" in top:
                clean_name = bot
            else:
                clean_name = f"{top}_{bot}"
            new_cols.append(clean_name)
    else:
        new_cols = [str(c) for c in df.columns]

    return [c.lower().strip().replace(" ", "_").replace("/", "_") for c in new_cols]

def procesar_stats(filepath):
    filename = os.path.basename(filepath)
    season = extraer_temporada(filename)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            raw_html = f.read()
        
        # 1. DESCOMENTAR
        clean_html = limpiar_comentarios_html(raw_html)
        dfs = pd.read_html(StringIO(clean_html))
        
        df_target = None
        
        # 2. BUSCAR TABLA
        for df in dfs:
            cols_temp = aplanar_columnas_cirujano(df)
            # Criterios: Player + MP + Gls (sin per 90)
            if any('player' == c for c in cols_temp) and any('mp' == c for c in cols_temp):
                 if any('gls' in c and '90' not in c for c in cols_temp):
                    df_target = df
                    df_target.columns = cols_temp
                    break
        
        if df_target is None:
            # Fallback: Buscar Player + Minutos
            for df in dfs:
                cols_temp = aplanar_columnas_cirujano(df)
                if any('player' == c for c in cols_temp) and any('min' in c for c in cols_temp):
                    df_target = df
                    df_target.columns = cols_temp
                    break

        if df_target is None:
            return None

        df = df_target.copy()
        col_player = 'player'
        
        # 2. FILTRAR FILAS
        df = df[df[col_player].notna()]
        df = df[df[col_player] != 'player']
        df = df[~df[col_player].astype(str).str.lower().str.contains("total")]
        df = df[~df[col_player].astype(str).str.lower().str.contains("opponent")]
        
        # 3. EXTRAER
        clean_df = pd.DataFrame()
        clean_df['season'] = [season] * len(df)
        clean_df['player'] = df[col_player].values
        
        def get_data(keywords):
            for kw in keywords:
                match = next((c for c in df.columns if kw in c), None)
                if match:
                    return df[match].values
            return 0

        clean_df['nation'] = get_data(['nation'])
        clean_df['pos'] = get_data(['pos'])
        clean_df['age'] = get_data(['age'])
        clean_df['mp'] = get_data(['mp', 'matches'])
        clean_df['starts'] = get_data(['starts'])
        clean_df['min'] = get_data(['min', 'minutes'])
        
        col_gls = next((c for c in df.columns if ('gls' in c or 'goals' in c) and '90' not in c), None)
        clean_df['goals'] = df[col_gls].values if col_gls else 0
        
        col_ast = next((c for c in df.columns if ('ast' in c or 'assists' in c) and '90' not in c), None)
        clean_df['assists'] = df[col_ast].values if col_ast else 0

        for c in ['mp', 'starts', 'min', 'goals', 'assists']:
            clean_df[c] = pd.to_numeric(clean_df[c], errors='coerce').fillna(0).astype(int)

        return clean_df

    except Exception as e:
        # print(f"❌ Error en {filename}: {e}") # Descomenta si quieres ver errores de archivos que no son stats
        return None

def main():
    print("--- 📊 GENERADOR STATS LA LIGA ---")
    if not os.path.exists(INPUT_FOLDER):
        print("Carpeta no encontrada.")
        return

    archivos = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".html")]
    all_stats = []
    print(f"📂 Procesando {len(archivos)} archivos...")
    
    for archivo in archivos:
        df = procesar_stats(os.path.join(INPUT_FOLDER, archivo))
        if df is not None and not df.empty:
            all_stats.append(df)
            print(f"   ✅ {archivo}: {len(df)} jugadores.")

    if all_stats:
        df_final = pd.concat(all_stats, ignore_index=True)
        df_final = df_final.sort_values(['season', 'goals'], ascending=[True, False])
        
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n🎉 HECHO: {OUTPUT_FILE} ({len(df_final)} registros)")
    else:
        print("❌ No se generaron datos.")

if __name__ == "__main__":
    main()