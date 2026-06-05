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

# --- CONFIGURACIÓN DEL SISTEMA DE AUDITORÍA (LOGGING) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ETL] - %(message)s')

# ========================================================
# FASE 1: SANEAMIENTO DEL DIRECTORIO LOCAL (PURGA DE ARCHIVOS RESIDUALES)
# ========================================================
DIR_BASE_DATOS = 'datos_fbref_estable'
# Búsqueda recursiva de archivos correspondientes a ejecuciones previas anómalas
archivos_residuales = glob.glob(f'{DIR_BASE_DATOS}/**/General_Supercopa_Europa_*.csv', recursive=True)

logging.info("--- INICIANDO FASE 1: SANEAMIENTO DE ARCHIVOS RESIDUALES ---")
if not archivos_residuales:
    logging.info("Auditoría completada: No se detectaron archivos residuales de la Supercopa de Europa.")
else:
    for archivo in archivos_residuales:
        try:
            os.remove(archivo)
            logging.info(f"[ELIMINADO] Archivo residual purgado: {archivo}")
        except Exception as e:
            logging.error(f"[ERROR DE SISTEMA] No se pudo eliminar el archivo {archivo}: {e}")

# ========================================================
# FASE 2: EXTRACCIÓN SELECTIVA (RESOLUCIÓN DE EXCEPCIONES)
# ========================================================
# Catálogo acotado a las ediciones específicas no capturadas en ejecuciones masivas previas
lote_excepciones_objetivo = [
    {"comp": "Supercopa_Europa", "temp": "2006-2007", "url": "https://fbref.com/en/squads/206d90db/2006-2007/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Europa", "temp": "2009-2010", "url": "https://fbref.com/en/squads/206d90db/2009-2010/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Europa", "temp": "2011-2012", "url": "https://fbref.com/en/squads/206d90db/2011-2012/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Europa", "temp": "2015-2016", "url": "https://fbref.com/en/squads/206d90db/2015-2016/c122/Barcelona-Stats-UEFA-Super-Cup"},
    {"comp": "Supercopa_Espana", "temp": "2024-2025", "url": "https://fbref.com/en/squads/206d90db/2024-2025/c646/Barcelona-Stats-Supercopa-de-Espana"}
]

def preprocesar_y_extraer_tabla(html_source):
    """
    Subrutina de extracción. Aplica preprocesamiento eliminando etiquetas 
    de comentarios para exponer las estructuras tabulares secundarias en el DOM.
    """
    html_expuesto = html_source.replace('', '')
    soup = BeautifulSoup(html_expuesto, 'html.parser')
    tablas_dom = soup.find_all('table')
    
    for tabla in tablas_dom:
        try:
            df = pd.read_html(StringIO(str(tabla)), header=1)[0]
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except Exception:
            continue
    return None        

def normalizar_esquema_estadisticas(df):
    """
    Depura el DataFrame eliminando filas de agregación y encabezados residuales.
    Inyecta la dimensión del equipo.
    """
    filtro_encabezados = df.iloc[:, 0].astype(str) == 'Rk'
    df_limpio = df[~filtro_encabezados].reset_index(drop=True)
    df_limpio = df_limpio[df_limpio['Player'] != 'Squad Total']
    df_limpio = df_limpio[df_limpio['Player'] != 'Opponent Total']
    df_limpio['Squad'] = 'Barcelona'
    return df_limpio

logging.info("\n--- INICIANDO FASE 2: EXTRACCIÓN Y RECUPERACIÓN DE DATOS ---")

opciones_navegador = uc.ChromeOptions()
# Estrategia 'eager': El WebDriver no espera la carga de recursos bloqueantes (CSS/JS pesado).
# Optimiza el tiempo de ejecución y mitiga bloqueos de red.
opciones_navegador.page_load_strategy = 'eager' 
driver = uc.Chrome(options=opciones_navegador)
# Reducción drástica del timeout máximo a 20 segundos para forzar la tolerancia a fallos
driver.set_page_load_timeout(20)

try:
    for tarea in lote_excepciones_objetivo:
        nombre_competicion = tarea["comp"]
        temporada = tarea["temp"]
        url_objetivo = tarea["url"]
        
        logging.info(f" -> Procesando dominio analítico: {nombre_competicion} ({temporada})...")
        
        directorio_destino = os.path.join(DIR_BASE_DATOS, temporada)
        os.makedirs(directorio_destino, exist_ok=True)
        
        html_crudo = ""
        try:
            driver.get(url_objetivo)
            time.sleep(2.5) 
            html_crudo = driver.page_source
        except TimeoutException:
            # Tolerancia a fallos: Recuperación asíncrona del DOM parcial si se excede el límite de tiempo
            logging.warning(f"    [AVISO] Timeout excedido. Ejecutando extracción sobre el DOM renderizado parcialmente...")
            html_crudo = driver.page_source
        except Exception as e:
            logging.error(f"    [ERROR DE RED] Fallo en la petición HTTP: {e}")
            continue
            
        if html_crudo:
            df_estadisticas = preprocesar_y_extraer_tabla(html_crudo)        
            if df_estadisticas is not None:
                df_estadisticas = normalizar_esquema_estadisticas(df_estadisticas)
                
                if not df_estadisticas.empty:
                    ruta_salida = os.path.join(directorio_destino, f'General_{nombre_competicion}_{temporada}.csv')
                    df_estadisticas.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
                    logging.info(f"    [ÉXITO] Persistencia completada: {len(df_estadisticas)} entidades procesadas en {nombre_competicion} {temporada}.")
            else:
                logging.warning(f"    [ANOMALÍA] Matriz de datos no localizada en el documento.")
        
        # Latencia operativa para evitar bloqueos por Rate Limiting
        time.sleep(1.5)

except Exception as e:
    logging.error(f"[EXCEPCIÓN CRÍTICA DE ORQUESTACIÓN] {e}")
finally:
    driver.quit()

logging.info("\nOperaciones de mantenimiento y extracción selectiva finalizadas con éxito.")