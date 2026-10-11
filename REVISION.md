# Revisión de integración y validación

## Estado final (versión de entrega)

- Implementación única: `Tarea C1/prolog_lexer/`. La implementación alternativa
  `Tarea C1/src/` se eliminó en el commit 71428a8 para evitar dos interfaces y
  políticas léxicas incompatibles; sigue disponible en el historial y en la rama `diego`.
- Corpus: `corpus/validos/` (20 archivos), `corpus/invalidos/` (8 archivos),
  `programa_valido.pl` y `programa_con_errores.pl`.
- Pruebas: `python -m pytest -q` desde la raíz ejecuta 83 pruebas, todas aprobadas.
  - `programa_valido.pl`: 380 tokens, 0 errores.
  - `programa_con_errores.pl`: 73 tokens, 9 errores, código de salida 1.
- Correcciones posteriores a 71428a8:
  - Los números solo aceptan dígitos ASCII `0-9`. Un dígito Unicode como `²`
    se informa como carácter no admitido en vez de interrumpir el programa.
  - `1.2.3.4` se descarta completo como número mal formado.
  - Dos pruebas de regresión cubren ambos casos.

## Historial de la integración

| Rama | Aporte |
|---|---|
| nataly | Implementación modular `prolog_lexer`, enunciado y formato. |
| diego | Implementación alternativa `src/` y corpus de 20 válidos y 8 inválidos. |
| alvaro | Pruebas de regresión, correcciones de límites numéricos y posiciones, CLI y workflow. |

La rama `main` integra estos aportes. El corpus de `diego` se trasladó a
`prolog_lexer/corpus/` y se valida con `tests/test_corpus_archivos.py`.

La suite valida los casos implementados y los mínimos del enunciado; no constituye
una demostración de ausencia de errores. El alcance es el subconjunto documentado
en el informe, no la totalidad de ISO Prolog o SWI-Prolog.
