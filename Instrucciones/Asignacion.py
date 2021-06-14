from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO


class Asignacion(Instruccion):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value
        # traer de la tabla el tipo de valor que tiene id
        tipoVar = table.getTabla(self.identificador)
        if tipoVar.tipo == TIPO.NULO or tipoVar.tipo == self.expresion.tipo:
            simbolo = Simbolo(self.identificador, self.expresion.tipo, self.fila, self.columna, value)
            result = table.actualizarTabla(simbolo)
        elif tipoVar != self.expresion.tipo:
            return Excepcion("Semantico", "Tipo de dato diferente en Declaracion", self.fila, self.columna)
        if isinstance(result, Excepcion): return result
        return None

