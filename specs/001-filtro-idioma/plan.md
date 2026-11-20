# Plan 001: Idioma de las fuentes

**Spec:** [spec.md](spec.md) · **Investigación:** [research.md](research.md) · **Contrato:** [contracts/settings.md](contracts/settings.md)

## Resumen
Un ajuste entero `filter.language` (0/1/2) controla el modo de idioma. `check_foreign_audio()` pasa a
devolver el modo (`False`/`True` en inglés, `'es'` o `'multi'`) y `remove_lang()` ramifica según él.
Torrentio añade su configuración a la URL y etiqueta como español lo que lleva bandera ES/MX.

## Contexto técnico
- **Lenguaje:** Python 3 (Kodi 19+). **Dependencias nuevas:** ninguna.
- **Pruebas:** [`tests/test_language_filter.py`](../../tests/test_language_filter.py) (extracción por AST + fixture real de Torrentio).
- **Restricción:** las firmas `remove_lang(release_info, check_foreign_audio)` y `check_foreign_audio()` no cambian.

## Comprobación de la constitución
| Principio | Cumple | Nota |
|---|---|---|
| I. Independencia | ✅ | Solo toca cocoesp. |
| II. Contrato de las apps | ✅ | Sin cambios en la API ni en el formato de resultados. |
| III. Por defecto = original | ✅ | `filter.language` = 0 → lógica heredada intacta. |
| IV. Cambios mínimos | ✅ | `source_utils.py` + `torrentio.py`; los otros 25 proveedores no se tocan. |
| V. Verificable sin terceros | ✅ | Prueba por AST con fixture capturado; sin red ni Kodi. |
| VI. Publicación reproducible | ✅ | Vía `build_repo.py`. |
| VII. Privacidad y seguridad | ✅ | Textos en `en_gb` y `es_es`; sin `exec` nuevos. |

## Diseño

### Flujo de decisión en `remove_lang()`
```
check_foreign_audio()
  ├─ fs_filterless_search == 'true' ──► False          (sin filtro de idioma)
  ├─ filter.language == '1' ─────────► 'es'
  ├─ filter.language == '2' ─────────► 'multi'
  └─ en otro caso ───────────────────► filter.foreign.single.audio == 'true'  (heredado)

remove_lang(name_info, modo)
  ├─ modo == 'es'    ──► descarta si NOT is_spanish(name_info)
  ├─ modo == 'multi' ──► descarta solo «.srt.» sueltos (heredado)
  └─ modo bool       ──► lógica heredada (DUBBED, SUBS, LANG/ABV_LANG si True, .srt.)
```

### Torrentio
- `language_mode()` se lee en `__init__` del proveedor:
  - `'es'` → `base_link += '/providers=mejortorrent,wolfmax4k,cinecalidad|language=spanish'`
  - `'multi'` → `base_link += '/providers=<DEFAULT_PROVIDERS>,<SPANISH_PROVIDERS>|language=spanish'`
- Tras `info_from_name()`, si `file['title']` contiene 🇪🇸 o 🇲🇽 → `name_info += 'spanish.'`
  (en `sources()` y en `sources_packs()`).

## Ficheros afectados
| Fichero | Cambio |
|---|---|
| `src/script.module.cocoesp/lib/cocoesp/modules/source_utils.py` | Constantes `LANG_SPANISH`, `LANG_MULTI`, `SPA_WORDS`, `SPA_TOKENS`, `SPA_FLAGS`, `SPA_TAG`; funciones `is_spanish()`, `has_spanish_flag()`, `language_mode()`; `check_foreign_audio()` y `remove_lang()` ampliadas. |
| `src/script.module.cocoesp/lib/cocoesp/sources_cocoesp/torrents/torrentio.py` | `SPANISH_PROVIDERS`, `DEFAULT_PROVIDERS`, URL según el modo, etiqueta por bandera. |
| `src/script.module.cocoesp/resources/settings.xml` | Ajuste `filter.language`; dependencia de visibilidad en `filter.foreign.single.audio`. |
| `src/script.module.cocoesp/resources/language/resource.language.en_gb/strings.po` | Cadenas 32700–32704. |
| `src/script.module.cocoesp/resources/language/resource.language.es_es/strings.po` | Nuevo: traducción de 32700–32704. |

## Riesgos y mitigaciones
| Riesgo | Mitigación |
|---|---|
| Falsos negativos en «Solo español» (releases sin marca) | Documentado; Torrentio se cubre con banderas. |
| Torrentio cambia ids de proveedores o formato de banderas | Constantes centralizadas en `torrentio.py`; fixture para detectar regresiones. |
| Títulos en español no coinciden con el título en inglés de la app (`check_title`) | Fuera de alcance; anotado como pregunta abierta en tasks. |
