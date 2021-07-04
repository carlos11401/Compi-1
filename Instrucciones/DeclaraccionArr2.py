from Abstract.NodoAST import NodoAST
from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo
import gramatica as Grammar


class DeclaracionArr2(Instruccion):
    def __init__(self, tipo, dimensiones, id, lista, fila, columna):
        self.list = lista
        self.identificador = id
        self.tipo = tipo
        self.dimensions = dimensiones
        self.isArray = True
        self.fila = fila
        self.columna = columna
        self.isArray = True

    def interpretar(self, tree, table):
        listDimensions = self.getDimensions(self.list)
        if len(listDimensions) != self.dimensions:
            return Excepcion("Semantico", "Tamaño de arreglo diferente en asignacion.", self.fila, self.columna)
        array = self.setValues(tree, table, self.list)
        simbolo = Simbolo(str(self.identificador), self.tipo, self.isArray, self.fila, self.columna, array)
        Grammar.infTS[self.identificador.lower() + str(table)][2] = simbolo.getValor()
        Grammar.infTS[self.identificador.lower() + str(table)][3] = simbolo.getTipo()
        Grammar.infTS[self.identificador.lower() + str(table)][4] = simbolo.getIsArray()
        result = table.setTabla(simbolo)
        if isinstance(result, Excepcion): return result
        return None

    def getNode(self):
        node = NodoAST("DECLARACION ARREGLO")
        node.addChild(str(self.tipo))
        node.addChild(str(self.dimensions))
        node.addChild(str(self.identificador))
        return node

    def getDimensions(self, array):
        dim = [len(array)]
        if not isinstance(array[0], list):
            return dim
        else:
            return dim + self.getDimensions(array[0])

    def setValues(self, tree, table, array):
        for i in range(0, len(array)):
            if isinstance(array[i], list):
                array[i] = self.setValues(tree, table, array[i])
            else:
                array[i] = array[i].interpretar(tree, table)
        return array


