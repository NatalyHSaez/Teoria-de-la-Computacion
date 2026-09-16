"""
Analizador léxico para el subconjunto de Prolog definido en el enunciado
de la tarea de Teoría de la Computación (INFO1148, 2do semestre 2026).

Alcance: solo análisis léxico (alfabetos, expresiones regulares y
autómatas finitos aplicados al reconocimiento de tokens). No se realiza
ningún análisis sintáctico: no se valida el orden gramatical de las
cláusulas ni se construyen árboles de derivación.

Decisiones de diseño relevantes (deben mantenerse coherentes con el
informe técnico y con los autómatas presentados en él):

1. Signo en números. El signo ('+' u '-') NUNCA forma parte del lexema
   de un ENTERO o un REAL. Todo número se reconoce sin signo, y el '+' o
   '-' que lo precede se tokeniza por separado como OP_ARITMETICO. Este
   es el criterio que adoptamos para eliminar toda ambigüedad respecto
   del operador aritmético: decidir si un '-' es "menos unario" o "resta"
   es un problema sintáctico, fuera del alcance de esta tarea.

2. Escapes en átomos entrecomillados y cadenas. Se admite la comilla
   doblada (''  o  "") como forma de incluir el propio delimitador de
   forma literal (convención ISO/SWI-Prolog), y además un conjunto de
   secuencias de escape con barra invertida: salto de línea, tabulador,
   retorno de carro, alerta, retroceso, avance de página, tabulador
   vertical, comilla simple, comilla doble y barra invertida literal
   (ver el diccionario _ESCAPES_SIMPLES más abajo). También se admite el
   escape de continuación de línea (barra invertida seguida de un salto
   de línea real dentro del literal), que no genera ningún carácter.
   Cualquier otra secuencia con barra invertida se conserva literalmente
   (no se considera error).

3. Máxima coincidencia (maximal munch) para operadores y delimitadores.
   Se listan todos los lexemas fijos de operadores/delimitadores y se
   ordenan por longitud descendente; en cada posición se elige el lexema
   más largo que calce. Esto resuelve automáticamente las superposiciones
   entre patrones, por ejemplo '=' / '==' / '=..' , '\\=' / '\\==',
   '=' / '=<', '>' / '>=', '-' / '-->', etc.

4. Recuperación ante errores léxicos.
   - Carácter no admitido: se descarta ese único carácter y se continúa.
   - Átomo entre comillas simples o cadena sin cierre: se avanza hasta el
     fin de línea (o fin de archivo) y se continúa el análisis desde la
     línea siguiente.
   - Número mal formado: se consume el fragmento problemático completo
     (p. ej. "1.2.3" o "1e+") y se continúa el análisis desde el
     carácter siguiente.
   - Comentario de bloque sin cierre: se reporta el error y se consume
     hasta el final del archivo, ya que un comentario de bloque no tiene
     un delimitador de recuperación razonable dentro de su propio texto.
"""

from .token_types import TipoToken, Token
from .errors import ErrorLexico
from .symbol_table import TablaDeSimbolos


# Operadores y delimitadores de lexema fijo, ordenados por longitud
# descendente para garantizar máxima coincidencia (maximal munch): en
# cada posición se prueba primero el lexema más largo.
_OPERADORES = [
    ("-->", TipoToken.OP_CLAUSULA),
    (":-", TipoToken.OP_CLAUSULA),
    ("?-", TipoToken.OP_CLAUSULA),

    ("=..", TipoToken.OP_RELACIONAL),
    ("\\==", TipoToken.OP_RELACIONAL),
    ("==", TipoToken.OP_RELACIONAL),
    ("\\=", TipoToken.OP_RELACIONAL),
    ("=<", TipoToken.OP_RELACIONAL),
    (">=", TipoToken.OP_RELACIONAL),
    ("=", TipoToken.OP_RELACIONAL),
    ("<", TipoToken.OP_RELACIONAL),
    (">", TipoToken.OP_RELACIONAL),

    ("**", TipoToken.OP_ARITMETICO),
    ("//", TipoToken.OP_ARITMETICO),
    ("+", TipoToken.OP_ARITMETICO),
    ("-", TipoToken.OP_ARITMETICO),
    ("*", TipoToken.OP_ARITMETICO),
    ("/", TipoToken.OP_ARITMETICO),

    ("\\+", TipoToken.OP_CONTROL),
    ("!", TipoToken.OP_CONTROL),
    (";", TipoToken.OP_CONTROL),

    (",", TipoToken.COMA),
    (".", TipoToken.PUNTO),
    ("(", TipoToken.PARENTESIS_IZQ),
    (")", TipoToken.PARENTESIS_DER),
    ("[", TipoToken.CORCHETE_IZQ),
    ("]", TipoToken.CORCHETE_DER),
    ("{", TipoToken.LLAVE_IZQ),
    ("}", TipoToken.LLAVE_DER),
    ("|", TipoToken.BARRA_VERTICAL),
]
_OPERADORES.sort(key=lambda par: len(par[0]), reverse=True)


_ESCAPES_SIMPLES = {
    "n": "\n", "t": "\t", "r": "\r", "a": "\a",
    "b": "\b", "f": "\f", "v": "\v",
    "\\": "\\", "'": "'", '"': '"',
}


def _es_inicio_atomo(c):
    return c.isalpha() and c.islower()


def _es_inicio_variable(c):
    return c == "_" or (c.isalpha() and c.isupper())


def _es_continuacion_id(c):
    return c.isalnum() or c == "_"


class AnalizadorLexico:
    """Analizador léxico de barrido único (una pasada) sobre el texto fuente."""

    def __init__(self, fuente):
        self.fuente = fuente
        self.n = len(fuente)
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []
        self.errores = []
        self.tabla = TablaDeSimbolos()

    # ---------------- utilidades básicas de recorrido ----------------

    def _fin(self, offset=0):
        return self.pos + offset >= self.n

    def _actual(self, offset=0):
        idx = self.pos + offset
        return self.fuente[idx] if idx < self.n else ""

    def _avanzar(self, cantidad=1):
        for _ in range(cantidad):
            if self.pos >= self.n:
                return
            if self.fuente[self.pos] == "\n":
                self.linea += 1
                self.columna = 1
            else:
                self.columna += 1
            self.pos += 1

    # ---------------------------- API pública ----------------------------

    def analizar(self):
        """
        Ejecuta el análisis léxico completo sobre self.fuente.
        Devuelve (tokens, errores, tabla_de_simbolos).
        """
        while True:
            self._saltar_espacios_y_comentarios()
            if self._fin():
                break

            c = self._actual()
            linea_ini, col_ini = self.linea, self.columna

            if c.isdigit():
                self._leer_numero(linea_ini, col_ini)
            elif c == "'":
                self._leer_atomo_comillas(linea_ini, col_ini)
            elif c == '"':
                self._leer_cadena(linea_ini, col_ini)
            elif _es_inicio_variable(c):
                self._leer_variable(linea_ini, col_ini)
            elif _es_inicio_atomo(c):
                self._leer_atomo(linea_ini, col_ini)
            else:
                self._leer_operador_o_error(linea_ini, col_ini)

        self.tokens.append(Token(TipoToken.EOF, "", self.linea, self.columna))
        return self.tokens, self.errores, self.tabla

    # ----------------------- espacios y comentarios -----------------------

    def _saltar_espacios_y_comentarios(self):
        cambio = True
        while cambio:
            cambio = False

            while not self._fin() and self._actual() in " \t\r\n":
                self._avanzar()
                cambio = True

            if not self._fin() and self._actual() == "%":
                while not self._fin() and self._actual() != "\n":
                    self._avanzar()
                cambio = True

            elif not self._fin() and self._actual() == "/" and self._actual(1) == "*":
                linea_ini, col_ini = self.linea, self.columna
                self._avanzar(2)
                cerrado = False
                while not self._fin():
                    if self._actual() == "*" and self._actual(1) == "/":
                        self._avanzar(2)
                        cerrado = True
                        break
                    self._avanzar()
                if not cerrado:
                    self.errores.append(ErrorLexico(
                        "comentario de bloque sin cierre",
                        "/*...(sin cierre '*/', se consume hasta EOF)",
                        linea_ini, col_ini,
                    ))
                cambio = True

    # ------------------------------ números ------------------------------

    def _leer_numero(self, linea_ini, col_ini):
        inicio = self.pos

        while not self._fin() and self._actual().isdigit():
            self._avanzar()

        es_real = False

        # Parte decimal: solo si el punto va seguido de un dígito, para no
        # confundirlo con el punto final de cláusula (p. ej. "3." -> ENTERO
        # '3' seguido de PUNTO '.').
        if self._actual() == "." and self._actual(1).isdigit():
            es_real = True
            self._avanzar()  # '.'
            while not self._fin() and self._actual().isdigit():
                self._avanzar()

        # Parte exponencial opcional.
        if self._actual() in ("e", "E"):
            self._avanzar()  # 'e' / 'E'
            if self._actual() in ("+", "-"):
                self._avanzar()
            n_digitos = 0
            while not self._fin() and self._actual().isdigit():
                self._avanzar()
                n_digitos += 1
            if n_digitos == 0:
                lexema = self.fuente[inicio:self.pos]
                self.errores.append(ErrorLexico(
                    "número mal formado (exponente sin dígitos)",
                    lexema, linea_ini, col_ini,
                ))
                return
            es_real = True

        # Punto decimal adicional -> número mal formado ("1.2.3").
        if self._actual() == "." and self._actual(1).isdigit():
            self._avanzar()
            while not self._fin() and self._actual().isdigit():
                self._avanzar()
            lexema = self.fuente[inicio:self.pos]
            self.errores.append(ErrorLexico(
                "número mal formado (demasiados puntos decimales)",
                lexema, linea_ini, col_ini,
            ))
            return

        lexema = self.fuente[inicio:self.pos]
        if es_real:
            indice = self.tabla.registrar("real", lexema)
            self.tokens.append(Token(
                TipoToken.REAL, lexema, linea_ini, col_ini,
                valor=float(lexema), indice_tabla=indice,
            ))
        else:
            indice = self.tabla.registrar("entero", lexema)
            self.tokens.append(Token(
                TipoToken.ENTERO, lexema, linea_ini, col_ini,
                valor=int(lexema), indice_tabla=indice,
            ))

    # -------------------------- identificadores --------------------------

    def _leer_variable(self, linea_ini, col_ini):
        inicio = self.pos
        self._avanzar()
        while not self._fin() and _es_continuacion_id(self._actual()):
            self._avanzar()
        lexema = self.fuente[inicio:self.pos]

        if lexema == "_":
            indice = None  # variable anónima: no se registra en la tabla
        else:
            indice = self.tabla.registrar("variable", lexema)

        self.tokens.append(Token(
            TipoToken.VARIABLE, lexema, linea_ini, col_ini, indice_tabla=indice,
        ))

    def _leer_atomo(self, linea_ini, col_ini):
        inicio = self.pos
        self._avanzar()
        while not self._fin() and _es_continuacion_id(self._actual()):
            self._avanzar()
        lexema = self.fuente[inicio:self.pos]
        indice = self.tabla.registrar("atomo", lexema)
        self.tokens.append(Token(
            TipoToken.ATOMO, lexema, linea_ini, col_ini,
            valor=lexema, indice_tabla=indice,
        ))

    # ----------------------- literales entre comillas -----------------------

    def _leer_secuencia_entrecomillada(self, delimitador):
        """
        Asume que self.pos está posicionado en el delimitador de apertura.
        Consume hasta el delimitador de cierre (no escapado), procesando
        las secuencias de escape y la comilla doblada.

        Devuelve (valor_decodificado, cerrado_correctamente).
        Si se alcanza un salto de línea o el fin de archivo antes de
        encontrar el cierre, se detiene y reporta que no cerró.
        """
        self._avanzar()  # delimitador de apertura
        partes = []
        while True:
            if self._fin() or self._actual() == "\n":
                return "".join(partes), False

            c = self._actual()

            if c == delimitador:
                if self._actual(1) == delimitador:
                    # Delimitador doblado -> carácter literal.
                    partes.append(delimitador)
                    self._avanzar(2)
                    continue
                self._avanzar()  # delimitador de cierre
                return "".join(partes), True

            if c == "\\":
                siguiente = self._actual(1)
                if siguiente == "\n":
                    self._avanzar(2)  # continuación de línea: no agrega nada
                    continue
                if siguiente in _ESCAPES_SIMPLES:
                    partes.append(_ESCAPES_SIMPLES[siguiente])
                    self._avanzar(2)
                    continue
                # Secuencia de escape desconocida: se conserva literalmente.
                partes.append(c)
                self._avanzar()
                continue

            partes.append(c)
            self._avanzar()

    def _leer_atomo_comillas(self, linea_ini, col_ini):
        inicio = self.pos
        valor, cerrado = self._leer_secuencia_entrecomillada("'")
        lexema = self.fuente[inicio:self.pos]

        if not cerrado:
            self.errores.append(ErrorLexico(
                "átomo entre comillas simples sin cierre",
                lexema, linea_ini, col_ini,
            ))
            return

        indice = self.tabla.registrar("atomo", valor)
        self.tokens.append(Token(
            TipoToken.ATOMO_COMILLAS, lexema, linea_ini, col_ini,
            valor=valor, indice_tabla=indice,
        ))

    def _leer_cadena(self, linea_ini, col_ini):
        inicio = self.pos
        valor, cerrado = self._leer_secuencia_entrecomillada('"')
        lexema = self.fuente[inicio:self.pos]

        if not cerrado:
            self.errores.append(ErrorLexico(
                "cadena sin cierre",
                lexema, linea_ini, col_ini,
            ))
            return

        indice = self.tabla.registrar("cadena", valor)
        self.tokens.append(Token(
            TipoToken.CADENA, lexema, linea_ini, col_ini,
            valor=valor, indice_tabla=indice,
        ))

    # ----------------- operadores, delimitadores y errores -----------------

    def _leer_operador_o_error(self, linea_ini, col_ini):
        for lexema, tipo in _OPERADORES:
            largo = len(lexema)
            if self.fuente[self.pos:self.pos + largo] == lexema:
                self._avanzar(largo)
                self.tokens.append(Token(tipo, lexema, linea_ini, col_ini))
                return

        # Ningún operador/delimitador válido calzó: carácter no admitido.
        c = self._actual()
        self.errores.append(ErrorLexico(
            "carácter no admitido",
            c, linea_ini, col_ini,
        ))
        self._avanzar()
