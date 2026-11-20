# Plan 007: Proveedor YourBittorrent

**Spec:** [spec.md](spec.md)

## Comprobación de la constitución
| Principio | Cumple | Nota |
|---|---|---|
| I. Independencia | ✅ | Solo cocoesp. |
| II. Contrato | ✅ | Clase `source` estándar; mismo formato de resultado. |
| III. Por defecto = original | ✅ | Desactivado por defecto. |
| IV. Cambios mínimos | ✅ | Reutiliza `torrent_info`/`is_archive_only` de `spanish_sites.py`. |
| V. Verificable sin terceros | ✅ | RSS reales como fixtures + `source_utils` real con dobles de Kodi. |
| VI. Publicación reproducible | ✅ | `build_repo.py`. |
| VII. Seguridad | ✅ | No se resuelve Cloudflare (FR-005). |

## Flujo
```
consultas (FR-002) ─► rss.xml?q=… ─► parse_rss → [{title, torrent, seeders, size}]
   por item: clean_name → check_title → info_from_name → remove_lang → indeseables → min_seeders
   ordenar por semillas, 10 primeros ─► descargar .torrent ─► torrent_info → hash
   descartar solo-comprimidos y hashes repetidos ─► resultado (magnet, tamaño del RSS o del torrent)
```

## Ficheros
| Fichero | Cambio |
|---|---|
| `sources_cocoesp/torrents/yourbittorrent.py` | Nuevo (`parse_rss`, `source`) |
| `modules/source_utils.py` | `SPA_TOKENS` sin `dual` |
| `resources/settings.xml` | `provider.yourbittorrent` (false), antes de «Webs en castellano» |
| `resources/language/*/strings.po` | 32718–32719 |
| `tests/test_yourbittorrent.py`, `tests/fixtures/yourbittorrent/*.xml` | Nuevos |
