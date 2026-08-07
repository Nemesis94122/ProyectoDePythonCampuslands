from datetime import datetime
from collections import Counter
from modulos.persistencia import cargar_datos
import modulos.herramientas as m_herr
import modulos.usuarios as m_usr

def stock_bajo(limite=3):
    return {k: v for k, v in m_herr.listar_herramientas().items() if v["cantidad"] < limite}

def prestamos_por_estado():
    prestamos = cargar_datos("prestamos.json", {})
    hoy = datetime.now().date()
    activos, vencidos = [], []
    
    for p in prestamos.values():
        if p["estado"] == "activo":
            fecha_est = datetime.strptime(p["fecha_estimada"], "%Y-%m-%d").date()
            if hoy > fecha_est:
                vencidos.append(p)
            else:
                activos.append(p)
    return activos, vencidos

def historial_usuario(id_u):
    prestamos = cargar_datos("prestamos.json", {})
    return [p for p in prestamos.values() if p["usuario"] == id_u]

def herramientas_mas_solicitadas():
    prestamos = cargar_datos("prestamos.json", {})
    contador = Counter([p["herramienta"] for p in prestamos.values()])
    herr = m_herr.listar_herramientas()
    return [(herr.get(id_h, {}).get("nombre", "Desconocida"), cant) for id_h, cant in contador.most_common()]

def usuarios_mas_activos():
    prestamos = cargar_datos("prestamos.json", {})
    contador = Counter([p["usuario"] for p in prestamos.values()])
    usrs = m_usr.listar_usuarios()
    return [(f"{usrs.get(id_u, {}).get('nombres', 'Desconocido')} {usrs.get(id_u, {}).get('apellidos', '')}", cant) for id_u, cant in contador.most_common()]