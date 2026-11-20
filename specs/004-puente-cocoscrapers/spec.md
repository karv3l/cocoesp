# Especificación 004: Add-on puente para Fen, Umbrella y similares

**ID:** `004-puente-cocoscrapers` · **Estado:** Implementada (validación en Kodi pendiente) · **Fecha:** 2026-11-20
**Principios afectados:** I (excepción explícita), II (contrato de las apps), V (verificable)

## Contexto
Tras la [spec 002](../002-addon-independiente/spec.md), las apps que dependen de
`script.module.cocoscrapers` (Fen, Umbrella…) no encuentran cocoesp. Se valoraron tres opciones
(ver [research.md](research.md)); el usuario eligió un **add-on puente** con el id de CocoScrapers,
aceptando que sustituye al original.

## Historias de usuario

### HU-1 — Usar cocoesp desde Fen/Umbrella sin modificarlas (P1)
Como usuario quiero que mis apps actuales usen cocoesp sin tocar su código.

1. **Dado** el puente y cocoesp instalados, **cuando** Fen/Umbrella buscan fuentes, **entonces**
   obtienen los resultados de cocoesp con su ajuste de idioma.
2. **Dado** el puente instalado, **cuando** la app pulsa su botón de «ajustes de CocoScrapers»,
   **entonces** se abren los ajustes de cocoesp.
3. **Dado** el puente, **cuando** se instala desde el repositorio karv3l, **entonces** Kodi instala
   cocoesp automáticamente como dependencia.

### HU-2 — Desactivar el puente (P2)
1. **Dado** el puente instalado, **cuando** lo desinstalo, **entonces** cocoesp sigue instalado y
   funcionando por su cuenta, y puedo volver a instalar el CocoScrapers original.

## Casos límite
- `from cocoscrapers import sources_cocoscrapers` en un intérprete limpio: Python busca
  `cocoesp.sources_cocoscrapers` (porque `cocoscrapers` es `cocoesp`) → debe resolverse.
- Importar el puente varias veces no debe registrar el buscador más de una vez.
- Un submódulo inexistente debe dar `ModuleNotFoundError`, como siempre.
- Si Kodi no añade al `sys.path` la carpeta `lib` de la dependencia transitiva, el puente la añade.
- Apps que leen directamente ajustes de `script.module.cocoscrapers` (p. ej. `provider.*`) ven los
  del puente, que no los tiene.
- Repositorio original también instalado: compite por el mismo id; gana la versión más alta.

## Requisitos funcionales
- **FR-001**: DEBE existir un add-on con id `script.module.cocoscrapers`, nombre
  «cocoesp (puente CocoScrapers)» y dependencia de `script.module.cocoesp` ≥ 1.0.0.
- **FR-002**: `import cocoscrapers` DEBE devolver el módulo `cocoesp`.
- **FR-003**: Todo submódulo `cocoscrapers.X` DEBE resolverse como `cocoesp.X`, y
  `sources_cocoscrapers` como `sources_cocoesp`, devolviendo **los mismos objetos** (sin cargar dos veces).
- **FR-004**: `plugin://script.module.cocoscrapers/?<query>` DEBE reenviarse a
  `plugin://script.module.cocoesp/?<query>`, traduciendo `CocoScrapersSettings` → `cocoespSettings`.
- **FR-005**: Los ajustes del puente DEBEN ofrecer un botón que abra los de cocoesp.
- **FR-006**: La versión DEBE ser mayor que cualquier versión publicada del original (serie 9.x).

## Criterios de éxito
- **SC-001**: Las 8 comprobaciones de [`tests/test_bridge_alias.py`](../../tests/test_bridge_alias.py) pasan. ✅
- **SC-002**: El zip del puente está en `addons.xml` y se descarga desde GitHub. ✅
- **SC-003**: Fen y Umbrella obtienen fuentes de cocoesp en Kodi. ⏳ (validación manual)

## Supuestos
- Las apps acceden al módulo mediante importaciones Python y acciones `plugin://`, no leyendo sus ficheros.

## Fuera de alcance
- Sincronizar los ajustes `provider.*` del puente con los de cocoesp.
- Permitir CocoScrapers original y puente a la vez (imposible: mismo id).
