# Analizador léxico de Prolog

## Ejecutar

Desde esta carpeta, con Python 3.10 o posterior:

```sh
python -m pip install -r requirements.txt
python -m src.main corpus/programa_limpio.pl --tabla
python -m pytest -q
```

Los tokens se imprimen como `<TIPO, lexema, linea, columna>`, usando `repr`
para representar comillas y escapes del lexema. Los diagnósticos van a stderr
e incluyen posición, fragmento y recuperación. La tabla opcional muestra
índice, lexema y número de apariciones.

Códigos de salida: 0 sin errores léxicos; 1 con errores léxicos; 2 si no se
puede leer el archivo UTF-8 o los argumentos no son válidos. Se admite BOM.

## Subconjunto y decisiones verificables

- Identificadores: clasificación Unicode de Python (`islower`, `isupper`,
  `isalnum`); también admiten guion bajo en la continuación. No se normaliza
  Unicode. Los átomos operadores `is` y `mod` son `ATOMO`.
- `_` produce `VARIABLE_ANON`; `_Nombre` produce `VARIABLE`.
- Números: dígitos ASCII `0-9`, fracción opcional con dígitos a ambos lados del
  punto, exponente opcional `e`/`E`, signo opcional del exponente y uno o más
  dígitos. Ejemplos: `25`, `3.14`, `1e3`, `1.2E-3`. Se conserva el lexema sin
  convertirlo a `float`, por lo que no se pierde precisión ni se desborda.
- `3.14.` produce `NUMERO('3.14')`, `PUNTO('.')`. `1.2.3` y `12abc` son errores
  completos. Por decisión de recuperación, `1.2.3` se considera inválido
  incluso si se pretendía escribir varias cláusulas numéricas sin separación.
- Se conserva la política de signos de Diego: con `signed_numbers=True`
  (predeterminado), un signo unido a un dígito se integra al número si el
  token anterior no es un operando. Son operandos números, átomos, variables,
  cadenas y cierres `)`, `]`, `}`. Espacios y comentarios no cambian ese token.
  Por eso `p(-3)` contiene `NUMERO('-3')`, pero `X is -3` contiene `ATOMO('is')`,
  `OPERADOR('-')`, `NUMERO('3')`. Con `Lexer(texto, tabla, signed_numbers=False)`
  los signos se separan siempre. Es una política léxica, no análisis sintáctico.
- Operadores: `:-`, `?-`, `-->`, `=`, `\=`, `==`, `\==`, `=..`, `<`, `=<`, `>`,
  `>=`, `+`, `-`, `*`, `/`, `//`, `**`, `\+`, `!`, `;`. Se reconocen primero
  los de mayor longitud. `:`, `?` y `\` aislados producen error.
- Delimitadores: `(`, `)`, `[`, `]`, `{`, `}`, `|`, `,`, `.`.
- Literales: comillas simples para `ATOMO_QUOTADO`, dobles para `CADENA`.
  Se admiten literales vacíos, comillas dobladas, `\n`, `\t`, `\\` y la comilla
  delimitadora escapada. Las secuencias desconocidas se conservan literalmente;
  no se decodifica el contenido. No se admiten literales con saltos de línea.
  Esta política no reproduce todas las reglas de escape de SWI-Prolog.
- Comentarios: `%` hasta fin de línea y `/* ... */` hasta el primer cierre,
  sin anidamiento. Se ignoran junto con espacio, tabulador, CR y LF.
- Posiciones: línea y columna desde 1; el tabulador cuenta como un carácter.
  CRLF cuenta como un salto, igual que LF o CR por separado.
- Tabla: deduplicación por lexema exacto y contador de apariciones. `juan`
  y `'juan'` son entradas distintas. Registrar `_` no implica unificar las
  variables anónimas: solo se cuenta su grafía, sin análisis semántico.
- Recuperación: descartar un carácter inválido, un literal sin cierre hasta
  fin de línea o un número mal formado completo. Un comentario sin cierre
  consume hasta EOF.

El lexer acepta secuencias de tokens que un intérprete podría rechazar por
sintaxis. No admite bases numéricas alternativas, comentarios anidados ni
el conjunto completo de operadores de SWI-Prolog.

## Archivos y validación

- `src/`: lexer, tokens, tabla y consola.
- `corpus/validos/`: 20 archivos válidos.
- `corpus/invalidos/`: 8 archivos inválidos.
- `corpus/programa_limpio.pl`: entrada completa sin errores.
- `corpus/programa_con_errores.pl`: entrada completa con errores recuperables.
- `tests/`: pruebas originales y regresiones de límites, posiciones y consola.

La suite comprueba los mínimos de 20/8 archivos. GitHub Actions está configurado
para Python 3.10, 3.12 y 3.14; configurar el workflow no equivale a ejecutarlo.
La evidencia local está en `../REVISION.md`.
