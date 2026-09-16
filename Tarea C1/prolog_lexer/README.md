# Analizador léxico de un subconjunto de Prolog

Implementación en Python (sin dependencias externas, salvo `pytest` para las
pruebas) del analizador léxico solicitado en la tarea de **Teoría de la
Computación (INFO1148, 2° semestre 2026)**: reconoce los tokens de un
subconjunto de Prolog inspirado en ISO Prolog / SWI-Prolog, administra una
tabla de lexemas y reporta errores léxicos con recuperación.

**Alcance:** solo análisis léxico. No se implementa ni se pretende
implementar análisis sintáctico (no hay parser, no hay árbol sintáctico, no
se valida el orden gramatical de los tokens), tal como indica el enunciado.

## Estructura del repositorio

```
prolog_lexer/
├── lexer/
│   ├── token_types.py   # Enum TipoToken + clase Token
│   ├── errors.py         # Clase ErrorLexico
│   ├── symbol_table.py   # Clase TablaDeSimbolos
│   └── lexer.py           # Clase AnalizadorLexico (el analizador en sí)
├── cli.py                 # Interfaz de línea de comandos
├── corpus/
│   ├── programa_valido.pl        # Archivo completo SIN errores
│   └── programa_con_errores.pl   # Archivo completo con múltiples errores recuperables
├── tests/
│   ├── conftest.py
│   ├── test_categorias.py   # ≥20 pruebas válidas (una por categoría léxica)
│   ├── test_prioridad.py     # Casos de máxima coincidencia / prioridad
│   ├── test_errores.py       # ≥8 pruebas inválidas + recuperación de errores
│   └── test_corpus.py         # Pruebas de integración sobre los 2 archivos completos
├── requirements.txt
└── README.md
```

## Requisitos

- Python 3.8 o superior (solo biblioteca estándar).
- `pytest` únicamente para ejecutar la suite de pruebas.

## Instalación

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución del analizador

```bash
python cli.py corpus/programa_valido.pl
python cli.py corpus/programa_con_errores.pl
python cli.py corpus/programa_valido.pl --tabla          # además imprime la tabla de lexemas
python cli.py corpus/programa_con_errores.pl --solo-errores
```

Cada token se imprime en el formato pedido por el enunciado:

```
<TIPO, 'lexema', línea, columna>
```

Por ejemplo, para el fragmento de ejemplo del propio enunciado (`padre(juan, ana).`)
el analizador produce exactamente:

```
<ATOMO, 'padre', 2, 1>
<PARENTESIS_IZQ, '(', 2, 6>
<ATOMO, 'juan', 2, 7>
<COMA, ',', 2, 11>
<ATOMO, 'ana', 2, 13>
<PARENTESIS_DER, ')', 2, 16>
<PUNTO, '.', 2, 17>
```

El código de salida del CLI es `1` si se detectó al menos un error léxico y
`0` en caso contrario (útil para integrarlo en CI).

## Ejecución de las pruebas

```bash
pytest -v
```

La suite actual tiene **79 pruebas** y cubre:

- Las 19 categorías léxicas definidas (`test_categorias.py`, ≥20 casos).
- Prioridad y máxima coincidencia entre operadores/átomos/variables
  (`test_prioridad.py`).
- Errores léxicos y su recuperación (`test_errores.py`, ≥8 casos inválidos).
- Los dos archivos de entrada completos exigidos en la sección 6 del
  enunciado (`test_corpus.py`).

## Categorías léxicas reconocidas y su correspondencia con expresiones regulares

Esta tabla resume la especificación implementada en `lexer/lexer.py`; se
recomienda usarla como base para la sección "Especificación del subconjunto"
y "Expresiones regulares" del informe técnico, y comprobar que sea
coherente con los autómatas presentados allí.

| Token            | Expresión regular equivalente                          | Ejemplos válidos                | Ejemplos inválidos |
|-------------------|----------------------------------------------------------|----------------------------------|----------------------|
| `ATOMO`           | `[a-z][A-Za-z0-9_]*`                                     | `padre`, `persona_1`, `is`      | `Padre` (var), `1abc` |
| `ATOMO_COMILLAS`  | `'([^'\\]\|\\.\|'')*'`                                    | `'Juan Pérez'`, `':-'`          | `'sin cierre`         |
| `VARIABLE`        | `(_\|[A-Z])[A-Za-z0-9_]*`                                 | `X`, `Persona`, `_Temporal`, `_`| `1X` (no es var)      |
| `ENTERO`          | `[0-9]+`                                                  | `42`, `0`                        | `-3` (el signo es token aparte) |
| `REAL`            | `[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?` \| `[0-9]+[eE][+-]?[0-9]+` | `3.14`, `6.022e23`         | `1.2.3`, `1e+`        |
| `CADENA`          | `"([^"\\]\|\\.\|"")*"`                                    | `"hola"`                         | `"sin cierre`         |
| `OP_CLAUSULA`     | `:-` \| `\?-` \| `-->`                                    | `:-`, `?-`, `-->`                | `:` solo               |
| `OP_RELACIONAL`   | `=\.\.` \| `\\==` \| `==` \| `\\=` \| `=<` \| `>=` \| `=` \| `<` \| `>` | `=`, `\=`, `==`, `=..`, `=<`, `>=` | — |
| `OP_ARITMETICO`   | `\*\*` \| `//` \| `[+\-*/]`                                | `+`, `-`, `*`, `/`, `//`, `**`  | — |
| `OP_CONTROL`      | `\\\+` \| `!` \| `;`                                       | `\+`, `!`, `;`                   | — |
| `COMA`            | `,`                                                        | `,`                               | — |
| `PUNTO`           | `\.`                                                       | `.`                               | — |
| Delimitadores     | `\(` \| `\)` \| `\[` \| `\]` \| `\{` \| `\}` \| `\|`         | `(`, `)`, `[`, `]`, `{`, `}`, `\|` | — |
| Comentario línea | `%[^\n]*`                                                  | `% texto`                        | se descarta, no es token |
| Comentario bloque| `/\*.*?\*/` (con `.` incluyendo saltos de línea)            | `/* texto */`                    | `/* sin cierre`       |
| Espacios          | `[ \t\r\n]+`                                               | —                                 | se descarta, no es token |

## Decisiones de diseño (deben citarse en el informe)

1. **Signo de los números:** el signo (`+`/`-`) nunca forma parte del
   lexema de un `ENTERO`/`REAL`. Siempre se tokeniza por separado como
   `OP_ARITMETICO`. Esto elimina toda ambigüedad léxica entre "menos
   unario" y "resta"; distinguir ambos casos es un problema sintáctico y
   queda fuera del alcance de esta tarea.
2. **Máxima coincidencia (maximal munch):** los operadores/delimitadores
   de lexema fijo se prueban ordenados por longitud descendente en cada
   posición, de modo que `=..` gane sobre `=`/`==`, `\==` sobre `\=`,
   `=<`/`>=` sobre `=`/`>`, `-->` sobre `-`, etc.
3. **Escapes documentados:** en átomos entrecomillados y cadenas se
   admite la comilla doblada (`''`, `""`) como carácter literal, y las
   secuencias `\n \t \r \a \b \f \v \\ \' \"`, además del escape de
   continuación de línea (`\` seguido de un salto de línea real).
4. **Recuperación de errores:** carácter no admitido → se descarta un
   carácter y se continúa; átomo/cadena sin cierre → se avanza hasta fin
   de línea y se continúa en la línea siguiente; número mal formado → se
   descarta el fragmento completo y se continúa; comentario de bloque
   sin cierre → se reporta y se consume hasta EOF (no existe un punto de
   recuperación razonable dentro de un comentario).

## Tabla de lexemas

`lexer/symbol_table.py` implementa `TablaDeSimbolos`, que registra sin
duplicados los átomos, variables, enteros, reales y cadenas encontrados.
La variable anónima (`_`) nunca se registra, porque cada ocurrencia
representa una variable distinta. Cada `Token` expone `indice_tabla` con
el índice asignado (o `None` si no aplica), cumpliendo el requisito de
"atributo o referencia a tabla de símbolos" del punto 5 del enunciado.

## Pendiente para completar la entrega

Este repositorio cubre el punto 5 (implementación), parte del punto 6
(tabla de lexemas), el punto 7 (errores léxicos) y el punto 8 (corpus de
pruebas) del "Trabajo solicitado". Aún deben desarrollarse, como parte del
**informe técnico en PDF**, los puntos 1-4 (especificación formal,
expresiones regulares explícitas, autómatas AFN/AFD, determinización y
minimización) apoyándose en la tabla de correspondencias de este README, y
debe completarse el anexo con el enlace al repositorio Git y el historial
de contribuciones de todos los integrantes.
