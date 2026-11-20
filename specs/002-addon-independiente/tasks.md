# Tareas 002: cocoesp como add-on independiente

**Entrada:** [spec.md](spec.md), [plan.md](plan.md)

## Fase 1 — Antecedente
- [x] T001 Primera versión: solo nombre visible «cocoesp» con id original, versión 1.1.0 (sustituida por esta spec)

## Fase 2 — Implementación
- [x] T002 [FR-001][FR-002] Renombrar carpetas: add-on, paquete y proveedores — `src/script.module.cocoesp/`
- [x] T003 [FR-003] Sustituir identificadores en minúsculas en todos los ficheros de texto
- [x] T004 [FR-004] `CocoScrapersSettings` → `cocoespSettings` — `lib/default.py`
- [x] T005 [FR-001] Textos visibles: notificaciones de log (`default.py`), `module.provider` (`service.py`, `settings.xml`), ayuda (`packScrapers.txt`)
- [x] T006 [FR-005][FR-006] `version="1.0.0"`, `provider-name="karv3l"`, changelog con historial de CocoScrapers — `addon.xml`, `changelog.txt`

## Fase 3 — Verificación
- [x] T007 [SC-001] Buscar `cocoscrapers` en el zip generado: solo créditos
- [x] T008 [SC-002] Compilar el módulo y validar `addon.xml` / `settings.xml`
- [x] T009 [FR-007] Repetir las pruebas de la spec 001 con la nueva ruta
- [ ] T010 [SC-003] Validación manual en Kodi con CocoScrapers y cocoesp instalados a la vez

## Fase 4 — Publicación
- [x] T011 Commit `6253606` y push a `karv3l/cocoesp`
