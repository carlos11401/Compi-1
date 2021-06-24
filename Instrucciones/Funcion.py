from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Funcion(Instruccion):
    def __init__(self, nombre, parametros, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.parametros = parametros
        self.nombre = nombre.lower()
        self.columna = columna
        self.fila = fila
        self.tipo = None

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)
        for instruccion in self.instrucciones:  # REALIZAR LAS ACCIONES
            value = instruccion.interpretar(tree, nuevaTabla)
            if isinstance(value, Excepcion):
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break):
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())
        return None
