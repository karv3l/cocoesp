# Especificación 002: cocoesp como add-on independiente

**ID:** `002-addon-independiente` · **Estado:** Implementada · **Fecha:** 2026-11-20
**Principios afectados:** I (independencia), II (contrato), VII (privacidad)

## Contexto
La primera versión modificada mantenía el id `script.module.cocoscrapers` y solo cambiaba el nombre
visible (1.1.0). Eso hacía que el repositorio original y el de karv3l compitieran por el mismo add-on:
el de versión más alta sobrescribía al otro. El usuario quiere **dos add-ons independientes**.

## Historias de usuario

### HU-1 — Convivir con CocoScrapers (P1)
Como usuario quiero instalar cocoesp sin que afecte a CocoScrapers, y viceversa.

1. **Dado** CocoScrapers instalado, **cuando** instalo cocoesp, **entonces** ambos aparecen en Kodi
   con ajustes, datos y logs separados.
2. **Dado** ambos instalados, **cuando** cambio un ajuste de cocoesp, **entonces** CocoScrapers no cambia.
3. **Dado** ambos instalados, **cuando** el repositorio original publica una versión nueva,
   **entonces** cocoesp no se actualiza ni se sobrescribe.

### HU-2 — Identidad propia visible (P2)
Como usuario quiero ver «cocoesp» en Kodi (nombre, títulos, notificaciones, log).

## Casos límite
- Ambos add-ons se ejecutan en el mismo proceso de Kodi: las propiedades de la ventana Home son
  compartidas → los nombres de propiedad deben ser distintos.
- Las apps que buscan `script.module.cocoscrapers` dejan de encontrar este módulo (lo resuelve la [spec 004](../004-puente-cocoscrapers/spec.md)).

## Requisitos funcionales
- **FR-001**: El id DEBE ser `script.module.cocoesp` y el nombre visible «cocoesp».
- **FR-002**: El paquete Python DEBE ser `cocoesp` y la carpeta de proveedores `sources_cocoesp`.
- **FR-003**: Las propiedades de ventana, el log (`cocoesp.log`), las URLs `plugin://` y la carpeta
  `addon_data` DEBEN usar el nuevo id o nombre.
- **FR-004**: La acción de abrir ajustes DEBE llamarse `cocoespSettings`.
- **FR-005**: La versión DEBE empezar en `1.0.0`, independiente de la numeración original.
- **FR-006**: DEBE conservarse el crédito a CocoScrapers (descripción, comentarios, historial del changelog).
- **FR-007**: La API pública (`sources()`, `pack_sources()`, clase `source`) NO DEBE cambiar salvo el nombre del paquete.

## Criterios de éxito
- **SC-001**: Ninguna referencia funcional a `cocoscrapers` en el zip de cocoesp (solo créditos). ✅
- **SC-002**: Todo el módulo compila; `addon.xml` y `settings.xml` son XML válidos. ✅
- **SC-003**: En Kodi, ambos add-ons instalados a la vez funcionan por separado. ⏳ (validación manual)

## Fuera de alcance
- Que las apps encuentren cocoesp por su cuenta (spec 004).
