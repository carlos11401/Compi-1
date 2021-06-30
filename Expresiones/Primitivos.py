from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion

class Primitivos(Instruccion):
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        return self.valor

    def getNode(self):
        node = NodoAST("PRIMITIVO")
        node.addChild(str(self.valor))
        return node
