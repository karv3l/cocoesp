# Especificación 006: Proveedores de webs en castellano

**ID:** `006-webs-castellano` · **Estado:** Implementada sin verificar contra las webs · **Fecha:** 2026-11-20
**Principios afectados:** II (contrato), III (por defecto = original), V (verificable), VII (seguridad)

## Contexto
Torrentio ya cubre MejorTorrent, Wolfmax4K y CineCalidad ([spec 001](../001-filtro-idioma/spec.md)).
El usuario quiere más webs con contenido en **castellano** (sin webs solo latinas). Según los canales
activos de Alfa (`alfa-addon/addon`, GPL-3), faltan: **DonTorrent, Elite Torrent, DivxTotal y GranTorrent**.

> **Restricción conocida:** desde la red del usuario las cuatro webs están bloqueadas por DNS (resuelven a
> `127.0.0.1`, bloqueo de operadora). No se ha podido descargar su HTML: la implementación se basa en la
> estructura que usa Alfa y en patrones genéricos, y queda **pendiente de validar en un Kodi con acceso**.

## Historias de usuario

### HU-1 — Más fuentes en castellano (P1)
Como usuario hispanohablante quiero que cocoesp busque también en webs españolas para encontrar
versiones en castellano que no están en los indexadores internacionales.

1. **Dado** Elite Torrent activado y accesible, **cuando** busco *Interstellar*, **entonces** aparecen sus
   torrents con calidad, tamaño y hash, marcados como español.
2. **Dado** un resultado cuyo torrent solo contiene `.rar`/`.zip` (con clave), **entonces** se descarta.

### HU-2 — Sobrevivir a los cambios de dominio (P1)
Como usuario quiero cambiar el dominio de cada web desde los ajustes cuando la web se mude.

1. **Dado** el ajuste de dominio de DivxTotal vacío, **entonces** se usa el dominio por defecto.
2. **Dado** un dominio escrito en el ajuste, **entonces** se usa ese.

## Casos límite
- Web caída o bloqueada → el proveedor devuelve `[]` sin romper la búsqueda.
- Títulos en español distintos del inglés (*El Padrino*): se busca también con los alias de España que envía la app.
- DonTorrent protege muchas descargas con una prueba de trabajo (*proof-of-work*) antibot: **no se resuelve**;
  solo se usan enlaces directos, así que puede devolver pocos resultados.
- Torrents protegidos con contraseña (contenido en `.rar`): descartados.

## Requisitos funcionales
- **FR-001**: Cuatro proveedores nuevos: `dontorrent`, `elitetorrent`, `divxtotal`, `grantorrent`, **desactivados por defecto**.
- **FR-002**: Solo películas (`hasEpisodes = False`); las series quedan fuera de alcance.
- **FR-003**: Buscar con el título y con los alias de país `es` enviados por la app (máximo 2 términos).
- **FR-004**: Aceptar un resultado solo si su título normalizado (sin acentos ni etiquetas) coincide con el título
  o un alias, y, si indica año, este está a ±1 del de la película.
- **FR-005**: Descargar el `.torrent`, calcular el *infohash* (SHA-1 del diccionario `info`) y construir el magnet;
  nombre y tamaño salen del propio torrent.
- **FR-006**: Marcar los resultados como español (`name_info` + `spanish.`) y pasarlos por `remove_lang` y `remove_undesirables`.
- **FR-007**: Dominio configurable por web (`<web>.url`), con valor por defecto si está vacío.
- **FR-008**: Límite de 5 fichas y 10 torrents por búsqueda; respetar `data['timeout']`.
- **FR-009**: No resolver captchas ni pruebas antibot.

## Criterios de éxito
- **SC-001**: Pruebas sin red con HTML y torrents sintéticos pasan ([`tests/test_spanish_sites.py`](../../tests/test_spanish_sites.py)). ✅
- **SC-002**: En un Kodi con acceso a las webs, cada proveedor devuelve resultados para *Interstellar*. ⏳
- **SC-003**: Con los proveedores desactivados (por defecto), las búsquedas no cambian. ✅ (por diseño)

## Fuera de alcance
- Series y temporadas; DonTorrent con *proof-of-work*; webs solo latinas (PelisPanda, Hacktorrent, Mitorrent).
- Saltar el bloqueo DNS (decisión del usuario sobre su red).
