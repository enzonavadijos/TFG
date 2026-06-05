import requests
import pandas as pd

# --- CONFIGURACIÓN DE ENDPOINTS ---
# Repositorio estático (Open Data) de StatsBomb en GitHub
URL_COMPETICIONES = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json"

print("--- INICIANDO INGESTA DE DATOS (API STATSBOMB) ---")
print("Info: Solicitando el catálogo general de competiciones...")

# Ingesta del catálogo maestro en formato JSON
competiciones = requests.get(URL_COMPETICIONES).json()

# Filtrado dimensional (Scope analítico)
# Se aíslan los identificadores correspondientes a LaLiga (11) y Champions League (16)
temporadas_objetivo = [
    comp for comp in competiciones 
    if comp['competition_id'] in [11, 16]
]

coleccion_partidos_historicos = []

print(f"Info: Detectadas {len(temporadas_objetivo)} temporadas objetivo. Iniciando descarga granular...")

# Iteración secuencial para la ingesta de los registros de partido por temporada
for comp in temporadas_objetivo:
    comp_id = comp['competition_id']
    season_id = comp['season_id']
    
    # Construcción dinámica del endpoint para la temporada específica
    url_partidos = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/{comp_id}/{season_id}.json"
    respuesta = requests.get(url_partidos)
    
    # Validación de respuesta HTTP exitosa
    if respuesta.status_code == 200:
        partidos = respuesta.json()
        coleccion_partidos_historicos.extend(partidos)

print("Info: Aplicando aplanamiento estructural (Flattening) al modelo JSON jerárquico...")

# Transformación de modelo documental (JSON anidado) a modelo tabular desnormalizado.
# pd.json_normalize resuelve la profundidad de atributos (ej. home_team.home_team_name).
df_partidos = pd.json_normalize(coleccion_partidos_historicos)

# Persistencia del modelo analítico
nombre_archivo = "Partidos_StatsBomb.csv"
# Se emplea utf-8-sig para garantizar la integridad de caracteres especiales en herramientas BI
df_partidos.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')

print(f"\nProceso finalizado exitosamente. Tabla de hechos consolidada.")
print(f"Volumen de registros extraídos: {len(df_partidos)} encuentros.")
print(f"Ruta de destino local: {nombre_archivo}")