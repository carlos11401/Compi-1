from Abstract.instruccion import Instruccion
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
        foundCase = False
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
                    foundCase = True
                    for instruccion in instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        # to accept BRAKE and not how error
                        if isinstance(result, Break) : return None
        # if there's default
        if not foundCase and (self.default is not None):
            nuevaTabla = TablaSimbolos(table)
            for instruccion in self.default:
                result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                if isinstance(result, Excepcion):
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())
                    # to accept BRAKE and not how error
                    if isinstance(result, Break): return None
            return None
