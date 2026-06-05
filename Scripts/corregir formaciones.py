import pandas as pd
import os

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = r"C:\Users\enson\Desktop\TFG\ETL\CSV"
PATH_TACTICA = os.path.join(BASE_DIR, "Fact_Tactica_Avanzada.csv")
PATH_STATSBOMB = os.path.join(BASE_DIR, "Fact_Tacticas_Oficiales_SB.csv")

def imputar_formaciones_tacticas():
    """
    Realiza un cruce relacional entre la tabla de hechos tácticos y los datos 
    oficiales de StatsBomb para imputar los valores nulos o desconocidos en 
    la columna de formaciones, utilizando la fecha como clave temporal.
    """
    print("--- INICIANDO IMPUTACIÓN DE FORMACIONES TÁCTICAS ---")
    
    # 1. Lectura de las tablas de datos
    df_tactica = pd.read_csv(PATH_TACTICA)
    df_statsbomb = pd.read_csv(PATH_STATSBOMB)
    
    registros_desconocidos_iniciales = len(df_tactica[df_tactica['Formacion'] == 'Desconocida'])
    print(f"Info: Registros con formación 'Desconocida' antes del cruce: {registros_desconocidos_iniciales}")
    
    # 2. Cruce relacional (Left Merge) utilizando la fecha como puente
    df_resultado = df_tactica.merge(
        df_statsbomb[['fecha', 'formacion_oficial']], 
        left_on='Fecha', 
        right_on='fecha', 
        how='left'
    )
    
    # 3. Regla de imputación: 
    # Solo se actualiza el registro si el valor actual es 'Desconocida' 
    # y existe información válida en la fuente secundaria (StatsBomb)
    condicion_imputacion = (df_resultado['Formacion'] == 'Desconocida') & (df_resultado['formacion_oficial'].notna())
    df_resultado.loc[condicion_imputacion, 'Formacion'] = df_resultado.loc[condicion_imputacion, 'formacion_oficial']
    
    # 4. Limpieza de columnas auxiliares utilizadas durante el cruce
    df_resultado = df_resultado.drop(columns=['fecha', 'formacion_oficial'])
    
    registros_desconocidos_finales = len(df_resultado[df_resultado['Formacion'] == 'Desconocida'])
    registros_recuperados = registros_desconocidos_iniciales - registros_desconocidos_finales
    
    print(f"Info: Registros con formación 'Desconocida' después del cruce: {registros_desconocidos_finales}")
    print(f"Éxito: Se han imputado correctamente {registros_recuperados} formaciones históricas.")
    
    # 5. Exportación sobrescribiendo el archivo original para su ingesta en Power BI
    df_resultado.to_csv(PATH_TACTICA, index=False, encoding='utf-8-sig')
    print("Archivo de táctica avanzada actualizado y exportado exitosamente.")

if __name__ == "__main__":
    imputar_formaciones_tacticas()