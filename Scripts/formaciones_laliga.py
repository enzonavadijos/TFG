from statsbombpy import sb
import pandas as pd
import warnings
import os

# Ignoramos advertencias para tener la consola limpia
warnings.filterwarnings('ignore')

# --- CONFIGURACIÓN DE RUTA ---
OUTPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\ETL\CSV"

# --- FUNCIÓN DE LIMPIEZA INTEGRADA ---
def normalizar_formacion(codigo):
    """
    Convierte códigos de StatsBomb (41212) a formato legible (4-1-2-1-2).
    """
    codigo = str(codigo).replace("-", "") # Quitar guiones para tratar todo igual
    
    # Diccionario de traducción
    mapa = {
        "433": "4-3-3",
        "41221": "4-3-3",  # 4-3-3 con pivote
        "41212": "4-1-2-1-2", # El famoso Rombo (CORREGIDO)
        "442": "4-4-2",
        "4231": "4-2-3-1",
        "352": "3-5-2",
        "343": "3-4-3",
        "3142": "3-5-2",
        "3412": "3-4-1-2",
        "3421": "3-4-2-1",
        "3511": "3-5-1-1",
        "4222": "4-2-2-2",
        "4141": "4-1-4-1",
        "4411": "4-4-1-1",
        "4321": "4-3-2-1"
    }
    
    if codigo in mapa:
        return mapa[codigo]
    
    # Formateo genérico si no está en el mapa
    if len(codigo) == 3: return f"{codigo[0]}-{codigo[1]}-{codigo[2]}"
    if len(codigo) == 4: return f"{codigo[0]}-{codigo[1]}-{codigo[2]}-{codigo[3]}"
    if len(codigo) == 5: return f"{codigo[0]}-{codigo[1]}-{codigo[2]}-{codigo[3]}-{codigo[4]}"
        
    return codigo

def obtener_tacticas_statsbomb_final():
    print("--- 📡 CONECTANDO CON STATSBOMB (MESSI DATA) + LIMPIEZA ---")
    
    # 1. OBTENER LISTA DE COMPETICIONES
    print("Descargando índice de competiciones...")
    try:
        comps = sb.competitions()
    except Exception as e:
        print(f"❌ Error conectando con StatsBomb: {e}")
        return

    # Filtramos solo La Liga (11) y Champions League (16)
    mis_comps = comps[comps["competition_id"].isin([11, 16])]
    
    if mis_comps.empty:
        print("⚠️ No se encontraron competiciones.")
        return

    print(f"✅ Se encontraron {len(mis_comps)} temporadas disponibles.")
    
    all_matches = []

    # 2. DESCARGAR PARTIDOS TEMPORADA A TEMPORADA
    for index, row in mis_comps.iterrows():
        c_id = row["competition_id"]
        s_id = row["season_id"]
        c_name = row["competition_name"]
        s_name = row["season_name"]
        
        print(f"📥 Descargando: {c_name} - {s_name}...")
        
        try:
            m = sb.matches(competition_id=c_id, season_id=s_id)
            m["competition_name"] = c_name
            all_matches.append(m)
        except Exception as e:
            pass

    if not all_matches:
        print("❌ No se pudieron descargar partidos.")
        return

    # Unimos todo
    matches = pd.concat(all_matches, ignore_index=True)

    # Filtramos solo los del Barça
    matches_barca = matches[
        (matches["home_team"] == "Barcelona") | 
        (matches["away_team"] == "Barcelona")
    ]
    
    print(f"\n✅ Total partidos del Barça encontrados: {len(matches_barca)}")
    
    tacticas_oficiales = []
    
    # 3. EXTRAER FORMACIONES
    total = len(matches_barca)
    
    for index, row in matches_barca.iterrows():
        match_id = row["match_id"]
        fecha = row["match_date"]
        rival = row["away_team"] if row["home_team"] == "Barcelona" else row["home_team"]
        competicion = row["competition_name"]
        
        try:
            # Descargamos eventos de alineación (Starting XI)
            events = sb.events(match_id=match_id)
            starting_xi = events[
                (events["type"] == "Starting XI") & 
                (events["team"] == "Barcelona")
            ]
            
            if not starting_xi.empty:
                # Extraer táctica (A veces es dict, a veces objeto)
                tactics_data = starting_xi.iloc[0]["tactics"]
                formacion_raw = "Desconocida"
                
                if isinstance(tactics_data, dict) and "formation" in tactics_data:
                    formacion_raw = tactics_data["formation"]
                
                # Guardamos el dato crudo, la limpieza va al final
                tacticas_oficiales.append({
                    "id_partido_sb": match_id,
                    "fecha": fecha,
                    "rival": rival,
                    "competicion": competicion,
                    "formacion_oficial": formacion_raw 
                })
                
        except Exception as e:
            pass

        # Barra de progreso
        if (index + 1) % 10 == 0:
            print(f"Procesados {index + 1}/{total} partidos...")

    # 4. LIMPIEZA Y GUARDADO
    if tacticas_oficiales:
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
            print(f"📂 Carpeta creada: {OUTPUT_FOLDER}")
            
        df_final = pd.DataFrame(tacticas_oficiales)
        
        # --- APLICANDO LA MAGIA DE LIMPIEZA ---
        print("\n🧹 Normalizando formaciones (41212 -> 4-1-2-1-2)...")
        df_final['formacion_oficial'] = df_final['formacion_oficial'].apply(normalizar_formacion)
        
        ruta_completa = os.path.join(OUTPUT_FOLDER, "Fact_Tacticas_Oficiales_SB.csv")
        
        df_final.to_csv(ruta_completa, index=False)
        
        print("\n" + "="*50)
        print(f"🎉 ¡ÉXITO TOTAL! Archivo extraído y limpio en:")
        print(f"👉 {ruta_completa}")
        print("="*50)
        print("Muestra de datos:")
        print(df_final["formacion_oficial"].value_counts().head())
    else:
        print("⚠️ No se extrajeron tácticas.")

if __name__ == "__main__":
    obtener_tacticas_statsbomb_final()