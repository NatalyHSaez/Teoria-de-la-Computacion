% Sistema de citas medicas
paciente(juan, 25).
paciente(ana, 30).

medico(carlos, cardiologia).
medico(luisa, dermatologia).

/* Regla: edad de un paciente */
tiene_edad(Paciente, Edad) :-
    paciente(Paciente, Edad).

mensaje("cita confirmada").

?- tiene_edad(juan, Quien).