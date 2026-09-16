% ============================================================
% Programa Prolog con múltiples errores léxicos recuperables.
% Cada error se reporta con su ubicación y el análisis continúa
% después de él, EXCEPTO el comentario de bloque sin cierre del
% final, que por definición consume el resto del archivo.
% ============================================================

hecho_valido(uno).

% Error 1: carácter no admitido (@)
dato_con_error(@raro).

hecho_valido(dos).

% Error 2: átomo entre comillas simples sin cierre
atomo_roto('sin cierre de comillas).

hecho_valido(tres).

% Error 3: cadena sin cierre
cadena_rota("sin cierre de cadena).

hecho_valido(cuatro).

% Error 4: número mal formado (dos puntos decimales)
numero_malo(1.2.3).

hecho_valido(cinco).

% Error 5: número mal formado (exponente sin dígitos)
numero_malo2(1e+).

hecho_valido(seis).

% Error 6: carácter no admitido (^)
otro_error(X) :- X ^ 2.

hecho_valido(siete).

% Errores 7 y 8: caracteres no admitidos adicionales
raro(~).
raro2(`).

hecho_valido(ocho).

% Error 9: comentario de bloque sin cierre (consume hasta EOF)
/* este comentario de bloque nunca se cierra
y por lo tanto todo lo que sigue queda dentro de él
hecho_perdido(nueve).
