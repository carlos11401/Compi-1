from TS.Tipo import TIPO
from Abstract.NodoAST import NodoAST
from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo
import copy
import gramatica as Grammar

class DeclaracionArr1(Instruccion):

    def __init__(self, tipo1, dimensiones, identificador, tipo2, expresiones, fila, columna):
        self.identificador = identificador
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.dimensiones = dimensiones
        self.expresiones = expresiones
        self.fila = fila
        self.columna = columna
        self.isArray = True

    def interpretar(self, tree, table):
        if self.tipo1 != self.tipo2:  # VERIFICACION DE TIPOS
            return Excepcion("Semantico", "Tipo de dato diferente en Arreglo.", self.fila, self.columna)
        if self.dimensiones != len(self.expresiones):  # VERIFICACION DE DIMENSIONES
            return Excepcion("Semantico", "Dimensiones diferentes en Arreglo.", self.fila, self.columna)

        # CREACION DEL ARREGLO
        value = self.crearDimensiones(tree, table, copy.copy(self.expresiones))  # RETORNA EL ARREGLO DE DIMENSIONES
        if isinstance(value, Excepcion): return value

        simbolo = Simbolo(str(self.identificador), self.tipo1, self.isArray, self.fila, self.columna, value)
        result = table.setTabla(simbolo)
        Grammar.infTS[self.identificador.lower() + str(table)][2] = simbolo.getValor()
        Grammar.infTS[self.identificador.lower() + str(table)][3] = simbolo.getTipo()
        Grammar.infTS[self.identificador.lower() + str(table)][4] = simbolo.getIsArray()
        if isinstance(result, Excepcion): return result
        return None

    def getNode(self):
        nodo = NodoAST("DECLARACION ARREGLO")
        nodo.addChild(str(self.tipo1))
        nodo.addChild(str(self.dimensiones))
        nodo.addChild(str(self.identificador))
        nodo.addChild(str(self.tipo2))
        exp = NodoAST("EXPRESIONES DE LAS DIMENSIONES")
        for expresion in self.expresiones:
            exp.addNodeChild(expresion.getNodo())
        nodo.addNodeChild(exp)
        return nodo

    def crearDimensiones(self, tree, table, expresiones):
        arr = []
        if len(expresiones) == 0:
            return None
        dimension = expresiones.pop(0)
        num = dimension.interpretar(tree, table)
        if isinstance(num, Excepcion): return num
        if dimension.tipo != TIPO.ENTERO:
            return Excepcion("Semantico", "Expresion diferente a ENTERO en Arreglo.", self.fila, self.columna)
        contador = 0
        while contador < num:
            arr.append(self.crearDimensiones(tree, table, copy.copy(expresiones)))
            contador += 1
        return arr
