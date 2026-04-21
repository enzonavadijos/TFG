import requests
import os
import time
import random

# --- CONFIGURACIÓN ---
OUTPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\HTML_Champions"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# IDs
FBREF_TEAM_ID = "206d90db"
COMP_ID = "c8" # Champions League
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def main():
    print("--- 💾 FASE 1: DESCARGA MASIVA DE HTMLs (CHAMPIONS) ---")
    
    # Rango de temporadas (2003 a 2025)
    for year in range(2003, 2026):
        season_str = f"{year}-{year+1}"
        
        # URL ESPECÍFICA DE "MATCH LOGS" (Resultados y xG partido a partido)
        # Es la más limpia para lo que queremos.
        url = f"https://fbref.com/en/squads/{FBREF_TEAM_ID}/{season_str}/matchlogs/{COMP_ID}/Barcelona-Match-Logs-Champions-League"
        
        filename = f"champions_{season_str}.html"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        
        # Si ya existe, no lo volvemos a descargar (ahorramos tiempo y riesgo)
        if os.path.exists(filepath):
            print(f"✅ {season_str} ya existe en local. Saltando.")
            continue
            
        print(f"⬇️ Descargando {season_str}...", end=" ")
        
        try:
            response = requests.get(url, headers=HEADERS)
            
            if response.status_code == 200:
                # Guardamos el HTML crudo
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("✅ Guardado.")
                
                # Pausa de seguridad (Vital para FBref)
                time.sleep(random.uniform(5, 8))
                
            elif response.status_code == 429:
                print("🛑 BLOQUEO (Too Many Requests). Espera 1 minuto.")
                break # Paramos para no empeorarlo
            else:
                print(f"⚠️ Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error de conexión: {e}")

    print(f"\n📁 Todos los archivos guardados en: {OUTPUT_FOLDER}")

if __name__ == "__main__":
    main()