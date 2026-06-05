import pandas as pd
from statsbombpy import sb
import os
import warnings
import time

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
PATH_INPUT = r"C:\Users\enson\Desktop\TFG\ETL\DatosLaLiga2003_2021.csv"
PATH_OUTPUT = r"C:\Users\enson\Desktop\TFG\ETL\Metricas_Barca_LaLiga_Final.csv"
TARGET_TEAM = "Barcelona"

def calcular_metricas_agregadas_equipo(match_id, equipo_nombre):
    """
    Consume la API de StatsBomb para descargar los eventos granulares de un partido
    específico y calcula métricas agregadas a nivel de equipo, divididas en tres
    fases del juego: Ofensiva, Control (Posesión) y Defensiva.
    """
    try:
        # Petición a la API para obtener el DataFrame de eventos del partido
        df_eventos = sb.events(match_id=match_id)
        
        # Inicialización del diccionario de métricas. Se preasignan valores a cero
        # para garantizar la integridad estructural en caso de ausencia de datos.
        diccionario_metricas = {
            'goles_favor': 0,
            'xg_favor': 0.0,
            'xg_contra': 0.0,
            'tiros_totales': 0,
            'tiros_a_puerta': 0,
            'pases_intentados': 0,
            'pases_completados': 0,
            'posesion_pct': 0.0,
            'presiones': 0,
            'recuperaciones': 0,
            'intercepciones': 0,
            'faltas_cometidas': 0,
            'status': 'OK'
        }

        # Validación estructural: Si el DataFrame no contiene la columna 'team', 
        # carece de la granularidad necesaria para la agregación.
        if 'team' not in df_eventos.columns:
            return diccionario_metricas 

        # --- 1. MÉTRICAS OFENSIVAS ---
        if 'type' in df_eventos.columns and 'shot_outcome' in df_eventos.columns:
            df_tiros = df_eventos[(df_eventos['type'] == 'Shot') & (df_eventos['team'] == equipo_nombre)]
            
            # Volumen ofensivo bruto
            diccionario_metricas['tiros_totales'] = len(df_tiros)
            
            # Efectividad (Goles reales)
            diccionario_metricas['goles_favor'] = len(df_tiros[df_tiros['shot_outcome'] == 'Goal'])
            
            # Tiros a Puerta: Se agrupan los resultados que estadísticamente cuentan como tiro a puerta
            resultados_tiro_a_puerta = ['Goal', 'Saved', 'Saved to Post']
            diccionario_metricas['tiros_a_puerta'] = len(df_tiros[df_tiros['shot_outcome'].isin(resultados_tiro_a_puerta)])

            # Goles Esperados (xG): Métrica avanzada de probabilidad
            if 'shot_statsbomb_xg' in df_eventos.columns:
                df_xg = df_eventos[df_eventos['type'] == 'Shot'] 
                diccionario_metricas['xg_favor'] = df_xg[df_xg['team'] == equipo_nombre]['shot_statsbomb_xg'].fillna(0).sum()
                diccionario_metricas['xg_contra'] = df_xg[df_xg['team'] != equipo_nombre]['shot_statsbomb_xg'].fillna(0).sum()

        # --- 2. MÉTRICAS DE CONTROL (DISTRIBUCIÓN Y POSESIÓN) ---
        if 'type' in df_eventos.columns:
            df_pases = df_eventos[(df_eventos['type'] == 'Pass') & (df_eventos['team'] == equipo_nombre)]
            diccionario_metricas['pases_intentados'] = len(df_pases)
            
            if 'pass_outcome' in df_eventos.columns:
                # En StatsBomb, un 'pass_outcome' nulo (NaN) indica que el pase fue completado con éxito
                diccionario_metricas['pases_completados'] = len(df_pases[df_pases['pass_outcome'].isnull()])
            else:
                diccionario_metricas['pases_completados'] = len(df_pases)

            # Cálculo de posesión aproximada mediante volumen de pases relativos
            total_pases_partido = len(df_eventos[df_eventos['type'] == 'Pass'])
            if total_pases_partido > 0:
                diccionario_metricas['posesion_pct'] = round((diccionario_metricas['pases_intentados'] / total_pases_partido) * 100, 2)

        # --- 3. MÉTRICAS DEFENSIVAS (INTENSIDAD SIN BALÓN) ---
        if 'type' in df_eventos.columns:
            diccionario_metricas['presiones'] = len(df_eventos[(df_eventos['type'] == 'Pressure') & (df_eventos['team'] == equipo_nombre)])
            diccionario_metricas['recuperaciones'] = len(df_eventos[(df_eventos['type'] == 'Ball Recovery') & (df_eventos['team'] == equipo_nombre)])
            diccionario_metricas['intercepciones'] = len(df_eventos[(df_eventos['type'] == 'Interception') & (df_eventos['team'] == equipo_nombre)])
            diccionario_metricas['faltas_cometidas'] = len(df_eventos[(df_eventos['type'] == 'Foul Committed') & (df_eventos['team'] == equipo_nombre)])

        # Redondeo de métricas continuas para su exportación
        diccionario_metricas['xg_favor'] = round(diccionario_metricas['xg_favor'], 2)
        diccionario_metricas['xg_contra'] = round(diccionario_metricas['xg_contra'], 2)
        
        return diccionario_metricas

    except Exception as e:
        return {'status': 'ERROR', 'error_msg': str(e)}

def ejecutar_extraccion_metricas():
    """
    Orquesta la lectura del catálogo de partidos, itera sobre los encuentros 
    del equipo objetivo y anexa las métricas agregadas para generar el dataset final.
    """
    print("--- INICIANDO EXTRACCIÓN DE MÉTRICAS AGREGADAS (STATSBOMB API) ---")
    
    if not os.path.exists(PATH_INPUT):
        print(f"Error crítico: No se localizó el archivo de entrada en {PATH_INPUT}")
        return

    df_partidos = pd.read_csv(PATH_INPUT)
    
    # Filtrado del dataset para procesar únicamente los partidos del equipo objetivo
    df_partidos_objetivo = df_partidos[
        (df_partidos['home_team'] == TARGET_TEAM) | 
        (df_partidos['away_team'] == TARGET_TEAM)
    ].copy()
    
    total_partidos = len(df_partidos_objetivo)
    print(f"Info: Total de partidos a analizar: {total_partidos}")
    print("Iniciando agregación de volumen ofensivo, posesión y métricas defensivas...")

    lista_metricas_partidos = []
    
    for index, row in df_partidos_objetivo.iterrows():
        match_id = row['match_id']
        fecha = row['match_date']
        rival = row['away_team'] if row['home_team'] == TARGET_TEAM else row['home_team']
        
        print(f"Procesando [{len(lista_metricas_partidos)+1}/{total_partidos}] {fecha} vs {rival}...", end=" ")
        
        datos_agregados = calcular_metricas_agregadas_equipo(match_id, TARGET_TEAM)
        
        if datos_agregados['status'] == 'OK':
            print("Completado")
            fila_completa = row.to_dict()
            fila_completa.update(datos_agregados)
            lista_metricas_partidos.append(fila_completa)
        else:
            print(f"Fallo: {datos_agregados.get('error_msg')}")

    # Estructuración y guardado del conjunto de datos final
    if lista_metricas_partidos:
        df_resultado = pd.DataFrame(lista_metricas_partidos)
        
        # Ordenación semántica de las columnas para facilitar el análisis posterior
        cols_info = ['match_date', 'season', 'home_team', 'away_team', 'home_score', 'away_score']
        cols_ataque = ['goles_favor', 'xg_favor', 'xg_contra', 'tiros_totales', 'tiros_a_puerta']
        cols_control = ['posesion_pct', 'pases_intentados', 'pases_completados']
        cols_defensa = ['presiones', 'recuperaciones', 'intercepciones', 'faltas_cometidas']
        
        cols_ordenadas = cols_info + cols_ataque + cols_control + cols_defensa
        
        # Preservación de atributos adicionales inherentes a la fuente original
        otras_cols = [c for c in df_resultado.columns if c not in cols_ordenadas and c not in ['status', 'error_msg']]
        
        df_resultado = df_resultado[cols_ordenadas + otras_cols]
        
        df_resultado.to_csv(PATH_OUTPUT, index=False)
        print(f"\nProceso finalizado con éxito. Dataset consolidado guardado en: {PATH_OUTPUT}")
        print(f"Total de registros exportados: {len(df_resultado)}")
    else:
        print("Aviso: No se generaron métricas para exportar.")

if __name__ == "__main__":
    # Supresión de advertencias relacionadas con la obsolescencia de funciones internas de dependencias
    warnings.filterwarnings("ignore")
    ejecutar_extraccion_metricas()