from TS.Exception import Excepcion


class TablaSimbolos:
    def __init__(self, anterior=None):
        self.tabla = {}  # Diccionario Vacio
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):  # Agregar una variable
        if simbolo.id in self.tabla:
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id] = simbolo
            return None

    def getTabla(self, id):  # obtener una variable
        tablaActual = self
        while tablaActual.tabla != None:
            if id in tablaActual.tabla:
                return tablaActual.tabla[id]
            else:
                tablaActual = tablaActual.anterior
                if tablaActual is None:
                    return None
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual is not None:
            if simbolo.id in tablaActual.tabla:
                tablaActual.tabla[simbolo.id].setValor(simbolo.getValor())
                tablaActual.tabla[simbolo.id].setTipo(simbolo.getTipo())
                return "Variable Actualizada"
            else:
                tablaActual = tablaActual.anterior
                if tablaActual is None:
                    return None
        return None
