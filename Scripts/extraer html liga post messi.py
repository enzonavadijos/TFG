import pandas as pd
import os
import time
import undetected_chromedriver as uc

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL"
# Origen: Listado de enlaces generados específicamente para la etapa contemporánea
PATH_LINKS = os.path.join(BASE_DIR, "CSV", "Lista_Links_PostMessi_FBref.csv")
# Destino: Directorio aislado para evitar sobreescrituras y mantener la separación de universos de datos
OUTPUT_DIR = os.path.join(BASE_DIR, "HTML_Partidos_PostMessi")

def descargar_html_partidos_postmessi():
    """
    Despliega un controlador web automatizado (undetected_chromedriver) para ejecutar 
    la extracción masiva de documentos HTML correspondientes a los informes de 
    partidos de la etapa Post-Messi. Incorpora validación de integridad estructural 
    y persistencia de sesión para evadir sistemas antibot.
    """
    print("--- INICIANDO EXTRACCIÓN AUTOMATIZADA DE PARTIDOS (ETAPA POST-MESSI) ---")
    
    # 1. Verificación y aprovisionamiento del directorio de salida
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Info: Directorio de destino inicializado en {OUTPUT_DIR}")
        
    try:
        df_enlaces = pd.read_csv(PATH_LINKS)
    except FileNotFoundError:
        print(f"Error crítico: No se ha localizado el archivo de enlaces en {PATH_LINKS}")
        return

    # 2. Inicialización del controlador web automatizado
    print("Info: Levantando instancia del navegador con evasión algorítmica (v146)...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=146)

    total_registros = len(df_enlaces)
    descargas_exitosas = 0
    archivos_existentes = 0

    print(f"Info: Total de encuentros encolados para extracción: {total_registros}")
    print("Iniciando peticiones HTTP secuenciales...\n")

    for index, row in df_enlaces.iterrows():
        id_partido = row['ID_Partido']
        url_objetivo = row['URL_FBref']
        fecha = row['Fecha']
        
        # Saneamiento de la cadena de texto del rival para evitar excepciones en el sistema de archivos (NTFS/FAT32)
        rival = str(row['Rival']).replace(" ", "_").replace("/", "_") 
        
        nombre_archivo = f"{id_partido}_{fecha}_{rival}.html"
        ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)
        
        # 3. Control de idempotencia para optimizar ejecuciones pausadas/reanudadas
        if os.path.exists(ruta_archivo):
            archivos_existentes += 1
            continue
            
        try:
            print(f"[{index + 1}/{total_registros}] Extrayendo código fuente: {nombre_archivo}...")
            driver.get(url_objetivo)
            
            # 4. Mecanismo de evasión reactiva (Cloudflare)
            intentos_bloqueo = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("Aviso: Firewall de Cloudflare detectado. Pausando ejecución para validación del reto...")
                time.sleep(3)
                intentos_bloqueo += 1
                if intentos_bloqueo > 15: # Timeout tras 45 segundos de bloqueo persistente
                    print("Alerta: Bloqueo persistente. Se requiere resolución manual del CAPTCHA en la ventana del navegador.")
                    break
            
            # 5. Retardo asíncrono para asegurar la ejecución y renderizado del JavaScript cliente
            time.sleep(4)
            
            html_content = driver.page_source
            
            # 6. Validación de integridad del Document Object Model (DOM)
            # Garantiza que las tablas estadísticas objetivo se han instanciado correctamente
            if "stats" in html_content or "timeline" in html_content or "matchlogs_for" in html_content:
                with open(ruta_archivo, 'w', encoding='utf-8') as archivo_salida:
                    archivo_salida.write(html_content)
                descargas_exitosas += 1
                print("Operación completada: Documento persistido exitosamente.")
            else:
                print("Fallo de integridad: La página carece de las estructuras tabulares requeridas.")
                
        except Exception as e:
            print(f"Error crítico durante la extracción de {url_objetivo}: {e}")

    # 7. Liberación de recursos de memoria y cierre del proceso navegador
    driver.quit()
    print(f"\nProceso finalizado. Resumen: {descargas_exitosas} nuevos HTML extraídos | {archivos_existentes} omitidos (ya existentes).")

if __name__ == "__main__":
    descargar_html_partidos_postmessi()