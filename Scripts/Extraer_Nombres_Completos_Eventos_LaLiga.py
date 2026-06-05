import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
DIR_LALIGA = r"C:\Users\enson\Desktop\TFG\ETL\CSV\LaLiga"
PATH_INPUT = os.path.join(DIR_LALIGA, "Detalle_Eventos_LaLiga_Total.csv")
PATH_OUTPUT = os.path.join(DIR_LALIGA, "Nombres_Unicos_LaLiga.csv")

def extraer_entidades_jugadores():
    """
    Lee el registro detallado de eventos tabulados de LaLiga, aísla la columna 
    de jugadores y genera un catálogo de entidades únicas (dimensión incipiente). 
    Elimina registros nulos para garantizar la consistencia referencial.
    """
    print("--- INICIANDO EXTRACCIÓN DE ENTIDADES ÚNICAS (JUGADORES) ---")
    
    try:
        print("Info: Cargando el registro histórico de eventos en memoria...")
        df_eventos = pd.read_csv(PATH_INPUT) 

        # Aislamiento estructural y deduplicación de la identidad de los jugadores
        # Se emplea .dropna() para omitir eventos sin autoría (ej. incidentes de partido) 
        # y .unique() para optimizar el vector reduciéndolo a valores únicos.
        df_nombres_unicos = pd.DataFrame(df_eventos['jugador'].dropna().unique(), columns=['Nombre_Largo_LaLiga'])

        # Exportación del conjunto de datos.
        # Se emplea el separador ';' para mantener la compatibilidad nativa con la 
        # configuración regional europea de Microsoft Excel / Power BI.
        # Se inyecta 'utf-8-sig' para preservar la codificación de caracteres especiales (tildes, diéresis).
        df_nombres_unicos.to_csv(PATH_OUTPUT, index=False, sep=';', encoding='utf-8-sig')

        print(f"Operación completada: Se ha consolidado un catálogo con {len(df_nombres_unicos)} nombres únicos.")
        print(f"Archivo persistido exitosamente en: {PATH_OUTPUT}")
        
    except FileNotFoundError:
        print(f"Error crítico: No se ha localizado el archivo de origen en {PATH_INPUT}")
    except Exception as e:
        print(f"Error inesperado durante la extracción de entidades: {e}")

if __name__ == "__main__":
    extraer_entidades_jugadores()