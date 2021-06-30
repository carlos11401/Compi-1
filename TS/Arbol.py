class Arbol:
    def __init__(self, instrucciones ):
        self.instrucciones = instrucciones
        self.funciones = []
        self.excepciones = []
        self.consola = ""
        self.TSglobal = None
        self.dot = ""
        self.contador = 0

    def getInstrucciones(self):
        return self.instrucciones

    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones

    def getExcepciones(self):
        return self.excepciones

    def setExcepciones(self, excepciones):
        self.excepciones = excepciones

    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola

    def updateConsola(self,cadena):
        self.consola += str(cadena) + '\n'

    def getTSGlobal(self):
        return self.TSglobal
    
    def setTSglobal(self, TSglobal):
        self.TSglobal = TSglobal

    def getFunciones(self):
        return self.funciones

    def getFuncion(self, nombre):
        for funcion in self.funciones:
            if funcion.nombre == nombre:
                return funcion
        return None

    def addFuncion(self, funcion):
        self.funciones.append(funcion)

    def getDot(self, raiz):
        self.dot = ""
        self.dot += "digraph {\n"
        self.dot += "n0[label=\"" + raiz.getValue().replace("\"","\\\"")+"\"];\n"
        self.contador = 1
        self.roamAST("n0", raiz)
        self.dot += "}"
        return self.dot

    def roamAST(self, idFather, nodeFather):
        for child in nodeFather.getChildren():
            nameChild = "n"+str(self.contador)
            value = child.getValue()
            if value == "OperadorAritmetico.MAS": value = "+"
            elif value == "OperadorAritmetico.MENOS": value = "-"
            elif value == "OperadorAritmetico.UMENOS": value = "-"
            elif value == "OperadorAritmetico.POR": value = "-"
            elif value == "OperadorAritmetico.DIV":
                value = "/"
            elif value == "OperadorAritmetico.MOD":
                value = "%"
            elif value == "TIPO.ENTERO":
                value = "INT"
            elif value == "TIPO.DECIMAL":
                value = "DOUBLE"
            elif value == "TIPO.BOOLEANO":
                value = "BOOLEAN"
            elif value == "TIPO.CHARACTER":
                value = "CHAR"
            elif value == "TIPO.CADENA":
                value = "STRING"
            elif value == "TIPO.NULO":
                value = "NULL"
            elif value == "TIPO.ARREGLO":
                value = "ARRAY"
            elif value == "OperadorRelacional.MENOR":
                value = "<"
            elif value == "OperadorRelacional.MAYOR":
                value = ">"
            elif value == "OperadorRelacional.MENIGUAL":
                value = "<="
            elif value == "OperadorRelacional.MAYIGUAL":
                value = ">="
            elif value == "OperadorRelacional.IGUALIGUAL":
                value = "=="
            elif value == "OperadorRelacional.DIFERENTE":
                value = "!="
            elif value == "OperadorLogico.NOT":
                value = "!"
            elif value == "OperadorLogico.AND":
                value = "&&"
            elif value == "OperadorLogico.OR":
                value = "||"
            self.dot += nameChild + "[label=\"" + value + "\"];\n"
            self.dot += idFather + "->" + nameChild + ";\n"
            self.contador += 1
            self.roamAST(nameChild, child)
