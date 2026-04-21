import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# --- RUTAS EXACTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL"
ruta_csv = os.path.join(CARPETA_BASE, "CSV", "Lista_Links_StatsBomb_Para_FBref.csv")
carpeta_salida = os.path.join(CARPETA_BASE, "HTML_Partidos")

def descargar_htmls_faltantes():
    print("--- 🚜 INICIANDO EL TANQUE FURTIVO 2.0 ---")
    
    # 1. Comprobar que existe la carpeta de salida
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        
    # 2. Leer la lista de objetivos
    try:
        df_links = pd.read_csv(ruta_csv)
        print(f"🎯 Cargados {len(df_links)} objetivos desde el CSV.")
    except Exception as e:
        print(f"❌ Error leyendo el CSV: {e}")
        return

    # 3. Configurar el Robot (Chrome)
    chrome_options = Options()
    # Descomenta la siguiente línea si quieres que lo haga de fondo sin abrir ventana:
    # chrome_options.add_argument("--headless") 
    
    print("🤖 Arrancando motores de Chrome...")
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"❌ Error abriendo Chrome. ¿Tienes instalada la librería selenium? (pip install selenium): {e}")
        return

    # 4. Iniciar el asalto
    descargados_hoy = 0
    
    for index, fila in df_links.iterrows():
        id_partido = fila['ID_Partido']
        fecha = fila['Fecha']
        rival = str(fila['Rival']).replace(" ", "_").replace("/", "-") # Limpiamos nombres raros
        url = fila['URL_FBref']
        
        # Generar nombre del archivo
        nombre_archivo = f"{id_partido}_{fecha}_{rival}.html"
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
        
        # ESCUDO: Si ya lo tenemos, lo saltamos
        if os.path.exists(ruta_archivo):
            print(f"⏭️ {nombre_archivo} ya existe. Saltando...")
            continue
            
        print(f"📥 [{index+1}/{len(df_links)}] Descargando: {nombre_archivo}...")
        
        try:
            driver.get(url)
            
            # ⏳ PAUSA ESTRATÉGICA (Crucial para que FBref no nos bloquee)
            # 4 segundos es lo ideal para parecer un humano leyendo la web
            time.sleep(4) 
            
            # Guardar el código fuente exacto
            html_content = driver.page_source
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            descargados_hoy += 1
            
        except Exception as e:
            print(f"⚠️ Error descargando {url}: {e}")
            
    # 5. Apagar motores
    driver.quit()
    print(f"\n✅ ¡MISIÓN CUMPLIDA! Se han descargado {descargados_hoy} nuevos partidos.")
    print("📍 Ya puedes lanzar la 'Excavadora Nivel Dios'.")

if __name__ == "__main__":
    descargar_htmls_faltantes()