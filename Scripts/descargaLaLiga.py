import os
import pandas as pd
from statsbombpy import sb
import warnings

# Configuracion de rutas y archivos
OUTPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\ETL"
OUTPUT_FILENAME = "DatosLaLiga2003_2021.csv"
FULL_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)

# Configuracion de la competicion
LIGA_ID = 11  # ID de La Liga en StatsBomb
START_YEAR = 2003
END_YEAR = 2021

def main():
    print("Iniciando proceso de descarga de La Liga...")
    
    # 1. Crear directorio si no existe
    if not os.path.exists(OUTPUT_FOLDER):
        print(f"Creando carpeta: {OUTPUT_FOLDER}")
        os.makedirs(OUTPUT_FOLDER)

    # 2. Obtener catalogo de competiciones
    print("Consultando temporadas disponibles en StatsBomb...")
    competitions = sb.competitions()
    
    # Filtrar solo La Liga
    laliga_comps = competitions[competitions['competition_id'] == LIGA_ID]
    
    if laliga_comps.empty:
        print("Error: No se encontraron datos de La Liga (ID 11).")
        return

    # 3. Filtrar temporadas por rango de anos
    target_seasons = []
    
    for index, row in laliga_comps.iterrows():
        season_name = row['season_name'] # Formato "2010/2011"
        season_id = row['season_id']
        
        try:
            # Extraer el ano de inicio de la temporada
            s_start = int(season_name.split('/')[0])
            s_end = int(season_name.split('/')[1])
            
            # Logica de filtrado: Entre 2003 y 2021 (inclusive final de temporada)
            if s_start >= START_YEAR and s_end <= END_YEAR:
                target_seasons.append((season_id, season_name))
                
        except ValueError:
            continue

    # Ordenar temporadas cronologicamente
    target_seasons.sort(key=lambda x: x[1])

    print(f"Se han encontrado {len(target_seasons)} temporadas en el rango {START_YEAR}-{END_YEAR}.")

    # 4. Descargar partidos
    all_matches = []
    
    for season_id, season_name in target_seasons:
        print(f"Descargando partidos de la temporada {season_name}...")
        
        try:
            matches = sb.matches(competition_id=LIGA_ID, season_id=season_id)
            
            # Anadir columna para identificar la temporada facilmente si no existe
            if 'season' not in matches.columns:
                matches['season'] = season_name
                
            all_matches.append(matches)
            
        except Exception as e:
            print(f"Error descargando temporada {season_name}: {e}")

    # 5. Guardar archivo unificado
    if all_matches:
        print("Unificando datos...")
        master_df = pd.concat(all_matches, ignore_index=True)
        
        print(f"Guardando archivo en: {FULL_PATH}")
        master_df.to_csv(FULL_PATH, index=False)
        
        print("Proceso finalizado correctamente.")
        print(f"Total de partidos descargados: {len(master_df)}")
    else:
        print("No se han descargado datos. Verifica la conexion o los filtros.")

if __name__ == "__main__":
    # Suprimir advertencias de credenciales (StatsBomb Open Data)
    warnings.filterwarnings("ignore")
    main()