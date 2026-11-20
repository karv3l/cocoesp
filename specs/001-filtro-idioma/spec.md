# Especificación 001: Idioma de las fuentes

**ID:** `001-filtro-idioma` · **Estado:** Implementada · **Fecha:** 2026-11-20
**Principios afectados:** II (contrato), III (por defecto = original), IV (cambios mínimos), V (verificable)

## Contexto
CocoScrapers está orientado al inglés: su filtro de idioma **descarta** los releases en español
(ver [línea base](../000-baseline/architecture.md#filtro-de-idioma-heredado-remove_lang)) y casi todos
sus proveedores son indexadores anglosajones. Un usuario hispanohablante no puede pedir «solo español»
ni ver todos los idiomas sin perder el comportamiento original.

## Historias de usuario

### HU-1 — Ver solo contenido en español (P1)
Como usuario hispanohablante quiero que las búsquedas devuelvan solo versiones en español
(castellano, latino o VOSE) para no tener que revisar resultados que no entiendo.

**Escenarios de aceptación**
1. **Dado** el ajuste en «Solo español», **cuando** un proveedor devuelve `Pelicula.2014.1080p.CASTELLANO`,
   **entonces** el resultado se muestra.
2. **Dado** el ajuste en «Solo español», **cuando** un proveedor devuelve `Pelicula.2014.1080p.x264-GRUPO`
   (sin marca de idioma), **entonces** el resultado se descarta.
3. **Dado** el ajuste en «Solo español», **cuando** Torrentio devuelve un resultado marcado con la
   bandera de España o México aunque el nombre no indique idioma, **entonces** el resultado se muestra.
4. **Dado** el ajuste en «Solo español», **cuando** se busca en Torrentio, **entonces** se consultan
   trackers en español.

### HU-2 — Ver todos los idiomas (P2)
Como usuario multilingüe quiero desactivar cualquier filtro de idioma para ver todas las versiones.

1. **Dado** el ajuste en «Multidioma», **cuando** llegan releases `FRENCH`, `SPANISH`, `German.DUBBED`
   o sin marca, **entonces** se muestran todos.
2. **Dado** el ajuste en «Multidioma», **cuando** se busca en Torrentio, **entonces** se consultan sus
   proveedores habituales **y** los trackers en español.

### HU-3 — Conservar el comportamiento original (P1)
Como usuario actual quiero que, si no toco nada, el módulo se comporte como CocoScrapers.

1. **Dado** una instalación nueva, **cuando** abro los ajustes, **entonces** «Idioma de las fuentes» vale «Inglés».
2. **Dado** el ajuste en «Inglés», **cuando** filtro, **entonces** se aplica exactamente la lógica heredada,
   incluido el interruptor «Remove identified Foreign single audio sources».

## Casos límite
- Abreviaturas dentro de otras palabras (`Lastday` contiene `lat`) **no** cuentan como español.
- `Español` llega como `espaol` tras eliminar caracteres no ASCII: debe reconocerse.
- `dual-lat` cuenta como español por `lat`; `dual` solo no (ver spec 007).
- `multi` **no** cuenta como español (suele ser francés + inglés).
- La «búsqueda sin filtros» de la app (`fs_filterless_search`) anula cualquier filtro de idioma.
- Proveedores que no son Torrentio y no ponen el idioma en el nombre: en «Solo español» se descartan.

## Requisitos funcionales
- **FR-001**: Los ajustes DEBEN ofrecer «Idioma de las fuentes» con tres valores: Inglés (0, por defecto),
  Solo español (1) y Multidioma (2).
- **FR-002**: En «Inglés», el filtrado DEBE ser idéntico al heredado.
- **FR-003**: En «Solo español», DEBE descartarse todo release que no se identifique como español.
- **FR-004**: En «Multidioma», NO DEBE descartarse ningún release por idioma, doblaje o subtítulos
  (solo se mantiene el descarte heredado de ficheros `.srt` sueltos).
- **FR-005**: El interruptor de audio extranjero DEBE ocultarse cuando el modo no es «Inglés».
- **FR-006**: Torrentio DEBE consultar trackers en español en «Solo español» y añadirlos a los habituales en «Multidioma».
- **FR-007**: Un resultado de Torrentio con bandera 🇪🇸 o 🇲🇽 DEBE considerarse español.
- **FR-008**: El filtro DEBE aplicarse a los 26 proveedores sin modificar cada uno (salvo Torrentio).
- **FR-009**: Los textos nuevos DEBEN existir en inglés y en español.

## Requisitos no funcionales
- **NFR-001**: El modo se lee una vez por búsqueda de proveedor, no por resultado.
- **NFR-002**: Sin dependencias nuevas.

## Criterios de éxito
- **SC-001**: Con la respuesta real de Torrentio para *Interstellar* (20 resultados), «Solo español»
  mantiene los 15 con bandera ES/MX y descarta los 5 polacos. ✅
- **SC-002**: Los casos de [`tests/test_language_filter.py`](../../tests/test_language_filter.py) pasan en los tres modos. ✅
- **SC-003**: La URL de «Multidioma» devuelve resultados de los proveedores habituales y de los españoles (377 en la prueba). ✅
- **SC-004**: En Kodi, cambiar el ajuste cambia los resultados de Fen/Umbrella sin reiniciar. ⏳ (validación manual)

## Supuestos y dependencias
- Torrentio acepta la configuración en la ruta (`/providers=…|language=…/`) y los ids `mejortorrent`,
  `wolfmax4k`, `cinecalidad` (verificado 2026-11-20).
- Las apps usan `name_info` y el filtrado del módulo; no filtran el idioma por su cuenta.

## Fuera de alcance
- Scrapers nuevos de sitios en español (se cubriría con Prowlarr/Jackett o una spec nueva).
- Configurar el idioma de Comet, MediaFusion o Prowlarr (se hace en sus propias páginas).
- Cambiar el campo `language` de los resultados (sigue siendo `'en'`).
