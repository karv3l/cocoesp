# Contrato 004: alias de importación y reenvío del plugin

## Importaciones

| Lo que pide la app | Lo que recibe |
|---|---|
| `import cocoscrapers` | módulo `cocoesp` (`cocoscrapers is cocoesp`) |
| `from cocoscrapers import sources` | `cocoesp.sources` |
| `import cocoscrapers.modules.X` / `from cocoscrapers.modules import X` | `cocoesp.modules.X` (mismo objeto) |
| `cocoscrapers.sources_cocoscrapers[.Y]` | `cocoesp.sources_cocoesp[.Y]` |
| `from cocoscrapers import sources_cocoscrapers` | `cocoesp.sources_cocoesp` (vía `cocoesp.sources_cocoscrapers`) |
| `cocoscrapers.noexiste` | `ModuleNotFoundError: No module named 'cocoesp.noexiste'` |

Tabla de mapeo (`_RENAMES`, se aplica la primera coincidencia de prefijo):

| Prefijo | Sustituto |
|---|---|
| `cocoscrapers.sources_cocoscrapers` | `cocoesp.sources_cocoesp` |
| `cocoesp.sources_cocoscrapers` | `cocoesp.sources_cocoesp` |
| `cocoscrapers` | `cocoesp` |

Invariantes:
- El buscador se registra una sola vez (marca `_cocoesp_alias`).
- No se ejecuta código de cocoesp dos veces: el alias devuelve el módulo ya importado.

## Acciones del plugin

`plugin://script.module.cocoscrapers/<query>` → `RunPlugin(plugin://script.module.cocoesp/<query'>)`, donde
`query'` = `query` con `CocoScrapersSettings` → `cocoespSettings` y `script.module.cocoscrapers` → `script.module.cocoesp`.

Acciones de cocoesp disponibles: `cocoespSettings`, `ShowChangelog`, `ShowHelp`, `Defaults`, `toggleAll`,
`toggleAllHosters`, `toggleAllTorrent`, `toggleAllPackTorrent`, y las de log/estadísticas de `lib/default.py`.

## Ajustes del puente
| id | Tipo | Acción |
|---|---|---|
| `open.cocoesp.settings` | action | `RunPlugin(plugin://script.module.cocoesp/?action=cocoespSettings)` |
