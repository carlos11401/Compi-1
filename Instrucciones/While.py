from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from Instrucciones.Continue import Continue
from TS.Exception import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Return import Return
from Instrucciones.Break import Break

class While(Instruccion):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion
            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion):   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       # NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla)  # ejecutar instrucciones dentro de WHILE
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

    def getNode(self):
        node = NodoAST("WHILE")
        node.addNodeChild(self.condicion.getNode())
        instrucciones = NodoAST("INSTRUCCIONES WHILE")

        for inst in self.instrucciones:
            instrucciones.addNodeChild(inst.getNode())
        node.addNodeChild(instrucciones)
        return node
