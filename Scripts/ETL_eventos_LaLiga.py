import pandas as pd
from statsbombpy import sb
import os
import warnings
import time

# --- CONFIGURACIÓN ---
INPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\Metricas_FCB_LaLiga_Final.csv"
OUTPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\Detalle_Eventos_LaLiga_Total.csv"
EQUIPO_OBJETIVO = "Barcelona"

def extraer_detalle_partido(match_id, fecha_partido, rival):
    """
    Extrae la cronología (Timeline) de un partido: Titulares, Goles, Cambios, Tarjetas.
    """
    eventos_partido = []
    
    try:
        # 1. Obtener Alineaciones (Para saber titulares y dorsales)
        lineups = sb.lineups(match_id=match_id)
        
        # Diccionario para guardar dorsales {Nombre: Numero}
        dorsales_map = {}
        
        # Procesamos ambos equipos para tener el contexto completo
        for equipo in lineups.keys():
            df_lineup = lineups[equipo]
            # Guardamos dorsales
            for _, player in df_lineup.iterrows():
                dorsales_map[player['player_name']] = player['jersey_number']
                
            # Si es el Barça, guardamos los titulares como evento minuto 0
            if equipo == EQUIPO_OBJETIVO:
                titulares = df_lineup[df_lineup['positions'].apply(lambda x: len(x) > 0)] # Los que tienen posición son titulares
                for _, titular in titulares.iterrows():
                    eventos_partido.append({
                        'match_id': match_id,
                        'fecha': fecha_partido,
                        'rival': rival,
                        'minuto': 0,
                        'equipo': equipo,
                        'jugador': titular['player_name'],
                        'dorsal': titular['jersey_number'],
                        'tipo_evento': 'TITULAR',
                        'detalle': 'Alineación Inicial'
                    })

        # 2. Descargar Eventos del Partido
        events = sb.events(match_id=match_id)
        
        # Filtramos eventos clave cronológicos
        for i, row in events.iterrows():
            tipo = row['type']
            minuto = row['minute']
            equipo = row['team']
            jugador = row['player'] if 'player' in row else None
            
            # Solo nos interesan eventos con jugador identificado
            if pd.isna(jugador): continue
            
            # Recuperar dorsal
            dorsal = dorsales_map.get(jugador, 0)
            
            # A) GOLES
            if tipo == 'Shot' and row['shot_outcome'] == 'Goal':
                eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto,
                    'equipo': equipo,
                    'jugador': jugador,
                    'dorsal': dorsal,
                    'tipo_evento': 'GOL',
                    'detalle': f"Gol ({row['play_pattern']})"
                })
                
            # B) CAMBIOS
            elif tipo == 'Substitution':
                entra = row['substitution_replacement']
                dorsal_entra = dorsales_map.get(entra, 0)
                
                # Evento SALE
                eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto,
                    'equipo': equipo,
                    'jugador': jugador,
                    'dorsal': dorsal,
                    'tipo_evento': 'CAMBIO_SALE',
                    'detalle': f"Sale (Entra {entra})"
                })
                # Evento ENTRA
                eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto,
                    'equipo': equipo,
                    'jugador': entra,
                    'dorsal': dorsal_entra,
                    'tipo_evento': 'CAMBIO_ENTRA',
                    'detalle': f"Entra (Por {jugador})"
                })
                
            # C) TARJETAS (Buscamos en columnas de faltas o mala conducta)
            elif 'card' in row and pd.notnull(row.get('bad_behaviour_card', None)):
                eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto,
                    'equipo': equipo,
                    'jugador': jugador,
                    'dorsal': dorsal,
                    'tipo_evento': 'TARJETA',
                    'detalle': row['bad_behaviour_card'] # Yellow / Red
                })
            elif 'foul_committed_card' in row and pd.notnull(row.get('foul_committed_card', None)):
                eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto,
                    'equipo': equipo,
                    'jugador': jugador,
                    'dorsal': dorsal,
                    'tipo_evento': 'TARJETA',
                    'detalle': row['foul_committed_card']
                })
            
            # D) LESIONES (Importante para ver historial médico)
            elif tipo == 'Injury Stoppage':
                eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto,
                    'equipo': equipo,
                    'jugador': jugador,
                    'dorsal': dorsal,
                    'tipo_evento': 'LESION',
                    'detalle': 'Juego detenido por lesión'
                })

        return eventos_partido

    except Exception as e:
        print(f"⚠️ Error en match {match_id}: {e}")
        return []

def main():
    print("--- 🏗️ INICIANDO GENERACIÓN DE HISTORIAL DE EVENTOS ---")
    
    # 1. Cargar el Master Dataset para obtener los IDs
    if not os.path.exists(INPUT_FILE):
        print(f"Error: No encuentro el archivo maestro {INPUT_FILE}")
        return

    df_master = pd.read_csv(INPUT_FILE)
    
    # Optimizacion: Solo necesitamos ID, Fecha y Rival para contexto
    lista_partidos = df_master[['match_id', 'match_date', 'away_team', 'home_team']].to_dict('records')
    
    print(f"Objetivo: Extraer detalle de {len(lista_partidos)} partidos.")
    print("Se generará un único archivo CSV consolidado.")
    
    todos_los_eventos = []
    start_time = time.time()

    # 2. Bucle de extracción
    for i, partido in enumerate(lista_partidos):
        match_id = partido['match_id']
        fecha = partido['match_date']
        # Identificar rival (el que no sea el Barça)
        rival = partido['away_team'] if partido['home_team'] == EQUIPO_OBJETIVO else partido['home_team']
        
        print(f"[{i+1}/{len(lista_partidos)}] {fecha} vs {rival}...", end=" ")
        
        eventos = extraer_detalle_partido(match_id, fecha, rival)
        
        if eventos:
            todos_los_eventos.extend(eventos)
            print(f"✅ ({len(eventos)} evts)")
        else:
            print("❌ Sin datos")

    # 3. Guardado
    if todos_los_eventos:
        df_final = pd.DataFrame(todos_los_eventos)
        
        # Ordenamos por Fecha -> Minuto -> Tipo
        df_final = df_final.sort_values(['fecha', 'minuto'])
        
        df_final.to_csv(OUTPUT_FILE, index=False)
        
        minutes = (time.time() - start_time) / 60
        print("\n------------------------------------------------")
        print(f"🚀 PROCESO FINALIZADO en {minutes:.1f} minutos.")
        print(f"Archivo generado: {OUTPUT_FILE}")
        print(f"Total de líneas de detalle: {len(df_final)}")
        print("------------------------------------------------")
        print("💡 TIP POWER BI: Conecta este archivo con el de Métricas usando 'match_id'.")
    else:
        print("No se generaron datos.")

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()