# Constitución de cocoesp

**Versión:** 1.0.0 · **Ratificada:** 2026-11-20 · **Última enmienda:** 2026-11-20

Principios que toda especificación, plan e implementación debe cumplir. Un plan que viole un
principio debe justificarlo en su sección *Comprobación de la constitución* o no se implementa.

## I. Independencia del add-on original
cocoesp (`script.module.cocoesp`, paquete `cocoesp`) es un add-on **independiente** de CocoScrapers:
id, paquete Python, carpeta de datos, propiedades de ventana, log y versión propios.
Ningún cambio en cocoesp puede alterar una instalación de `script.module.cocoscrapers`.
La **única** excepción explícita es el add-on puente ([spec 004](004-puente-cocoscrapers/spec.md)),
que el usuario instala voluntariamente.

## II. Compatibilidad con el contrato de las apps
La API pública heredada se mantiene estable: `sources(specified_folders=None, ret_all=False)`,
`pack_sources()`, la clase `source` de cada proveedor (`sources()`, `sources_packs()`, atributos
`priority`, `pack_capable`, `hasMovies`, `hasEpisodes`) y el formato de los diccionarios de resultado.
Cualquier cambio en ese contrato requiere spec propia.

## III. Comportamiento por defecto = original
Toda opción nueva tiene como valor por defecto el comportamiento de CocoScrapers 1.0.45.
Un usuario que no toque los ajustes obtiene los mismos resultados que con el original.

## IV. Cambios mínimos y centralizados
Preferir un cambio en un punto común (`modules/source_utils.py`) antes que tocar los 26 proveedores.
No reformatear ni reescribir código heredado que no forma parte del cambio.

## V. Verificable sin ejecutar código de terceros
Cada cambio de lógica tiene una prueba que puede correr fuera de Kodi y sin descargar ni ejecutar
scrapers (extracción por AST, paquetes falsos, datos capturados). Lo que solo puede validarse en Kodi
se documenta en el `quickstart.md` de la funcionalidad como validación manual pendiente.

## VI. Publicación reproducible
Los artefactos de Kodi (`zips/`, `addons.xml`, `addons.xml.md5`, `index.html`, zip del repositorio)
**solo** se generan con `tools/build_repo.py` y nunca se editan a mano. Cada publicación sube la
`version` del add-on afectado y añade su entrada en `changelog.txt`.

## VII. Privacidad y seguridad
- No se publican datos personales: los commits usan `karv3l@users.noreply.github.com`.
- El código descargado se trata como no confiable; no se añaden nuevos `exec`/`eval`
  (el `exec` heredado de `client.sucuri` está documentado en la [línea base](000-baseline/architecture.md#riesgos-conocidos)).
- Los textos visibles para el usuario existen en `en_gb` y `es_es`.

## Gobernanza
- Las enmiendas se registran aquí con versión semántica: MAJOR (se elimina o redefine un principio),
  MINOR (principio nuevo), PATCH (aclaraciones).
- Toda spec enlaza los principios que afecta; todo plan incluye la comprobación.

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-20 | Versión inicial |
