from Abstract.instruccion import Instruccion
from TS.Exception import Excepcion
from TS.Tipo import TIPO
from TS.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class Switch(Instruccion):
    def __init__(self, condicion, cases, fila, columna):
        self.condicion = condicion
        self.cases = cases
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion1 = self.condicion.interpretar(tree, table)
        if isinstance(condicion1, Excepcion): return condicion1
        for case in self.cases:
            nuevaTabla = TablaSimbolos(table)  # NUEVO ENTORNO
            instrucciones,condicion2 = case.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
            if isinstance(condicion2, Excepcion):
                tree.getExcepciones().append(condicion2)
                tree.updateConsola(condicion2.toString())
            if isinstance(condicion2, Break): return condicion2
            if condicion1 == condicion2:
                for instruccion in instrucciones:
                    result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion):
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break): return result
