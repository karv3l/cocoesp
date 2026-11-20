# Plan 003: Repositorio de Kodi en GitHub

**Spec:** [spec.md](spec.md)

## Resumen
El repo `karv3l/cocoesp` es a la vez código fuente y repositorio de Kodi. `tools/build_repo.py`
recorre `src/`, empaqueta cada add-on y regenera los índices en la raíz del repo.

## Comprobación de la constitución
| Principio | Cumple | Nota |
|---|---|---|
| I. Independencia | ✅ | Repositorio propio; no reutiliza URLs del original. |
| VI. Publicación reproducible | ✅ | Un solo script genera todo. |
| VII. Privacidad | ✅ | Autor de commits `karv3l <karv3l@users.noreply.github.com>` (config local del repo). |

## Estructura del repositorio

```
karv3l/cocoesp (rama main)
├── index.html                         ← enlace al zip del repositorio (GitHub Pages)
├── repository.karv3l-1.0.0.zip        ← se instala «desde zip»
├── .nojekyll                          ← Pages sirve los ficheros tal cual
├── zips/                              ← lo que lee Kodi (raw.githubusercontent.com)
│   ├── addons.xml
│   ├── addons.xml.md5
│   ├── repository.karv3l/             repository.karv3l-1.0.0.zip + addon.xml, icon, fanart
│   ├── script.module.cocoesp/         script.module.cocoesp-1.0.0.zip + addon.xml, icon, fanart, changelog
│   └── script.module.cocoscrapers/    puente (spec 004)
├── src/                               ← código fuente de cada add-on (carpeta = id)
├── tools/build_repo.py
├── tests/
├── specs/                             ← esta documentación
├── requirements.txt, README.md, .gitignore
```

## Algoritmo de `build_repo.py`
1. Para cada carpeta de `src/` con `addon.xml`: leer `id` y `version`; exigir carpeta == id.
2. Crear `zips/<id>/<id>-<version>.zip` (recorrido ordenado, exclusiones de FR-003, rutas con `/`).
3. Copiar `addon.xml`, `icon.png`, `fanart.png`, `changelog.txt` junto al zip.
4. `addons.xml` = `<addons>` + cuerpo de cada `addon.xml` sin la declaración XML; validar con `ElementTree`.
5. `addons.xml.md5` = MD5 del texto escrito (UTF-8, saltos `\n`).
6. Copiar el zip de `repository.karv3l` a la raíz (borrando versiones anteriores de la raíz) y escribir `index.html`.

## Decisiones
| Decisión | Motivo |
|---|---|
| `raw.githubusercontent.com` para los datos | Igual que el repositorio original; no depende de Pages. |
| Pages solo para `index.html` | El gestor de archivos de Kodi necesita un listado HTML. |
| Saltos de línea `\n` en `addons.xml` | Git normaliza a LF en el repo (`core.autocrlf`); el MD5 publicado coincide. |
| Código y artefactos en el mismo repo | Un único sitio que mantener; trazabilidad entre fuente y zip. |

## Riesgos
| Riesgo | Mitigación |
|---|---|
| Editar `zips/` a mano rompe el MD5 | Constitución VI: solo `build_repo.py`. |
| Caché de raw (≈5 min) tras publicar | Esperar antes de probar en Kodi. |
| Repo renombrado o rama distinta de `main` | Las URLs están solo en `src/repository.karv3l/addon.xml`; cambiar, subir su versión y regenerar. |
