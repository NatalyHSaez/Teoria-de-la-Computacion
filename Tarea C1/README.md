# Analizador Lexico de Prolog (subconjunto)

Tarea INFO1148 - Teoria de la Computacion. Analizador lexico para un subconjunto
del lenguaje Prolog, implementado en Python con un scanner manual y la regla de
maxima coincidencia (maximal munch).

## Requisitos

- Python 3.10+
- pytest (para las pruebas)

## Instalar dependencias

```
pip install -r requirements.txt
```

## Ejecutar el lexer

Desde la raiz del proyecto:

```
python -m src.main corpus\programa_limpio.pl --tabla
```

Cada token se imprime como `<TIPO_TOKEN, 'lexema', linea, columna>` y con
`--tabla` ademas se muestra la tabla de lexemas.

## Ejecutar las pruebas

```
python -m pytest -v
```

## Estructura

- `src/` - codigo del analizador (tokens, lexer, tabla de lexemas, CLI)
- `corpus/validos/` - 17 archivos .pl validos (una prueba por categoria)
- `corpus/invalidos/` - 6 archivos .pl invalidos (errores lexicos recuperables)
- `corpus/programa_limpio.pl` - archivo integral sin errores
- `corpus/programa_con_errores.pl` - archivo integral con errores recuperables
- `tests/` - pruebas automatizadas con pytest