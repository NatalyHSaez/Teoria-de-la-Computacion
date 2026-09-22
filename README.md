# Analizador léxico de Prolog

Proyecto INFO1148, segundo semestre de 2026. Requiere Python 3.10 o posterior.

## Ejecutar desde la raíz del repositorio

```sh
python -m pip install -r "Tarea C1/prolog_lexer/requirements.txt"
python -m pytest -q
cd "Tarea C1/prolog_lexer"
python cli.py corpus/programa_valido.pl --tabla
python cli.py corpus/programa_con_errores.pl --solo-errores
```

- [Instrucciones y decisiones del lexer](Tarea%20C1/prolog_lexer/README.md)
- [Revision de ramas y requisitos](REVISION.md)
- [Enunciado original](Tarea%20C1/Tarea%20INFO1148%20sem2_2026.pdf)
- [Formato original](Tarea%20C1/Formato%20Informe%20Tarea.docx)
