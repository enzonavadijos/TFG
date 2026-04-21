import pandas as pd
from bs4 import BeautifulSoup
import time
import os
import undetected_chromedriver as uc

# --- RUTAS ---
CARPETA_CSV = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ruta_salida = os.path.join(CARPETA_CSV, "Lista_Links_PostMessi_FBref.csv")

# Las 4 temporadas que nos faltan
temporadas = {
    "2021-2022": "https://fbref.com/en/squads/206d90db/2021-2022/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga",
    "2022-2023": "https://fbref.com/en/squads/206d90db/2022-2023/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga",
    "2023-2024": "https://fbref.com/en/squads/206d90db/2023-2024/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga",
    "2024-2025": "https://fbref.com/en/squads/206d90db/2024-2025/matchlogs/c12/schedule/Barcelona-Scores-and-Fixtures-La-Liga"
}

def extraer_enlaces_furtivo():
    print("--- 🥷 INICIANDO MODO FURTIVO: RASTREO DE ENLACES ---")
    
    # 🔥 Variables seguras dentro de la función
    datos_partidos = []
    id_ficticio = 5000 
    
    # 1. Levantamos el Chrome camuflado (fijado a tu versión 146)
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, version_main=146) 

    for temp, url in temporadas.items():
        print(f"\n🚀 Infiltrándonos en la temporada: {temp}...")
        try:
            driver.get(url)
            
            # 2. ESPERA INTELIGENTE ANTI-CLOUDFLARE
            intentos = 0
            while "Just a moment" in driver.title or "Cloudflare" in driver.title:
                print("   🛡️ Cloudflare detectado. El camuflaje está actuando, espera...")
                time.sleep(3)
                intentos += 1
                if intentos > 15:
                    print("   ⚠️ Atascado. Haz clic manual en la casilla de Chrome si la ves.")
                    break
            
            # Pausa de seguridad para que la tabla HTML termine de renderizarse
            time.sleep(5)
            
            # 3. Cogemos el HTML ya validado y lo pasamos a BeautifulSoup
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 4. Buscamos la tabla principal
            tabla = soup.find('table', {'id': 'matchlogs_for'})
            
            if not tabla:
                print(f"   ⚠️ No se encontró la tabla en {temp}. Quizá la página cargó mal.")
                continue

            filas = tabla.find('tbody').find_all('tr')
            enlaces_temp = 0

            for fila in filas:
                if 'spacer' in fila.get('class', []): 
                    continue

                td_fecha = fila.find('th', {'data-stat': 'date'})
                if not td_fecha or not td_fecha.text.strip(): 
                    continue
                fecha = td_fecha.text.strip()

                td_rival = fila.find('td', {'data-stat': 'opponent'})
                rival = td_rival.text.strip() if td_rival else "Desconocido"

                td_report = fila.find('td', {'data-stat': 'match_report'})
                a_tag = td_report.find('a') if td_report else None

                if a_tag and 'href' in a_tag.attrs:
                    link_completo = "https://fbref.com" + a_tag['href']

                    datos_partidos.append({
                        'ID_Partido': id_ficticio,
                        'Temporada': temp,
                        'Fecha': fecha,
                        'Rival': rival,
                        'URL_FBref': link_completo
                    })
                    id_ficticio += 1
                    enlaces_temp += 1

            print(f"   ✅ {enlaces_temp} enlaces extraídos de {temp}.")
            time.sleep(3) # Pausa de cortesía entre temporadas

        except Exception as e:
            print(f"   ❌ Fallo en {temp}: {e}")

    # 5. Cerramos el navegador ninja y guardamos
    driver.quit()
    
    if datos_partidos:
        df_links = pd.DataFrame(datos_partidos)
        df_links.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"\n🎉 ¡VICTORIA! {len(df_links)} enlaces guardados en: {ruta_salida}")
    else:
        print("\n⚠️ Operación fallida. No se ha extraído ningún enlace.")

if __name__ == "__main__":
    extraer_enlaces_furtivo()