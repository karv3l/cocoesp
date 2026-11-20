# cocoesp

Add-on de Kodi (`script.module.cocoesp`) basado en CocoScrapers 1.0.45, con la opción
**«Idioma de las fuentes»**: Inglés / Solo español / Multidioma.
Es independiente de CocoScrapers: tiene su propio id, paquete Python (`cocoesp`), ajustes, datos y log,
así que los dos pueden estar instalados a la vez.

### Usar cocoesp en Fen, Umbrella y similares
Esas apps buscan `script.module.cocoscrapers`. El repositorio incluye un **add-on puente** con ese id
(versión 9.0.0) que redirige todo `import cocoscrapers` a `cocoesp` y sus acciones/ajustes a cocoesp.
- Instálalo desde «karv3l Repository» si quieres que esas apps usen cocoesp.
- Sustituye al CocoScrapers original (mismo id): no pueden estar los dos.
- Los proveedores y el idioma se configuran en los ajustes de cocoesp.

## Instalar en Kodi
1. Ajustes → Explorador de archivos → Añadir fuente: `https://karv3l.github.io/cocoesp/`
2. Add-ons → Instalar desde un archivo zip → esa fuente → `repository.karv3l-1.0.0.zip`
3. Add-ons → Instalar desde repositorio → karv3l Repository → cocoesp

## Estructura
- `src/script.module.cocoesp/` — código fuente del add-on
- `src/script.module.cocoscrapers/` — add-on puente (id de CocoScrapers → cocoesp)
- `src/repository.karv3l/` — add-on repositorio (apunta a `raw.githubusercontent.com/karv3l/cocoesp/main/zips/`)
- `tools/build_repo.py` — genera `zips/`, `addons.xml`, `addons.xml.md5`, el zip del repositorio e `index.html`
- `zips/`, `index.html`, `repository.karv3l-*.zip` — generados; es lo que lee Kodi

## Publicar una nueva versión
1. Sube `version` en `src/script.module.cocoesp/addon.xml` y añade la entrada en `changelog.txt`.
2. `py -3 -m venv .venv` y `.venv\Scripts\python -m pip install -r requirements.txt` (solo la primera vez).
3. `.venv\Scripts\python tools\build_repo.py`
4. Commit y push a `main`.
