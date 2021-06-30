from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion
from TS.Tipo import TIPO, OperadorLogico


class Casteo(Instruccion):
    def __init__(self, tipo, expresion, fila, columna):
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        val = self.expresion.interpretar(tree, table)
        if self.tipo == TIPO.DECIMAL:
            if self.expresion.tipo == TIPO.ENTERO:
                try:
                    return float(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para Float.", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CHARACTER:
                try:
                    return float(ord(self.obtenerVal(self.expresion.tipo, val)))
                except:
                    return Exception("Semantico", "No se puede castear para Float.", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CADENA:
                try:
                    return float(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para Float.", self.fila, self.columna)
        elif self.tipo == TIPO.ENTERO:
            if self.expresion.tipo == TIPO.DECIMAL:
                try:
                    return int(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para Int.", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CHARACTER:
                try:
                    return ord(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para Int.", self.fila, self.columna)
            elif self.expresion.tipo == TIPO.CADENA:
                try:
                    return int(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para Int.", self.fila, self.columna)
        elif self.tipo == TIPO.CADENA:
            if self.expresion.tipo == TIPO.ENTERO:
                try:
                    return str(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para String.", self.fila, self.columna)
            if self.expresion.tipo == TIPO.DECIMAL:
                try:
                    return str(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para String.", self.fila, self.columna)
        elif self.tipo == TIPO.CHARACTER:
            if self.expresion.tipo == TIPO.ENTERO:
                try:
                    return chr(self.obtenerVal(self.expresion.tipo, val))
                except:
                    return Exception("Semantico", "No se puede castear para Char.", self.fila, self.columna)
        elif self.tipo == TIPO.BOOLEANO:
            if self.expresion.tipo == TIPO.CADENA:
                if val.lower() == "true":
                    return True
                elif val.lower() == "false":
                    return False
                return Exception("Semantico", "No se puede castear para Bool.", self.fila, self.columna)
        return Exception("Semantico", "Tipo de casteo no permitido.", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)

    def getNode(self):
        node = NodoAST("CASTEO")
        node.addChild(str(self.tipo))
        node.addNodeChild(self.expresion.getNode())
        return node