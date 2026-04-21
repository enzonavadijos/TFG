# -*- coding: utf-8 -*-
import os
import glob
import time
from io import StringIO
import logging
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# ========================================================
# FASE 1: LA PURGA (Borrar archivos fantasma)
# ========================================================
directorio_base = 'datos_fbref_estable'
archivos_a_borrar = glob.glob(f'{directorio_base}/**/General_Supercopa_Europa_*.csv', recursive=True)

logging.info("--- INICIANDO FASE 1: LIMPIEZA DE FANTASMAS ---")
if not archivos_a_borrar:
    logging.info("No se encontraron archivos de Supercopa de Europa para borrar.")
else:
    for archivo in archivos_a_borrar:
        try:
            os.remove(archivo)
            logging.info(f"[ELIMINADO] {archivo}")
        except Exception as e:
            logging.error(f"No se pudo borrar {archivo}: {e}")

# ========================================================
# FASE 2: EXTRACCIÓN QUIRÚRGICA
# ========================================================
# Solo las 4 Supercopas de Europa reales y la Supercopa de España que falló
tareas_pendientes = [
    {"comp": "Supercopa_Europa", "temp": "2006-2007", "url": "https://fbref.com/en/squads/206d90db/2006-2007/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Europa", "temp": "2009-2010", "url": "https://fbref.com/en/squads/206d90db/2009-2010/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Europa", "temp": "2011-2012", "url": "https://fbref.com/en/squads/206d90db/2011-2012/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Europa", "temp": "2015-2016", "url": "https://fbref.com/en/squads/206d90db/2015-2016/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Espana", "temp": "2024-2025", "url": "https://fbref.com/en/squads/206d90db/2024-2025/c646/Barcelona-Stats-Supercopa-de-Espana"}
]

def extraer_tabla_general(html_source):
    html_desbloqueado = html_source.replace('', '')
    soup = BeautifulSoup(html_desbloqueado, 'html.parser')
    tablas = soup.find_all('table')
    for t in tablas:
        try:
            df = pd.read_html(StringIO(str(t)), header=1)[0]
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except:
            continue
    return None        

def limpiar_tabla(df):
    serie = df.iloc[:,0].astype(str) == 'Rk'
    df = df[~serie].reset_index(drop=True)
    df = df[df['Player'] != 'Squad Total']
    df = df[df['Player'] != 'Opponent Total']
    df['Squad'] = 'Barcelona'
    return df

logging.info("\n--- INICIANDO FASE 2: RESCATE DE DATOS ---")

options = uc.ChromeOptions()
options.page_load_strategy = 'eager' # Modo ultrarrápido anti-timeouts
driver = uc.Chrome(options=options)
driver.set_page_load_timeout(20)

try:
    for tarea in tareas_pendientes:
        nombre_comp = tarea["comp"]
        temporada = tarea["temp"]
        url = tarea["url"]
        
        logging.info(f" -> Atacando {nombre_comp} de la {temporada}...")
        
        directorio = os.path.join(directorio_base, temporada)
        os.makedirs(directorio, exist_ok=True)
        
        html_crudo = ""
        try:
            driver.get(url)
            time.sleep(2.5) 
            html_crudo = driver.page_source
        except TimeoutException:
            logging.warning(f"    [AVISO] Timeout. Robando HTML cargado...")
            html_crudo = driver.page_source
        except Exception as e:
            logging.error(f"    [ERROR DE RED] {e}")
            continue
            
        if html_crudo:
            tabla_jug = extraer_tabla_general(html_crudo)         
            if tabla_jug is not None:
                tabla_jug = limpiar_tabla(tabla_jug)
                if not tabla_jug.empty:
                    ruta_jug = os.path.join(directorio, f'General_{nombre_comp}_{temporada}.csv')
                    tabla_jug.to_csv(ruta_jug, index=False, encoding='utf-8-sig')
                    logging.info(f"    [ÉXITO] Guardados {len(tabla_jug)} jugadores en {nombre_comp} {temporada}.")
            else:
                logging.warning(f"    [FALLO] No se encontró la tabla.")
        time.sleep(1.5)

except Exception as e:
    logging.error(f"[CRASHEO CRÍTICO] {e}")
finally:
    driver.quit()

logging.info("\n¡Casa limpia y datos asegurados!")