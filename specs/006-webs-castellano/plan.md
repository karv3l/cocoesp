# Plan 006: Proveedores de webs en castellano

**Spec:** [spec.md](spec.md)

## Resumen
Un módulo común `modules/spanish_sites.py` implementa el flujo (buscar → fichas → `.torrent` → hash) y un
decodificador *bencode* mínimo. Cada web es un fichero pequeño en `sources_cocoesp/torrents/` que solo
declara su configuración (dominio, URL de búsqueda, patrón de fichas).

## Comprobación de la constitución
| Principio | Cumple | Nota |
|---|---|---|
| I. Independencia | ✅ | Solo cocoesp. |
| II. Contrato | ✅ | Clase `source` con `sources(data, hostDict)`; mismo formato de resultado. |
| III. Por defecto = original | ✅ | Los cuatro proveedores vienen desactivados. |
| IV. Cambios mínimos | ✅ | Lógica común en un módulo; los proveedores existentes no se tocan. |
| V. Verificable sin terceros | ⚠️ | Pruebas con HTML/torrents sintéticos; **sin** HTML real por el bloqueo DNS. |
| VI. Publicación reproducible | ✅ | `build_repo.py`. |
| VII. Seguridad | ✅ | Sin `exec`; no se resuelven pruebas antibot (FR-009). |

## Flujo
```
sources(data)
  términos = [título] + alias país 'es'            (FR-003)
  por término: búsqueda (GET o POST según la web)  → HTML
     enlaces a fichas que casan con movie_link_re  → (url, texto)
     filtrar por título/alias y año ±1             (FR-004)   máx. 5 fichas
  por ficha: enlaces .torrent / magnet             máx. 10 torrents
     .torrent → bdecode → infohash, nombre, tamaño, ficheros
     descartar si todo son .rar/.zip               (HU-1.2)
  name_info = info_from_name(nombre) + 'spanish.'  → remove_lang, remove_undesirables
  → {'source':'torrent','provider':<web>,'hash','url':magnet,'name','name_info','quality','info','size','seeders':0,...}
```

## Configuración por web

| Web | Dominio por defecto (Alfa, 2026-11) | Búsqueda | Fichas |
|---|---|---|---|
| DonTorrent | `https://dontorrent.shopping` | `POST /buscar` `valor=<t>&Buscar=Buscar&p=1` | `/pelicula/` |
| Elite Torrent | `https://www.elitetorrent.com` | `GET /?s=<t>&x=0&y=0` | `/peliculas/` |
| DivxTotal | `https://divxtotal.foo` | `GET /?s=<t>` | `/peliculas` |
| GranTorrent | `https://grantorrent.zip` | `GET /peliculas/?query=<t>` | `/peliculas/` |

## Ficheros
| Fichero | Cambio |
|---|---|
| `lib/cocoesp/modules/spanish_sites.py` | Nuevo: `bdecode`, `torrent_info`, `SpanishTorrentSite` |
| `lib/cocoesp/sources_cocoesp/torrents/{dontorrent,elitetorrent,divxtotal,grantorrent}.py` | Nuevos |
| `resources/settings.xml` | `provider.<web>` (false) + `<web>.url` |
| `resources/language/*/strings.po` | Cadenas 32710–32715 |
| `tests/test_spanish_sites.py` | Pruebas sin red |

## Riesgos
| Riesgo | Mitigación |
|---|---|
| Maquetación real distinta de la supuesta | Patrones genéricos (enlaces a fichas y a `.torrent`), no clases CSS; validación pendiente en Kodi. |
| Cambios de dominio | Ajuste `<web>.url`. |
| Bloqueo DNS en la red del usuario | Documentado; fuera de alcance. |
