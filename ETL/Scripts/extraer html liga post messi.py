import pandas as pd
import os
import time
import undetected_chromedriver as uc

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL"
# 1. Apuntamos al nuevo CSV que acabas de generar
ruta_links = os.path.join(CARPETA_BASE, "CSV", "Lista_Links_PostMessi_FBref.csv")
# 2. Creamos una carpeta nueva para no mezclar los de StatsBomb con estos
carpeta_salida = os.path.join(CARPETA_BASE, "HTML_Partidos_PostMessi")

def robot_descargador_furtivo():
    print("--- 🥷 INICIANDO MODO FURTIVO: DESCARGA MASIVA DE HTML ---")
    
    # 1. Crear carpeta si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"📁 Carpeta de destino creada: {carpeta_salida}")
        
    try:
        df_links = pd.read_csv(ruta_links)
    except FileNotFoundError:
        print(f"❌ Error: No encuentro el archivo {ruta_links}")
        return

    # 2. ARRANCAMOS EL CHROME INDETECTABLE (Fijado a tu versión 146)
    print("🚀 Levantando el navegador camuflado...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=146)

    total = len(df_links)
    descargados = 0
    ya_existentes = 0

    print(f"📊 Total de partidos a descargar: {total}")
    print("⏳ Iniciando ataque a FBref...\n")

    for index, row in df_links.iterrows():
        id_partido = row['ID_Partido']
        url = row['URL_FBref']
        fecha = row['Fecha']
        # Limpiamos el nombre para que Windows no dé error al guardar el archivo
        rival = str(row['Rival']).replace(" ", "_").replace("/", "_") 
        
        nombre_archivo = f"{id_partido}_{fecha}_{rival}.html"
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
        
        # 3. Si ya lo tienes, salta al siguiente (ideal si se corta y tienes que reanudar)
        if os.path.exists(ruta_archivo):
            ya_existentes += 1
            continue
            
        try:
            print(f"[{index + 1}/{total}] Descargando: {nombre_archivo}...")
            driver.get(url)
            
            # 4. ESPERA INTELIGENTE ANTI-CLOUDFLARE
            intentos = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("   🛡️ Cloudflare detectado. El camuflaje está actuando, espera...")
                time.sleep(3)
                intentos += 1
                if intentos > 15: # Si pasan 45 segundos y sigue bloqueado
                    print("   ⚠️ Atascado. Haz clic manual en la casilla de Chrome si la ves.")
                    break
            
            # 5. Pausa de seguridad para que las tablas HTML de Stats terminen de renderizarse
            time.sleep(4)
            
            html_content = driver.page_source
            
            # 6. Comprobamos que la página tiene la tabla buena ("stats") y no es un error
            if "stats" in html_content or "timeline" in html_content or "matchlogs_for" in html_content:
                with open(ruta_archivo, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                descargados += 1
                print("   ✅ ¡Guardado con éxito!")
            else:
                print(f"   ❌ La página cargó incompleta o en blanco.")
                
        except Exception as e:
            print(f"   ⚠️ Fallo crítico en {url}: {e}")

    # 7. Cerramos Chrome al terminar
    driver.quit()
    print(f"\n🎉 ¡VICTORIA! {descargados} archivos HTML nuevos descargados | {ya_existentes} ya existían.")

if __name__ == "__main__":
    robot_descargador_furtivo()