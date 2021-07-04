from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from Instrucciones.DeclaraccionArr2 import DeclaracionArr2
from Instrucciones.Declaracion import Declaracion
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from TS.Exception import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
import gramatica as Grammar

class Main(Instruccion):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        nuevaTabla = TablaSimbolos(table)
        for instruccion in self.instrucciones:  # REALIZAR LAS ACCIONES
            if isinstance(instruccion, DeclaracionArr2) or isinstance(instruccion, Declaracion) or isinstance(instruccion, DeclaracionArr1):
                Grammar.infTS[instruccion.identificador.lower() + str(nuevaTabla)] = ["Main",
                                                                                      instruccion.identificador,
                                                                                      None, None, None,
                                                                                      instruccion.fila,
                                                                                      instruccion.columna]

            value = instruccion.interpretar(tree, nuevaTabla)
            if isinstance(value, Excepcion):
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break):
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())

    def getNode(self):
        node = NodoAST("MAIN")
        instrucciones = NodoAST("INSTRUCCIONES MAIN")
        for inst in self.instrucciones:
            instrucciones.addNodeChild(inst.getNode())
        node.addNodeChild(instrucciones)
        return node
