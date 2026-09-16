from .tokens import Token, TokenType, LexicalError
""" Lexer para analizar el texto de entrada"""
MULTI_OPERADORES ={
    "\\":("\\==","\\=","\\+"),
    ":":(":-",),
    "?":("?-",),
    "=":("=..","==","=<"),
    ">":  (">=",),
    "*":  ("**",),
    "/":  ("//",),
}
'''lista de caracteres que son operadores'''
OPERADORES_UNO = "=<>*/+\\!;:?"
'''diccionario de delimitadores y su tipo de token'''
DELIMITADORES = {"(": TokenType.PARENTESIS_IZQ, 
")": TokenType.PARENTESIS_DER, 
"[": TokenType.CORCHETE_IZQ, 
"]": TokenType.CORCHETE_DER,
"{": TokenType.LLAVE_IZQ,
"}": TokenType.LLAVE_DER, 
"|": TokenType.BARRA,
".": TokenType.PUNTO, 
",": TokenType.COMA
}

'''tipos de tokens que se guardan en la tabla de lexemas'''
TIPOS_EN_TABLA = { TokenType.ATOMO, 
                  TokenType.ATOMO_QUOTADO,
                    TokenType.VARIABLE,
                      TokenType.VARIABLE_ANON, 
                  TokenType.NUMERO,
                        TokenType.CADENA }
'''tipos de tokens que se consideran como operandos'''
ULTIMO_ES_OPERANDO= (TokenType.NUMERO, 
                    TokenType.ATOMO, 
                    TokenType.ATOMO_QUOTADO,
                    TokenType.VARIABLE,
                    TokenType.VARIABLE_ANON, 
                    TokenType.CADENA, 
                    TokenType.PARENTESIS_DER, 
                    TokenType.CORCHETE_DER, 
                    TokenType.LLAVE_DER)
''' Clase Lexer para analizar el texto de entrada y generar tokens y errores léxicos'''
class Lexer:
    def __init__(self, texto, tabla, signed_numbers=True):
        self.texto = texto
        self.longitud = len(texto)
        self.pos = 0
        self.linea = 1
        self.columna = 1
        self.tabla = tabla
        self.signed_numbers = signed_numbers
        self.tokens = []
        self.errores = []
        self.ultimo_token = None

    def _peek(self, k=0):
        p = self.pos + k
        return self.texto[p] if p < self.longitud else ""

    def _avanzar(self, n=1):
        for _ in range(n):
            if self.pos < self.longitud:
                if self.texto[self.pos] == "\n":
                    self.linea += 1
                    self.columna = 1
                else:
                    self.columna += 1
                self.pos += 1

    def _emitir(self, tipo, lexema, linea, columna):
        indice = self.tabla.insertar(lexema) if tipo in TIPOS_EN_TABLA else -1
        tok = Token(tipo, lexema, linea, columna, indice)
        self.tokens.append(tok)
        self.ultimo_token = tok

    def _error(self, mensaje, linea, columna, fragmento, recuperacion):
        self.errores.append(LexicalError(mensaje, linea, columna, fragmento, recuperacion))

    def _saltar_espacios_y_comentarios(self):
        while self.pos < self.longitud:
            c = self.texto[self.pos]
            if c in " \t\r\n":
                self._avanzar()
            elif c == "%":
                while self.pos < self.longitud and self.texto[self.pos] != "\n":
                    self._avanzar()
            elif c == "/" and self._peek(1) == "*":
                ini_l, ini_c, ini_p = self.linea, self.columna, self.pos
                self._avanzar(2)
                cerrado = False
                while self.pos < self.longitud:
                    if self.texto[self.pos] == "*" and self._peek(1) == "/":
                        self._avanzar(2)
                        cerrado = True
                        break
                    self._avanzar()
                if not cerrado:
                    self._error("Comentario de bloque sin cierre */", ini_l, ini_c,
                                self.texto[ini_p:self.pos], "Finalizar análisis en EOF")
                    return
            else:
                break

    def analizar(self):
        while self.pos < self.longitud:
            self._saltar_espacios_y_comentarios()
            if self.pos >= self.longitud:
                break
            linea, columna = self.linea, self.columna
            c = self.texto[self.pos]
            if c.islower():
                self._scan_atomo(linea, columna)
            elif c.isupper() or c == "_":
                self._scan_variable(linea, columna)
            elif c.isdigit():
                self._scan_numero(linea, columna)
            elif c == "'":
                self._scan_citado(linea, columna, "'", TokenType.ATOMO_QUOTADO, "'")
            elif c == '"':
                self._scan_citado(linea, columna, '"', TokenType.CADENA, '"')
            elif c in "+-":
                self._scan_signo(linea, columna)
            else:
                self._scan_operador_delimitador(linea, columna)
        self._emitir(TokenType.EOF, "", self.linea, self.columna)
        return self.tokens, self.errores

    def _scan_atomo(self, linea, columna):
        inicio = self.pos
        while self.pos < self.longitud:
            c = self.texto[self.pos]
            if c.isalnum() or c == "_":
                self._avanzar()
            else:
                break
        self._emitir(TokenType.ATOMO, self.texto[inicio:self.pos], linea, columna)

    def _scan_variable(self, linea, columna):
        inicio = self.pos
        while self.pos < self.longitud:
            c = self.texto[self.pos]
            if c.isalnum() or c == "_":
                self._avanzar()
            else:
                break
        lexema = self.texto[inicio:self.pos]
        tipo = TokenType.VARIABLE_ANON if lexema == "_" else TokenType.VARIABLE
        self._emitir(tipo, lexema, linea, columna)

    def _scan_numero(self, linea, columna, inicio=None):
        if inicio is None:
            inicio = self.pos
        while self._peek().isdigit():
            self._avanzar()
        if self._peek() == "." and self._peek(1).isdigit():
            self._avanzar()
            while self._peek().isdigit():
                self._avanzar()
            if self._peek() == ".":
                self._avanzar()
                self._error("Numero mal formado", linea, columna,
                            self.texto[inicio:self.pos], "Consumir y continuar")
                return
        elif self._peek().isalpha() or self._peek() == "_":
            while self.pos < self.longitud and (self.texto[self.pos].isalnum()
                                                or self.texto[self.pos] == "_"):
                self._avanzar()
            self._error("Numero mal formado (digitos mezclados con letras)", linea, columna,
                        self.texto[inicio:self.pos], "Consumir el fragmento y continuar")
            return
        self._emitir(TokenType.NUMERO, self.texto[inicio:self.pos], linea, columna)

    def _scan_signo(self, linea, columna):
        if self.texto[self.pos:self.pos + 3] == "-->":
            self._avanzar(3)
            self._emitir(TokenType.OPERADOR, "-->", linea, columna)
            return
        c = self.texto[self.pos]
        if self.signed_numbers and self._peek(1).isdigit() and not self._ultimo_es_operando():
            inicio = self.pos
            self._avanzar()
            self._scan_numero(linea, columna, inicio)
        else:
            self._avanzar()
            self._emitir(TokenType.OPERADOR, c, linea, columna)

    def _ultimo_es_operando(self):
        tok = self.ultimo_token
        return tok is not None and tok.tipo in ULTIMO_ES_OPERANDO

    def _scan_citado(self, linea, columna, delim, tipo, escape_delim):
        inicio = self.pos
        self._avanzar()
        while self.pos < self.longitud:
            c = self.texto[self.pos]
            if c == "\\":
                nxt = self._peek(1)
                if nxt == "n" or nxt == "t" or nxt == "\\" or nxt == escape_delim:
                    self._avanzar(2)
                else:
                    self._avanzar()
                continue
            if c == delim:
                self._avanzar()
                self._emitir(tipo, self.texto[inicio:self.pos], linea, columna)
                return
            if c == "\n":
                break
            self._avanzar()
        self._error("Atomo/cadena sin cierre", linea, columna,
                    self.texto[inicio:self.pos], "Descartar y continuar hasta fin de linea")
        while self.pos < self.longitud and self.texto[self.pos] != "\n":
            self._avanzar()

    def _scan_operador_delimitador(self, linea, columna):
        c = self.texto[self.pos]
        if c in DELIMITADORES:
            self._avanzar()
            self._emitir(DELIMITADORES[c], c, linea, columna)
            return
        for op in MULTI_OPERADORES.get(c, ()):
            if self.texto[self.pos:self.pos + len(op)] == op:
                self._avanzar(len(op))
                self._emitir(TokenType.OPERADOR, op, linea, columna)
                return
        if c in OPERADORES_UNO:
            self._avanzar()
            self._emitir(TokenType.OPERADOR, c, linea, columna)
            return
        self._avanzar()
        self._error(f"Caracter no admitido {c!r}", linea, columna, c,
                    "Consumir el caracter y continuar")