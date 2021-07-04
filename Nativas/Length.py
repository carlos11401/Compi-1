from Abstract.NodoAST import NodoAST
from TS.Exception import Excepcion
from Instrucciones.Funcion import Funcion
from TS.Tipo import TIPO


class Length(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.nombre = nombre.lower()
        self.columna = columna
        self.fila = fila
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla("$length_param")
        if simbolo is None :
            return Excepcion("Semantico", "Parametro no encontrado en funcion Length", self.fila, self.columna)
        if simbolo.getTipo() != TIPO.CADENA and not simbolo.getIsArray():
            return Exception("Semantico", "Parametro en funcion Length deberia ser de tipo CADENA.",self.fila,self.columna)
        self.tipo = simbolo.getTipo()
        return len(simbolo.getValor())

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
