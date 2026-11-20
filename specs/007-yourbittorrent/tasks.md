# Tareas 007: Proveedor YourBittorrent

- [x] T001 Probar la web: HTML con desafío de Cloudflare (403); RSS de búsqueda accesible (200)
- [x] T002 Analizar el RSS (título, semillas, tamaño, enclosure) y la descarga de `.torrent`
- [x] T003 [FR-001][FR-002][FR-003][FR-004] Proveedor — `sources_cocoesp/torrents/yourbittorrent.py`
- [x] T004 [P] Ajuste `provider.yourbittorrent` y cadenas 32718–32719
- [x] T005 Capturar RSS reales — `tests/fixtures/yourbittorrent/`
- [x] T006 [SC-001] Pruebas con `source_utils` real — `tests/test_yourbittorrent.py`
- [x] T007 **Defecto encontrado por T006:** `dual` marcaba `Dual.PTBR` como español → eliminado de `SPA_TOKENS`
- [x] T008 [SC-002] Hash de un `.torrent` real
- [ ] T009 [SC-003] Validación en Kodi
- [ ] T010 Valorar relajar `check_title` para títulos con numeral añadido («The Godfather I»)
