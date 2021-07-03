from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from TS.Simbolo import Simbolo
from TS.Tipo import TIPO


class Llamada(Instruccion):
    def __init__(self, nombre, parametros, fila, columna):
        self.parametros = parametros
        self.nombre = nombre
        self.columna = columna
        self.fila = fila

    def interpretar(self, tree, table):
        result = tree.getFuncion(self.nombre.lower())  # OBTENER LA FUNCION
        if result is None:  # NO SE ENCONTRO LA FUNCION
            return Excepcion("Semantico", "NO SE ENCONTRO LA FUNCION: " + self.nombre, self.fila, self.columna)
        newTable = TablaSimbolos(tree.getTSGlobal())
        if result.nombre == "typeof":
            if len(self.parametros) == 1:
                contador = 0
                for expresion in self.parametros:
                    resultExpresion = expresion.interpretar(tree, table)
                    if isinstance(resultExpresion, Excepcion): return resultExpresion
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(),
                                      expresion.tipo, False, self.fila, self.columna, resultExpresion)
                    resultTabla = newTable.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                    contador += 1
            else:
                return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
        # para funcion TRUNCATE y ROUND
        elif result.nombre == "truncate" or result.nombre == "round":
            if len(self.parametros) == 1:
                contador = 0
                for expresion in self.parametros:
                    resultExpresion = expresion.interpretar(tree, table)
                    if isinstance(resultExpresion, Excepcion): return resultExpresion
                    if result.parametros[0]["tipo"] == expresion.tipo or result.parametros[1]["tipo"] == expresion.tipo:
                        # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                        simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(),
                                          result.parametros[contador]['tipo'], False, self.fila, self.columna, resultExpresion)
                        resultTabla = newTable.setTabla(simbolo)
                        if isinstance(resultTabla, Excepcion): return resultTabla
                    else:
                        return Excepcion("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila,
                                         self.columna)
                    contador += 1
            else:
                return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
        # OBTENER PARAMETROS
        elif len(result.parametros) == len(self.parametros):
            contador = 0
            for expresion in self.parametros:
                resultExpresion = expresion.interpretar(tree,table)
                if isinstance(resultExpresion, Excepcion): return resultExpresion
                # VERIFICACION DE TIPO
                if result.parametros[contador]["tipo"] == expresion.tipo:
                    # CREACION DE SIMBOLO E INGRESARLO A LA TABLA DE SIMBOLOS
                    simbolo = Simbolo(str(result.parametros[contador]['identificador']).lower(),
                    result.parametros[contador]['tipo'], False, self.fila, self.columna, resultExpresion)
                    resultTabla = newTable.setTabla(simbolo)
                    if isinstance(resultTabla, Excepcion): return resultTabla
                else:
                    return Excepcion("Semantico", "Tipo de dato diferente en Parametros de la llamada.", self.fila,
                                     self.columna)
                contador += 1
        else:
            return Excepcion("Semantico", "Cantidad de Parametros incorrecta.", self.fila, self.columna)
        # INTERPRETAR EL NODO FUNCION
        value = result.interpretar(tree, newTable)
        if isinstance(value, Excepcion): return value
        self.tipo = result.tipo
        return value

    def getNode(self):
        node = NodoAST("LLAMADA A FUNCION")
        node.addChild(str(self.nombre))
        parametros = NodoAST("PARAMETROS")
        for param in self.parametros:
            parametros.addNodeChild(param.getNode())
        node.addNodeChild(parametros)
        return node
