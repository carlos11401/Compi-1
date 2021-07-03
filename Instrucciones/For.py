from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from Instrucciones.Continue import Continue
from Instrucciones.Declaracion import Declaracion
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from TS.Exception import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Return import Return
from Instrucciones.Break import Break
import gramatica as Grammar

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
                        if isinstance(instruccion, Declaracion) or isinstance(instruccion, DeclaracionArr1):
                            Grammar.infTS[instruccion.identificador.lower() + str(newTableInstr)] = ["For",
                                                                                                  instruccion.identificador,
                                                                                                  None, None, None,
                                                                                                  instruccion.fila,
                                                                                                  instruccion.columna]
                        result = instruccion.interpretar(tree, newTableInstr)  # ejecutar instrucciones dentro de WHILE
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                else:
                    break
            else:
                return Excepcion("Semantico", "Tipo de dato no booleano en While.", self.fila, self.columna)
            actualizacion = self.actualizacion.interpretar(tree, newTableInstr)
            if isinstance(actualizacion, Excepcion): return actualizacion

    def getNode(self):
        node = NodoAST("FOR")
        instrucciones = NodoAST("INSTRUCCIONES FOR")
        for inst in self.instrucciones:
            instrucciones.addNodeChild(inst.getNode())
        node.addNodeChild(instrucciones)
        return node
