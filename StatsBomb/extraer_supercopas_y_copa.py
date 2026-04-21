# -*- coding: utf-8 -*-
import os
import time
from io import StringIO
import logging
import pandas as pd
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# Configuración del log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# === EL DESCUBRIMIENTO: URLs QUIRÚRGICAS AISLADAS ===
competiciones = {
    "CopaDelRey": "https://fbref.com/en/squads/206d90db/{temporada}/c569/Barcelona-Stats-Copa-del-Rey",
    "Supercopa_Espana": "https://fbref.com/en/squads/206d90db/{temporada}/c646/Barcelona-Stats-Supercopa-de-Espana",
    "Supercopa_Europa": "https://fbref.com/en/squads/206d90db/{temporada}/c122/Barcelona-Stats-UEFA-Super-Cup"
}

# Rango histórico completo
temporadas = [f"{anyo}-{anyo+1}" for anyo in range(2024, 2002, -1)]

def extraer_tabla_general(html_source):
    """Aplica la Opción Nuclear y busca la tabla General de forma infalible"""
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
    """Limpia cabeceras repetidas y totales, y añade la columna del equipo"""
    serie = df.iloc[:,0].astype(str) == 'Rk'
    df = df[~serie].reset_index(drop=True)
    df = df[df['Player'] != 'Squad Total']
    df = df[df['Player'] != 'Opponent Total']
    df['Squad'] = 'Barcelona'
    return df

logging.info("Arrancando script: extraer_supercopas_y_copa.py")
tiempo_inicio = time.time()

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.set_page_load_timeout(60)

try:
    for temporada in temporadas:
        logging.info(f"\n=========================================")
        logging.info(f"   ATACANDO TEMPORADA: {temporada}")
        logging.info(f"=========================================")
        
        directorio = os.path.join('datos_fbref_estable', temporada)
        os.makedirs(directorio, exist_ok=True)
        
        for nombre_comp, url_plantilla in competiciones.items():
            url = url_plantilla.format(temporada=temporada)
            logging.info(f" -> Buscando {nombre_comp}...")
            
            try:
                driver.get(url)
                time.sleep(3.5) # Pausa técnica para evitar baneos
                
                html_crudo = driver.page_source
                
                # Comprobamos si FBref nos ha devuelto una página de "Page Not Found" (404)
                if "Page Not Found" in html_crudo or "404 Error" in html_crudo:
                    logging.warning(f"    [OMITIDO] No hay datos o no se jugó la {nombre_comp} en la {temporada}.")
                    continue
                
                tabla_jug = extraer_tabla_general(html_crudo)         
                
                if tabla_jug is not None:
                    tabla_jug = limpiar_tabla(tabla_jug)
                    
                    if not tabla_jug.empty:
                        ruta_jug = os.path.join(directorio, f'General_{nombre_comp}_{temporada}.csv')
                        tabla_jug.to_csv(ruta_jug, index=False, encoding='utf-8-sig')
                        logging.info(f"    [ÉXITO] Guardados {len(tabla_jug)} jugadores en {nombre_comp}.")
                    else:
                        logging.error(f"    [ERROR] Tabla vacía tras limpieza.")
                else:
                    logging.warning(f"    [AVISO] Página cargada, pero no hay tabla General (Normal en años pre-Opta).")
                    
            except Exception as e:
                logging.error(f"    [ERROR DE CONEXIÓN] {type(e).__name__} en {nombre_comp}.")
            
            time.sleep(1.5)

except Exception as e:
    logging.error(f"[CRASHEO DEL BUCLE PRINCIPAL] {e}")
finally:
    driver.quit()

tiempo_fin = time.time()
logging.info(f"\n¡Misión completada! Tiempo total: {int((tiempo_fin - tiempo_inicio) // 60)} min y {int((tiempo_fin - tiempo_inicio) % 60)} seg")