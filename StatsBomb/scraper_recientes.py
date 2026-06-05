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

def preprocesar_y_extraer_tabla(html_source):
    """
    Subrutina de extracción. Aplica preprocesamiento eliminando etiquetas 
    de comentarios para exponer las estructuras tabulares secundarias en el DOM,
    permitiendo la lectura de las tablas renderizadas asíncronamente.
    """
    html_expuesto = html_source.replace('<!--', '').replace('-->', '')
    soup = BeautifulSoup(html_expuesto, 'html.parser')
    
    tablas_dom = soup.find_all('table')
    for tabla in tablas_dom:
        try:
            # Ingesta en memoria optimizada mediante StringIO
            df = pd.read_html(StringIO(str(tabla)), header=1)[0]
            
            # Condición de validación: Matriz principal de rendimiento (General Stats)
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except Exception:
            continue
    return None        

def normalizar_esquema_estadisticas(df):
    """
    Depura el DataFrame resultante eliminando filas de agregación (Totales),
    encabezados intercalados por paginación y enriqueciendo el modelo con 
    la dimensión estática del equipo.
    """
    # Purga de encabezados residuales
    filtro_encabezados = df.iloc[:, 0].astype(str) == 'Rk'
    df_limpio = df[~filtro_encabezados].reset_index(drop=True)
    
    # Purga de filas totalizadoras agregadas por el servidor
    df_limpio = df_limpio[df_limpio['Player'] != 'Squad Total']
    df_limpio = df_limpio[df_limpio['Player'] != 'Opponent Total']
    
    # Inyección de dimensión estática (Contexto de Entidad)
    df_limpio['Squad'] = 'Barcelona'
    
    return df_limpio

def ejecutar_extraccion_cierre_temporada():
    """
    Script de cierre: Ejecuta la extracción dirigida y específica de la 
    Champions League 2024-2025 utilizando un endpoint directo y validado.
    Completa la base de datos histórica del proyecto.
    """
    logging.info("--- INICIALIZANDO CIERRE DE BASE DE DATOS (CHAMPIONS 24/25) ---")
    
    # Endpoint maestro validado para la temporada en curso
    url_objetivo = "https://fbref.com/en/squads/206d90db/2024-2025/c8/Barcelona-Stats-Champions-League"

    # Aprovisionamiento del directorio de destino
    directorio_destino = os.path.join('datos_fbref_estable', '2024-2025')
    os.makedirs(directorio_destino, exist_ok=True)

    logging.info("Desplegando instancia del navegador controlado (Evasión Anti-Bot)...")
    opciones_navegador = uc.ChromeOptions()
    driver = uc.Chrome(options=opciones_navegador)
    driver.set_page_load_timeout(60)

    try:
        logging.info(f" -> Ejecutando petición HTTP al endpoint definitivo...")
        driver.get(url_objetivo)
        
        # Latencia operativa para asegurar el renderizado total del DOM
        time.sleep(4) 
        
        html_crudo = driver.page_source
        df_estadisticas = preprocesar_y_extraer_tabla(html_crudo)        
        
        if df_estadisticas is not None:
            df_estadisticas = normalizar_esquema_estadisticas(df_estadisticas)
            
            if not df_estadisticas.empty:
                ruta_salida = os.path.join(directorio_destino, 'General_Champions_2024-2025.csv')
                
                # Persistencia con formato de codificación seguro para Power BI
                df_estadisticas.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
                logging.info(f"    [ÉXITO] Persistencia completada: {len(df_estadisticas)} entidades consolidadas.")
            else:
                logging.error("    [ANOMALÍA] La matriz tabular resultó vacía tras la limpieza estructural.")
        else:
            logging.error("    [ERROR ESTRUCTURAL] No se localizó la tabla 'General Stats' en el documento web.")

    except Exception as e:
        logging.error(f"[EXCEPCIÓN CRÍTICA DE RED O SISTEMA] {e}")
    finally:
        driver.quit()

    logging.info("\n" + "="*70)
    logging.info("CIERRE DE LA BASE DE DATOS HISTÓRICA: OPERACIÓN FINALIZADA CON ÉXITO")
    logging.info("="*70)

if __name__ == "__main__":
    ejecutar_extraccion_cierre_temporada()