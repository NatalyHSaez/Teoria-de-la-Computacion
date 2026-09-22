sistema(paciente_1, 'Juan Perez').
atender(X, Y) :-
    X >= 18,
    Y is X * 2 / 100.0,
    notificar(Y, "valor aceptado").
?- atender(25, Z).