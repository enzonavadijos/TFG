import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL"
PATH_LINKS = os.path.join(BASE_DIR, "CSV", "Lista_Links_StatsBomb_Para_FBref.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "HTML_Partidos")

def ejecutar_extraccion_selenium():
    """
    Orquesta la descarga automatizada de documentos HTML correspondientes 
    a los informes de partido. Emplea Selenium WebDriver para la navegación y 
    renderizado del DOM, incorporando validación de idempotencia y control de tasa.
    """
    print("--- INICIANDO EXTRACCIÓN DE DOCUMENTOS HTML (SELENIUM WEBDRIVER) ---")
    
    # 1. Verificación de infraestructura de directorios
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Info: Directorio de destino inicializado en {OUTPUT_DIR}")
        
    # 2. Ingesta del catálogo de enlaces objetivo
    try:
        df_enlaces = pd.read_csv(PATH_LINKS)
        print(f"Info: Catálogo cargado exitosamente con {len(df_enlaces)} registros objetivo.")
    except Exception as e:
        print(f"Error crítico durante la lectura del catálogo en {PATH_LINKS}: {e}")
        return

    # 3. Inicialización del controlador web automatizado
    chrome_options = Options()
    # Nota: La ejecución en segundo plano (headless) está desactivada por defecto 
    # para simular un entorno de usuario real y reducir la intercepción por firewalls.
    # chrome_options.add_argument("--headless") 
    
    print("Info: Inicializando instancia de Google Chrome via Selenium...")
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Error de inicialización del WebDriver. Verifique la instalación de dependencias (Selenium): {e}")
        return

    # 4. Iteración de descargas secuenciales
    descargas_exitosas = 0
    total_registros = len(df_enlaces)
    
    for index, fila in df_enlaces.iterrows():
        id_partido = fila['ID_Partido']
        fecha = fila['Fecha']
        
        # Saneamiento de caracteres especiales en el nombre del equipo rival
        # para garantizar la compatibilidad con el sistema de archivos del SO
        rival = str(fila['Rival']).replace(" ", "_").replace("/", "-") 
        url_objetivo = fila['URL_FBref']
        
        # Construcción estandarizada de la nomenclatura del archivo local
        nombre_archivo = f"{id_partido}_{fecha}_{rival}.html"
        ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)
        
        # Control de idempotencia para optimizar ejecuciones interrumpidas o iterativas
        if os.path.exists(ruta_archivo):
            print(f"Aviso: El documento {nombre_archivo} ya existe en el directorio local. Omitiendo extracción.")
            continue
            
        print(f"[{index+1}/{total_registros}] Extrayendo código fuente: {nombre_archivo}...")
        
        try:
            driver.get(url_objetivo)
            
            # Estrategia de Control de Tasa (Rate Limiting)
            # Se introduce una latencia controlada para simular el comportamiento de 
            # navegación humana y mitigar posibles bloqueos (HTTP 429) del servidor de origen.
            time.sleep(4) 
            
            # Persistencia del Document Object Model (DOM) íntegramente renderizado
            html_content = driver.page_source
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo_salida:
                archivo_salida.write(html_content)
                
            descargas_exitosas += 1
            
        except Exception as e:
            print(f"Error durante la extracción del recurso en {url_objetivo}: {e}")
            
    # 5. Liberación de recursos de memoria y cierre de sesión
    driver.quit()
    print(f"\nProceso finalizado exitosamente. Se han extraído y consolidado {descargas_exitosas} nuevos documentos HTML.")
    print("El sistema está preparado para la fase de parseo de metadatos (ETL Local).")

if __name__ == "__main__":
    ejecutar_extraccion_selenium()