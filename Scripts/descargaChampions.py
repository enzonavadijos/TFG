import requests
import os
import time
import random

# --- CONFIGURACIÓN DE PARÁMETROS Y RUTAS ---
OUTPUT_DIR = r"C:\Users\enson\Desktop\TFG\HTML_Champions"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Identificadores estáticos de la fuente de datos
FBREF_TEAM_ID = "206d90db"
COMPETITION_ID = "c8" # Identificador interno para la Champions League

# Falsificación de cabeceras HTTP para simular peticiones orgánicas de navegadores
HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def extraer_match_logs_champions():
    """
    Realiza peticiones HTTP estándar para descargar de forma masiva el código 
    fuente (HTML) de los registros de partidos (Match Logs) de la Champions League, 
    implementando control de tasa de peticiones (Rate Limiting).
    """
    print("--- INICIANDO EXTRACCIÓN MASIVA DE HTML (CHAMPIONS LEAGUE) ---")
    
    # Iteración sobre el rango de temporadas históricas (2003 a 2025)
    for anio in range(2003, 2026):
        temporada_str = f"{anio}-{anio+1}"
        
        # Construcción dinámica de la URL objetivo
        url_objetivo = f"https://fbref.com/en/squads/{FBREF_TEAM_ID}/{temporada_str}/matchlogs/{COMPETITION_ID}/Barcelona-Match-Logs-Champions-League"
        
        nombre_archivo = f"champions_{temporada_str}.html"
        ruta_archivo = os.path.join(OUTPUT_DIR, nombre_archivo)
        
        # Control de idempotencia para omitir descargas redundantes y optimizar tiempos de red
        if os.path.exists(ruta_archivo):
            print(f"Info: La temporada {temporada_str} ya existe en el directorio local. Omitiendo descarga.")
            continue
            
        print(f"Extrayendo datos de la temporada {temporada_str}...", end=" ")
        
        try:
            # Ejecución de la petición GET inyectando el User-Agent
            respuesta = requests.get(url_objetivo, headers=HTTP_HEADERS)
            
            # Evaluación de los códigos de estado HTTP
            if respuesta.status_code == 200:
                # Persistencia del código HTML en bruto
                with open(ruta_archivo, "w", encoding="utf-8") as archivo_html:
                    archivo_html.write(respuesta.text)
                print("Completado.")
                
                # Estrategia de Throttling: Pausa estocástica para evitar bloqueos por Rate Limiting
                time.sleep(random.uniform(5, 8))
                
            elif respuesta.status_code == 429:
                print("Alerta: Límite de peticiones excedido (Error HTTP 429 - Too Many Requests).")
                print("Abortando la ejecución secuencial para prevenir un bloqueo de la dirección IP.")
                break 
            else:
                print(f"Error de protocolo: Código HTTP {respuesta.status_code}")
                
        except Exception as e:
            print(f"Error crítico de conexión durante la extracción: {e}")

    print(f"\nProceso finalizado. El conjunto de archivos HTML se encuentra persistido en: {OUTPUT_DIR}")

if __name__ == "__main__":
    extraer_match_logs_champions()