from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion

class Return(Instruccion):
    def __init__(self, expresion, fila, columna):
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.tipo = None
        self.result = None

    def interpretar(self, tree, table):
        result = self.expresion.interpretar(tree, table)
        if isinstance(result, Excepcion): return result

        self.tipo = self.expresion.tipo  # TIPO DEL RESULT
        self.result = result            # VALOR DEL RESULT

        return self

    def getNode(self):
        node = NodoAST("RETURN")
        node.addNodeChild(self.expresion.getNode())
        return node
