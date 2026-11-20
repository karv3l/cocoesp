# Validación 003: Repositorio de Kodi

## Publicar una versión
```
.venv\Scripts\python -I tests\test_language_filter.py
.venv\Scripts\python -I tests\test_bridge_alias.py
.venv\Scripts\python -I tools\build_repo.py
git add -A
git commit
git push
```
Antes: subir `version` en el `addon.xml` del add-on cambiado y añadir su entrada en `changelog.txt`.

## Comprobar lo publicado (≈5 min después del push)
```
curl -s https://raw.githubusercontent.com/karv3l/cocoesp/main/zips/addons.xml.md5
curl -s https://raw.githubusercontent.com/karv3l/cocoesp/main/zips/addons.xml | md5sum
curl -sI https://karv3l.github.io/cocoesp/
```
Los dos MD5 deben coincidir y Pages debe responder `200`.

## Instalación en Kodi
| # | Paso | Resultado esperado |
|---|---|---|
| 1 | Ajustes → Explorador de archivos → Añadir fuente → `https://karv3l.github.io/cocoesp/` (nombre: karv3l) | Fuente creada |
| 2 | Add-ons → Instalar desde un archivo zip → karv3l → `repository.karv3l-1.0.0.zip` | «karv3l Repository» instalado |
| 3 | Add-ons → Instalar desde repositorio → karv3l Repository → Módulos de programa | Aparecen **cocoesp** y **cocoesp (puente CocoScrapers)** |
| 4 | Instalar cocoesp | Instalado; la versión coincide con `src/script.module.cocoesp/addon.xml` |
| 5 | Publicar una versión mayor y en Kodi «Buscar actualizaciones» | Kodi propone la nueva versión |

Si Kodi bloquea la instalación desde zip: Ajustes → Sistema → Add-ons → «Fuentes desconocidas».
