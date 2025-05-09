# Paso 1.0: Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Paso 1.2: Crear la carpeta donde Kaggle busca las credenciales y librerias necesarias
# "os" es una librería de Python que nos deja interactuar con el sistema operativo.
import os
import pandas as pd
import zipfile # Para trabajar con archivos .zip
import numpy as np

# os.environ['KAGGLE_CONFIG_DIR'] le dice a Kaggle dónde buscar el archivo de configuración.
# os.makedirs crea la carpeta si no existe. 'exist_ok=True' evita un error si la carpeta ya fue creada.
kaggle_config_dir = os.path.join(os.environ.get('KAGGLE_CONFIG_DIR', '/root/.kaggle'))
os.makedirs(kaggle_config_dir, exist_ok=True)
print(f"Carpeta de configuración de Kaggle creada en: {kaggle_config_dir}")

# Paso 1.3: Definir la ruta del archivo kaggle.json en su Google Drive
drive_source_path = '/content/drive/MyDrive/Educacion/Ingenieria_ITM/kaggle.json'
destination_path = os.path.join(kaggle_config_dir, 'kaggle.json')

print(f"Buscando archivo kaggle.json en: {drive_source_path}")

# Paso 1.4: Copiar el archivo kaggle.json desde Drive a la carpeta de Kaggle
if os.path.exists(drive_source_path):
    # Copiar el archivo en lugar de moverlo, para que conserve su original en Drive.
    import shutil # "shutil" es otra librería para operaciones de archivos.
    shutil.copy(drive_source_path, destination_path)
    print(f"Archivo '{drive_source_path}' copiado exitosamente a '{destination_path}'.")

    # Paso 1.5: Establecer los permisos correctos para el archivo kaggle.json
    !chmod 600 {destination_path}
    print(f"\nPermisos establecidos para '{destination_path}'. ¡Configuración lista!")

    # Paso 1.6 (Opcional pero recomendado): Verificar la configuración
    print("\nIntentando listar datasets de Kaggle para verificar...")
    !kaggle datasets list -s "titanic" # Buscamos datasets que contengan la palabra "titanic" como ejemplo.
else:
    print(f"¡ERROR! No se encontró el archivo '{drive_source_path}'.")
    print("Por favor, verifique lo siguiente:")
    print("   1. Que la ruta en Google Drive sea correcta.")
    print("   2. Que el archivo se llame 'kaggle.json' (y no 'kaggle.js' u otro nombre).")
    print("   3. Que haya autorizado el acceso a Google Drive en el paso de montaje.")

# Paso 1: Importar las librerías necesarias
import os
import pandas as pd # Para manipular las tablas de datos (DataFrames)
import zipfile # Para trabajar con archivos .zip

# Paso 2: Definir el slug del dataset en Kaggle
# El formato es 'usuario/nombre-dataset'
dataset_slug = "vinicius150987/titanic3" # ¡Este es el dataset que me pasaste, baby!

# Paso 3: Crear un directorio para guardar los datos del dataset
# Usaremos el nombre del dataset para la carpeta.
dataset_name = dataset_slug.split('/')[-1] # Esto extrae 'titanic3' del slug
data_path = f'/content/{dataset_name}_data/'
os.makedirs(data_path, exist_ok=True)
print(f"Directorio para los datos creado en: {data_path}")

# Paso 4: Descargar los archivos del dataset
# Usamos el comando: kaggle datasets download -d [SLUG_DEL_DATASET] -p [RUTA_DESTINO]
print(f"\nDescargando datos del dataset '{dataset_slug}'...")
!kaggle datasets download -d {dataset_slug} -p {data_path} --force

# Paso 5: Listar los archivos descargados para ver qué tenemos
print("\nArchivos descargados en el directorio de datos (antes de posible descompresión):")
downloaded_files = os.listdir(data_path)
for f_name in downloaded_files:
    print(os.path.join(data_path, f_name))

# Paso 6: Descomprimir el archivo .zip si se descargó uno
# El archivo descargado por 'kaggle datasets download' a veces conserva el nombre original
# o se llama 'dataset_slug_sin_usuario.zip', por ejemplo 'titanic3.zip'.
# Vamos a buscar un archivo .zip en la carpeta de destino.

zip_file_path_generic = os.path.join(data_path, f'{dataset_name}.zip') # Ej: /content/titanic3_data/titanic3.zip

if os.path.exists(zip_file_path_generic):
    print(f"\nArchivo zip '{zip_file_path_generic}' encontrado. Descomprimiendo...")
    with zipfile.ZipFile(zip_file_path_generic, 'r') as zip_ref:
        zip_ref.extractall(data_path)
    print(f"Archivos descomprimidos en: {data_path}")
    # Opcional: Borrar el archivo .zip después de descomprimir
    # os.remove(zip_file_path_generic)
    # print(f"Archivo zip '{zip_file_path_generic}' eliminado.")
else:
    print(f"\nNo se encontró el archivo '{zip_file_path_generic}'.")
    print("Verificando si hay archivos CSV o XLS directamente o si ya se descomprimió.")

# Paso 7: Listar los archivos nuevamente después de la posible descompresión
print("\nArchivos en el directorio de datos (después de posible descompresión):")
all_files_in_path = []
for dirname, _, filenames in os.walk(data_path):
    for filename in filenames:
        full_path = os.path.join(dirname, filename)
        all_files_in_path.append(full_path)
        print(full_path)

# Paso 8: Identificar y cargar el archivo de datos principal (CSV o XLS)
# Basado en tu reporte, el archivo es 'titanic3.xls'.
# Vamos a buscarlo.
data_file_to_load = None
df_bronze = None

# Nombres de archivo esperados
csv_file_name = "titanic3.csv"
xls_file_name = "titanic3.xls"

# Rutas completas esperadas
expected_csv_path = os.path.join(data_path, csv_file_name)
expected_xls_path = os.path.join(data_path, xls_file_name)

print(f"\nBuscando archivo de datos principal...")

if os.path.exists(expected_xls_path):
    print(f"Archivo Excel '{expected_xls_path}' encontrado.")
    data_file_to_load = expected_xls_path
    try:
        df_bronze = pd.read_excel(data_file_to_load) # ¡Usamos read_excel para archivos .xls!
        print(f"'{data_file_to_load}' cargado exitosamente en un DataFrame.")
    except Exception as e:
        print(f"Error al cargar el archivo Excel '{data_file_to_load}': {e}")
        df_bronze = None # Aseguramos que df_bronze sea None si hay error
elif os.path.exists(expected_csv_path):
    print(f"Archivo CSV '{expected_csv_path}' encontrado.")
    data_file_to_load = expected_csv_path
    try:
        df_bronze = pd.read_csv(data_file_to_load)
        print(f"'{data_file_to_load}' cargado exitosamente en un DataFrame.")
    except Exception as e:
        print(f"Error al cargar el archivo CSV '{data_file_to_load}': {e}")
        df_bronze = None
else:
    print(f"\nNo se encontró '{xls_file_name}' ni '{csv_file_name}' directamente.")
    print("Buscando otros archivos .csv o .xls en el directorio...")
    found_files = [f for f in all_files_in_path if f.endswith('.csv') or f.endswith('.xls') or f.endswith('.xlsx')]
    if found_files:
        data_file_to_load = found_files[0] # Tomamos el primer archivo compatible encontrado
        print(f"Se intentará cargar el primer archivo compatible encontrado: '{data_file_to_load}'")
        try:
            if data_file_to_load.endswith('.csv'):
                df_bronze = pd.read_csv(data_file_to_load)
            elif data_file_to_load.endswith('.xls') or data_file_to_load.endswith('.xlsx'):
                df_bronze = pd.read_excel(data_file_to_load)
            print(f"'{data_file_to_load}' cargado exitosamente en un DataFrame.")
        except Exception as e:
            print(f"Error al cargar el archivo '{data_file_to_load}': {e}")
            df_bronze = None
    else:
        print("No se encontraron archivos CSV o Excel compatibles en el directorio.")

if df_bronze is not None:
    # Paso 9: Echarle un ojito a los primeros datos (¡el chismoseo inicial!)
    print("\nPrimeras 5 filas del DataFrame (Capa Bronce):")
    print(df_bronze.head())

    print("\nInformación general del DataFrame (Capa Bronce):")
    df_bronze.info()

    print(f"\n¡Listo! El dataset '{data_file_to_load}' está cargado en 'df_bronze'.")
else:
    print(f"\n¡ERROR! No se pudo encontrar o cargar un archivo de datos principal (CSV o Excel).")
    print("Por favor, revise la lista de archivos descomprimidos arriba y la lógica de carga.")
    print("Archivos encontrados en el directorio:")
    for f in all_files_in_path:
        print(f)

# Asumimos que df_bronze ya está cargado de la etapa anterior.
# Si no, deberías ejecutar el código de la Capa Bronce primero.

import pandas as pd
import numpy as np # Numpy es fundamental para operaciones numéricas, y Pandas lo usa por debajo.

# Paso 0: Verificar que df_bronze existe
if 'df_bronze' not in globals() or df_bronze is None:
    print("¡ERROR! El DataFrame 'df_bronze' no existe o está vacío.")
    print("Asegúrate de haber ejecutado el código de la Capa Bronce para cargar los datos primero.")
    # Aquí podrías detener la ejecución o intentar recargar los datos si es necesario.
else:
    print("DataFrame 'df_bronze' encontrado. ¡Empezando la Capa de Plata!\n")

    # Paso 1: Crear una copia de df_bronze para la Capa de Plata
    # ¡Siempre trabajamos sobre una copia para no dañar los datos originales!
    df_silver = df_bronze.copy()
    print("Copia de df_bronze creada como df_silver.\n")

    # Paso 2: Análisis inicial de valores faltantes (en porcentaje)
    print("Porcentaje de valores faltantes por columna en df_silver (antes de la limpieza):")
    missing_percentage = (df_silver.isnull().sum() / len(df_silver)) * 100
    print(missing_percentage.sort_values(ascending=False))
    print("-" * 50)

    # Paso 3: Imputación de valores faltantes
    # 3.1. Columna 'age' (Edad)
    # Usaremos la mediana porque la edad puede tener valores extremos (outliers)
    # y la mediana es menos sensible a ellos que la media.
    median_age = df_silver['age'].median()
    df_silver['age'].fillna(median_age, inplace=True) # inplace=True modifica el DataFrame directamente
    print(f"Valores faltantes en 'age' imputados con la mediana: {median_age:.2f}")

    # 3.2. Columna 'embarked' (Puerto de Embarque)
    # Es una variable categórica. Usaremos la moda (el valor más frecuente).
    mode_embarked = df_silver['embarked'].mode()[0] # .mode() puede devolver varios si hay empate, tomamos el primero
    df_silver['embarked'].fillna(mode_embarked, inplace=True)
    print(f"Valores faltantes en 'embarked' imputados con la moda: {mode_embarked}")

    # 3.3. Columna 'fare' (Tarifa)
    # Similar a 'age', usaremos la mediana.
    # Primero verificamos si tiene faltantes que necesiten imputación.
    if df_silver['fare'].isnull().any():
        median_fare = df_silver['fare'].median()
        df_silver['fare'].fillna(median_fare, inplace=True)
        print(f"Valores faltantes en 'fare' imputados con la mediana: {median_fare:.2f}")
    else:
        print("La columna 'fare' no tiene valores faltantes significativos para imputar.")
    print("-" * 50)

    # Paso 4: Manejo de columnas con muchísimos faltantes o potencialmente menos informativas
    # Columnas como 'cabin', 'boat', 'body' tienen un alto porcentaje de NaN.
    # 'home.dest' también tiene bastantes.
    # 'ticket' es a menudo muy variado y difícil de usar directamente.

    # 4.1. 'cabin': Tiene demasiados faltantes.
    # Podríamos crear una característica 'has_cabin' (1 si tiene cabina, 0 si no).
    df_silver['has_cabin'] = df_silver['cabin'].notnull().astype(int)
    # Y luego eliminar la columna original 'cabin'.
    df_silver.drop('cabin', axis=1, inplace=True)
    print("Columna 'cabin' transformada a 'has_cabin' (1 o 0) y original eliminada.")

    # 4.2. Columnas a eliminar directamente por ahora (muchos NaNs o baja utilidad inicial)
    # 'boat', 'body', 'home.dest', 'ticket'
    # ¡OJO! La decisión de eliminar columnas depende mucho del objetivo del análisis.
    # Para este ejercicio inicial, las quitaremos para simplificar.
    columns_to_drop = ['boat', 'body', 'home.dest', 'ticket']
    # Verificamos que las columnas existan antes de intentar borrarlas
    existing_columns_to_drop = [col for col in columns_to_drop if col in df_silver.columns]
    if existing_columns_to_drop:
        df_silver.drop(columns=existing_columns_to_drop, axis=1, inplace=True)
        print(f"Columnas eliminadas: {existing_columns_to_drop}")
    else:
        print("Ninguna de las columnas especificadas para eliminar ('boat', 'body', 'home.dest', 'ticket') fue encontrada.")
    print("-" * 50)

    # Paso 5: Feature Engineering Básico - Crear 'family_size'
    # family_size = sibsp + parch + 1 (la persona misma)
    df_silver['family_size'] = df_silver['sibsp'] + df_silver['parch'] + 1
    print("Nueva columna 'family_size' creada.")
    # Podríamos considerar eliminar 'sibsp' y 'parch' después si 'family_size' las representa bien.
    # Por ahora las dejaremos.
    print("-" * 50)

    # Paso 6: Verificar el estado del DataFrame después de las transformaciones
    print("\nPrimeras 5 filas del DataFrame (Capa Silver):")
    print(df_silver.head())

    print("\nInformación general del DataFrame (Capa Silver):")
    df_silver.info()

    print("\nPorcentaje de valores faltantes por columna en df_silver (después de la limpieza):")
    missing_percentage_after = (df_silver.isnull().sum() / len(df_silver)) * 100
    print(missing_percentage_after.sort_values(ascending=False))

    print("\nEl DataFrame 'df_silver' está más limpio y con nuevas características.")

# streamlit_app.py

import streamlit as st
import pandas as pd
import snowflake.connector
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuración de la Página de Streamlit ---
st.set_page_config(
    page_title="Dashboard Titanic Básico",
    page_icon="🚢",
    layout="wide", # Puede ser "centered" o "wide"
    initial_sidebar_state="expanded" # Puede ser "auto", "expanded", "collapsed"
)

# --- Estilos Personalizados (Cozy & Pastel Blue - Básico) ---
# Streamlit tiene temas 'light' y 'dark'. Para más personalización, se usa CSS.
# Aquí un intento de guiar los colores a través de markdown y colores de gráficos.
st.markdown("""
<style>
    /* Intento de tonos azules pastel y cozy - esto es limitado sin CSS completo */
    /* Streamlit usa principalmente su propio sistema de theming */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #f0f8ff; /* AliceBlue - un azul muy pastel */
    }
    h1, h2, h3 {
        color: #2c3e50; /* Un azul oscuro para contraste y sensación 'cozy' */
    }
    .stButton>button {
        background-color: #77aadd; /* Un azul más fuerte para botones */
        color: white;
        border-radius: 5px;
    }
    /* Para aplicar un fondo a la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #e6f3ff; /* Un azul pastel más claro para la sidebar */
    }
</style>
""", unsafe_allow_html=True)

# --- Conexión a Snowflake ---
# ¡OJO, MOR! Estas credenciales son de ejemplo. Debe usar las suyas.
# Es MEJOR práctica usar los "Secrets" de Streamlit para esto.
# st.secrets["snowflake"]["user"], etc.

@st.cache_resource # Cachea el recurso de conexión
def init_connection():
    try:
        conn = snowflake.connector.connect(
            user=st.secrets.get("SNOWFLAKE_USER", "SU_USUARIO_DE_SNOWFLAKE"),
            password=st.secrets.get("SNOWFLAKE_PASSWORD", "SU_CONTRASENA"),
            account=st.secrets.get("SNOWFLAKE_ACCOUNT", "SU_URL_DE_CUENTA_SNOWFLAKE"), # ej: suorganizacion-suidentificador
            warehouse=st.secrets.get("SNOWFLAKE_WAREHOUSE", "SU_WAREHOUSE"),
            database=st.secrets.get("SNOWFLAKE_DATABASE", "SU_BASE_DE_DATOS"),
            schema=st.secrets.get("SNOWFLAKE_SCHEMA", "SU_ESQUEMA")
        )
        print("Conexión a Snowflake exitosa!")
        return conn
    except Exception as e:
        st.error(f"Error al conectar a Snowflake: {e}")
        print(f"Error al conectar a Snowflake: {e}")
        return None

conn = init_connection()

@st.cache_data(ttl=600) # Cachea los datos por 10 minutos
def run_query(_query):
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(_query)
                # Si es una consulta SELECT, obtener los resultados
                if cur.description: # Verifica si la consulta produjo resultados (como un SELECT)
                    df = cur.fetch_pandas_all()
                    return df
                else: # Para DML/DDL que no retornan dataframes directamente
                    return None
        except Exception as e:
            st.error(f"Error al ejecutar la consulta: {e}")
            print(f"Error al ejecutar la consulta: {e}")
            return pd.DataFrame() # Retorna DataFrame vacío en caso de error para evitar problemas posteriores
    return pd.DataFrame() # Retorna DataFrame vacío si no hay conexión


# --- Título del Dashboard ---
st.title("🚢 Dashboard de Supervivencia del Titanic 🚢")
st.markdown("### Explorando los datos de los pasajeros para entender los patrones de supervivencia.")
st.markdown("---")

# --- Sidebar para Navegación o Filtros (Opcional) ---
st.sidebar.header("Opciones de Análisis")
# Aquí podría agregar filtros si tuviera datos más granulares o diferentes datasets

# --- Análisis 1: Edad vs. Supervivencia ---
st.header("1. Relación entre Edad y Supervivencia")

# Asumimos que tiene una tabla en Snowflake llamada 'TITANIC_EDAD_SUPERVIVENCIA'
# con columnas: AGE_GROUP (VARCHAR), SURVIVAL_STATUS (VARCHAR), COUNT (NUMBER)
# Esta tabla la crearía a partir de los resultados de su análisis previo.
# Ejemplo de cómo podría haberla creado en Snowflake:
# CREATE OR REPLACE TABLE TITANIC_EDAD_SUPERVIVENCIA AS
# SELECT AGE_GROUP, SURVIVAL_STATUS, COUNT(*) AS COUNT
# FROM (
#   SELECT
#     CASE
#       WHEN AGE < 18 THEN 'Niño (<18)'
#       WHEN AGE >= 18 AND AGE <= 50 THEN 'Adulto Joven (18-50)'
#       ELSE 'Adulto Mayor (>50)'
#     END AS AGE_GROUP,
#     CASE WHEN SURVIVED = 1 THEN 'Sobrevivió' ELSE 'No Sobrevivió' END AS SURVIVAL_STATUS,
#     AGE, SURVIVED -- Columnas originales necesarias para el pre-procesamiento
#   FROM SU_TABLA_TITANIC_SILVER -- Su tabla principal del Titanic en Snowflake
#   WHERE AGE IS NOT NULL -- Importante manejar nulos en AGE
# )
# GROUP BY AGE_GROUP, SURVIVAL_STATUS;

query_edad = """
SELECT AGE_GROUP, SURVIVAL_STATUS, PASSENGER_COUNT
FROM SU_ESQUEMA.TITANIC_ANALYSIS_AGE_SURVIVAL;
-- Reemplace SU_ESQUEMA.TITANIC_ANALYSIS_AGE_SURVIVAL con el nombre real de su tabla agregada
"""
# Esta consulta asume que ya tiene una tabla pre-agregada en Snowflake.
# Si no, necesitaría hacer la agregación en la consulta SQL o en Pandas después de traer datos más crudos.

df_edad_data = run_query(query_edad)

if not df_edad_data.empty and 'AGE_GROUP' in df_edad_data.columns and 'SURVIVAL_STATUS' in df_edad_data.columns and 'PASSENGER_COUNT' in df_edad_data.columns:
    # Pivotear la tabla para graficarla fácilmente con Seaborn o Matplotlib
    try:
        df_edad_pivot = df_edad_data.pivot(index='AGE_GROUP', columns='SURVIVAL_STATUS', values='PASSENGER_COUNT').fillna(0)

        # Asegurar el orden de las categorías de edad
        age_order = ['Niño (<18)', 'Adulto Joven (18-50)', 'Adulto Mayor (>50)']
        df_edad_pivot = df_edad_pivot.reindex(age_order)

        fig_edad, ax_edad = plt.subplots(figsize=(10, 6))
        df_edad_pivot.plot(kind='bar', ax=ax_edad, color={'Sobrevivió':'#82E0AA', 'No Sobrevivió':'#EC7063'}, stacked=False)
        ax_edad.set_title('Supervivencia por Grupo de Edad', fontsize=14)
        ax_edad.set_xlabel('Grupo de Edad', fontsize=10)
        ax_edad.set_ylabel('Número de Pasajeros', fontsize=10)
        ax_edad.tick_params(axis='x', rotation=0)
        ax_edad.legend(title='Estado')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_edad)
    except Exception as e:
        st.error(f"Error al procesar o graficar datos de edad: {e}")
        st.dataframe(df_edad_data) # Mostrar los datos crudos si hay error en el pivote/gráfico
else:
    st.warning("No se pudieron cargar los datos para el análisis de edad o las columnas esperadas no existen.")
    if not df_edad_data.empty:
        st.write("Datos recibidos para edad (verificar nombres de columnas):", df_edad_data)

st.markdown("---")

# --- Análisis 2: Clase vs. Supervivencia ---
st.header("2. Supervivencia según Clase del Pasajero")
# Asumimos tabla 'TITANIC_CLASE_SUPERVIVENCIA' en Snowflake
# Columnas: PCLASS_LABEL (VARCHAR), SURVIVAL_STATUS (VARCHAR), COUNT (NUMBER)
query_clase = """
SELECT PCLASS_LABEL, SURVIVAL_STATUS, PASSENGER_COUNT
FROM SU_ESQUEMA.TITANIC_ANALYSIS_CLASS_SURVIVAL;
-- Reemplace SU_ESQUEMA.TITANIC_ANALYSIS_CLASS_SURVIVAL con el nombre real de su tabla agregada
"""
df_clase_data = run_query(query_clase)

if not df_clase_data.empty and 'PCLASS_LABEL' in df_clase_data.columns and 'SURVIVAL_STATUS' in df_clase_data.columns and 'PASSENGER_COUNT' in df_clase_data.columns:
    try:
        df_clase_pivot = df_clase_data.pivot(index='PCLASS_LABEL', columns='SURVIVAL_STATUS', values='PASSENGER_COUNT').fillna(0)

        # Asegurar el orden de las clases
        class_order = ['Primera Clase', 'Segunda Clase', 'Tercera Clase']
        df_clase_pivot = df_clase_pivot.reindex(class_order)

        fig_clase, ax_clase = plt.subplots(figsize=(10, 6))
        df_clase_pivot.plot(kind='bar', ax=ax_clase, color={'Sobrevivió':'#3498DB', 'No Sobrevivió':'#E74C3C'}, stacked=False)
        ax_clase.set_title('Supervivencia por Clase del Pasajero', fontsize=14)
        ax_clase.set_xlabel('Clase del Pasajero', fontsize=10)
        ax_clase.set_ylabel('Número de Pasajeros', fontsize=10)
        ax_clase.tick_params(axis='x', rotation=0)
        ax_clase.legend(title='Estado')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_clase)
    except Exception as e:
        st.error(f"Error al procesar o graficar datos de clase: {e}")
        st.dataframe(df_clase_data)
else:
    st.warning("No se pudieron cargar los datos para el análisis de clase o las columnas esperadas no existen.")
    if not df_clase_data.empty:
        st.write("Datos recibidos para clase (verificar nombres de columnas):", df_clase_data)

st.markdown("---")

# --- Análisis 3: Costo del Boleto vs. Supervivencia ---
st.header("3. Relación entre el Costo del Boleto y Supervivencia")
# Asumimos tabla 'TITANIC_TARIFA_PROMEDIO_SUPERVIVENCIA' en Snowflake
# Columnas: SURVIVAL_STATUS (VARCHAR), AVERAGE_FARE (NUMBER)
query_tarifa = """
SELECT SURVIVAL_STATUS, AVERAGE_FARE
FROM SU_ESQUEMA.TITANIC_ANALYSIS_FARE_SURVIVAL;
-- Reemplace SU_ESQUEMA.TITANIC_ANALYSIS_FARE_SURVIVAL con el nombre real de su tabla agregada
"""
df_tarifa_data = run_query(query_tarifa)

if not df_tarifa_data.empty and 'SURVIVAL_STATUS' in df_tarifa_data.columns and 'AVERAGE_FARE' in df_tarifa_data.columns:
    try:
        fig_tarifa, ax_tarifa = plt.subplots(figsize=(8, 6))
        # Crear el gráfico de barras directamente desde el DataFrame (ya está agregado)
        sns.barplot(x='SURVIVAL_STATUS', y='AVERAGE_FARE', data=df_tarifa_data,
                    palette={'Sobrevivió':'#2ECC71', 'No Sobrevivió':'#E74C3C'},
                    ax=ax_tarifa, order=['No Sobrevivió', 'Sobrevivió']) # Asegurar orden

        ax_tarifa.set_title('Costo Promedio del Boleto por Supervivencia', fontsize=14)
        ax_tarifa.set_xlabel('Estado de Supervivencia', fontsize=10)
        ax_tarifa.set_ylabel('Costo Promedio del Boleto ($)', fontsize=10)

        # Añadir el valor encima de cada barra
        for p in ax_tarifa.patches:
            ax_tarifa.annotate(f"${p.get_height():.2f}",
                               (p.get_x() + p.get_width() / 2., p.get_height()),
                               ha='center', va='center', fontsize=10, color='black',
                               xytext=(0, 5), textcoords='offset points')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_tarifa)
    except Exception as e:
        st.error(f"Error al procesar o graficar datos de tarifa: {e}")
        st.dataframe(df_tarifa_data)
else:
    st.warning("No se pudieron cargar los datos para el análisis de tarifa o las columnas esperadas no existen.")
    if not df_tarifa_data.empty:
        st.write("Datos recibidos para tarifa (verificar nombres de columnas):", df_tarifa_data)

st.markdown("---")
st.sidebar.info("""
    **Sobre este Dashboard:**
    Este dashboard presenta un análisis básico de los factores de supervivencia en el desastre del Titanic.
    Los datos son consultados desde Snowflake.

    *¡Hecho con cariño paisa y Python!* Antioquia-Nia te saluda.
    """)

# Para ejecutar esta aplicación:
# 1. Guarde este código como un archivo .py (ej: streamlit_app.py)
# 2. Asegúrese de tener Streamlit y snowflake-connector-python instalados.
# 3. Configure sus secretos de Streamlit (archivo secrets.toml) con sus credenciales de Snowflake:
#    [SNOWFLAKE]
#    USER = "SU_USUARIO"
#    PASSWORD = "SU_CONTRASENA"
#    ACCOUNT = "SU_CUENTA"
#    WAREHOUSE = "SU_WAREHOUSE"
#    DATABASE = "SU_BASE_DE_DATOS"
#    SCHEMA = "SU_ESQUEMA_CON_LAS_TABLAS_AGREGADAS"
# 4. Ejecute desde su terminal: streamlit run streamlit_app.py
# 5. ¡IMPORTANTE! Este código asume que usted ya ha creado tablas agregadas en Snowflake
#    (ej: TITANIC_ANALYSIS_AGE_SURVIVAL, TITANIC_ANALYSIS_CLASS_SURVIVAL, TITANIC_ANALYSIS_FARE_SURVIVAL)
#    con los datos ya procesados para cada gráfico. Si no, las consultas SQL deberían ser más complejas
#    para realizar las agregaciones al vuelo, o debería traer los datos crudos (o de capa Silver)
#    y procesarlos con Pandas dentro de Streamlit (lo cual puede ser menos eficiente para datasets grandes).
