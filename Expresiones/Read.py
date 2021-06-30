from tkinter import simpledialog

from Abstract.NodoAST import NodoAST
from Abstract.instruccion import Instruccion
from TS.Tipo import TIPO
import gramatica as Grammar

class Read(Instruccion):

    def __init__(self, fila, columna):
        self.tipo = TIPO.CADENA
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        Grammar.active = True
        read = simpledialog.askstring('Read',"Fila: "+str(self.fila)+" Col: "+str(self.columna))
        tree.updateConsola(read)
        return read

    def getNode(self):
        node = NodoAST("READ")
        return node
