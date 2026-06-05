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
# Generación dinámica del rango cronológico de estudio (Descendente: 2024-2025 hasta 2003-2004)
RANGO_TEMPORADAS = [f"{anyo}-{anyo+1}" for anyo in range(2024, 2002, -1)]

# Catálogo de URIs parametrizadas para competiciones de formato regular e histórico
ENDPOINTS_COMPETICIONES = {
    "LaLiga": "https://fbref.com/en/comps/12/{temporada}/stats/{temporada}-La-Liga-Stats",
    "Champions": "https://fbref.com/en/comps/8/{temporada}/stats/{temporada}-Champions-League-Stats",
    "CopaDelRey": "https://fbref.com/en/comps/569/{temporada}/{temporada}-Copa-del-Rey-Stats",
    "Supercopa_Espana": "https://fbref.com/en/comps/570/{temporada}/{temporada}-Supercopa-de-Espana-Stats"
}

DIR_OUTPUT_BASE = "datos_fbref_estable"

def extraer_matriz_rendimiento(soup):
    """
    Subrutina de extracción de datos.
    Escanea el árbol DOM en busca de estructuras tabulares, realiza una ingesta 
    en memoria y valida heurísticamente que se trata de la matriz principal de 
    rendimiento (presencia de las métricas 'Player' y 'Min').
    """
    tablas_dom = soup.find_all('table')
    for tabla in tablas_dom:
        try:
            # Ingesta optimizada mediante StringIO
            df = pd.read_html(StringIO(str(tabla)), header=1)[0]
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except Exception:
            continue
    return None        

def depurar_encabezados_intercalados(df):
    """
    Elimina las filas de paginación o encabezados residuales inyectados 
    por el servidor web en el cuerpo de la tabla (ej. filas donde el índice es 'Rk').
    """
    filtro_encabezados = df.iloc[:, 0].astype(str) == 'Rk'
    return df[~filtro_encabezados].reset_index(drop=True)

def ejecutar_extraccion_competiciones_regulares():
    """
    Orquesta la extracción iterativa de estadísticas generales para las competiciones 
    principales. Emplea Selenium WebDriver (undetected) para mitigar defensas Anti-Bot 
    y aplica un filtrado dimensional dinámico para aislar los registros del equipo objetivo.
    """
    logging.info("Inicializando pipeline de extracción: Competiciones Regulares e Históricas...")
    tiempo_inicio = time.time()

    opciones_navegador = uc.ChromeOptions()
    # Ejecución sin interfaz gráfica (Headless Mode) desactivada temporalmente 
    # para evitar bloqueos por heurística del firewall (WAF).
    # opciones_navegador.add_argument("--headless") 
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
                logging.info(f" -> Analizando dominio analítico: {nombre_competicion}...")
                
                driver.get(url_objetivo)
                
                # Latencia operativa obligatoria para elusión de Rate Limiting
                time.sleep(3) 
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                df_estadisticas = extraer_matriz_rendimiento(soup)        
                
                if df_estadisticas is not None:
                    df_estadisticas = depurar_encabezados_intercalados(df_estadisticas)
                    try:
                        # Resolución Dinámica de Dimensión: Identificación de la columna de equipo
                        col_equipo = [col for col in df_estadisticas.columns if 'Squad' in str(col) or 'Equipo' in str(col)][0]
                        
                        # Filtrado Dimensional por Entidad Deportiva (Barcelona)
                        filtro_entidad = df_estadisticas[col_equipo].astype(str).str.contains('Barcelona', case=False, na=False)
                        df_estadisticas = df_estadisticas[filtro_entidad]
                        
                        if not df_estadisticas.empty:
                            ruta_salida = os.path.join(directorio_destino, f'General_{nombre_competicion}_{temporada}.csv')
                            df_estadisticas.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
                            logging.info(f"    [ÉXITO] Persistencia completada: {len(df_estadisticas)} registros de entidad asilados.")
                        else:
                            logging.warning("    [OMITIDO] Entidad deportiva ausente en la matriz de la competición.")
                    except Exception as e:
                        logging.warning(f"    [ANOMALÍA] Imposible resolver la dimensión de equipo en {nombre_competicion}: {e}")
                else:
                    logging.error(f"    [AVISO] Matriz tabular no localizada (Comportamiento esperado en registros históricos o ausencias).")
                    
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
    ejecutar_extraccion_competiciones_regulares()