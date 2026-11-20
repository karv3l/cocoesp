# Especificación 007: Proveedor YourBittorrent

**ID:** `007-yourbittorrent` · **Estado:** Implementada · **Fecha:** 2026-11-20
**Principios afectados:** II (contrato), III (por defecto = original), V (verificable), VII (seguridad)

## Contexto
El usuario propone `https://yourbittorrent.com/?q=spa`. YourBittorrent es un índice general (todos los
idiomas) muy utilizado por releases europeos multi-idioma (`ENG-ITA-SPA`, `iTA-SPA`…), que no están en
los trackers españoles. A diferencia de las webs de la [spec 006](../006-webs-castellano/spec.md), **no está
bloqueado por DNS**.

Hallazgos (2026-11-20):
- La web HTML (`/?q=`) devuelve **403 con desafío de Cloudflare** («Just a moment…»): no se intenta resolver.
- El **RSS público de búsqueda** `https://yourbittorrent.com/rss.xml?q=<texto>` responde 200, sin desafío,
  con hasta 30 resultados: título, semillas, tamaño y `<enclosure>` al `.torrent` (`yt.t0r.store/down/<id>.torrent`).
- El RSS no trae el *infohash*: se calcula descargando el `.torrent`.
- `?q=spa` a secas trae mucho ruido (vídeos de «spa», etc.): hay que combinarlo con el título.
- Búsquedas AND: `interstellar castellano` → 0; `interstellar spa` → el remux multi-idioma con `Spa`.

## Historias de usuario
### HU-1 — Releases multi-idioma con español (P1)
1. **Dado** «Solo español», **cuando** busco *Interstellar*, **entonces** aparece
   `Interstellar.2014.Eng.Fre.Ger.Ita.Por.Spa…Remux` y no los releases sin español.
2. **Dado** «Inglés», **cuando** busco, **entonces** se hace una sola consulta (`<título> <año>`) y se aplica el filtro heredado.

## Requisitos funcionales
- **FR-001**: Proveedor `yourbittorrent`, **desactivado por defecto**, películas y episodios.
- **FR-002**: Consultas: `<título> <año|SxxEyy>`; en «Solo español»/«Multidioma» además `<título> spa`
  (o `<título> SxxEyy spa`) y `<alias es> <año|SxxEyy>`. Máximo 3.
- **FR-003**: Filtrado estándar de cocoesp (`check_title`, `info_from_name`, `remove_lang`, indeseables) **antes** de descargar torrents.
- **FR-004**: Descargar como máximo 10 `.torrent` (los de más semillas), calcular el hash y descartar los que solo contienen comprimidos.
- **FR-005**: No resolver el desafío de Cloudflare de la web HTML; usar solo el RSS.

## Criterios de éxito
- **SC-001**: [`tests/test_yourbittorrent.py`](../../tests/test_yourbittorrent.py) con RSS reales capturados y el `source_utils` real pasa. ✅
- **SC-002**: Hash de un `.torrent` real de YourBittorrent calculado y tamaño coincidente con el RSS (110,7 GB). ✅
- **SC-003**: Resultados en Kodi con el proveedor activado. ⏳

## Cambio colateral en la spec 001
`dual` deja de contar como español: en índices generales aparece en `Dual.PTBR` (portugués). En los trackers
españoles siempre va con `lat`/`castellano`, que ya cuentan. Ver [research 001 · R2](../001-filtro-idioma/research.md#r2--cómo-reconocer-un-release-en-español).

## Limitaciones conocidas
- `check_title` heredado rechaza títulos como «The Godfather **I** (1972)» (con numeral añadido).
- Dependencia de un dominio externo para los `.torrent` (`yt.t0r.store`).
