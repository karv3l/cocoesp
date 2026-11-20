# Plan 004: Add-on puente

**Spec:** [spec.md](spec.md) · **Investigación:** [research.md](research.md) · **Contrato:** [contracts/import-alias.md](contracts/import-alias.md)

## Resumen
Add-on mínimo `script.module.cocoscrapers` (sin scrapers) que depende de cocoesp, redirige las
importaciones con un `MetaPathFinder` y reenvía las acciones del plugin.

## Comprobación de la constitución
| Principio | Cumple | Nota |
|---|---|---|
| I. Independencia | ⚠️ | **Excepción explícita** recogida en la constitución: el puente ocupa el id del original, pero es opcional; cocoesp sigue siendo independiente. |
| II. Contrato de las apps | ✅ | Las apps reciben exactamente la API de cocoesp. |
| III. Por defecto = original | ✅ | No cambia comportamiento; la configuración es la de cocoesp. |
| IV. Cambios mínimos | ✅ | cocoesp no se modifica. |
| V. Verificable sin terceros | ✅ | Prueba con paquete falso en subprocesos limpios. |
| VI. Publicación reproducible | ✅ | `build_repo.py` lo incluye automáticamente. |
| VII. Privacidad y seguridad | ✅ | Sin red ni `exec`. |

## Estructura
```
src/script.module.cocoscrapers/
├── addon.xml                 id script.module.cocoscrapers · 9.0.x · requiere script.module.cocoesp 1.0.0
├── icon.png, fanart.png
├── lib/
│   ├── cocoscrapers/__init__.py   alias (buscador + sustitución en sys.modules)
│   └── default.py                 reenvío de plugin://
└── resources/
    ├── settings.xml               botón «Abrir ajustes de cocoesp»
    └── language/{en_gb,es_es}/strings.po
```

## Ficheros afectados
| Fichero | Cambio |
|---|---|
| `src/script.module.cocoscrapers/**` | Nuevo add-on |
| `README.md` | Sección «Usar cocoesp en Fen, Umbrella y similares» |

## Riesgos
| Riesgo | Mitigación |
|---|---|
| Una app lee ajustes del puente directamente | Documentado; la búsqueda funciona igual. |
| Usuario con el repositorio original | Versión 9.x. |
| Cambios internos de `importlib` en futuras versiones de Python | API pública (`MetaPathFinder`, `Loader`, `spec_from_loader`); pruebas automáticas. |
