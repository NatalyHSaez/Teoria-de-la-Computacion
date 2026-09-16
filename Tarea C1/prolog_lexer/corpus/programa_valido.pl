% ============================================================
% Programa Prolog de ejemplo: base de conocimiento familiar.
% No contiene errores léxicos. Cubre todas las categorías del
% subconjunto definido en el enunciado.
% ============================================================

% --- Hechos: átomos, delimitadores, punto final de cláusula ---
padre(juan, ana).
padre(juan, pedro).
padre(pedro, luis).
madre('Maria Jose', ana).
persona_1(juan).

/* Bloque de comentario
   de varias líneas, se ignora por completo. */

% --- Regla con variables y operador de cláusula :- ---
abuelo(X, Z) :-
    padre(X, Y),
    padre(Y, Z).

% --- Operadores aritméticos (is, mod, +, -, *, /, //, **) ---
promedio(A, B, Prom) :- Prom is (A + B) / 2.
resto(A, B, R) :- R is A mod B.
producto(A, B, P) :- P is A * B.
potencia(Base, Exp, R) :- R is Base ** Exp.
division_entera(A, B, R) :- R is A // B.

% --- Operadores relacionales (=, \=, ==, \==, =.., <, =<, >, >=) ---
iguales(X, Y) :- X == Y.
distintos(X, Y) :- X \== Y.
unifica(X, Y) :- X = Y.
no_unifica(X, Y) :- X \= Y.
menor(X, Y) :- X < Y.
menor_o_igual(X, Y) :- X =< Y.
mayor(X, Y) :- X > Y.
mayor_o_igual(X, Y) :- X >= Y.
descompone(T, F, A) :- T =.. [F | A].

% --- Operadores de control: !, \+, ; y coma ---
primero_o_segundo(X) :- padre(X, _) ; madre(X, _).
no_es_padre(X) :- \+ padre(X, _).
corte_ejemplo(X) :- padre(X, _), !.

% --- Números enteros y reales (el signo NUNCA forma parte del lexema) ---
constante_entera(42).
constante_real(3.14).
constante_real_exp(6.022e23).
constante_negativa(R) :- R = -7.
temperatura(-3.5).

% --- Cadenas con secuencias de escape documentadas ---
saludo("Hola \"mundo\"\n").
ruta("C:\\datos\\archivo.txt").

% --- Átomo entrecomillado que representa un operador ---
nombre_operador(':-').

% --- Listas, barra vertical, llaves y variable anónima ---
lista_ejemplo([1, 2, 3 | Resto]).
descarta(_, X, X).
termino_con_llaves(curly({X})).

% --- Regla DCG (operador opcional -->) ---
saludo_dcg --> [hola], [mundo].

% --- Consulta (operador ?-) ---
?- abuelo(juan, Quien).
