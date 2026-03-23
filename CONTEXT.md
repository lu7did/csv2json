# CONTEXT

Este archivo preserva las metareglas de creación del proyecto y debe reiterarse al iniciar cada nueva secuencia de construcción.

## Reglas base de construcción

- Python objetivo: `3.13`.
- Implementación sobre un esqueleto de proyecto estilo cookiecutter.
- Crear dos directorios adicionales en la estructura: `script/` y `ejemplos/`.
- El contenido de `script/` y `ejemplos/` no debe incluirse en el workflow de validación de push.
- Preservar este archivo `CONTEXT.md` en el repositorio.
- Generar un `README.md` básico y mantenerlo actualizado con cada push exitoso para reflejar las funciones disponibles.
- Generar un `CHANGELOG.md` y mantenerlo actualizado con cada push exitoso para trazabilidad.
- Registrar en `STORIES.md` todos los requerimientos y peticiones que produzcan un nuevo push, indicando el timestamp de ingreso.
- Agregar licencia MIT.
- Generar documentación automáticamente con `pdoc` o `sphinx`.
- Comenzar con versión `1.0 build 000`.
- Cada push exitoso aumenta en `1` el número de build y debe actualizarse en `README.md` y `CHANGELOG.md`.

## Requisitos de validación y CI

Se debe crear y mantener actualizado un workflow de validación que ejecute:

- `ruff` para validar reglas y detectar errores.
- `black` para validar formato consistente.
- Validación de formato PEP8.
- Validación de convenciones PEP257 para docstrings, aceptando solo si no hay errores.
- `mypy` para módulos no excluidos explícitamente.
- `pyright` para módulos no excluidos explícitamente.
- `pytest` con tests unitarios e hipótesis, exigiendo cobertura de `80%` o superior.
- `bandit` para evaluación básica de seguridad sin observaciones.
- No usar `trufflehog`.
- Generar y mantener documentación básica del módulo.
- Mantener `requirements.txt` actualizado.
- Automatizar un workflow de GitHub integrando la fase completa de CI/CD.

## Reglas de diseño e implementación

- Separar, siempre que sea posible, la lógica funcional de la lógica de presentación e interacción con el usuario.
- Usar programación orientada a objetos.
- Implementar funciones mediante patrones cuando sea posible.
- Gestionar excepciones de runtime y las excepciones específicas requeridas por cada historia.
- Optimizar por performance.
- Permitir uso como paquete de Python.
- Producir un archivo comprimido con toda la estructura necesaria para subir el proyecto a GitHub.

## Validaciones obligatorias antes de cada commit/push

- Revisar que las modificaciones introducidas hayan sido consideradas en todos los módulos afectados.
- Ejecutar localmente los mismos programas del workflow antes del push para minimizar builds fallidos.
- Cuando se introduzca un nuevo argumento o variable global, revisar definición y uso en todos los módulos.
- Cuando se introduzca una nueva librería o package Python, revisar definición y uso en todos los módulos.
- Cuando se haga una modificación estructural en un módulo, realizar análisis de impacto y actualizar el resto para evitar inconsistencias, excepciones, faltantes y otros problemas.
