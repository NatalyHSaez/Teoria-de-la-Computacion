class TablaLexemas:
    """Tabla de símbolos para almacenar lexemas y sus atributos."""

    def __init__(self):
        self.tabla = {}
        self._siguiente = 0

    def insertar(self, lexema: str) -> int:
        """Agrega un lexema a la tabla si no existe y devuelve su índice."""
        if lexema not in self.tabla:
            self.tabla[lexema] = {"indice": self._siguiente,"veces":0}
            self._siguiente += 1
        self.tabla[lexema]["veces"] += 1
        return self.tabla[lexema]["indice"]

    def items(self):
        """Devuelve los elementos de la tabla."""
        return self.tabla.items()

    def __len__(self):
        return len(self.tabla)