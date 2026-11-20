# Tareas 004: Add-on puente

**Entrada:** [spec.md](spec.md), [plan.md](plan.md)

## Fase 1 — Decisión
- [x] T001 Presentar las tres opciones al usuario; elegida la opción 1 — [research.md](research.md)

## Fase 2 — Implementación
- [x] T002 [P] [FR-001][FR-006] `addon.xml` con id original, dependencia de cocoesp y versión 9.x
- [x] T003 [FR-002][FR-003] Alias de importación — `lib/cocoscrapers/__init__.py`
- [x] T004 [P] [FR-004] Reenvío de acciones — `lib/default.py`
- [x] T005 [P] [FR-005] Ajustes con botón a cocoesp + textos `en_gb`/`es_es` — `resources/`
- [x] T006 Sección en `README.md`

## Fase 3 — Verificación
- [x] T007 Prueba inicial del alias con paquete falso (scratchpad)
- [x] T008 [SC-001] Prueba reproducible en el repo con subprocesos limpios — `tests/test_bridge_alias.py`
- [x] T009 **Defecto encontrado por T008:** `from cocoscrapers import sources_cocoscrapers` fallaba en intérprete limpio → mapeo `cocoesp.sources_cocoscrapers` añadido
- [x] T010 [SC-002] Zip del puente en `addons.xml` y accesible en GitHub
- [ ] T011 [SC-003] Validación manual en Kodi con Fen y Umbrella — [quickstart.md](quickstart.md)

## Fase 4 — Publicación
- [x] T012 Puente 9.0.0 publicado (commit `c37bb80`)
- [x] T013 Puente 9.0.1 con la corrección de T009

## Pendiente
- [ ] T014 Comprobar en Kodi si la carpeta `lib` de cocoesp llega al `sys.path` sin la ruta de respaldo.
- [ ] T015 Identificar qué ajustes de `script.module.cocoscrapers` leen Fen/Umbrella directamente y, si hace falta, reflejarlos.
