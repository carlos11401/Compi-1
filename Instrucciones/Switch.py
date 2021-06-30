from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from Instrucciones.Continue import Continue
from TS.Exception import Excepcion
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Switch(Instruccion):
    def __init__(self, condicion, cases, default,fila, columna):
        self.condicion = condicion
        self.cases = cases
        self.default = default
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion1 = self.condicion.interpretar(tree, table)
        brakeFound = False
        if isinstance(condicion1, Excepcion): return condicion1
        if self.cases is not None:
            for case in self.cases:
                nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
                instrucciones,condicion2 = case.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                if isinstance(condicion2, Excepcion):
                    tree.getExcepciones().append(condicion2)
                    tree.updateConsola(condicion2.toString())
                if isinstance(condicion2, Break): return condicion2
                # prove which case choose
                if condicion1 == condicion2:
                    for instruccion in instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        # to accept BRAKE and not how error
                        if isinstance(result, Break) :
                            brakeFound = True
                            return None
                        if isinstance(result, Continue): return result
        # if there's default
        if not brakeFound and (self.default is not None):
            nuevaTabla = TablaSimbolos(table)
            for instruccion in self.default:
                result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                if isinstance(result, Excepcion):
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())
                    # to accept BRAKE and not how error
                if isinstance(result, Break): return None
                if isinstance(result, Continue): return result
            return None

    def getNode(self):
        node = NodoAST("SWITCH")
        node.addNodeChild(self.condicion.getNode())
        instruccionesCases = NodoAST("INSTRUCCIONES CASES")
        for case in self.cases:
            instruccionesCases.addNodeChild(case.getNode())
        node.addNodeChild(instruccionesCases)
        if self.default is not None:
            instruccionesDefault = NodoAST("INSTRUCCIONES DEFAULT")
            for inst in self.default:
                instruccionesDefault.addNodeChild(inst.getNode())
            node.addNodeChild(instruccionesDefault)
        return node
