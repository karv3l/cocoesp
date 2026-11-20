# Tareas 003: Repositorio de Kodi en GitHub

**Entrada:** [spec.md](spec.md), [plan.md](plan.md)

## Fase 1 — Implementación
- [x] T001 [FR-001] Add-on `repository.karv3l` 1.0.0 con URLs a `karv3l/cocoesp/main/zips/` — `src/repository.karv3l/addon.xml`
- [x] T002 [FR-002][FR-003][FR-004][FR-005][FR-006][FR-007] Script de generación — `tools/build_repo.py`
- [x] T003 [FR-008] `.gitignore` (excluye `.venv`, `site/`, `repo-cocoscrapers/`, `extracted/`, `__pycache__`) y `.nojekyll`
- [x] T004 README con instalación y proceso de publicación — `README.md`

## Fase 2 — Verificación
- [x] T005 [SC-001] MD5 local y remoto coinciden con `addons.xml`
- [x] T006 [FR-003] Zips sin basura y con raíz = id; `testzip()` sin errores
- [x] T007 [SC-002] Zips accesibles con HTTP 200 en `raw.githubusercontent.com`

## Fase 3 — Publicación
- [x] T008 Repo git local con autor noreply; commit `6253606`; push a `main`
- [x] T009 [SC-003] Activar GitHub Pages: *Settings → Pages → Deploy from a branch → main → / (root)* (activado por el propietario; verificado 200)
- [ ] T010 [SC-004] Instalación completa en Kodi — [quickstart.md](quickstart.md)

## Mejoras futuras
- [ ] T011 GitHub Action que ejecute `build_repo.py` y las pruebas en cada push y falle si `zips/` no está al día.
