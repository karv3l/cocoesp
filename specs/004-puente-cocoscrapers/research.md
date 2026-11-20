# Investigación 004: cómo hacer que las apps encuentren cocoesp

## Opciones evaluadas

| Opción | Ventajas | Inconvenientes | Decisión |
|---|---|---|---|
| 1. Add-on puente con id `script.module.cocoscrapers` | Funciona con todas las apps sin tocarlas | Sustituye al original (mismo id); compite con el repositorio original | **Elegida por el usuario** |
| 2. Selector de «módulo externo» de cada app | Mantiene la independencia total | No verificado que Fen/Umbrella acepten módulos arbitrarios | No investigada a fondo |
| 3. Forks de Fen/Umbrella | Independencia total | Mantener forks de terceros | Descartada |

## Mecanismo de alias de módulos (Python ≥ 3.4)
1. **Paquete raíz:** al final de `cocoscrapers/__init__.py`, `sys.modules['cocoscrapers'] = cocoesp`.
   Tras ejecutar un módulo, `importlib` vuelve a leer `sys.modules[nombre]`, así que el importador
   recibe `cocoesp`.
2. **Submódulos:** un `MetaPathFinder` al principio de `sys.meta_path` responde a `cocoscrapers.*` con
   un `Loader` cuyo `create_module()` devuelve `importlib.import_module('cocoesp.*')` y cuyo
   `exec_module()` no hace nada → mismo objeto, sin doble carga.
3. **Hallazgo durante las pruebas:** `from cocoscrapers import sources_cocoscrapers` en un intérprete
   limpio pide `cocoesp.sources_cocoscrapers` (el `__name__` del paquete es `cocoesp`). Se añade ese
   nombre al mapeo → corregido en el puente 9.0.1.

## Dependencias transitivas en Kodi
Kodi añade al `sys.path` la carpeta `lib` de los módulos de los que depende el add-on en ejecución.
Por si no incluyera la dependencia del puente (cocoesp), el puente la añade con
`xbmcaddon.Addon('script.module.cocoesp').getAddonInfo('path')`.

## Versión 9.x
El original va por la 1.0.45. Con la 9.x, si alguien tiene ambos repositorios, Kodi prefiere el puente.
