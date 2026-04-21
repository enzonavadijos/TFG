import pandas as pd
from statsbombpy import sb
import os
import warnings
import time

# --- CONFIGURACION ---
INPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\DatosLaLiga2003_2021.csv"
OUTPUT_FILE = r"C:\Users\enson\Desktop\TFG\ETL\Metricas_Barca_LaLiga_Final.csv"
EQUIPO_OBJETIVO = "Barcelona"

def calcular_metricas_equipo(match_id, equipo_nombre):
    """
    Calcula metricas colectivas (Ofensivas, Defensivas y de Control).
    """
    try:
        events = sb.events(match_id=match_id)
        
        # Inicializamos todo a 0 para evitar errores si faltan datos
        metrics = {
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

        # SI NO HAY COLUMNA 'TEAM', ES UN ERROR CRITICO DEL DATAFRAME
        if 'team' not in events.columns:
            return metrics # Retorna todo a 0 pero con status OK

        # --- 1. METRICAS OFENSIVAS ---
        if 'type' in events.columns and 'shot_outcome' in events.columns:
            tiros = events[(events['type'] == 'Shot') & (events['team'] == equipo_nombre)]
            
            # Volumen
            metrics['tiros_totales'] = len(tiros)
            
            # Goles
            metrics['goles_favor'] = len(tiros[tiros['shot_outcome'] == 'Goal'])
            
            # Tiros a Puerta (Goal + Saved + Saved to Post)
            # Nota: StatsBomb distingue muchos tipos de outcome. Simplificamos.
            outcome_a_puerta = ['Goal', 'Saved', 'Saved to Post']
            metrics['tiros_a_puerta'] = len(tiros[tiros['shot_outcome'].isin(outcome_a_puerta)])

            # xG
            if 'shot_statsbomb_xg' in events.columns:
                xg_data = events[events['type'] == 'Shot'] # Recuperamos todos para sacar a favor y contra
                metrics['xg_favor'] = xg_data[xg_data['team'] == equipo_nombre]['shot_statsbomb_xg'].fillna(0).sum()
                metrics['xg_contra'] = xg_data[xg_data['team'] != equipo_nombre]['shot_statsbomb_xg'].fillna(0).sum()

        # --- 2. METRICAS DE CONTROL (PASES) ---
        if 'type' in events.columns:
            pases = events[(events['type'] == 'Pass') & (events['team'] == equipo_nombre)]
            metrics['pases_intentados'] = len(pases)
            
            if 'pass_outcome' in events.columns:
                # pass_outcome NaN significa pase bueno
                metrics['pases_completados'] = len(pases[pases['pass_outcome'].isnull()])
            else:
                metrics['pases_completados'] = len(pases)

            # Posesion aproximada
            total_pases_partido = len(events[events['type'] == 'Pass'])
            if total_pases_partido > 0:
                metrics['posesion_pct'] = round((metrics['pases_intentados'] / total_pases_partido) * 100, 2)

        # --- 3. METRICAS DEFENSIVAS (EL SELLO DE IDENTIDAD) ---
        # Estas metricas definen la intensidad del equipo
        if 'type' in events.columns:
            # Presion alta (Pressure)
            metrics['presiones'] = len(events[(events['type'] == 'Pressure') & (events['team'] == equipo_nombre)])
            
            # Recuperaciones (Ball Recovery)
            metrics['recuperaciones'] = len(events[(events['type'] == 'Ball Recovery') & (events['team'] == equipo_nombre)])
            
            # Intercepciones (Interception)
            metrics['intercepciones'] = len(events[(events['type'] == 'Interception') & (events['team'] == equipo_nombre)])
            
            # Faltas (Foul Committed)
            metrics['faltas_cometidas'] = len(events[(events['type'] == 'Foul Committed') & (events['team'] == equipo_nombre)])

        # Redondeos finales
        metrics['xg_favor'] = round(metrics['xg_favor'], 2)
        metrics['xg_contra'] = round(metrics['xg_contra'], 2)
        
        return metrics

    except Exception as e:
        return {'status': 'ERROR', 'error_msg': str(e)}

def main():
    print("--- INICIANDO EXTRACTOR DE METRICAS DE EQUIPO (BARCA TOTAL) ---")
    
    if not os.path.exists(INPUT_FILE):
        print(f"Error: No encuentro el archivo {INPUT_FILE}")
        return

    df_matches = pd.read_csv(INPUT_FILE)
    
    # Filtrar solo Barcelona
    df_barca = df_matches[
        (df_matches['home_team'] == EQUIPO_OBJETIVO) | 
        (df_matches['away_team'] == EQUIPO_OBJETIVO)
    ].copy()
    
    print(f"Total partidos a analizar: {len(df_barca)}")
    print("Extrayendo: Tiros, Pases, Presion, Recuperaciones, Faltas...")

    metricas_list = []
    start_time = time.time()

    for index, row in df_barca.iterrows():
        match_id = row['match_id']
        fecha = row['match_date']
        rival = row['away_team'] if row['home_team'] == EQUIPO_OBJETIVO else row['home_team']
        
        print(f"[{index+1}/{len(df_matches)}] {fecha} vs {rival}...", end=" ")
        
        datos = calcular_metricas_equipo(match_id, EQUIPO_OBJETIVO)
        
        if datos['status'] == 'OK':
            print("✅")
            fila_completa = row.to_dict()
            fila_completa.update(datos)
            metricas_list.append(fila_completa)
        else:
            print(f"{datos.get('error_msg')}")

    # Guardado final
    if metricas_list:
        df_final = pd.DataFrame(metricas_list)
        
        # Ordenamos columnas logicamente
        cols_info = ['match_date', 'season', 'home_team', 'away_team', 'home_score', 'away_score']
        cols_ataque = ['goles_favor', 'xg_favor', 'xg_contra', 'tiros_totales', 'tiros_a_puerta']
        cols_control = ['posesion_pct', 'pases_intentados', 'pases_completados']
        cols_defensa = ['presiones', 'recuperaciones', 'intercepciones', 'faltas_cometidas']
        
        # Construimos la lista de columnas forzando el orden
        cols_final = cols_info + cols_ataque + cols_control + cols_defensa
        
        # Anadimos cualquier otra columna que pudiera haber en el original (ids, etc)
        otras_cols = [c for c in df_final.columns if c not in cols_final and c != 'status' and c != 'error_msg']
        
        df_final = df_final[cols_final + otras_cols]
        
        df_final.to_csv(OUTPUT_FILE, index=False)
        print(f"\nPROCESO FINALIZADO. Dataset guardado en: {OUTPUT_FILE}")
        print(f"Partidos procesados: {len(df_final)}")
    else:
        print("No se pudieron extraer metricas.")

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    main()