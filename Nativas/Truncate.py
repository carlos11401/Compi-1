import math

from Abstract.NodoAST import NodoAST
from TS.Exception import Excepcion
from Instrucciones.Funcion import Funcion
from TS.Tipo import TIPO


class Truncate(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.nombre = nombre.lower()
        self.columna = columna
        self.fila = fila
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla("$truncate_param")
        if simbolo is None :
            return Excepcion("Semantico", "Parametro no encontrado en funcion Truncate", self.fila, self.columna)
        if not(simbolo.getTipo() != TIPO.ENTERO or simbolo.getTipo() != TIPO.DECIMAL):
            return Exception("Semantico", "Parametro en funcion Truncate deberia ser de tipo entero o decimal.",self.fila,self.columna)

        self.tipo = TIPO.ENTERO
        return math.floor(simbolo.getValor())

    def getNode(self):
        node = NodoAST("FUNCION")
        node.addChild(str(self.nombre))
        parametros = NodoAST("PARAMETROs")
        for param in self.parametros:
            parametro = NodoAST("PARAMETRO")
            parametro.addChild(param["tipo"])
            parametro.addChild(param["identificador"])
            parametros.addNodeChild(parametro)
        node.addNodeChild(parametros)
        return node
