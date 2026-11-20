# Validación 004: Add-on puente

## Prueba automática (sin Kodi)
```
.venv\Scripts\python -I tests\test_bridge_alias.py
```
Esperado: 8 líneas `OK` y `FALLOS: 0`.

## Validación manual en Kodi
| # | Paso | Resultado esperado |
|---|---|---|
| 1 | Desinstalar el CocoScrapers original (si está) | — |
| 2 | karv3l Repository → instalar «cocoesp (puente CocoScrapers)» | Se instalan el puente y cocoesp |
| 3 | En Fen/Umbrella, abrir los ajustes de CocoScrapers desde la app | Se abren los ajustes de **cocoesp** |
| 4 | En cocoesp: «Idioma de las fuentes» = Solo español; activar Torrentio | — |
| 5 | Buscar una película en Fen/Umbrella | Fuentes en español; en el log de Kodi aparecen rutas de `script.module.cocoesp` |
| 6 | Ajustes del puente → «Abrir ajustes de cocoesp» | Se abren los de cocoesp |
| 7 | Desinstalar el puente | cocoesp sigue instalado; la app ya no encuentra CocoScrapers |

Si la búsqueda falla con `No module named 'cocoesp'`, la tarea T014 aplica: revisar el log y el `sys.path`.
