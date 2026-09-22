control(X) :-
    \+ \+ X,
    !,
    (X ; Y).