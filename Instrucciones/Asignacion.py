from Abstract.NodoAST import NodoAST
from TS.Exception import Excepcion
from Abstract.instruccion import Instruccion
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO


class Asignacion(Instruccion):
    def __init__(self, identificador, expresion, fila, columna):
        self.identificador = identificador
        self.expresion = expresion
        self.fila = fila
        self.columna = columna
        self.isArray = False

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table) # Valor a asignar a la variable
        if isinstance(value, Excepcion): return value
        # traer de la tabla el tipo de valor que tiene id
        id = table.getTabla(self.identificador)
        if id is None:
            return Excepcion("Semantico", "Variable \'"+self.identificador+"\' no encontrado.", self.fila, self.columna)
        if self.expresion.tipo == TIPO.NULO:
            simbolo = Simbolo(self.identificador, TIPO.NULO, False,self.fila, self.columna, "null")
            result = table.actualizarTabla(simbolo)
        elif id.tipo == TIPO.NULO or id.tipo == self.expresion.tipo:
            simbolo = Simbolo(self.identificador, self.expresion.tipo, False, self.fila, self.columna, value)
            result = table.actualizarTabla(simbolo)
        elif id.tipo != self.expresion.tipo:
            return Excepcion("Semantico", "Tipo de dato diferente en Declaracion", self.fila, self.columna)
        if isinstance(result, Excepcion): return result
        return None

    def getNode(self):
        node = NodoAST("ASIGNACION")
        node.addChild(str(self.identificador))
        node.addNodeChild((self.expresion.getNode()))
        return node
