# -*- coding: utf-8 -*-
import os
import time
from io import StringIO
import logging
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# === TODAS LAS TEMPORADAS (Desde 2024/25 hasta 2003/04) ===
temporadas = [f"{anyo}-{anyo+1}" for anyo in range(2024, 2002, -1)]

# === DICCIONARIO DE COMPETICIONES ESTABLES ===
competiciones = {
    "LaLiga": "https://fbref.com/en/comps/12/{temporada}/stats/{temporada}-La-Liga-Stats",
    "Champions": "https://fbref.com/en/comps/8/{temporada}/stats/{temporada}-Champions-League-Stats",
    "CopaDelRey": "https://fbref.com/en/comps/569/{temporada}/{temporada}-Copa-del-Rey-Stats",
    "Supercopa_Espana": "https://fbref.com/en/comps/570/{temporada}/{temporada}-Supercopa-de-Espana-Stats"
}

def extraer_tabla_general(soup):
    tablas = soup.find_all('table')
    for t in tablas:
        try:
            df = pd.read_html(StringIO(str(t)), header=1)[0]
            if 'Player' in df.columns and 'Min' in df.columns:
                return df
        except:
            continue
    return None        

def eliminar_cabeceras_extra(df):
    serie = df.iloc[:,0].astype(str) == 'Rk'
    return df[~serie].reset_index(drop=True)

logging.info("Arrancando el motor de extracción de Competiciones Estables...")
tiempo_inicio = time.time()

options = uc.ChromeOptions()
# options.add_argument("--headless") # Lo mantenemos comentado por seguridad anti-bot
driver = uc.Chrome(options=options)
driver.set_page_load_timeout(60)

try:
    for temporada in temporadas:
        logging.info(f"\n=========================================")
        logging.info(f"   INICIANDO TEMPORADA: {temporada}")
        logging.info(f"=========================================")
        
        directorio = os.path.join('datos_fbref_estable', temporada)
        os.makedirs(directorio, exist_ok=True)
        
        for nombre_comp, url_plantilla in competiciones.items():
            url = url_plantilla.format(temporada=temporada)
            logging.info(f" -> Buscando {nombre_comp}...")
            
            driver.get(url)
            time.sleep(3) # Pausa rápida pero segura
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            tabla_jug = extraer_tabla_general(soup)         
            
            if tabla_jug is not None:
                tabla_jug = eliminar_cabeceras_extra(tabla_jug)
                try:
                    col_equipo = [col for col in tabla_jug.columns if 'Squad' in str(col) or 'Equipo' in str(col)][0]
                    tabla_jug = tabla_jug[tabla_jug[col_equipo].astype(str).str.contains('Barcelona', case=False, na=False)]
                    
                    if not tabla_jug.empty:
                        ruta_jug = os.path.join(directorio, f'General_{nombre_comp}_{temporada}.csv')
                        tabla_jug.to_csv(ruta_jug, index=False, encoding='utf-8-sig')
                        logging.info(f"    [ÉXITO] Guardados {len(tabla_jug)} jugadores del Barça.")
                    else:
                        logging.warning("    [OMITIDO] El Barcelona no aparece en esta competición.")
                except Exception as e:
                    logging.warning(f"    [ATENCIÓN] No se pudo filtrar el Barça en {nombre_comp}.")
            else:
                logging.error(f"    [FALLO] Tabla no encontrada (Normal en Copas antiguas o años no jugados).")
                
            time.sleep(1.5) 

except Exception as e:
    logging.error(f"Error crítico en el bucle principal: {e}")
finally:
    driver.quit()

tiempo_fin = time.time()
logging.info(f"\nProceso finalizado. Tiempo total: {int((tiempo_fin - tiempo_inicio) // 60)} min y {int((tiempo_fin - tiempo_inicio) % 60)} seg")