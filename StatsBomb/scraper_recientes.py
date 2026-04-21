# -*- coding: utf-8 -*-
import os
import time
from io import StringIO
import logging
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def extraer_tabla_general(html_source):
    # Desbloqueamos los comentarios por si acaso
    html_desbloqueado = html_source.replace('', '')
    soup = BeautifulSoup(html_desbloqueado, 'html.parser')
    
    tablas = soup.find_all('table')
    for t in tablas:
        try:
            df = pd.read_html(StringIO(str(t)), header=1)[0]
            # Si tiene Jugadores y Minutos, bingo.
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except:
            continue
    return None        

def eliminar_cabeceras_extra(df):
    serie = df.iloc[:,0].astype(str) == 'Rk'
    return df[~serie].reset_index(drop=True)

logging.info("Iniciando extracción final con el enlace maestro de la Champions 24/25...")

# ¡TU ENLACE!
url_victoria = "https://fbref.com/en/squads/206d90db/2024-2025/c8/Barcelona-Stats-Champions-League"

directorio = os.path.join('datos_fbref_estable', '2024-2025')
os.makedirs(directorio, exist_ok=True)

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.set_page_load_timeout(60)

try:
    driver.get(url_victoria)
    time.sleep(4) 
    
    html_crudo = driver.page_source
    tabla_jug = extraer_tabla_general(html_crudo)         
    
    if tabla_jug is not None:
        tabla_jug = eliminar_cabeceras_extra(tabla_jug)
        
        # Limpiamos las filas de totales por si FBref las incluye al final
        tabla_jug = tabla_jug[tabla_jug['Player'] != 'Squad Total']
        tabla_jug = tabla_jug[tabla_jug['Player'] != 'Opponent Total']
        
        # Le añadimos el nombre del equipo para mantener la estructura
        tabla_jug['Squad'] = 'Barcelona'
        
        if not tabla_jug.empty:
            ruta_jug = os.path.join(directorio, 'General_Champions_2024-2025.csv')
            tabla_jug.to_csv(ruta_jug, index=False, encoding='utf-8-sig')
            logging.info(f"    [ÉXITO TOTAL] ¡Conseguido! Guardados {len(tabla_jug)} jugadores.")
        else:
            logging.error("    [ERROR] La tabla se descargó vacía.")
    else:
        logging.error("    [FALLO] No se encontró la tabla General en la web.")

except Exception as e:
    logging.error(f"[ERROR CRÍTICO] {e}")
finally:
    driver.quit()

logging.info("¡Base de datos HISTÓRICA CERRADA!")