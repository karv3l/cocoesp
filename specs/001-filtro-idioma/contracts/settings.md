# Contrato 001: ajustes y funciones de idioma

## Ajuste `filter.language` (`script.module.cocoesp`)

| Campo | Valor |
|---|---|
| Tipo | `integer`, control `spinner` |
| Valores | `0` Inglés (por defecto) · `1` Solo español · `2` Multidioma |
| Etiquetas | 32700 (título), 32701–32703 (opciones), 32704 (ayuda) |
| Efecto lateral | `filter.foreign.single.audio` visible solo si `filter.language == 0` |

## `source_utils.check_foreign_audio() -> bool | str`

| Condición | Devuelve |
|---|---|
| Propiedad de ventana `fs_filterless_search == 'true'` | `False` |
| `filter.language == '1'` | `'es'` (`LANG_SPANISH`) |
| `filter.language == '2'` | `'multi'` (`LANG_MULTI`) |
| Otro caso | `getSetting('filter.foreign.single.audio') == 'true'` |

## `source_utils.remove_lang(release_info: str, check_foreign_audio: bool | str) -> bool`
Devuelve `True` si el release **debe descartarse**. `release_info` vacío → `False`.

| Modo | Descarta |
|---|---|
| `'es'` | `not is_spanish(release_info)` |
| `'multi'` | solo `release_info.endswith('.srt.')` sin `with.srt/.avi/.mkv/.mp4` |
| `True` | DUBBED, SUBS, LANG/ABV_LANG sin ENG_CHECK, `.srt.` suelto |
| `False` | DUBBED, SUBS, `.srt.` suelto |

## `source_utils.is_spanish(release_info: str) -> bool`
`True` si contiene alguna de `SPA_WORDS` como subcadena o alguno de `SPA_TOKENS` como token entre puntos.

## `source_utils.has_spanish_flag(text: str) -> bool`
`True` si `text` contiene 🇪🇸 (`U+1F1EA U+1F1F8`) o 🇲🇽 (`U+1F1F2 U+1F1FD`).

## `source_utils.language_mode() -> str | None`
`'es'`, `'multi'` o `None` (inglés), según `filter.language`.

## URL de Torrentio

| Modo | `base_link` |
|---|---|
| Inglés | `https://torrentio.strem.fun` |
| Solo español | `https://torrentio.strem.fun/providers=mejortorrent,wolfmax4k,cinecalidad\|language=spanish` |
| Multidioma | `https://torrentio.strem.fun/providers=yts,eztv,rarbg,1337x,thepiratebay,kickasstorrents,torrentgalaxy,magnetdl,horriblesubs,nyaasi,tokyotosho,anidex,mejortorrent,wolfmax4k,cinecalidad\|language=spanish` |
