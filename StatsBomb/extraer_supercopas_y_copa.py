# -*- coding: utf-8 -*-
import os
import time
from io import StringIO
import logging
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN DEL SISTEMA DE AUDITORÍA (LOGGING) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [ETL] - %(message)s')

# --- CONFIGURACIÓN DE ENDPOINTS Y ALCANCE TEMPORAL ---
# Catálogo de URIs parametrizadas para competiciones de formato copa/torneo corto
ENDPOINTS_COMPETICIONES = {
    "CopaDelRey": "https://fbref.com/en/squads/206d90db/{temporada}/c569/Barcelona-Stats-Copa-del-Rey",
    "Supercopa_Espana": "https://fbref.com/en/squads/206d90db/{temporada}/c646/Barcelona-Stats-Supercopa-de-Espana",
    "Supercopa_Europa": "https://fbref.com/en/squads/206d90db/{temporada}/c122/Barcelona-Stats-UEFA-Super-Cup"
}

# Generación dinámica del rango cronológico de estudio (Descendente: 2024-2025 hasta 2003-2004)
RANGO_TEMPORADAS = [f"{anyo}-{anyo+1}" for anyo in range(2024, 2002, -1)]
DIR_OUTPUT_BASE = "datos_fbref_estable"

def preprocesar_y_extraer_tabla(html_source):
    """
    Subrutina de extracción de datos incrustados.
    Aplica un preprocesamiento del código fuente (eliminación de etiquetas de comentario HTML)
    para exponer matrices de datos secundarias ocultas en el DOM, permitiendo su parseo tabular.
    """
    html_expuesto = html_source.replace('<!--', '').replace('-->', '')
    soup = BeautifulSoup(html_expuesto, 'html.parser')
    
    tablas_dom = soup.find_all('table')
    for tabla in tablas_dom:
        try:
            # Ingesta en memoria optimizada mediante StringIO
            df = pd.read_html(StringIO(str(tabla)), header=1)[0]
            
            # Condición heurística de validación: Tabla principal de rendimiento (General Stats)
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except Exception:
            continue
            
    return None        

def normalizar_esquema_estadisticas(df):
    """
    Depura el DataFrame resultante eliminando filas de agregación (Totales),
    encabezados intercalados y enriqueciendo el modelo con la dimensión de equipo.
    """
    # Filtrado de filas de encabezado residual ('Rk')
    filtro_encabezados = df.iloc[:, 0].astype(str) == 'Rk'
    df_limpio = df[~filtro_encabezados].reset_index(drop=True)
    
    # Purga de filas totalizadoras agregadas por el servidor
    df_limpio = df_limpio[df_limpio['Player'] != 'Squad Total']
    df_limpio = df_limpio[df_limpio['Player'] != 'Opponent Total']
    
    # Inyección de dimensión estática (Constante dimensional)
    df_limpio['Squad'] = 'Barcelona'
    return df_limpio

def ejecutar_extraccion_torneos_cortos():
    """
    Orquesta la extracción iterativa de estadísticas generales para competiciones 
    de eliminación directa. Emplea Selenium WebDriver (undetected) para mitigar 
    sistemas Anti-Bot e implementa un módulo de logging para trazabilidad.
    """
    logging.info("Inicializando pipeline de extracción: Torneos de Eliminación Directa y Supercopas")
    tiempo_inicio = time.time()

    opciones_navegador = uc.ChromeOptions()
    driver = uc.Chrome(options=opciones_navegador)
    driver.set_page_load_timeout(60)

    try:
        for temporada in RANGO_TEMPORADAS:
            logging.info("="*60)
            logging.info(f"PROCESANDO PERIODO CRONOLÓGICO: {temporada}")
            logging.info("="*60)
            
            directorio_destino = os.path.join(DIR_OUTPUT_BASE, temporada)
            os.makedirs(directorio_destino, exist_ok=True)
            
            for nombre_competicion, url_plantilla in ENDPOINTS_COMPETICIONES.items():
                url_objetivo = url_plantilla.format(temporada=temporada)
                logging.info(f"-> Analizando dominio: {nombre_competicion}...")
                
                try:
                    driver.get(url_objetivo)
                    # Latencia heurística para emulación de lectura y prevención de Rate Limiting
                    time.sleep(3.5) 
                    
                    html_crudo = driver.page_source
                    
                    # Manejo de error HTTP 404 semántico (Ausencia de participación en la competición)
                    if "Page Not Found" in html_crudo or "404 Error" in html_crudo:
                        logging.warning(f"  [OMITIDO] Sin registros. El equipo no disputó la {nombre_competicion} en la {temporada}.")
                        continue
                    
                    df_estadisticas = preprocesar_y_extraer_tabla(html_crudo)        
                    
                    if df_estadisticas is not None:
                        df_estadisticas = normalizar_esquema_estadisticas(df_estadisticas)
                        
                        if not df_estadisticas.empty:
                            ruta_salida = os.path.join(directorio_destino, f'General_{nombre_competicion}_{temporada}.csv')
                            df_estadisticas.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
                            logging.info(f"  [ÉXITO] Persistencia completada: {len(df_estadisticas)} registros de jugador consolidados.")
                        else:
                            logging.error(f"  [ANOMALÍA] El DataFrame resultó vacío tras la fase de normalización estructural.")
                    else:
                        logging.warning(f"  [AVISO] No se detectó la tabla 'General Stats' (Comportamiento esperado en registros pre-Opta).")
                        
                except Exception as e:
                    logging.error(f"  [ERROR DE RED/PARSE] Excepción tipo {type(e).__name__} en {nombre_competicion}: {e}")
                
                # Latencia base entre peticiones atómicas
                time.sleep(1.5)

    except Exception as e:
        logging.error(f"[EXCEPCIÓN CRÍTICA DE ORQUESTACIÓN] {e}")
    finally:
        # Liberación segura de recursos de memoria
        driver.quit()

    tiempo_fin = time.time()
    duracion_minutos = int((tiempo_fin - tiempo_inicio) // 60)
    duracion_segundos = int((tiempo_fin - tiempo_inicio) % 60)
    logging.info(f"\nPipeline finalizado exitosamente. Tiempo de cómputo total: {duracion_minutos} min y {duracion_segundos} seg.")

if __name__ == "__main__":
    ejecutar_extraccion_torneos_cortos()