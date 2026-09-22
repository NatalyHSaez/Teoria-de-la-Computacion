# Revisión de integración y validación

Fecha: 19 de septiembre de 2026. Rama de trabajo: `alvaro`.

## Estado comparado antes de los cambios

| Rama | Commit observado | Hallazgo |
|---|---|---|
| alvaro | 7be60b2 | Solo el commit inicial; no contenía implementación. |
| main | 2fa47c4 | Implementación modular bajo prolog_lexer, con enunciado y formato. |
| nataly | 2fa47c4 | Idéntica a main, sin cambios exclusivos. |
| diego | 06eb776 | Sustituye la estructura por src/tests/corpus; 20 entradas válidas, 8 inválidas y 32 pruebas. Eliminó el enunciado y el formato. |

Se adelantó alvaro hasta diego conservando el historial y la autoría original.
Se recuperaron los dos documentos desde main. Se mantuvo una sola implementación
activa para evitar dos interfaces y políticas incompatibles. La versión de main
sigue disponible en su rama y en el historial.

## Correcciones y extensiones

- Separación correcta entre un real y el punto final: `3.14.`.
- Descarte completo de números mal formados: `1.2abc`, `1.2.3.4`, `1e+`.
- Notación exponencial opcional, ya presente en la implementación anterior de main.
- Rechazo de `:`, `?` y barra invertida aislados.
- Comillas dobladas dentro de literales, además de los escapes existentes.
- Posiciones coherentes para LF, CRLF y CR; análisis repetido sin duplicar EOF.
- Consola con códigos 0/1/2, errores de archivo sin traceback y lexemas con repr.
- Pruebas ejecutables desde la raíz y verificación del tamaño mínimo del corpus.
- Workflow para ejecutar las pruebas en varias versiones de Python.

## Evidencia local

Entorno de validación: Windows, Python 3.12, pytest 9.1.1.

- Antes de modificar el lexer: las 32 pruebas originales pasaban.
- Con las 26 nuevas pruebas y el lexer anterior: 17 fallaban y 9 pasaban.
  Algunos fallos corresponden a extensiones incorporadas de main, como exponentes
  y comillas dobladas; los restantes revelan problemas de límites y diagnósticos.
- Después de las correcciones: **58 pruebas pasan**.
- Entrada completa limpia: 55 tokens, 0 errores, código de salida 0.
- Entrada completa con errores: 25 tokens, 6 diagnósticos, código de salida 1.
- El corpus conserva 20 archivos válidos y 8 inválidos, además de las entradas
  completas. Sus pruebas pasan.

La suite valida los casos implementados y los mínimos del enunciado; no constituye
una demostración de ausencia de todo error. El alcance es el subconjunto documentado,
no la totalidad de ISO Prolog o SWI-Prolog. Los resultados del workflow remoto
requieren su ejecución en GitHub; no se deducen de las pruebas locales.

## Requisitos que corresponden al informe

El programa cubre reconocimiento, posiciones, tabla, recuperación y corpus.
El informe todavía debe completar el catálogo de categorías faltantes, atributos
 y ejemplos inválidos; autómatas, determinización y minimización; arquitectura,
resultados y conclusiones. Esos contenidos no se desarrollaron en esta revisión
porque el alcance solicitado fue corregir únicamente lo ya escrito.

Las correcciones del informe se hicieron en el Google Docs compartido, no en el
archivo original de formato. El historial Git registra aportes de código reales;
las contribuciones anteriores siguen conservando a sus autores.
