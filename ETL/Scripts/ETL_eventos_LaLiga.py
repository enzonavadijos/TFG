import pandas as pd
from statsbombpy import sb
import os
import warnings
import time

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
PATH_INPUT = r"C:\Users\enson\Desktop\TFG\ETL\Metricas_FCB_LaLiga_Final.csv"
PATH_OUTPUT = r"C:\Users\enson\Desktop\TFG\ETL\Detalle_Eventos_LaLiga_Total.csv"
TARGET_TEAM = "Barcelona"

def extraer_cronologia_eventos(match_id, fecha_partido, rival):
    """
    Extrae la telemetría secuencial (Timeline) de un encuentro específico.
    Identifica la alineación titular y recupera eventos clave (Goles, Sustituciones, 
    Amonestaciones y Lesiones), cruzando la información con los dorsales oficiales.
    """
    lista_eventos_partido = []
    
    try:
        # 1. Extracción de alineaciones para mapeo de dorsales y titulares
        # Se requiere consultar el endpoint de alineaciones ANTES que el de eventos
        # para poder vincular posteriormente cada jugador con su dorsal correspondiente.
        diccionario_alineaciones = sb.lineups(match_id=match_id)
        diccionario_dorsales = {}
        
        # Procesamiento iterativo de ambos equipos para mantener el contexto global del partido
        for equipo in diccionario_alineaciones.keys():
            df_alineacion_equipo = diccionario_alineaciones[equipo]
            
            # Mapeo de identidad del jugador con su número de camiseta en ese encuentro
            for _, jugador in df_alineacion_equipo.iterrows():
                diccionario_dorsales[jugador['player_name']] = jugador['jersey_number']
                
            # Aislamiento de la alineación titular del equipo objetivo
            if equipo == TARGET_TEAM:
                # En la estructura de StatsBomb, un arreglo de 'positions' no vacío 
                # al inicio del partido garantiza posicionalmente que el jugador es titular.
                df_titulares = df_alineacion_equipo[df_alineacion_equipo['positions'].apply(lambda x: len(x) > 0)] 
                for _, titular in df_titulares.iterrows():
                    lista_eventos_partido.append({
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

        # 2. Descarga y procesamiento del registro granular de eventos
        df_eventos_partido = sb.events(match_id=match_id)
        
        # Filtrado secuencial de acciones clave a lo largo del tiempo reglamentario
        for i, row in df_eventos_partido.iterrows():
            tipo_evento = row['type']
            minuto_evento = row['minute']
            equipo_evento = row['team']
            nombre_jugador = row['player'] if 'player' in row else None
            
            # Omisión de eventos tácticos o contextuales que no están asociados a un jugador físico
            if pd.isna(nombre_jugador): 
                continue
            
            # Recuperación del dorsal; se asigna 0 como contingencia ante anomalías en el origen de datos
            dorsal_jugador = diccionario_dorsales.get(nombre_jugador, 0)
            
            # A) Evaluación de anotaciones (Goles)
            if tipo_evento == 'Shot' and row.get('shot_outcome') == 'Goal':
                lista_eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto_evento,
                    'equipo': equipo_evento,
                    'jugador': nombre_jugador,
                    'dorsal': dorsal_jugador,
                    'tipo_evento': 'GOL',
                    'detalle': f"Gol ({row.get('play_pattern', 'Desconocido')})"
                })
                
            # B) Evaluación de sustituciones técnicas o médicas
            elif tipo_evento == 'Substitution':
                jugador_entrante = row['substitution_replacement']
                dorsal_entrante = diccionario_dorsales.get(jugador_entrante, 0)
                
                # Desglose de la sustitución en dos eventos atómicos para facilitar el 
                # modelado analítico posterior.
                # 1. Evento de salida
                lista_eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto_evento,
                    'equipo': equipo_evento,
                    'jugador': nombre_jugador,
                    'dorsal': dorsal_jugador,
                    'tipo_evento': 'CAMBIO_SALE',
                    'detalle': f"Sale (Entra {jugador_entrante})"
                })
                # 2. Evento de entrada
                lista_eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto_evento,
                    'equipo': equipo_evento,
                    'jugador': jugador_entrante,
                    'dorsal': dorsal_entrante,
                    'tipo_evento': 'CAMBIO_ENTRA',
                    'detalle': f"Entra (Por {nombre_jugador})"
                })
                
            # C) Registro disciplinario (Amonestaciones y expulsiones)
            # El esquema interno de la API diversifica las tarjetas en base a si la 
            # infracción fue durante el juego (foul) o por mala conducta (bad behaviour).
            elif 'card' in row and pd.notnull(row.get('bad_behaviour_card')):
                lista_eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto_evento,
                    'equipo': equipo_evento,
                    'jugador': nombre_jugador,
                    'dorsal': dorsal_jugador,
                    'tipo_evento': 'TARJETA',
                    'detalle': row['bad_behaviour_card']
                })
            elif 'foul_committed_card' in row and pd.notnull(row.get('foul_committed_card')):
                lista_eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto_evento,
                    'equipo': equipo_evento,
                    'jugador': nombre_jugador,
                    'dorsal': dorsal_jugador,
                    'tipo_evento': 'TARJETA',
                    'detalle': row['foul_committed_card']
                })
            
            # D) Identificación de paradas médicas
            elif tipo_evento == 'Injury Stoppage':
                lista_eventos_partido.append({
                    'match_id': match_id,
                    'fecha': fecha_partido,
                    'rival': rival,
                    'minuto': minuto_evento,
                    'equipo': equipo_evento,
                    'jugador': nombre_jugador,
                    'dorsal': dorsal_jugador,
                    'tipo_evento': 'LESION',
                    'detalle': 'Juego detenido por lesión'
                })

        return lista_eventos_partido

    except Exception as e:
        print(f"Error crítico durante el procesamiento del partido ID {match_id}: {e}")
        return []

def ejecutar_extraccion_cronologica():
    """
    Orquesta la lectura de los metadatos base, itera sobre los identificadores de
    los partidos y consolida un único archivo relacional que define la línea temporal
    de eventos de cada enfrentamiento.
    """
    print("--- INICIANDO CONSOLIDACIÓN HISTÓRICA DE EVENTOS CRONOLÓGICOS ---")
    
    # 1. Validación e ingesta del modelo de datos de origen
    if not os.path.exists(PATH_INPUT):
        print(f"Error crítico: No se encuentra el archivo maestro en {PATH_INPUT}")
        return

    df_maestro_partidos = pd.read_csv(PATH_INPUT)
    
    # Reducción dimensional del DataFrame original para optimizar el consumo de RAM
    lista_metadatos_partidos = df_maestro_partidos[['match_id', 'match_date', 'away_team', 'home_team']].to_dict('records')
    
    print(f"Info: Objetivo fijado en la extracción paramétrica de {len(lista_metadatos_partidos)} partidos.")
    
    coleccion_eventos_global = []
    tiempo_inicio = time.time()

    # 2. Ciclo principal de procesamiento automatizado
    for index, partido in enumerate(lista_metadatos_partidos):
        match_id = partido['match_id']
        fecha_partido = partido['match_date']
        
        # Lógica de resolución del equipo adversario basándose en la localía
        rival = partido['away_team'] if partido['home_team'] == TARGET_TEAM else partido['home_team']
        
        print(f"Procesando [{index+1}/{len(lista_metadatos_partidos)}] Fecha: {fecha_partido} vs {rival}...", end=" ")
        
        eventos_extraidos = extraer_cronologia_eventos(match_id, fecha_partido, rival)
        
        if eventos_extraidos:
            coleccion_eventos_global.extend(eventos_extraidos)
            print(f"Completado ({len(eventos_extraidos)} registros)")
        else:
            print("Aviso: Registro sin incidencias contabilizadas.")

    # 3. Consolidación de datos tabulares y persistencia
    if coleccion_eventos_global:
        df_eventos_final = pd.DataFrame(coleccion_eventos_global)
        
        # Ordenamiento jerárquico: Cronología absoluta del calendario seguida de la evolución de minutos del juego
        df_eventos_final = df_eventos_final.sort_values(['fecha', 'minuto'])
        df_eventos_final.to_csv(PATH_OUTPUT, index=False, encoding='utf-8')
        
        tiempo_total = (time.time() - tiempo_inicio) / 60
        print("\n" + "="*60)
        print(f"PROCESO FINALIZADO EXITOSAMENTE (Tiempo de ejecución: {tiempo_total:.1f} minutos)")
        print(f"Ruta de exportación: {PATH_OUTPUT}")
        print(f"Volumen de registros generados: {len(df_eventos_final)} eventos.")
        print("="*60)
        print("Nota de Integración Analítica: Este dataset puede vincularse relacionalmente en Power BI mediante la clave primaria foránea 'match_id'.")
    else:
        print("Aviso: El proceso ha concluido sin generar extracción de datos.")

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    ejecutar_extraccion_cronologica()