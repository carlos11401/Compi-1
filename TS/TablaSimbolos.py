from TS.Exception import Excepcion
from TS.Tipo import TIPO

class TablaSimbolos:
    def __init__(self, anterior=None):
        self.tabla = {}  # Diccionario Vacio
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):  # Agregar una variable
        if simbolo.id.lower() in self.tabla:
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None

    def getTabla(self, id):  # obtener una variable
        tablaActual = self
        while tablaActual is not None:
            if id.lower() in tablaActual.tabla:
                return tablaActual.tabla[id.lower()]
            else:
                tablaActual = tablaActual.anterior
                if tablaActual is None:
                    return None
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual is not None:
            if simbolo.id.lower() in tablaActual.tabla:
                tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                return None
            else:
                tablaActual = tablaActual.anterior
        return Excepcion("Semantico", "Variable No encontrada en Asignacion", simbolo.getFila(), simbolo.getColumna())
