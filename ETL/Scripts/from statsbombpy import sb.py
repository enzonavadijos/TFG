from statsbombpy import sb
import pandas as pd
import os
import time

print("--- 🚜 INICIANDO LA GRAN RECOLECCIÓN (ESTO TARDARÁ UN POCO) ---")

# IDs de competiciones en StatsBomb
COMPETICIONES_OBJETIVO = {
    11: "La Liga",
    16: "Champions League",
    37: "Copa del Rey"
}

todos_los_partidos = []
total_encontrados = 0

# 1. Obtenemos el catálogo de qué temporadas existen
print("📚 Consultando catálogo de StatsBomb...")
todas_competiciones = sb.competitions()

# 2. Bucle Maestro
for comp_id, comp_nombre in COMPETICIONES_OBJETIVO.items():
    print(f"\n--- Analizando: {comp_nombre} ---")
    
    # Filtramos las temporadas disponibles para esa liga/copa
    temporadas = todas_competiciones[todas_competiciones['competition_id'] == comp_id]
    
    if temporadas.empty:
        print(f"   (No hay datos Open Data para {comp_nombre})")
        continue

    # Recorremos cada temporada (ej: 2010/2011, 2011/2012...)
    for index, row in temporadas.iterrows():
        season_id = row['season_id']
        season_name = row['season_name']
        
        try:
            print(f"   ⬇️ Descargando temporada {season_name}...", end=" ")
            
            # Descargamos los partidos de ese año
            matches = sb.matches(competition_id=comp_id, season_id=season_id)
            
            # Ajuste de columnas dinámico (por si cambian de nombre)
            col_local = 'home_team' if 'home_team' in matches.columns else 'home_team_name'
            col_visitante = 'away_team' if 'away_team' in matches.columns else 'away_team_name'

            # Filtramos SOLO BARÇA
            barca_games = matches[
                (matches[col_local] == "Barcelona") | 
                (matches[col_visitante] == "Barcelona")
            ]
            
            if not barca_games.empty:
                # Añadimos una columna extra para saber de qué competi es
                barca_games['competicion_nombre'] = comp_nombre
                
                todos_los_partidos.append(barca_games)
                num = len(barca_games)
                total_encontrados += num
                print(f"✅ {num} partidos encontrados.")
            else:
                print("⚪ (El Barça no jugó o no hay datos)")
                
            # Pequeña pausa para no saturar y que no nos bloqueen
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error en {season_name}: {e}")

# 3. Guardado Final
print("\n------------------------------------------------")
if todos_los_partidos:
    print("💾 Unificando todos los archivos...")
    df_master = pd.concat(todos_los_partidos, ignore_index=True)
    
    # Crear carpeta si no existe
    os.makedirs('data', exist_ok=True)
    
    # Guardar en CSV
    nombre_archivo = 'data/MASTER_PARTIDOS_BARCA_STATSBOMB.csv'
    df_master.to_csv(nombre_archivo, index=False)
    
    print(f"🎉 ¡MISIÓN CUMPLIDA! Se ha generado el archivo maestro.")
    print(f"📂 Ruta: {nombre_archivo}")
    print(f"📊 Total de partidos recuperados: {len(df_master)}")
    print("------------------------------------------------")
    print("NOTA: Recuerda que StatsBomb Open Data tiene mayormente La Liga.")
    print("Para Champions completas y años recientes, usaremos FBref en el siguiente paso.")
else:
    print("⚠️ No se encontraron partidos. Algo raro pasa.")