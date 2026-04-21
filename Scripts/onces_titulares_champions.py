import pandas as pd
import os
import re
import zlib
from bs4 import BeautifulSoup

# --- CONFIGURACIÓN ---
INPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\HTML_Champions\Partidos a analizar (Campeones_o_Semis)"
OUTPUT_FOLDER = r"C:\Users\enson\Desktop\TFG\ETL\CSV\Champions League"

def limpiar_html(html):
    return html.replace("", "")

def generar_id(fecha, rival):
    firma = f"{fecha}_{rival}"
    return zlib.crc32(firma.encode('utf-8'))

def limpiar_fecha_pbi(fecha_raw):
    clean = re.sub(r'\s*\(.*?\)', '', fecha_raw)
    clean = re.sub(r'El\s*Cl[áa]sico', '', clean, flags=re.IGNORECASE)
    return " ".join(clean.split())

def procesar_partido(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(limpiar_html(f.read()), "html.parser")
        
        # --- 1. METADATOS (Igual que antes) ---
        title = soup.title.string if soup.title else ""
        if "Barcelona" not in title and "vs." not in title:
            return None, [] 

        try:
            if "vs." in title:
                parts = title.split("vs.")
                rival = parts[1].split("Match Report")[0].strip() if "Barcelona" in parts[0] else parts[0].strip()
            else:
                rival = "Desconocido"
            
            date_match = re.search(r'Match Report – (.+)', title)
            fecha = limpiar_fecha_pbi(date_match.group(1).split("|")[0].strip()) if date_match else "Unknown"
            id_partido = generar_id(fecha, rival)
        except:
            return None, [] 

        # --- 2. DETECTAR SUPLENTES (Desde el Timeline) ---
        # Buscamos quién entró desde el banquillo para DESCARTARLO del 11 titular
        ids_suplentes = set()
        events_div = soup.find("div", id="events_wrap")
        
        if events_div:
            for event in events_div.find_all("div", class_="event"):
                # Si es una sustitución
                if "sub" in str(event).lower():
                    links = event.find_all("a")
                    # En FBref, formato: "Entra X por Y". El primer link es el que entra (Suplente)
                    if len(links) > 0:
                        href = links[0].get("href")
                        if href: ids_suplentes.add(href)

        # --- 3. EXTRAER STATS Y FILTRAR TITULARES ---
        stats_data = {
            "id_partido": id_partido, 
            "fecha": fecha, 
            "rival": rival,
            "posesion_barca": None,
            "goles_barca": 0
        }
        lineups = []

        # -- Posesión y Goles --
        try:
            # Posesión
            stats_div = soup.find("div", id="team_stats")
            if stats_div:
                for row in stats_div.find_all("tr"):
                    if "Possession" in row.get_text():
                        vals = row.find_all("td")
                        if vals: stats_data["posesion_barca"] = vals[0].get_text().strip()
            # Goles
            scorebox = soup.find("div", class_="scorebox")
            if scorebox:
                scores = scorebox.find_all("div", class_="score")
                if len(scores) >= 2: stats_data["goles_barca"] = scores[0].get_text().strip()
        except: pass

        # -- Titulares (Lógica de Descarte) --
        try:
            # Buscamos todas las tablas, nos quedamos con la del Barça que tenga stats
            tables = soup.find_all("table")
            for tab in tables:
                caption = tab.caption.get_text() if tab.caption else ""
                
                # Buscamos la tabla "Barcelona Player Stats"
                if "Barcelona" in caption and "Stats" in caption and "Goalkeeper" not in caption:
                    body = tab.find("tbody")
                    if body:
                        rows = body.find_all("tr")
                        for row in rows:
                            # Filtramos filas que no sean jugadores (cabeceras repetidas, separadores)
                            clase = row.get("class", [])
                            if "thead" in clase or "spacer" in clase: continue

                            # Buscamos el nombre y el link del jugador
                            th = row.find("th", {"data-stat": "player"})
                            if th:
                                link_tag = th.find("a")
                                if link_tag:
                                    jugador_nombre = link_tag.get_text(strip=True)
                                    jugador_href = link_tag.get("href") # El ID único
                                    
                                    # LÓGICA MAESTRA:
                                    # Si el jugador NO está en la lista de suplentes que entraron... ES TITULAR.
                                    # (Asumiendo que la tabla solo muestra gente que jugó, como vimos en tu imagen)
                                    if jugador_href not in ids_suplentes:
                                        lineups.append({
                                            "id_partido": id_partido,
                                            "fecha": fecha,
                                            "equipo_rival": rival,
                                            "minuto": 0,
                                            "jugador_implicado": jugador_nombre,
                                            "tipo_evento": "TITULAR",
                                            "detalle_accion": "Alineación Inicial",
                                            "fase": "Champions"
                                        })
        except Exception as e:
            pass

        return stats_data, lineups

    except Exception as e:
        print(f"❌ Error archivo {os.path.basename(filepath)}: {e}")
        return None, []

def main():
    print("--- 🕵️‍♂️ DETECTIVE DE ALINEACIONES (LOGICA DE DESCARTE) ---")
    
    if not os.path.exists(INPUT_FOLDER):
        print("❌ Carpeta no encontrada.")
        return

    archivos_stats = []
    archivos_lineups = []
    count = 0
    
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                stats, lineups = procesar_partido(path)
                
                if stats: 
                    archivos_stats.append(stats)
                    count += 1
                if lineups: 
                    archivos_lineups.extend(lineups)
                
                if count % 10 == 0: print(f".", end="")

    print(f"\nProcesados {count} partidos.")

    if archivos_stats:
        df_stats = pd.DataFrame(archivos_stats)
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        df_stats.to_csv(os.path.join(OUTPUT_FOLDER, "Fact_Champions_Stats.csv"), index=False)
        print("✅ Stats guardadas.")

    if archivos_lineups:
        df_lineups = pd.DataFrame(archivos_lineups)
        df_lineups.to_csv(os.path.join(OUTPUT_FOLDER, "Fact_Champions_Titulares.csv"), index=False)
        print("✅ Titulares guardados (usando cruce de IDs).")

if __name__ == "__main__":
    main()