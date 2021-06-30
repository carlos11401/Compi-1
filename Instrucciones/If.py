from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Instrucciones.Break import Break


class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, ElseIf, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = ElseIf
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion

        if self.condicion.tipo == TIPO.BOOLEANO:
            if bool(condicion):  # VERIFICA SI ES VERDADERA LA CONDICION
                nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
                for instruccion in self.instruccionesIf:
                    result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion):
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break) or isinstance(result, Return) or isinstance(result, Continue):
                        return result
            else:  # ELSE
                if self.instruccionesElse is not None:
                    nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break) or isinstance(result, Return) or isinstance(result, Continue):
                            return result
                elif self.elseIf is not None:
                    result = self.elseIf.interpretar(tree, table)
                    if isinstance(result, Excepcion): return result
                    if isinstance(result, Break) or isinstance(result, Return) or isinstance(result, Continue):
                        return result
        else:
            return Excepcion("Semantico", "Tipo de dato no booleano en IF.", self.fila, self.columna)

    def getNode(self):
        node = NodoAST("IF")
        instruccionesIf = NodoAST("INSTRUCCIONES IF")
        for inst in self.instruccionesIf:
            instruccionesIf.addNodeChild(inst.getNode())
        node.addNodeChild(instruccionesIf)
        if self.instruccionesElse is not None:
            instruccionesElse = NodoAST("INSTRUCCIONES ELSE")
            for inst in self.instruccionesElse:
                instruccionesElse.addNodeChild(inst.getNode())
            node.addNodeChild(instruccionesElse)
        elif self.elseIf is not None:
            node.addNodeChild(self.elseIf.getNode())
        return node
