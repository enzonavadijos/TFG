import pandas as pd
import os

# --- RUTAS ---
CARPETA_BASE = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
ruta_dim_partidos = os.path.join(CARPETA_BASE, "Dim_Partidos.csv")
ruta_entrenadores = os.path.join(CARPETA_BASE, "Dim_Entrenadores.csv")

def actualizar_dim_entrenadores():
    print("--- 👔 ACTUALIZANDO DIM_ENTRENADORES Y DIM_PARTIDOS (MODO ID NUMÉRICO) ---")
    
    # 1. Fechas oficiales de los banquillos del Barça
    datos_entrenadores = [
        {"Entrenador": "Frank Rijkaard", "Inicio": "2003-07-01", "Fin": "2008-06-30"},
        {"Entrenador": "Pep Guardiola", "Inicio": "2008-07-01", "Fin": "2012-06-30"},
        {"Entrenador": "Tito Vilanova", "Inicio": "2012-07-01", "Fin": "2013-07-19"},
        {"Entrenador": "Gerardo Martino", "Inicio": "2013-07-23", "Fin": "2014-05-17"},
        {"Entrenador": "Luis Enrique", "Inicio": "2014-05-19", "Fin": "2017-06-30"},
        {"Entrenador": "Ernesto Valverde", "Inicio": "2017-07-01", "Fin": "2020-01-13"},
        {"Entrenador": "Quique Setién", "Inicio": "2020-01-13", "Fin": "2020-08-17"},
        {"Entrenador": "Ronald Koeman", "Inicio": "2020-08-19", "Fin": "2021-10-27"},
        {"Entrenador": "Sergi Barjuan", "Inicio": "2021-10-28", "Fin": "2021-11-05"},
        {"Entrenador": "Xavi Hernández", "Inicio": "2021-11-06", "Fin": "2024-05-26"},
        {"Entrenador": "Hansi Flick", "Inicio": "2024-05-29", "Fin": "2026-06-30"}
    ]
    
    # Crear la Dimensión con su ID
    dim_entrenadores = pd.DataFrame(datos_entrenadores)
    dim_entrenadores['Inicio'] = pd.to_datetime(dim_entrenadores['Inicio'])
    dim_entrenadores['Fin'] = pd.to_datetime(dim_entrenadores['Fin'])
    dim_entrenadores.insert(0, 'ID_Entrenador', dim_entrenadores.index + 1)
    
    dim_entrenadores.to_csv(ruta_entrenadores, index=False)
    print(f"✅ Dim_Entrenadores guardada con {len(dim_entrenadores)} técnicos y sus IDs listos.")

    # 2. Conectar mediante el ID_Entrenador a la Dim_Partidos
    try:
        dim_partidos = pd.read_csv(ruta_dim_partidos)
        
        # Si ejecutaste el script anterior, borramos la columna de texto para dejarlo limpio
        if 'Entrenador' in dim_partidos.columns:
            dim_partidos = dim_partidos.drop(columns=['Entrenador'])
            print("🧹 Borrada la antigua columna de texto 'Entrenador'...")

        # Usamos una columna datetime temporal para comparar bien las fechas
        dim_partidos['Fecha_Temp'] = pd.to_datetime(dim_partidos['Fecha'])
        
        def obtener_id_entrenador(fecha):
            for _, row in dim_entrenadores.iterrows():
                if row['Inicio'] <= fecha <= row['Fin']:
                    return row['ID_Entrenador']
            return None # Nulo si no encuentra coincidencia
            
        dim_partidos['ID_Entrenador'] = dim_partidos['Fecha_Temp'].apply(obtener_id_entrenador)
        
        # Forzamos que sea un número entero (Int64 soporta nulos sin poner decimales feos)
        dim_partidos['ID_Entrenador'] = dim_partidos['ID_Entrenador'].astype('Int64')
        
        # Limpiamos la columna temporal
        dim_partidos = dim_partidos.drop(columns=['Fecha_Temp'])

        # Ponemos el ID_Entrenador al principio (junto a ID_Partido e ID_StatsBomb)
        cols = dim_partidos.columns.tolist()
        cols.remove('ID_Entrenador')
        cols.insert(2, 'ID_Entrenador') # Lo metemos en la 3ª posición
        dim_partidos = dim_partidos[cols]

        dim_partidos.to_csv(ruta_dim_partidos, index=False)
        print("✅ ¡Dim_Partidos actualizada con éxito! Ahora tienes la columna numérica 'ID_Entrenador'.")
        
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {ruta_dim_partidos}")

if __name__ == "__main__":
    actualizar_dim_entrenadores()