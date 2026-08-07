from modulos.persistencia import cargar_datos, guardar_datos, registrar_log

ARCH_HERRAMIENTAS = "herramientas.json"

def crear_herramienta(id_h, nombre, categoria, cantidad, estado, valor):
    herramientas = cargar_datos(ARCH_HERRAMIENTAS, {})
    if id_h in herramientas:
        registrar_log(f"Intento fallido de crear herramienta existente: ID {id_h}", es_error=True)
        return False, "El ID de la herramienta ya existe."
    
    herramientas[id_h] = {
        "id": id_h, "nombre": nombre, "categoria": categoria,
        "cantidad": int(cantidad), "estado": estado, "valor": float(valor)
    }
    guardar_datos(ARCH_HERRAMIENTAS, herramientas)
    registrar_log(f"Herramienta creada con éxito: {nombre} (ID: {id_h})")
    return True, "Herramienta registrada exitosamente."

def listar_herramientas():
    return cargar_datos(ARCH_HERRAMIENTAS, {})

def actualizar_herramienta(id_h, campos_nuevos):
    herramientas = cargar_datos(ARCH_HERRAMIENTAS, {})
    if id_h not in herramientas:
        return False, "Herramienta no encontrada."
    
    herramientas[id_h].update(campos_nuevos)
    guardar_datos(ARCH_HERRAMIENTAS, herramientas)
    registrar_log(f"Herramienta ID {id_h} actualizada.")
    return True, "Herramienta actualizada con éxito."

def eliminar_herramienta(id_h):
    herramientas = cargar_datos(ARCH_HERRAMIENTAS, {})
    if id_h not in herramientas:
        return False, "Herramienta no encontrada."
    
    herramientas[id_h]["estado"] = "fuera de servicio"
    guardar_datos(ARCH_HERRAMIENTAS, herramientas)
    registrar_log(f"Herramienta ID {id_h} marcada como fuera de servicio.")
    return True, "Herramienta inactivada (Fuera de servicio)."