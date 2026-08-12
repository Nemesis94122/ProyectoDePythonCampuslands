import datetime
from modulos.persistencia import cargar_datos as cd, guardar_datos as gd, registrar_log

ARCH_PRESTAMOS = "prestamos.json"

def solicitar_prestamo(id_usuario, id_herramienta, cantidad_solicitada, fecha_fin):
    prestamos = cd(ARCH_PRESTAMOS, {})
    import modulos.herramientas as m_herr
    herramientas = m_herr.listar_herramientas()
    
 
    if id_herramienta not in herramientas:
        return False, "La herramienta solicitada no existe."
    
    herr = herramientas[id_herramienta]
    
   
    if herr["estado"] != "activa":
        return False, f"La herramienta no está disponible. Estado actual: {herr['estado']}"
        
   
    if int(cantidad_solicitada) > herr["cantidad"]:
         registrar_log(f"STOCK INSUFICIENTE: Vecino {id_usuario} pidió {cantidad_solicitada} de {id_herramienta}. Stock: {herr['cantidad']}", es_error=True)
        return False, f"No hay suficientes unidades. Stock actual: {herr['cantidad']}."
        
   
    id_p = f"P{len(prestamos) + 1}"
    
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
    prestamos = cd(ARCH_PRESTAMOS, {})
    
    if id_p not in prestamos or prestamos[id_p]["estado"] != "pendiente_aprobacion":
        return False, "Préstamo no válido o ya procesado."
    
    p = prestamos[id_p]
    import modulos.herramientas as m_herr
    herramientas = m_herr.listar_herramientas()
    herr = herramientas[p["herramienta"]]
    
  
    nuevo_stock = herr["cantidad"] - p["cantidad"]
    m_herr.actualizar_herramienta(p["herramienta"], {"cantidad": nuevo_stock})
    
   
    p["estado"] = "activo"
    
    gd(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Préstamo ID {id_p} aprobado e inventario actualizado.")
    return True, "Préstamo aprobado e inventario actualizado con éxito."

def devolver_herramienta(id_p, observaciones):
    prestamos = cd(ARCH_PRESTAMOS, {})
    
    if id_p not in prestamos or prestamos[id_p]["estado"] != "activo":
        return False, "El préstamo no está activo o ya fue devuelto."
    
    p = prestamos[id_p]
    import modulos.herramientas as m_herr
    herramientas = m_herr.listar_herramientas()
    herr = herramientas[p["herramienta"]]
    
    nuevo_stock = herr["cantidad"] + p["cantidad"]
    m_herr.actualizar_herramienta(p["herramienta"], {"cantidad": nuevo_stock})
    
    p["estado"] = "devuelto"
    p["observaciones"] = observaciones
    
    gd(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Herramienta devuelta para el préstamo ID {id_p}. Notas: {observaciones}")
    return True, "Devolución registrada con éxito. Inventario de la junta restaurado."

def cargar_datos(archivo, por_defecto):
    return cd(archivo, por_defecto)

def guardar_datos(archivo, datos):
    gd(archivo, datos)
