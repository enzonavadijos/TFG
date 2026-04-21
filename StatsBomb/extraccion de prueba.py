from statsbombpy import sb
import os
import time

# Tu ruta exacta a una CARPETA NUEVA Y VACÍA
carpeta_destino = r"C:\Users\Enzo\OneDrive\Escritorio\Universidad\TFG\StatsBombMessi"
os.makedirs(carpeta_destino, exist_ok=True)

print("Iniciando conexión con StatsBomb Open Data...")
laliga = sb.competitions()[sb.competitions()['competition_id'] == 11]

for index, row in laliga.iterrows():
    season_id = row['season_id']
    season_name = row['season_name']
    print(f"\n--- Procesando temporada: {season_name} ---")
    
    try:
        partidos = sb.matches(competition_id=11, season_id=season_id)
        partidos_barca = partidos[(partidos['home_team'] == 'Barcelona') | (partidos['away_team'] == 'Barcelona')]
        
        for match_id in partidos_barca['match_id']:
            archivo_salida = os.path.join(carpeta_destino, f"Evento_{match_id}.csv")
            
            # Si el archivo ya existe, lo salta (Antifallos)
            if os.path.exists(archivo_salida):
                continue
                
            print(f"Descargando partido ID: {match_id}...")
            try:
                eventos = sb.events(match_id=match_id)
                # Le añadimos el contexto
                eventos['match_id'] = match_id
                eventos['season_name'] = season_name
                
                # Lo guarda en su propio archivo
                eventos.to_csv(archivo_salida, index=False)
                time.sleep(1.5)
            except Exception as e:
                print(f"❌ Error descargando {match_id}: {e}")
                time.sleep(3)
    except Exception as e:
        print(f"❌ ¡ALERTA FATAL! Falló la extracción de la temporada {season_name}. Error: {e}")

print("\n✅ ¡EXTRACCIÓN POR ARCHIVOS COMPLETADA!")