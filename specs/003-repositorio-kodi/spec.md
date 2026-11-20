# Especificación 003: Repositorio de Kodi en GitHub

**ID:** `003-repositorio-kodi` · **Estado:** Implementada (GitHub Pages pendiente de activar) · **Fecha:** 2026-11-20
**Principios afectados:** VI (publicación reproducible), VII (privacidad)

## Contexto
cocoesp debe instalarse y actualizarse en Kodi como cualquier add-on: añadiendo una fuente en el
gestor de archivos, instalando un add-on repositorio y, desde él, el módulo. Todo se publica en
`https://github.com/karv3l/cocoesp`, junto con el código fuente.

## Historias de usuario

### HU-1 — Instalar desde Kodi (P1)
Como usuario quiero añadir una URL como fuente, instalar el repositorio y desde él cocoesp.

1. **Dado** la fuente `https://karv3l.github.io/cocoesp/`, **cuando** elijo «Instalar desde zip»,
   **entonces** veo `repository.karv3l-<versión>.zip`.
2. **Dado** el repositorio instalado, **cuando** abro «Instalar desde repositorio → karv3l Repository»,
   **entonces** aparecen cocoesp y el puente.

### HU-2 — Recibir actualizaciones (P1)
1. **Dado** cocoesp 1.0.0 instalado, **cuando** se publica 1.0.1 en el repositorio,
   **entonces** Kodi la detecta y la instala.

### HU-3 — Publicar con un solo comando (P2)
Como mantenedor quiero regenerar todos los artefactos de Kodi con un comando.

## Requisitos funcionales
- **FR-001**: DEBE existir un add-on `repository.karv3l` que apunte a
  `https://raw.githubusercontent.com/karv3l/cocoesp/main/zips/` (`addons.xml`, `addons.xml.md5`, datadir con zips).
- **FR-002**: `zips/` DEBE contener, por cada add-on, `<id>/<id>-<versión>.zip` y al lado `addon.xml`,
  `icon.png`, `fanart.png` y `changelog.txt` si existen.
- **FR-003**: Cada zip DEBE tener como raíz una carpeta con el id del add-on y NO DEBE incluir
  `__pycache__`, `.pyc`, `.DS_Store`, `__MACOSX`.
- **FR-004**: `addons.xml` DEBE combinar los `addon.xml` de todos los add-ons de `src/` y `addons.xml.md5`
  DEBE ser su MD5.
- **FR-005**: La raíz del repo DEBE contener el zip de `repository.karv3l` y un `index.html` que lo enlace
  (lo lee el gestor de archivos de Kodi vía GitHub Pages).
- **FR-006**: Los zips de versiones anteriores DEBEN conservarse en `zips/`.
- **FR-007**: Todo lo anterior DEBE generarse con `tools/build_repo.py`.
- **FR-008**: El código fuente (`src/`, `tools/`, `tests/`, `specs/`) DEBE publicarse en el mismo repo;
  el material de referencia descargado (`site/`, `repo-cocoscrapers/`, `extracted/`) y `.venv` NO.

## Criterios de éxito
- **SC-001**: El MD5 publicado coincide con el `addons.xml` publicado. ✅
- **SC-002**: Los zips se descargan con HTTP 200 desde `raw.githubusercontent.com`. ✅
- **SC-003**: `https://karv3l.github.io/cocoesp/` responde 200. ⏳ (requiere activar Pages)
- **SC-004**: Instalación completa en Kodi siguiendo el [quickstart](quickstart.md). ⏳

## Supuestos
- Repo público `karv3l/cocoesp`, rama `main`.
- `raw.githubusercontent.com` cachea unos minutos: tras un push, el MD5 puede tardar en actualizarse.

## Fuera de alcance
- Firmar los zips; CI que ejecute `build_repo.py` automáticamente.
