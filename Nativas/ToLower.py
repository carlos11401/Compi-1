from Abstract.NodoAST import NodoAST
from TS.Exception import Excepcion
from Instrucciones.Funcion import Funcion
from TS.Tipo import TIPO


class ToLower(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.nombre = nombre.lower()
        self.columna = columna
        self.fila = fila
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla("$toLower_param")
        if simbolo is None :
            return Excepcion("Semantico", "Parametro no encontrado en ToLower", self.fila, self.columna)
        if simbolo.getTipo() != TIPO.CADENA:
            return Exception("Semantico", "Parametro en ToUpper deberia ser de tipo CADENA.",self.fila,self.columna)

        self.tipo = simbolo.getTipo()
        return simbolo.getValor().lower()

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
