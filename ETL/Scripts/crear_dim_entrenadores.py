import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_DIM_PARTIDOS = os.path.join(BASE_DIR, "Dim_Partidos.csv")
PATH_DIM_ENTRENADORES = os.path.join(BASE_DIR, "Dim_Entrenadores.csv")

def actualizar_dimension_entrenadores():
    """
    Genera la tabla dimensional de entrenadores con sus respectivos periodos 
    de vigencia y actualiza la tabla de partidos, asignando la clave foránea 
    (ID_Entrenador) correspondiente según la fecha del encuentro.
    """
    print("--- INICIANDO ACTUALIZACIÓN DE DIMENSIÓN DE ENTRENADORES ---")
    
    # 1. Definición de la cronología oficial del cuerpo técnico
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
    
    # Creación de la estructura dimensional y asignación de clave primaria secuencial
    df_dim_entrenadores = pd.DataFrame(datos_entrenadores)
    df_dim_entrenadores['Inicio'] = pd.to_datetime(df_dim_entrenadores['Inicio'])
    df_dim_entrenadores['Fin'] = pd.to_datetime(df_dim_entrenadores['Fin'])
    df_dim_entrenadores.insert(0, 'ID_Entrenador', df_dim_entrenadores.index + 1)
    
    # Exportación de la dimensión estática
    df_dim_entrenadores.to_csv(PATH_DIM_ENTRENADORES, index=False)
    print(f"Info: Dimensión de entrenadores exportada exitosamente con {len(df_dim_entrenadores)} registros estructurados.")

    # 2. Integración relacional con la dimensión de partidos
    try:
        df_dim_partidos = pd.read_csv(PATH_DIM_PARTIDOS)
        
        # Eliminación de la columna de texto original para normalizar el esquema a IDs numéricos
        if 'Entrenador' in df_dim_partidos.columns:
            df_dim_partidos = df_dim_partidos.drop(columns=['Entrenador'])
            print("Info: Columna de texto 'Entrenador' eliminada para proceder a la normalización relacional.")

        # Conversión de tipo a datetime en una columna temporal para permitir la evaluación lógica
        df_dim_partidos['Fecha_Temp'] = pd.to_datetime(df_dim_partidos['Fecha'])
        
        def obtener_id_entrenador(fecha):
            """Función auxiliar para identificar al entrenador vigente en una fecha dada."""
            for _, row in df_dim_entrenadores.iterrows():
                if row['Inicio'] <= fecha <= row['Fin']:
                    return row['ID_Entrenador']
            return None 
            
        df_dim_partidos['ID_Entrenador'] = df_dim_partidos['Fecha_Temp'].apply(obtener_id_entrenador)
        
        # Conversión al tipo Int64 nativo de Pandas. 
        # Este tipo permite la coexistencia de valores enteros puros y valores nulos (NaN) sin forzar decimales flotantes.
        df_dim_partidos['ID_Entrenador'] = df_dim_partidos['ID_Entrenador'].astype('Int64')
        
        # Eliminación de estructuras auxiliares
        df_dim_partidos = df_dim_partidos.drop(columns=['Fecha_Temp'])

        # Reordenación espacial: se desplaza la nueva clave foránea a las primeras posiciones del DataFrame
        columnas = df_dim_partidos.columns.tolist()
        columnas.remove('ID_Entrenador')
        columnas.insert(2, 'ID_Entrenador') 
        df_dim_partidos = df_dim_partidos[columnas]

        df_dim_partidos.to_csv(PATH_DIM_PARTIDOS, index=False)
        print("Proceso completado: Tabla de partidos actualizada exitosamente con la clave foránea numérica 'ID_Entrenador'.")
        
    except FileNotFoundError:
        print(f"Error crítico: No se ha localizado el archivo en la ruta especificada: {PATH_DIM_PARTIDOS}")

if __name__ == "__main__":
    actualizar_dimension_entrenadores()