"""Tipos de tokens y errores producidos por el analizador léxico."""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
	"""Clases de tokens reconocidas por el lexer."""
	ATOMO = auto()
	ATOMO_QUOTADO= auto()
	VARIABLE = auto()
	VARIABLE_ANON= auto()
	NUMERO = auto()
	CADENA = auto()
	OPERADOR = auto()
	PARENTESIS_IZQ = auto()
	PARENTESIS_DER = auto()
	CORCHETE_IZQ = auto()
	CORCHETE_DER = auto()
	LLAVE_IZQ = auto()
	LLAVE_DER = auto()
	BARRA= auto()
	PUNTO= auto()
	COMA= auto()
	EOF = auto()


@dataclass
class Token:
	"""Unidad léxica reconocida en el texto de entrada."""

	tipo: TokenType
	lexema: str
	linea: int
	columna: int 
	indice_tabla: int = -1
	def __str__(self) -> str:
		return f"<{self.tipo.name}, '{self.lexema}', {self.linea}, {self.columna}>"


@dataclass
class LexicalError(Exception):
	"""Error ocurrido mientras se analiza léxicamente la entrada."""

	mensaje: str
	linea: int 
	columna: int
	fragmento: str
	recuperacion: str 

	def __post_init__(self) -> None:
		super().__init__(self.__str__())

	def __str__(self) -> str:
		return f"{self.mensaje} (línea {self.linea}, columna {self.columna})"
