from datetime import datetime
from modulos.persistencia import cargar_datos, guardar_datos, registrar_log
import modulos.herramientas as m_herr

ARCH_PRESTAMOS = "prestamos.json"

def solicitar_prestamo(id_usuario, id_herramienta, cantidad_solicitada, fecha_fin):
    prestamos = cargar_datos(ARCH_PRESTAMOS, {})
    herramientas = m_herr.listar_herramientas()
    
    if id_herramienta not in herramientas:
        return False, "La herramienta no existe."
    
    herr = herramientas[id_herramienta]
    if herr["estado"] != "activa":
        return False, f"La herramienta no está disponible. Estado actual: {herr['estado']}"
        
    id_p = str(len(prestamos) + 1).zfill(4)
    prestamos[id_p] = {
        "id": id_p, "usuario": id_usuario, "herramienta": id_herramienta,
        "cantidad": int(cantidad_solicitada), 
        "fecha_inicio": datetime.now().strftime("%Y-%m-%d"),
        "fecha_estimada": fecha_fin, "estado": "pendiente_aprobacion",
        "observaciones": "Solicitado por el vecino vía consola."
    }
    guardar_datos(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Nueva solicitud de préstamo ID {id_p} generada por usuario {id_usuario}.")
    return True, f"Solicitud creada con éxito. ID: {id_p}. Esperando aprobación del Administrador."

def aprobar_prestamo(id_p):
    prestamos = cargar_datos(ARCH_PRESTAMOS, {})
    if id_p not in prestamos or prestamos[id_p]["estado"] != "pendiente_aprobacion":
        return False, "Préstamo no válido o ya procesado."
    
    p = prestamos[id_p]
    herramientas = m_herr.listar_herramientas()
    herr = herramientas[p["herramienta"]]
    
    if herr["cantidad"] < p["cantidad"]:
        registrar_log(f"Stock insuficiente para aprobar préstamo ID {id_p}. Solicitado: {p['cantidad']}, Stock: {herr['cantidad']}", es_error=True)
        return False, f"No hay stock suficiente. Stock disponible: {herr['cantidad']}"
    
    # Descontar del inventario
    m_herr.actualizar_herramienta(p["herramienta"], {"cantidad": herr["cantidad"] - p["cantidad"]})
    p["estado"] = "activo"
    guardar_datos(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Préstamo ID {id_p} aprobado y activo.")
    return True, "Préstamo aprobado e inventario actualizado."

def devolver_herramienta(id_p, observaciones="Sin novedades"):
    prestamos = cargar_datos(ARCH_PRESTAMOS, {})
    if id_p not in prestamos or prestamos[id_p]["estado"] != "activo":
        return False, "El préstamo no está activo."
    
    p = prestamos[id_p]
    herramientas = m_herr.listar_herramientas()
    herr = herramientas[p["herramienta"]]
    
    # Restaurar inventario
    m_herr.actualizar_herramienta(p["herramienta"], {"cantidad": herr["cantidad"] + p["cantidad"]})
    p["estado"] = "devuelto"
    p["observaciones"] = observaciones
    guardar_datos(ARCH_PRESTAMOS, prestamos)
    registrar_log(f"Herramienta devuelta para el préstamo ID {id_p}.")
    return True, "Devolución registrada con éxito. Inventario restaurado."