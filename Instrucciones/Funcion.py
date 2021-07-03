from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from Instrucciones.DeclaracionArr1 import DeclaracionArr1
from TS.Exception import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Return import Return
from Instrucciones.Break import Break
from Instrucciones.Declaracion import Declaracion
import gramatica as Grammar


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
            if isinstance(instruccion, Declaracion) or isinstance(instruccion, DeclaracionArr1):
                Grammar.infTS[instruccion.identificador.lower()+str(nuevaTabla)] = ["Funcion",instruccion.identificador,None,None,None,instruccion.fila,instruccion.columna]

            value = instruccion.interpretar(tree, nuevaTabla)
            if isinstance(value, Excepcion):
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break):
                err = Excepcion("Semantico", "Sentencia BREAK fuera de ciclo", instruccion.fila, instruccion.columna)
                tree.getExcepciones().append(err)
                tree.updateConsola(err.toString())
            if isinstance(value, Return):
                self.tipo = value.tipo
                return value.result
        return None

    def getNode(self):
        node = NodoAST("FUNCION")
        node.addChild(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametro = NodoAST("PARAMETRO")
            parametro.addChild(param["tipo"])
            parametro.addChild(param["identificador"])
            parametros.addNodeChild(parametro)
        node.addNodeChild(parametros)
        instrucciones = NodoAST("INSTRUCCIONES")
        for inst in self.instrucciones:
            instrucciones.addNodeChild(inst.getNode())
        node.addNodeChild(instrucciones)
        return node
