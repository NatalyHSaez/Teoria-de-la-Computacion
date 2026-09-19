# Analizador léxico de Prolog

Proyecto INFO1148, segundo semestre de 2026. Requiere Python 3.10 o posterior.
El lexer utiliza la biblioteca estándar; pytest es solo para las pruebas.

## Ejecutar desde la raíz del repositorio

```sh
python -m pip install -r "Tarea C1/requirements.txt"
python -m pytest -q
cd "Tarea C1"
python -m src.main corpus/programa_limpio.pl --tabla
python -m src.main corpus/programa_con_errores.pl --tabla
```

La última entrada contiene errores intencionales y debe terminar con código 1.
Código 0 indica análisis sin errores; código 2, un problema de lectura o argumentos.

- [Instrucciones y decisiones del lexer](Tarea%20C1/README.md)
- [Revisión de ramas y requisitos](REVISION.md)
- [Enunciado original](Tarea%20C1/Tarea%20INFO1148%20sem2_2026.pdf)
- [Formato original](Tarea%20C1/Formato%20Informe%20Tarea.docx)

El programa reconoce tokens: no valida sintaxis ni ejecuta Prolog.
El formato original se conserva; el informe compartido se revisa por separado.
