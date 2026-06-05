import pandas as pd
from bs4 import BeautifulSoup
import time
import os
import undetected_chromedriver as uc

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_OUTPUT = os.path.join(BASE_DIR, "Lista_Links_PostMessi_FBref.csv")

# Definición estática de las temporadas recientes (Periodo Post-Messi)
URLS_TEMPORADAS = {
    "2021-2022": "https://fbref.com/en/squads/206d90db/2021-2022/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga",
    "2022-2023": "https://fbref.com/en/squads/206d90db/2022-2023/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga",
    "2023-2024": "https://fbref.com/en/squads/206d90db/2023-2024/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga",
    "2024-2025": "https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga"
}

def extraer_enlaces_recientes_fbref():
    """
    Despliega un controlador web con evasión de detección para navegar por 
    los calendarios de las temporadas recientes. Utiliza BeautifulSoup para 
    parsear el DOM, localizar la tabla de resultados y extraer las URLs 
    de los informes detallados de cada partido.
    """
    print("--- INICIANDO EXTRACCIÓN DE ENLACES (PERIODO RECIENTE) ---")
    
    lista_datos_partidos = []
    
    # Identificador secuencial temporal para mantener la estructura de la base de datos
    id_partido_secuencial = 5000 
    
    # 1. Inicialización del controlador web automatizado
    print("Info: Inicializando instancia de undetected_chromedriver (v146)...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=146) 

    for temporada, url in URLS_TEMPORADAS.items():
        print(f"\nProcesando temporada: {temporada}...")
        try:
            driver.get(url)
            
            # 2. Mecanismo de evasión antibot (Cloudflare)
            intentos_bloqueo = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("Aviso: Firewall detectado. Pausando hilo de ejecución para resolución de desafío...")
                time.sleep(3)
                intentos_bloqueo += 1
                if intentos_bloqueo > 15:
                    print("Aviso: Límite de intentos superado. Intervención manual requerida.")
                    break
            
            # Retardo asíncrono para asegurar la renderización completa de los elementos DOM dinámicos
            time.sleep(5)
            
            # 3. Generación del árbol DOM e inicialización del parser
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 4. Navegación estructural y extracción de nodos
            tabla_principal = soup.find('table', {'id': 'matchlogs_for'})
            
            if not tabla_principal:
                print(f"Error de integridad: No se localizó la tabla principal en la temporada {temporada}.")
                continue

            filas = tabla_principal.find('tbody').find_all('tr')
            enlaces_extraidos_temp = 0

            for fila in filas:
                # Omisión de filas espaciadoras que no contienen datos estructurales válidos
                if 'spacer' in fila.get('class', []): 
                    continue

                # Extracción del nodo de fecha
                nodo_fecha = fila.find('th', {'data-stat': 'date'})
                if not nodo_fecha or not nodo_fecha.text.strip(): 
                    continue
                fecha_partido = nodo_fecha.text.strip()

                # Extracción del nodo del equipo rival
                nodo_rival = fila.find('td', {'data-stat': 'opponent'})
                nombre_rival = nodo_rival.text.strip() if nodo_rival else "Desconocido"

                # Extracción del nodo contenedor del enlace al informe detallado
                nodo_reporte = fila.find('td', {'data-stat': 'match_report'})
                etiqueta_enlace = nodo_reporte.find('a') if nodo_reporte else None

                if etiqueta_enlace and 'href' in etiqueta_enlace.attrs:
                    url_completa = "https://fbref.com" + etiqueta_enlace['href']

                    lista_datos_partidos.append({
                        'ID_Partido': id_partido_secuencial,
                        'Temporada': temporada,
                        'Fecha': fecha_partido,
                        'Rival': nombre_rival,
                        'URL_FBref': url_completa
                    })
                    id_partido_secuencial += 1
                    enlaces_extraidos_temp += 1

            print(f"Operación completada: {enlaces_extraidos_temp} enlaces extraídos exitosamente de {temporada}.")
            
            # Pausa de control de tasa entre iteraciones (Rate limiting)
            time.sleep(3) 

        except Exception as e:
            print(f"Error crítico durante el procesamiento de la temporada {temporada}: {e}")

    # 5. Cierre de sesión y persistencia de datos
    driver.quit()
    
    if lista_datos_partidos:
        df_enlaces = pd.DataFrame(lista_datos_partidos)
        df_enlaces.to_csv(PATH_OUTPUT, index=False, encoding='utf-8')
        print(f"\nProceso finalizado. Total consolidado: {len(df_enlaces)} enlaces guardados en: {PATH_OUTPUT}")
    else:
        print("\nAviso: La operación ha concluido sin extraer nuevos registros.")

if __name__ == "__main__":
    extraer_enlaces_recientes_fbref()