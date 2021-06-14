from TS.Tipo import TIPO
from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo


class Decremento(Instruccion):
    def __init__(self, identificador, fila, columna):
        self.identificador = identificador
        self.tipo = None
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        symbol = table.getTabla(self.identificador)
        if symbol != None:
            if symbol.tipo == TIPO.ENTERO or symbol.tipo == TIPO.DECIMAL:
                self.tipo = symbol.tipo
                updateSymbol = Simbolo(symbol.id,symbol.tipo,symbol.fila, symbol.columna,symbol.valor-1)
                table.actualizarTabla(updateSymbol)
            else:
                return Excepcion("Semantico", "Tipo de dato no se puede decrementar.", self.fila, self.columna)
        else:
            return Excepcion("Semantico", "Variable " + self.identificador + " no encontrada", self.fila, self.columna)
        return symbol.valor