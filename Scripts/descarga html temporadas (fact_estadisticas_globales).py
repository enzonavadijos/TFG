import os
import time
import undetected_chromedriver as uc

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL"
carpeta_salida = os.path.join(CARPETA_BASE, "HTML_Temporadas")

def descargar_temporadas_fbref():
    print("--- 🥷 INICIANDO MODO FURTIVO (UNDETECTED CHROMEDRIVER) ---")
    
    # 1. Crear carpeta si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        
    # 2. Lista de temporadas a descargar
    temporadas = [
        "2003-2004", "2004-2005", "2005-2006", "2006-2007", "2007-2008",
        "2008-2009", "2009-2010", "2010-2011", "2011-2012", "2012-2013",
        "2013-2014", "2014-2015", "2015-2016", "2016-2017", "2017-2018",
        "2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023",
        "2023-2024", "2024-2025"
    ]

    # 3. ARRANCAMOS EL CHROME INDETECTABLE
    print("🚀 Levantando el navegador camuflado...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=144)

    total = len(temporadas)
    descargados = 0
    ya_existentes = 0

    print(f"Total de temporadas a descargar: {total}")
    print("⏳ Iniciando ataque a FBref...\n")

    for index, temporada in enumerate(temporadas):
        url = f"https://fbref.com/en/squads/206d90db/{temporada}/all_comps/Barcelona-Stats-All-Competitions"
        nombre_archivo = f"Barcelona_Stats_{temporada}.html"
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
        
        # 4. Si ya lo tienes, salta al siguiente
        if os.path.exists(ruta_archivo):
            ya_existentes += 1
            print(f"[{index + 1}/{total}] Saltando: {nombre_archivo} (ya existe)")
            continue
            
        try:
            print(f"[{index + 1}/{total}] Descargando: {nombre_archivo}...")
            driver.get(url)
            
            # 5. ESPERA INTELIGENTE ANTI-CLOUDFLARE
            intentos = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("   🛡️ Cloudflare detectado. El camuflaje está actuando, espera...")
                time.sleep(3)
                intentos += 1
                if intentos > 10:
                    print("   ⚠️ Atascado. Haz clic manual en la casilla de Chrome si la ves.")
                    break
            
            # 6. Pausa de seguridad para que todo renderice bien
            time.sleep(5)
            
            html_content = driver.page_source
            
            # 7. Comprobación básica (buscamos alguna tabla clave o clase de FBref)
            if "stats_standard" in html_content or "stats_keeper" in html_content:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                descargados += 1
                print("   ✅ ¡Guardado con éxito!")
            else:
                print(f"   ❌ La página cargó incompleta o no se encontraron las tablas esperadas.")
                
        except Exception as e:
            print(f"   ⚠️ Fallo crítico en {url}: {e}")

    # 8. Cerramos Chrome al terminar
    driver.quit()
    print(f"\n🎉 ¡VICTORIA! {descargados} archivos nuevos descargados | {ya_existentes} ya existían.")

if __name__ == "__main__":
    descargar_temporadas_fbref()