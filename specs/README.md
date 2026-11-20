# Documentación SDD de cocoesp

Este proyecto se documenta con **Spec-Driven Development (SDD)**: cada cambio parte de una
especificación (*qué* y *por qué*), se traduce en un plan técnico (*cómo*) y en tareas verificables,
siempre dentro de los principios de la [constitución](constitution.md).

> Las especificaciones 001–004 son **retroactivas**: documentan trabajo ya implementado y publicado
> (commits `6253606` y `c37bb80`). Lo pendiente aparece como tareas abiertas `[ ]`.

## Flujo de trabajo

```
constitution.md ──► spec.md ──► plan.md (+ research.md, contracts/) ──► tasks.md ──► código ──► quickstart.md (validación)
   principios        qué/por qué     cómo                                  pasos           build_repo.py     pruebas manuales en Kodi
```

1. **Especificar** — copia [`templates/spec-template.md`](templates/spec-template.md) en `specs/NNN-nombre/spec.md`.
   Sin detalles de implementación; requisitos `FR-xxx` comprobables y criterios de éxito `SC-xxx`.
2. **Planificar** — `plan.md` con el diseño, la *comprobación de la constitución* y los ficheros afectados.
   Las dudas técnicas se resuelven en `research.md`; las interfaces públicas, en `contracts/`.
3. **Descomponer** — `tasks.md` con tareas pequeñas, ordenadas y trazables a requisitos (`[FR-xxx]`).
4. **Implementar y validar** — código, `tools/build_repo.py`, y el `quickstart.md` de la funcionalidad.
5. **Cerrar** — marcar tareas, subir versión en `addon.xml`, `changelog.txt`, commit y push.

## Índice

| Documento | Contenido | Estado |
|---|---|---|
| [constitution.md](constitution.md) | Principios no negociables del proyecto | Vigente v1.0.0 |
| [000-baseline](000-baseline/architecture.md) | Arquitectura heredada de CocoScrapers 1.0.45 | Referencia |
| [001-filtro-idioma](001-filtro-idioma/spec.md) | Ajuste «Idioma de las fuentes» y Torrentio en español | Implementado |
| [002-addon-independiente](002-addon-independiente/spec.md) | Renombrado a `script.module.cocoesp` | Implementado |
| [003-repositorio-kodi](003-repositorio-kodi/spec.md) | Repositorio `repository.karv3l` en GitHub | Implementado · Pages pendiente |
| [004-puente-cocoscrapers](004-puente-cocoscrapers/spec.md) | Add-on puente para Fen/Umbrella | Implementado · validación en Kodi pendiente |

## Glosario

| Término | Significado |
|---|---|
| **Add-on / módulo** | Paquete de Kodi identificado por su `id` en `addon.xml`. |
| **Front-end / app** | Add-on de vídeo que usa el módulo de scrapers (Fen, Umbrella…). |
| **Scraper / proveedor** | Clase `source` en `sources_cocoesp/torrents/*.py` que busca en un sitio o API. |
| **`name_info`** | Nombre del release normalizado (minúsculas, separado por puntos, `.x.y.`) sobre el que se filtra. |
| **Puente** | Add-on con id `script.module.cocoscrapers` que redirige a cocoesp. |
| **Repositorio Kodi** | `addons.xml` + `addons.xml.md5` + zips, servido desde GitHub. |
