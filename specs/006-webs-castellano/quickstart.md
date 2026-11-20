# Validación 006: Proveedores de webs en castellano

## Pruebas automáticas (sin Kodi ni red)
```
.venv\Scripts\python -I tests\test_spanish_sites.py
```
Esperado: `FALLOS: 0`. Usan HTML sintético: validan la lógica, **no** la maquetación real.

## Requisito de red
En España muchas operadoras bloquean estas webs por DNS (resuelven a `127.0.0.1`). Compruébalo:
```
nslookup www.elitetorrent.com
```
Si devuelve `127.0.0.1`, el Kodi de esa red no llegará a la web. Usar otro DNS es decisión tuya.

## Validación manual en Kodi
| # | Paso | Resultado esperado |
|---|---|---|
| 1 | Ajustes de cocoesp → «Idioma de las fuentes» = Solo español | — |
| 2 | Activar los cuatro proveedores de «Webs en castellano» | Aparece el campo «Dominio» de cada uno |
| 3 | Buscar *Interstellar* (o *El Padrino*) en Fen/Umbrella | Resultados con proveedor `elitetorrent`, `divxtotal`, `grantorrent` o `dontorrent` |
| 4 | Si una web no da resultados: activar el log de cocoesp y repetir | Revisar si la búsqueda devuelve HTML, si encuentra fichas y si hay enlaces `.torrent` |
| 5 | Si la web cambió de dominio: escribir el nuevo en «Dominio» | Vuelve a dar resultados |

Para afinar una web (T014) guarda con Ctrl+S la página de resultados y la ficha en `tests/fixtures/<web>/`.
