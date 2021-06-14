from TS.Tipo import TIPO
from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo


class Declaracion(Instruccion):
    def __init__(self, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        if self.expresion != None:
            value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
            if isinstance(value, Excepcion): return value
            simbolo = Simbolo(str(self.identificador), self.expresion.tipo, self.fila, self.columna, value)
            
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
        else:
            simbolo = Simbolo(str(self.identificador), TIPO.NULO, self.fila, self.columna, None)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
        return None

