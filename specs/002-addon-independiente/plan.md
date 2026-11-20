# Plan 002: cocoesp como add-on independiente

**Spec:** [spec.md](spec.md)

## Resumen
Renombrado sistemático de identificadores en minúsculas (`cocoscrapers` → `cocoesp`) en todos los
ficheros de texto, renombrado de carpetas, y ajuste manual de los textos visibles con mayúsculas.

## Comprobación de la constitución
| Principio | Cumple | Nota |
|---|---|---|
| I. Independencia | ✅ | Objetivo de la spec. |
| II. Contrato de las apps | ⚠️ | El contrato se mantiene, pero bajo otro nombre de paquete → las apps no lo encuentran. Mitigado por la spec 004. |
| III. Por defecto = original | ✅ | Mismos valores por defecto. |
| IV. Cambios mínimos | ✅ | Renombrado mecánico; sin cambios de lógica. |
| V. Verificable sin terceros | ✅ | Búsqueda de referencias en el zip + compilación. |
| VI. Publicación reproducible | ✅ | `build_repo.py`. |
| VII. Privacidad y seguridad | ✅ | Commits con dirección noreply. |

## Tabla de renombrado

| Antes | Después | Tipo |
|---|---|---|
| `script.module.cocoscrapers` | `script.module.cocoesp` | id del add-on, URLs `plugin://`, `special://profile/addon_data/…` |
| `lib/cocoscrapers/` | `lib/cocoesp/` | paquete Python |
| `sources_cocoscrapers/` | `sources_cocoesp/` | carpeta de proveedores (`sourceFolder` en `__init__.py`) |
| `cocoscrapers_settings`, `cocoscrapers.debug.reversed`, `cocoscrapers.text`, `cocoscrapers.heading` | `cocoesp_…` | propiedades de ventana (aislamiento en Home) |
| `cocoscrapers.log` | `cocoesp.log` | log propio |
| `CocoScrapersSettings` | `cocoespSettings` | acción del plugin |
| `CocoScrapers Module` / `CocoScrapers` (visibles) | `cocoesp` | nombre, títulos, notificaciones, user-agent, `module.provider` |
| `1.0.45` / `1.1.0` | `1.0.0` | versión |
| `provider-name="CocoJoe"` | `provider-name="karv3l"` | autor del add-on derivado |

**Se mantiene** «CocoScrapers» en: descripción de `addon.xml` («Based on CocoScrapers»), comentarios de
cabecera (`control.py`, `coco_compat.py`, `torrentgalaxy.py`) e historial del `changelog.txt`.

## Procedimiento
1. Copiar `src/script.module.cocoscrapers` → `src/script.module.cocoesp` y renombrar `lib/cocoscrapers`, `sources_cocoscrapers`.
2. Sustituir `cocoscrapers` → `cocoesp` en todos los ficheros de texto (excepto `changelog.txt`).
3. Sustituir `CocoScrapersSettings` → `cocoespSettings`.
4. Revisar a mano las apariciones restantes de `CocoScrapers` y decidir: visible → `cocoesp`; crédito → se mantiene.
5. `version="1.0.0"`, `provider-name="karv3l"`, entrada en `changelog.txt`.

## Riesgos
| Riesgo | Mitigación |
|---|---|
| Rutas construidas dinámicamente con el nombre antiguo | Búsqueda de `cocoscrapers` en todo el zip generado (SC-001). |
| Las apps dejan de encontrar el módulo | Spec 004 (puente). |
