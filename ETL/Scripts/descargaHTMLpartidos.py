import pandas as pd
import os
import time
import undetected_chromedriver as uc

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL"
PATH_LINKS_CSV = os.path.join(BASE_DIR, "CSV", "Lista_Links_StatsBomb_Para_FBref.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "HTML_Partidos")

def descargar_html_partidos():
    """
    Lee un listado de enlaces previamente consolidado y utiliza un controlador 
    web automatizado con evasión de detección para descargar el código fuente 
    (HTML) de los informes de los partidos. Implementa validación estructural 
    e idempotencia para permitir la reanudación ante interrupciones.
    """
    print("--- INICIANDO EXTRACCIÓN AUTOMATIZADA DE PARTIDOS (MATCH REPORTS) ---")
    
    # 1. Verificación y creación del directorio de salida
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    try:
        df_enlaces = pd.read_csv(PATH_LINKS_CSV)
    except FileNotFoundError:
        print(f"Error crítico: No se ha localizado el archivo de enlaces en {PATH_LINKS_CSV}")
        return

    # 2. Inicialización del controlador web
    print("Info: Inicializando instancia de undetected_chromedriver...")
    options = uc.ChromeOptions()
    # Se ejecuta de forma interactiva (non-headless) para minimizar la probabilidad 
    # de detección algorítmica por parte del firewall de origen.
    driver = uc.Chrome(options=options, version_main=144)

    total_partidos = len(df_enlaces)
    descargados_exito = 0
    archivos_existentes = 0

    print(f"Info: Total de encuentros encolados para extracción: {total_partidos}")
    print("Iniciando peticiones HTTP secuenciales...\n")

    for index, row in df_enlaces.iterrows():
        id_partido = row['ID_Partido']
        url = row['URL_FBref']
        fecha = row['Fecha']
        
        # Saneamiento del nombre del equipo rival para evitar conflictos de sistema de archivos
        rival = str(row['Rival']).replace(" ", "_").replace("/", "_") 
        
        nombre_archivo = f"{id_partido}_{fecha}_{rival}.html"
        ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)
        
        # 3. Control de idempotencia: Omisión de descargas previamente completadas
        if os.path.exists(ruta_archivo):
            archivos_existentes += 1
            continue
            
        try:
            print(f"[{index + 1}/{total_partidos}] Extrayendo código fuente: {nombre_archivo}...")
            driver.get(url)
            
            # 4. Mecanismo de evasión antibot (Cloudflare)
            intentos_bloqueo = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("Aviso: Intercepción por firewall detectada. Pausando hilo de ejecución...")
                time.sleep(3)
                intentos_bloqueo += 1
                if intentos_bloqueo > 10: 
                    print("Aviso: Tiempo máximo de espera superado. Intervención manual requerida en el navegador.")
                    break
            
            # 5. Retardo asíncrono para garantizar la correcta renderización de las tablas dinámicas (JS)
            time.sleep(4)
            
            html_content = driver.page_source
            
            # 6. Validación estructural del documento HTML
            # Se evalúa la presencia de identificadores CSS característicos de las tablas objetivo
            if "matchlogs_for" in html_content or "stats" in html_content or "timeline" in html_content:
                with open(ruta_archivo, 'w', encoding='utf-8') as archivo_html:
                    archivo_html.write(html_content)
                descargados_exito += 1
                print("Operación completada: Archivo guardado correctamente.")
            else:
                print("Fallo de integridad: La página cargó incompleta o carece de la estructura tabular esperada.")
                
        except Exception as e:
            print(f"Error crítico durante la extracción de {url}: {e}")

    # 7. Cierre de sesión y liberación de recursos en memoria
    driver.quit()
    print(f"\nProceso finalizado. Resumen: {descargados_exito} nuevos archivos extraídos | {archivos_existentes} archivos previamente existentes.")

if __name__ == "__main__":
    descargar_html_partidos()