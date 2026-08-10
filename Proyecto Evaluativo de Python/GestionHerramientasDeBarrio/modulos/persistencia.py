import os
import json
import logging

os.makedirs("logs", exist_ok=True)
os.makedirs("data", exist_ok=True)

logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def registrar_log(mensaje, es_error=False):
    if es_error:
        logging.error(mensaje)
    else:
        logging.info(mensaje)

def cargar_datos(archivo, por_defecto):
    ruta = f"data/{archivo}"
    if not os.path.exists(ruta):
        guardar_datos(archivo, por_defecto)
        return por_defecto
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        registrar_log(f"Error al leer {archivo}. Archivo corrupto.", es_error=True)
        return por_defecto

def guardar_datos(archivo, datos):
    ruta = f"data/{archivo}"
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        registrar_log(f"Error al guardar en {archivo}: {str(e)}", es_error=True)
