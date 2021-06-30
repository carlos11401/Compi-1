from TS.Exception import Excepcion
from Instrucciones.Funcion import Funcion
from TS.Tipo import TIPO


class TypeOf(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.nombre = nombre.lower()
        self.columna = columna
        self.fila = fila
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla("$typeof_param")
        if simbolo is None :
            return Excepcion("Semantico", "Parametro no encontrado en funcion Length", self.fila, self.columna)
        self.tipo = simbolo.getTipo()
        tipo = ""
        if self.tipo is not None:
            if self.tipo.name == "ENTERO": tipo = "INT"
            elif self.tipo.name == "DECIMAL": tipo = "DOUBLE"
            elif self.tipo.name == "BOOLEANO": tipo = "BOOLEAN"
            elif self.tipo.name == "CHARACTER": tipo = "CHAR"
            elif self.tipo.name == "CADENA": tipo = "STRING"
            elif self.tipo.name == "NULO": tipo = "NULL"
            elif self.tipo.name == "ARREGLO": tipo = "ARREGLO"
            return tipo
        else:
            tipo = "NULL"
            return tipo
