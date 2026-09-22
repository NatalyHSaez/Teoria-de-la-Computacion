from src.tokens import TokenType


def test_atomo(analizar):
    tokens, errores = analizar("padre(juan, ana).")
    assert errores == []
    tipos = [(t.tipo, t.lexema) for t in tokens]
    assert tipos[0] == (TokenType.ATOMO, "padre")
    assert tipos[1] == (TokenType.PARENTESIS_IZQ, "(")
    assert tipos[2] == (TokenType.ATOMO, "juan")
    assert tipos[3] == (TokenType.COMA, ",")
    assert tipos[4] == (TokenType.ATOMO, "ana")
    assert tipos[5] == (TokenType.PARENTESIS_DER, ")")
    assert tipos[6] == (TokenType.PUNTO, ".")


def test_atomo_quotado(analizar):
    tokens, errores = analizar("persona('Juan Perez').")
    assert errores == []
    assert (tokens[2].tipo, tokens[2].lexema) == (TokenType.ATOMO_QUOTADO, "'Juan Perez'")

def test_variable(analizar):
    tokens, errores = analizar("cliente(Nombre, Edad).")
    assert errores == []
    assert (tokens[2].tipo, tokens[2].lexema) == (TokenType.VARIABLE, "Nombre")


def test_variable_anonima(analizar):
    tokens, errores = analizar("hecho(_, dato).")
    assert errores == []
    assert tokens[2].tipo == TokenType.VARIABLE_ANON
    assert tokens[2].lexema == "_"


def test_numero_entero(analizar):
    tokens, errores = analizar("edad(juan, 25).")
    assert errores == []
    assert (tokens[4].tipo, tokens[4].lexema) == (TokenType.NUMERO, "25")


def test_numero_real(analizar):
    tokens, errores = analizar("pi(3.14).")
    assert errores == []
    assert (tokens[2].tipo, tokens[2].lexema) == (TokenType.NUMERO, "3.14")


def test_cadena(analizar):
    tokens, errores = analizar('saludo("hola mundo").')
    assert errores == []
    assert (tokens[2].tipo, tokens[2].lexema) == (TokenType.CADENA, '"hola mundo"')


def test_operadores_clausula(analizar):
    tokens, errores = analizar("a :- b. ?- c. d --> e.")
    assert errores == []
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == [":-", "?-", "-->"]


def test_operadores_unificacion(analizar):
    tokens, errores = analizar("p(A = B, A == B, A \\= B, A \\== B, A =.. B).")
    assert errores == []
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["=", "==", "\\=", "\\==", "=.."]


def test_operadores_comparacion(analizar):
    tokens, errores = analizar("p(<, =<, >, >=).")
    assert errores == []
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["<", "=<", ">", ">="]


def test_operadores_aritmeticos(analizar):
    tokens, errores = analizar("p(+, -, *, /, //, **).")
    assert errores == []
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["+", "-", "*", "/", "//", "**"]


def test_atomos_operadores_is_y_mod(analizar):
    tokens, errores = analizar("p(X is 1, Y mod 2).")
    assert errores == []
    lexemas = [t.lexema for t in tokens]
    assert "is" in lexemas and "mod" in lexemas


def test_operadores_control(analizar):
    tokens, errores = analizar("p(\\+, !, ;).")
    assert errores == []
    ops = [t.lexema for t in tokens if t.tipo == TokenType.OPERADOR]
    assert ops == ["\\+", "!", ";"]


def test_delimitadores(analizar):
    tokens, errores = analizar("p([], {}, |).")
    assert errores == []
    tipos = [t.tipo for t in tokens]
    assert TokenType.CORCHETE_IZQ in tipos
    assert TokenType.CORCHETE_DER in tipos
    assert TokenType.LLAVE_IZQ in tipos
    assert TokenType.LLAVE_DER in tipos
    assert TokenType.BARRA in tipos


def test_comentarios_ignorados(analizar):
    tokens, errores = analizar("% linea\nx(1). /* bloque */ y(2).")
    assert errores == []
    lexemas = [t.lexema for t in tokens]
    assert lexemas == ["x", "(", "1", ")", ".", "y", "(", "2", ")", "."]


def test_linea_y_columna(analizar):
    tokens, errores = analizar("padre(juan, ana).")
    assert errores == []
    assert (tokens[0].linea, tokens[0].columna) == (1, 1)
    assert (tokens[1].linea, tokens[1].columna) == (1, 6)
    assert (tokens[4].columna) == 13