# 000 — Línea base: arquitectura heredada

**Origen:** `script.module.cocoscrapers` 1.0.45 (repositorio `not-coco-joe/repository.cocoscrapers`),
publicado vía `cocojoe2411.github.io`. El código es Python plano (sin compilar ni ofuscar).
Este documento describe el sistema **tal como se heredó**; los cambios posteriores están en las specs 001–004.

## Cadena de distribución original

```
cocojoe2411.github.io ──► repository.cocoscrapers-1.0.1.zip
                                   │ addon.xml apunta a
                                   ▼
raw.githubusercontent.com/not-coco-joe/repository.cocoscrapers/master/zips/
        ├── addons.xml (+ .md5)
        └── script.module.cocoscrapers/script.module.cocoscrapers-1.0.0 … 1.0.45.zip
```

## Componentes

| Ruta (hoy en `src/script.module.cocoesp/`) | Responsabilidad |
|---|---|
| `addon.xml` | Id, versión, dependencias (`xbmc.python` 3.0.0, `script.module.requests`), extensiones: módulo Python (`lib`), plugin (`lib/default.py`) y servicio (`lib/service.py`). |
| `lib/<paquete>/__init__.py` | API pública: `sources()`, `enabledCheck()`, `pack_sources()`. Descubre proveedores recorriendo `sources_<paquete>/<subcarpeta>` con `pkgutil.walk_packages`. |
| `lib/<paquete>/sources_<paquete>/torrents/*.py` | 26 proveedores (una clase `source` por fichero). |
| `lib/<paquete>/modules/source_utils.py` | Filtros comunes: título, año, calidad, tamaño, idioma (`remove_lang`), indeseables. |
| `lib/<paquete>/modules/client.py`, `coco_client.py` | Cliente HTTP (`request`, `session`, `randomagent`) y resolución de protecciones anti-bot (`cfcookie`, `bfcookie`, `sucuri`). |
| `lib/<paquete>/modules/cfscrape/` | Copia de cloudscraper (Cloudflare, captchas, intérpretes JS). |
| `lib/<paquete>/modules/dom_parser.py` | Extracción de etiquetas/atributos HTML por regex. |
| `lib/<paquete>/modules/control.py` | Envoltorio de la API de Kodi (ajustes con caché en propiedad de ventana, rutas, diálogos). |
| `lib/<paquete>/modules/undesirables.py` | Lista de palabras para descartar releases (configurable). |
| `lib/default.py` | Acciones `plugin://…/?action=` (abrir ajustes, ayuda, changelog, activar/desactivar proveedores, logs). |
| `lib/service.py` | Al arrancar Kodi crea la carpeta de datos y el `settings.xml` inicial. |
| `resources/settings.xml`, `resources/language/` | Ajustes (formato v1) y textos. |

## Flujo de una búsqueda

```
App (Fen/Umbrella)
  │ from <paquete> import sources
  │ providers = sources()                         # [(nombre, clase source)] de los proveedores activos
  │ for nombre, cls in providers:
  │     cls().sources(data, hostDict)             # data: title/tvshowtitle, year, imdb, season, episode, aliases, timeout
  ▼
Proveedor (p. ej. torrentio.py)
  1. Construye la URL (base_link + ruta)                         → coco_client.session / client.request
  2. Parsea JSON o HTML                                           → json / dom_parser / regex
  3. Por cada resultado:
       check_title()  → info_from_name() → name_info (".1080p.castellano.x264.")
       remove_lang(name_info, check_foreign_audio())  ── descarta por idioma
       remove_undesirables(name_info, undesirables)   ── descarta por palabras
       get_release_quality(), _size()
  4. Devuelve dicts: source, language, direct, debridonly, provider, hash, url (magnet),
                     name, name_info, quality, info, size, seeders
```

## Filtro de idioma heredado (`remove_lang`)

- Siempre descarta `DUBBED` (`dubbed`, `dublado`…) y `SUBS` (`subspanish`, `subtitula`…).
- Si `filter.foreign.single.audio` = true (por defecto), descarta `LANG` (`spanish`, `castellano`,
  `latino`, `french`…) y `ABV_LANG` (`.es.`, `.spa.`, `.lat.`…) salvo que aparezca `ENG_CHECK`
  (`.eng.`, `.en.`, `english`, `multi`).
- **Consecuencia:** el módulo original está orientado al inglés y elimina el contenido en español.

## Proveedores

| Tipo | Ficheros |
|---|---|
| HTML | 1337x, bitsearch, limetorrents, torrentz2, torrentdownload, kickass2, rutor, torlock, eztv, torrentproject2 |
| API JSON | piratebay (apibay), ytsmx, knaben, nyaa, torrentio, torrentgalaxy, torrentsdb, dmm, bitmagnet, meteor |
| Configurables por el usuario | comet, mediafusion, zilean, torz, aiostreams, prowlarr |

## Dependencias

| Kodi | Equivalente pip (desarrollo) | Uso |
|---|---|---|
| `script.module.requests` | `requests`, `urllib3` | HTTP |
| incluido en `lib/` | `pyparsing` | intérprete JS nativo de cfscrape |
| opcionales (try/except) | `brotli`, `requests_toolbelt`, `polling2` | cfscrape |
| — | `Kodistubs` | stubs de `xbmc*` para análisis fuera de Kodi |

Ver [`requirements.txt`](../../requirements.txt).

## Riesgos conocidos

| Riesgo | Ubicación | Tratamiento |
|---|---|---|
| `exec()` de JavaScript decodificado de una web (desafío Sucuri) | `modules/client.py` (`class sucuri`) | Heredado; no se amplía (constitución VII). |
| `loader.load_module()` obsoleto en Python moderno | `__init__.py` (`sources`, `pack_sources`) | Funciona en Kodi (Python 3.8–3.11); revisar si Kodi sube de versión. |
| Cabecera `Accept-Language: en-US` fija | `modules/client.py` | Sin impacto conocido en los proveedores JSON. |
| Dominios de proveedores cambian a menudo | `sources_*/torrents/*.py` | Mantenimiento continuo. |
