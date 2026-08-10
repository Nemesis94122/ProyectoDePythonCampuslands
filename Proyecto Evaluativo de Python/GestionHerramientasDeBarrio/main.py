import sys
from modulos.persistencia import registrar_log
import modulos.usuarios as m_usr
import modulos.herramientas as m_herr
import modulos.prestamos as m_pres
import modulos.reportes as m_rep

def login():
    print("\n--- BIENVENIDO AL SISTEMA COMUNAL ---")
    id_u = input("Ingrese su ID de vecino: ").strip()
    usuarios = m_usr.listar_usuarios()
    
    if id_u in usuarios:
        return usuarios[id_u]
    else:
        print("Usuario no registrado en el sistema.")
        registrar_log(f"Intento de login fallido de ID: {id_u}", es_error=True)
        return None

def menu_admin():
    while True:
        print("\n=== PANEL DE ADMINISTRADOR ===")
        print("1. Registrar Vecino")
        print("2. Registrar Herramienta")
        print("3. Ver/Aprobar Préstamos Pendientes")
        print("4. Registrar Retorno/Devolución")
        print("5. Menú de Consultas y Reportes")
        print("6. Cerrar Sesión")
        op = input("Seleccione una opción: ")
        
        if op == "1":
            id_u = input("ID: ")
            nom = input("Nombres: ")
            ape = input("Apellidos: ")
            tel = input("Teléfono: ")
            dir_u = input("Dirección: ")
            tipo = input("Tipo (administrador/residente): ").lower()
            exito, msg = m_usr.crear_usuario(id_u, nom, ape, tel, dir_u, tipo)
            print(msg)
            
        elif op == "2":
            id_h = input("ID Herramienta: ")
            nom = input("Nombre: ")
            cat = input("Categoría: ")
            cant = input("Cantidad inicial: ")
            est = input("Estado (activa/en reparacion): ")
            val = input("Valor estimado: ")
            exito, msg = m_herr.crear_herramienta(id_h, nom, cat, cant, est, val)
            print(msg)
            
        elif op == "3":
            prestamos = m_pres.cargar_datos("prestamos.json", {})
            pendientes = {k: v for k, v in prestamos.items() if v["estado"] == "pendiente_aprobacion"}
            if not pendientes:
                print("No hay solicitudes pendientes.")
                continue
            for k, v in pendientes.items():
                print(f"ID Solicitud: {k} | Vecino: {v['usuario']} | Herramienta: {v['herramienta']} | Cantidad: {v['cantidad']}")
            id_a = input("Ingrese ID de solicitud a aprobar (o Enter para cancelar): ")
            if id_a in pendientes:
                exito, msg = m_pres.aprobar_prestamo(id_a)
                print(msg)
                
        elif op == "4":
            id_p = input("Ingrese ID del préstamo a devolver: ")
            obs = input("Observaciones del estado de entrega: ")
            exito, msg = m_pres.devolver_herramienta(id_p, obs)
            print(msg)
            
        elif op == "5":
            menu_reportes()
            
        elif op == "6":
            break

def menu_usuario(usuario):
    while True:
        print(f"\n=== PANEL DE VECINO: {usuario['nombres']} ===")
        print("1. Consultar Catálogo de Herramientas")
        print("2. Solicitar una Herramienta")
        print("3. Ver mis Préstamos")
        print("4. Consultar disponibilidad y poseedor de herramienta") # <-- REQUERIMIENTO AÑADIDO
        print("5. Cerrar Sesión")
        op = input("Seleccione una opción: ")
        
        if op == "1":
            for h in m_herr.listar_herramientas().values():
                print(f"[{h['id']}] {h['nombre']} ({h['categoria']}) - Disponibles: {h['cantidad']} - Estado: {h['estado']}")
                
        elif op == "2":
            id_h = input("Ingrese el ID de la herramienta: ")
            cant = input("Cantidad requerida: ")
            fecha = input("Fecha estimada de devolución (AAAA-MM-DD): ")
            exito, msg = m_pres.solicitar_prestamo(usuario["id"], id_h, cant, fecha)
            print(msg)
            
        elif op == "3":
            historial = m_rep.historial_usuario(usuario["id"])
            if not historial:
                print("No registras solicitudes en el sistema.")
            for p in historial:
                print(f"Préstamo {p['id']}: Herramienta: {p['herramienta']} | Estado: {p['estado']} | Devuelve: {p['fecha_estimada']}")
                
        elif op == "4": # <-- LÓGICA DEL REQUERIMIENTO AÑADIDA
            id_buscado = input("Ingrese el ID de la herramienta a consultar: ").strip().upper()
            msg_estado = m_rep.consultar_poseedor_herramienta(id_buscado)
            print(msg_estado)
            
        elif op == "5":
            break

def menu_reportes():
    while True: # MEJORA: Bucle iterativo para que el panel no se cierre tras ver un solo reporte
        print("\n--- REPORTES ESTADÍSTICOS ---")
        print("1. Stock crítico (< 3 unidades)")
        print("2. Préstamos Activos vs Vencidos")
        print("3. Herramientas más populares")
        print("4. Vecinos con más préstamos")
        print("5. Regresar al Panel de Administrador")
        op = input("Seleccione reporte: ")
        
        if op == "1":
            bajos = m_rep.stock_bajo()
            if not bajos:
                print("Inventario seguro. No hay stock bajo.")
            for h in bajos.values():
                print(f"ALERTA: {h['nombre']} - Solo quedan {h['cantidad']} unidades.")
        elif op == "2":
            activos, vencidos = m_rep.prestamos_por_estado()
            print(f"\n>> ACTIVOS ({len(activos)}):")
            for p in activos: print(f" ID {p['id']} - Vecino {p['usuario']} hasta {p['fecha_estimada']}")
            print(f"\n>> VENCIDOS ({len(vencidos)}):")
            for p in vencidos: print(f" ¡ALERTA! ID {p['id']} - Vecino {p['usuario']} venció el {p['fecha_estimada']}")
        elif op == "3":
            for nom, cant in m_rep.herramientas_mas_solicitadas():
                print(f"- {nom}: Solicitada {cant} veces.")
        elif op == "4":
            for nom, cant in m_rep.usuarios_mas_activos():
                print(f"- {nom}: Realizó {cant} préstamos.")
        elif op == "5":
            break

if __name__ == "__main__":
    # Inicialización de la cuenta semilla administrativa por defecto
    usuarios_iniciales = {"101": {"id": "101", "nombres": "Admin", "apellidos": "Comunal", "telefono": "0000", "direccion": "Central", "tipo": "administrador"}}
    m_usr.guardar_datos(m_usr.ARCH_USUARIOS, m_usr.cargar_datos(m_usr.ARCH_USUARIOS, usuarios_iniciales))
    
    while True:
        user = login()
        if user:
            if user["tipo"] == "administrador":
                menu_admin()
            else:
                menu_usuario(user)
