# Investigación 001: Idioma de las fuentes

## R1 — ¿Dónde filtrar?
- **Decisión:** en `source_utils.remove_lang()`, que ya llaman los 26 proveedores con
  `remove_lang(name_info, check_foreign_audio())`.
- **Alternativas descartadas:** modificar cada proveedor (26 cambios, contra el principio IV); filtrar
  en la app (fuera de nuestro control).
- **Truco de diseño:** `check_foreign_audio()` se evalúa una vez por búsqueda y su valor se pasa a
  `remove_lang()`; se amplía para devolver también `'es'` o `'multi'`, sin cambiar ninguna firma.

## R2 — ¿Cómo reconocer un release en español?
`name_info` llega en minúsculas, con todo lo no alfanumérico convertido en `.` y envuelto en puntos
(`.1080p.dual.lat.cinecalidad.`). Los caracteres no ASCII se eliminan antes (`Español` → `espaol`).

| Tipo | Valores | Cómo se comprueba |
|---|---|---|
| Palabras (pueden ir pegadas) | `spanish`, `castellano`, `latino`, `espanol`, `espaol`, `subtitulad` | subcadena |
| Abreviaturas | `es`, `esp`, `spa`, `cast`, `lat`, `vose`, `vos` | token completo entre puntos |

- `multi` se excluye a propósito (en releases europeos suele ser francés + inglés).
- `dual` **no** se incluye (enmienda de la [spec 007](../007-yourbittorrent/spec.md#cambio-colateral-en-la-spec-001)): en índices generales aparece en `Dual.PTBR`; en trackers hispanos va con `lat`/`castellano`, que ya cuentan.

## R3 — Torrentio: configuración y proveedores en español
Consulta real del 2026-11-20 a
`/providers=mejortorrent,wolfmax4k,cinecalidad,besttorrents|language=spanish/stream/movie/tt0816692.json`:

| Proveedor | Resultados | Idioma real |
|---|---|---|
| Wolfmax4k | 9 | Castellano (🇪🇸, a menudo `[ES-EN]`) |
| MejorTorrent | 4 | Castellano (🇪🇸) |
| Cinecalidad | 3 | Latino (🇲🇽, `dual-lat`) |
| BestTorrents | 4 | **Polaco** (🇵🇱, `Lektor PL`) |

- **Decisión:** usar `mejortorrent`, `wolfmax4k` y `cinecalidad`; **descartar BestTorrents**.
- El título de cada stream tiene varias líneas: nombre, `👤 semillas 💾 tamaño ⚙️ proveedor` y una
  línea de banderas. Algunos nombres no indican idioma (`Interstellar (2014) HDRip`) → **se usa la bandera**.
- Algunos resultados traen como primera línea el nombre de una carpeta (`Videos cosas`): comportamiento
  heredado de `clean_name`, fuera de alcance.

## R4 — Torrentio en «Multidioma»
Indicar `providers=` sustituye la lista por defecto, así que hay que enumerar los habituales:
`yts, eztv, rarbg, 1337x, thepiratebay, kickasstorrents, torrentgalaxy, magnetdl, horriblesubs,
nyaasi, tokyotosho, anidex` + los tres españoles. Prueba real: 377 resultados (ThePirateBay 178,
1337x 67, MagnetDL 67, TorrentGalaxy 29, RARBG 20, Wolfmax4k 8, MejorTorrent 4, Cinecalidad 3, YTS 1).
`language=spanish` solo ordena; no filtra.

## R5 — Otras fuentes con contenido en español (para futuras specs)
- **Prowlarr/Jackett** propio: indexadores DonTorrent, MejorTorrent, Wolfmax4K, EliteTorrent, DivxTotal
  (los dominios cambian a menudo). `prowlarr.py` ya se conecta con URL + API key.
- **Comet**: filtro de idiomas en su configuración (JSON en base64 en la URL).
- **MediaFusion**: idioma preferido en su `/configure`; su token se guarda en `mediafusion.userdata`.
