# Tareas 006: Proveedores de webs en castellano

**Entrada:** [spec.md](spec.md), [plan.md](plan.md) · `[P]` = paralelizable

## Fase 1 — Investigación
- [x] T001 Revisar los canales torrent activos de Alfa y elegir los de castellano (sin latinos)
- [x] T002 Extraer de Alfa dominio, búsqueda y rutas de DonTorrent, Elite Torrent, DivxTotal y GranTorrent
- [x] T003 Probar las webs desde la red de desarrollo → **bloqueadas por DNS** (`127.0.0.1`); el usuario elige implementar sin verificar
- [x] T004 [FR-009] Detectar la prueba de trabajo antibot de DonTorrent (`api_validate_pow.php`) → no se implementa

## Fase 2 — Implementación
- [x] T005 [FR-005] `bdecode`, `torrent_info`, `magnet_info`, `is_archive_only` — `modules/spanish_sites.py`
- [x] T006 [FR-003][FR-004] `norm_title`, `title_matches`, `slug_text`, términos con alias `es` — `modules/spanish_sites.py`
- [x] T007 [FR-006][FR-008] Clase `SpanishTorrentSite` con límites y marca `spanish.` — `modules/spanish_sites.py`
- [x] T008 [P] [FR-001][FR-002] Proveedores `dontorrent`, `elitetorrent`, `divxtotal`, `grantorrent` — `sources_cocoesp/torrents/`
- [x] T009 [P] [FR-001][FR-007] Ajustes `provider.<web>` (false) y `<web>.url` al final del grupo de proveedores — `resources/settings.xml`
- [x] T010 [P] Cadenas 32710–32717 en `en_gb` y `es_es`

## Fase 3 — Verificación
- [x] T011 [SC-001] 30 comprobaciones sin red — `tests/test_spanish_sites.py`
- [x] T012 Compilación del módulo y validación de `settings.xml`
- [ ] T013 [SC-002] Validación en un Kodi con acceso a las webs — [quickstart.md](quickstart.md)
- [ ] T014 Ajustar `movie_link_re` / enlaces de descarga de cada web según el HTML real (si T013 falla)

## Fase 4 — Publicación
- [x] T015 cocoesp 1.1.0 y changelog
- [ ] T016 Push a `karv3l/cocoesp`

## Notas
- Los resultados se marcan como español: en modo «Inglés» con el filtro de audio extranjero activo se
  descartan. Estos proveedores tienen sentido con «Solo español» o «Multidioma».
- Futuro: series (temporadas/episodios), y valorar Prowlarr/Jackett como alternativa más mantenible.
