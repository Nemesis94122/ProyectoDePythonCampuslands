import datetime
from modulos.persistencia import cargar_datos as cd, guardar_datos as gd, registrar_log

ARCH_PRESTAMOS = "prestamos.json"

def solicitar_prestamo(id_usuario, id_herramienta, cantidad_solicitada, fecha_fin):
    """Crea la solicitud de préstamo en el formato exacto que lee el menú principal."""
    prestamos = cd(ARCH_PRESTAMOS, {})
    import modulos.herramientas as m_herr
    herramientas = m_herr.listar_herramientas()
    
    # 1. Validación de existencia de la herramienta
    if id_herramienta not in herramientas:
        return False, "La herramienta solicitada no existe."
    
    herr = herramientas[id_herramienta]
    
    # Requerimiento: Estado operativo
    if herr["estado"] != "activa":
        return False, f"La herramienta no está disponible. Estado actual: {herr['estado']}"
        
    # Requerimiento: Stock disponible
    if int(cantidad_solicitada) > herr["cantidad"]:
        # Requerimiento de la junta: Registrar fallas de stock en el archivo de logs
        registrar_log(f"STOCK INSUFICIENTE: Vecino {id_usuario} pidió {cantidad_solicitada} de {id_herramienta}. Stock: {herr['cantidad']}", es_error=True)
        return False, f"No hay suficientes unidades. Stock actual: {herr['cantidad']}."
        
    # Generamos un ID correlativo simple para el diccionario (P1, P2, P3...)
    id_p = f"P{len(prestamos) + 1}"
    
    # Estructura exacta de llaves que tu compañero programó en el menú principal
    prestamos[id_p] = {
        "id": id_p,
        "usuario": id_usuario,          
        "herramienta": id_herramienta,  
        "cantidad": int(cantidad_solicitada), 
        "fecha_inicio": datetime.datetime.now().strftime("%Y-%m-%d"),
        "fecha_estimada": fecha_fin,    
        "estado": "pendiente_aprobacion", 
        "observaciones": "Solicitado vía consola."
    }
    
    gd(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Nueva solicitud de préstamo ID {id_p} generada por el usuario {id_usuario}.")
    return True, f"Solicitud {id_p} creada con éxito. Esperando aprobación del Administrador."

def aprobar_prestamo(id_p):
    """Aprueba el préstamo y descuenta las unidades usando la función del compañero."""
    prestamos = cd(ARCH_PRESTAMOS, {})
    
    if id_p not in prestamos or prestamos[id_p]["estado"] != "pendiente_aprobacion":
        return False, "Préstamo no válido o ya procesado."
    
    p = prestamos[id_p]
    import modulos.herramientas as m_herr
    herramientas = m_herr.listar_herramientas()
    herr = herramientas[p["herramienta"]]
    
    # Modificación del stock directo usando la función de tu compañero
    nuevo_stock = herr["cantidad"] - p["cantidad"]
    m_herr.actualizar_herramienta(p["herramienta"], {"cantidad": nuevo_stock})
    
    # Cambiamos el estado de la solicitud a activo
    p["estado"] = "activo"
    
    gd(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Préstamo ID {id_p} aprobado e inventario actualizado.")
    return True, "Préstamo aprobado e inventario actualizado con éxito."

def devolver_herramienta(id_p, observaciones):
    """Procesa el retorno y suma las unidades al JSON de herramientas del compañero."""
    prestamos = cd(ARCH_PRESTAMOS, {})
    
    if id_p not in prestamos or prestamos[id_p]["estado"] != "activo":
        return False, "El préstamo no está activo o ya fue devuelto."
    
    p = prestamos[id_p]
    import modulos.herramientas as m_herr
    herramientas = m_herr.listar_herramientas()
    herr = herramientas[p["herramienta"]]
    
    # Restauramos las existencias usando la función de actualización de tu compañero
    nuevo_stock = herr["cantidad"] + p["cantidad"]
    m_herr.actualizar_herramienta(p["herramienta"], {"cantidad": nuevo_stock})
    
    # Guardamos los cambios del recibo de préstamo
    p["estado"] = "devuelto"
    p["observaciones"] = observaciones
    
    gd(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Herramienta devuelta para el préstamo ID {id_p}. Notas: {observaciones}")
    return True, "Devolución registrada con éxito. Inventario de la junta restaurado."

# --- PUENTE DE INTERFAZ OBLIGATORIO ---
# Evita que main.py se caiga cuando llama a m_pres.cargar_datos en la línea 37
def cargar_datos(archivo, por_defecto):
    return cd(archivo, por_defecto)

def guardar_datos(archivo, datos):
    gd(archivo, datos)
