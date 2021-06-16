from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break

class For(Instruccion):
    def __init__(self, init, condicion, actualizacion, instrucciones, fila, columna):
        self.init = init
        self.condicion = condicion
        self.actualizacion = actualizacion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        newTable = TablaSimbolos(table)
        var = self.init.interpretar(tree, newTable)
        if isinstance(var, Excepcion): return var
        while True:
            condicion = self.condicion.interpretar(tree, newTable)
            if isinstance(condicion, Excepcion): return condicion
            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion):   # VERIFICA SI ES VERDADERA LA CONDICION
                    newTableInstr = TablaSimbolos(newTable)       # NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, newTableInstr)  # ejecutar instrucciones dentro de WHILE
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en While.", self.fila, self.columna)
            actualizacion = self.actualizacion.interpretar(tree, newTableInstr)
            if isinstance(actualizacion, Excepcion): return actualizacion
