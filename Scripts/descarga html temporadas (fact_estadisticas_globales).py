import os
import time
import undetected_chromedriver as uc

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL"
OUTPUT_DIR = os.path.join(BASE_DIR, "HTML_Temporadas")

def descargar_temporadas_fbref():
    """
    Despliega una instancia automatizada del navegador Chrome para descargar
    el código fuente (HTML) de los resúmenes estadísticos por temporada en FBref,
    implementando mecanismos de evasión para sistemas antibot (Cloudflare).
    """
    print("--- INICIANDO EXTRACCIÓN AUTOMATIZADA DE RESÚMENES DE TEMPORADA ---")
    
    # 1. Verificación y creación del directorio de salida local
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    # 2. Definición estática de las temporadas objetivo
    temporadas = [
        "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008",
        "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013",
        "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018",
        "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023",
        "2023-2024", "2024-2025"
    ]

    # 3. Inicialización del controlador web
    print("Info: Inicializando instancia de undetected_chromedriver...")
    options = uc.ChromeOptions()
    # Se fuerza la compatibilidad con la versión local del navegador para evitar conflictos
    driver = uc.Chrome(options=options, version_main=144)

    total_temporadas = len(temporadas)
    descargados_exito = 0
    archivos_existentes = 0

    print(f"Info: Total de temporadas encoladas para descarga: {total_temporadas}")
    print("Iniciando peticiones HTTP...\n")

    for index, temporada in enumerate(temporadas):
        url = f"https://fbref.com/en/squads/206d90db/{temporada}/all_comps/Barcelona-Stats-All-Competitions"
        nombre_archivo = f"Barcelona_Stats_{temporada}.html"
        ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)
        
        # 4. Control de idempotencia: omisión de archivos ya procesados
        if os.path.exists(ruta_archivo):
            archivos_existentes += 1
            print(f"[{index + 1}/{total_temporadas}] Omisión: {nombre_archivo} (El archivo ya existe en el directorio local)")
            continue
            
        try:
            print(f"[{index + 1}/{total_temporadas}] Descargando código fuente: {nombre_archivo}...")
            driver.get(url)
            
            # 5. Mecanismo de evasión antibot (Human-in-the-loop)
            # Evalúa el título de la página para detectar la intercepción de Cloudflare
            intentos_bloqueo = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("Aviso: Firewall de Cloudflare detectado. Pausando ejecución para validación.")
                time.sleep(3)
                intentos_bloqueo += 1
                if intentos_bloqueo > 10:
                    print("Aviso: Límite de tiempo excedido. Intervención manual requerida en el navegador.")
                    break
            
            # 6. Retardo asíncrono para garantizar la renderización completa del DOM
            time.sleep(5)
            
            html_content = driver.page_source
            
            # 7. Validación estructural del documento descargado
            # Se busca la presencia de clases CSS clave de las tablas estadísticas
            if "stats_standard" in html_content or "stats_keeper" in html_content:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                descargados_exito += 1
                print("Operación completada: Archivo guardado correctamente.")
            else:
                print("Fallo de integridad: La página cargó de forma incompleta o carece de las estructuras tabulares esperadas.")
                
        except Exception as e:
            print(f"Error crítico durante la extracción de {url}: {e}")

    # 8. Cierre y liberación de recursos
    driver.quit()
    print(f"\nProceso finalizado. Resumen: {descargados_exito} nuevos archivos extraídos | {archivos_existentes} archivos previamente existentes.")

if __name__ == "__main__":
    descargar_temporadas_fbref()