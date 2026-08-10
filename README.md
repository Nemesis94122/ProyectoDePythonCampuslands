# Proyecto: Sistema de préstamo de herramientas 
Sistema diseñado para gestionar y controlar el préstamo de herramientas entre vecinos, que permite llevar un registro sobre dichas herramientas, usuarios y los préstamos realizados en la comunidad.

---

## Estructura del proyecto

text
sistema-prestamo-herramientas/
├── data/
│   ├── herramientas.json
│   ├── prestamos.json
│   └── usuarios.json
├── modulos/
│   ├── herramientas.py
│   ├── persistencia.py
│   ├── prestamos.py
│   ├── reportes.py
│   └── usuarios.py
├── main.py
└── README.md

  

            
## Requerimientos del sistema 

### 1. Gestión de herramientas (herramientas.py)
-	*Información registrada:* ID de la herramienta, nombre, categoría y valor de la herramienta
-	*Operaciones:* Crear, listar, buscar, actualizar y eliminar o inactivar herramientas.

### 2. Gestión de usuarios (usuarios.py)
- *Información registrada:* Id del usuario, nombre, apellido, teléfono, dirección y tipo de usuario ( residente // administrador // ... )
- *Operaciones:* Crear, listar, buscar, actualizar y eliminar usuarios del registro.

### 3.  Gestión de préstamos (prestamos.py)
- *Información registrada:* Id del préstamo, usuario, herramienta, cantidad, fecha de inicio del préstamo, fecha de devolución, estado y observaciones de la herramienta.
- *Verificación:* Validación del stock de la herramienta, realizando el registro del préstamo y ajustando la cantidad disponible.
- *Devolución:* Actualización del estado del préstamo y restauración de la cantidad disponible al devolver la herramienta.

### 4. Consultas y reportes: (reportes.py)
- Herramientas con stock bajo.
- Prestamos activos y vencidos.
- Historial de préstamo de un usuario.
- Herramientas más solicitadas por la comunidad.
- Usuarios que más herramientas han solicitado.

### 5. Registro de eventos (persistencia.py)
- Errores o eventos relevantes que se puedan presentar.

---

##  Permisos y Roles

| Rol | Funciones y Permisos |
| :--- | :--- |
| *Administrador* | Encargado de registrar usuarios y herramientas para evitar suplantación de identidad. |
| *Usuario* | Puede consultar el estado de las herramientas, cuándo quedarán disponibles y quién las posee. Puede crear una solicitud de herramienta que debe ser aprobada por el administrador. |

---

##  Características Principales del Sistema

- *Modularidad en Python:* Código estructurado en módulos independientes (herramientas.py, usuarios.py, prestamos.py, reportes.py, persistencia.py y main.py) para facilitar el mantenimiento.
- *Control de Inventario en Tiempo Real:* Verificación automática de unidades disponibles previo al préstamo para evitar inconsistencias o sobrepedidos.
- *Control de Acceso por Roles:* Funcionalidades diferenciadas para Administrador (gestión total y aprobación) y Usuario (solicitud y consulta).
- *Interfaz de Consola Amigable:* Menús navegables e interactivos diseñados para una fácil operación en terminal.
