from Abstract.NodoAST import NodoAST
from TS.Tipo import TIPO
from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo
import gramatica as Grammar

class Declaracion(Instruccion):
    def __init__(self, identificador, fila, columna, expresion=None):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.isArray = False

    def interpretar(self, tree, table):
        if self.expresion is not None:
            value = self.expresion.interpretar(tree, table)  # Valor a asignar a la variable
            if isinstance(value, Excepcion): return value
            simbolo = Simbolo(str(self.identificador), self.expresion.tipo, False, self.fila, self.columna, value)

            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
        else:
            simbolo = Simbolo(str(self.identificador), TIPO.NULO, False, self.fila, self.columna, None)
            result = table.setTabla(simbolo)
            if isinstance(result, Excepcion): return result
        Grammar.infTS[self.identificador.lower()+str(table)][2] = simbolo.getValor()
        Grammar.infTS[self.identificador.lower() + str(table)][3] = simbolo.getTipo()
        Grammar.infTS[self.identificador.lower() + str(table)][4] = simbolo.getIsArray()
        return None

    def getNode(self):
        node = NodoAST("DECLARACION")
        node.addChild(str(self.identificador))
        if self.expresion is not None:
            node.addNodeChild((self.expresion.getNode()))
        return node
