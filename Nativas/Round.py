import math

from TS.Exception import Excepcion
from Instrucciones.Funcion import Funcion
from TS.Tipo import TIPO


class Round(Funcion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.nombre = nombre.lower()
        self.columna = columna
        self.fila = fila
        self.tipo = None

    def interpretar(self, tree, table):
        simbolo = table.getTabla("$round_param")
        if simbolo is None :
            return Excepcion("Semantico", "Parametro no encontrado en funcion Round", self.fila, self.columna)
        if not(simbolo.getTipo() != TIPO.ENTERO or simbolo.getTipo() != TIPO.DECIMAL):
            return Exception("Semantico", "Parametro en funcion Round deberia ser de tipo entero o decimal.",self.fila,self.columna)

        self.tipo = TIPO.ENTERO
        return round(simbolo.getValor())
