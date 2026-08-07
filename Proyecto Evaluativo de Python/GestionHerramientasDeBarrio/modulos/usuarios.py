from modulos.persistencia import cargar_datos, guardar_datos, registrar_log

ARCH_USUARIOS = "usuarios.json"

def crear_usuario(id_u, nombres, apellidos, telefono, direccion, tipo):
    usuarios = cargar_datos(ARCH_USUARIOS, {})
    if id_u in usuarios:
        registrar_log(f"Intento fallido de crear usuario existente: ID {id_u}", es_error=True)
        return False, "El ID del vecino ya está registrado."
    
    usuarios[id_u] = {
        "id": id_u, "nombres": nombres, "apellidos": apellidos,
        "telefono": telefono, "direccion": direccion, "tipo": tipo
    }
    guardar_datos(ARCH_USUARIOS, usuarios)
    registrar_log(f"Usuario registrado: {nombres} {apellidos} (ID: {id_u})")
    return True, "Vecino registrado exitosamente."

def listar_usuarios():
    return cargar_datos(ARCH_USUARIOS, {})

def actualizar_usuario(id_u, campos_nuevos):
    usuarios = cargar_datos(ARCH_USUARIOS, {})
    if id_u not in usuarios:
        return False, "Vecino no encontrado."
    
    usuarios[id_u].update(campos_nuevos)
    guardar_datos(ARCH_USUARIOS, usuarios)
    registrar_log(f"Usuario ID {id_u} actualizado.")
    return True, "Datos actualizados con éxito."

def eliminar_usuario(id_u):
    usuarios = cargar_datos(ARCH_USUARIOS, {})
    if id_u not in usuarios:
        return False, "Vecino no encontrado."
    
    del usuarios[id_u]
    guardar_datos(ARCH_USUARIOS, usuarios)
    registrar_log(f"Usuario ID {id_u} eliminado del sistema.")
    return True, "Vecino eliminado con éxito."