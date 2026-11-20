# Validación 001: Idioma de las fuentes

## Pruebas automáticas (sin Kodi)
```
.venv\Scripts\python -I tests\test_language_filter.py
```
Resultado esperado: `FALLOS: 0` y `Torrentio (fixture, modo es): 20 resultados, 15 se mantienen, 5 descartados`.

## Validación manual en Kodi
Requisitos: cocoesp instalado, una app que lo use (directamente o vía [puente](../004-puente-cocoscrapers/spec.md))
y Torrentio activado en los proveedores de cocoesp.

| # | Paso | Resultado esperado |
|---|---|---|
| 1 | Abrir ajustes de cocoesp → «Idioma de las fuentes» | Valor «Inglés»; el interruptor de audio extranjero visible |
| 2 | Buscar *Interstellar* en la app | Resultados en inglés; sin releases `CASTELLANO` |
| 3 | Cambiar a «Solo español» | El interruptor de audio extranjero desaparece |
| 4 | Repetir la búsqueda (sin caché) | Solo releases en castellano/latino; aparecen Wolfmax4k, MejorTorrent, Cinecalidad |
| 5 | Cambiar a «Multidioma» y repetir | Mezcla de idiomas, incluidos los trackers españoles |
| 6 | Volver a «Inglés» | Mismo resultado que en el paso 2 |

Si la app cachea resultados, limpiar su caché de fuentes entre pasos.
