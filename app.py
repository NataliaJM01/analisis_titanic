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
