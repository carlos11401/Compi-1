
class Simbolo:
    def __init__(self, identificador, tipo, fila, columna, valor ):
        self.id = identificador
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.valor = valor

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor