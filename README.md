# csv2json

`csv2json` es un paquete para convertir archivos CSV a JSON.
Proyecto de prueba para materia Calidad de Software - UFASTA - Mar del Plata

Este programase encuentra bajo una Licencia Creative Commons Atribución-NoComercial 4.0  Internacional.
Permite: Compartir, adaptar y modificar sin fines comerciales, citando al autor. 

## Estado

- Versión: `1.0 build 000`
- Python: `3.13`
- Licencia: `MIT`

## Funciones disponibles

- Conversión de CSV a JSON en memoria.
- Conversión de archivos CSV a archivos JSON.
- Soporte para salida JSON tradicional o JSON Lines.
- CLI separada de la lógica del dominio.
- Validaciones, tipado estático, pruebas e integración continua.

## Estructura

```text
src/        paquete Python
tests/      pruebas automáticas
docs/       documentación base y salida generada
script/     utilidades auxiliares fuera del alcance del workflow
ejemplos/   ejemplos fuera del alcance del workflow
```

## Uso rápido

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
csv2json ejemplos/sample.csv --output output.json --indent 2
```

## Calidad local

```bash
ruff check src tests
black --check src tests
mypy src tests
pyright src tests
pytest --cov=src/csv2json --cov-fail-under=80
bandit -r src
```

## Documentación

```bash
pdoc --output-directory docs/site src/csv2json
```
