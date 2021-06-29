from tkinter import simpledialog

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
        read = simpledialog.askstring('Read','Ingresa algo :)')
        tree.updateConsola(read)
        return read
