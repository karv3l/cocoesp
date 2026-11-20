# Tareas 001: Idioma de las fuentes

**Entrada:** [spec.md](spec.md), [plan.md](plan.md) · `[P]` = paralelizable

## Fase 1 — Investigación
- [x] T001 Localizar el filtro de idioma común y sus llamadas en los 26 proveedores — `modules/source_utils.py`
- [x] T002 [FR-006] Verificar la configuración por URL de Torrentio y los ids de trackers en español — [research.md](research.md#r3--torrentio-configuración-y-proveedores-en-español)
- [x] T003 Capturar la respuesta real de Torrentio como fixture — `tests/fixtures/torrentio_interstellar_es.json`

## Fase 2 — Implementación
- [x] T004 [P] [FR-001][FR-005] Ajuste `filter.language` y visibilidad del interruptor heredado — `resources/settings.xml`
- [x] T005 [P] [FR-009] Cadenas 32700–32704 en `en_gb` y nueva traducción `es_es` — `resources/language/`
- [x] T006 [FR-003] Constantes `SPA_*` e `is_spanish()` — `modules/source_utils.py`
- [x] T007 [FR-002][FR-004] `language_mode()`, `check_foreign_audio()` y ramas de `remove_lang()` — `modules/source_utils.py`
- [x] T008 [FR-006] URL de Torrentio según el modo — `sources_cocoesp/torrents/torrentio.py`
- [x] T009 [FR-007] Etiqueta por bandera en `sources()` y `sources_packs()` — `torrentio.py`

## Fase 3 — Verificación
- [x] T010 [SC-002] Casos sintéticos en los modos inglés, español y multidioma — `tests/test_language_filter.py`
- [x] T011 [SC-001] Fixture real: 20 resultados → 15 mantenidos, 5 polacos descartados
- [x] T012 [SC-003] URL «Multidioma» devuelve proveedores habituales + españoles (377 resultados)
- [x] T013 Compilación de todo el módulo y validación de `settings.xml`
- [ ] T014 [SC-004] Validación manual en Kodi con Fen/Umbrella — [quickstart.md](quickstart.md)

## Fase 4 — Publicación
- [x] T015 Changelog y publicación (cocoesp 1.0.0, commit `6253606`)

## Pendiente / preguntas abiertas
- [ ] T016 Evaluar si `check_title()` rechaza releases con el título traducido (p. ej. *El Padrino*
      frente a *The Godfather*) cuando la app no envía alias en español.
- [ ] T017 Valorar marcar `'language': 'es'` en los resultados españoles (hoy siempre `'en'`).
