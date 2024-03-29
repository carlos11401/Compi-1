from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion

class Break(Instruccion):
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self

    def getNode(self):
        node = NodoAST("BREAK")
        return node
