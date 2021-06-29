import time
from os import terminal_size
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import threading
import gramatica as Grammar
import tkinter.scrolledtext as st

# verify if there's a read in use
def verifyRead():
    while True:
        time.sleep(0.5)
        if Grammar.active == True:
            console.insert(INSERT, Grammar.ast.getConsola())
            Grammar.ast.setConsola("")
            Grammar.active = False
# create en start thread
t = threading.Thread(target = verifyRead)
t.start()

def lineas(*args):      #ACTUALIZAR LINEAS
    lines.delete("all")

    cont = editor.index("@1,0")
    while True :
        dline= editor.dlineinfo(cont)
        if dline is None:
            break
        y = dline[1]
        strline = str(cont).split(".")[0]
        lines.create_text(2,y,anchor="nw", text=strline, font = ("Arial", 10))
        cont = editor.index("%s+1line" % cont)
def recorrerInput(entrada):  #Funcion para obtener palabrvas reservadas, signos, numeros, etc
    lista = []
    val = ''
    counter = 0
    while counter < len(entrada):
        # ID and signs
        if val != '' and re.search(r"[a-zA-Z0-9]|_", entrada[counter]):
            val += entrada[counter]
        elif re.search(r"[a-zA-Z]", entrada[counter]):
            val += entrada[counter]
        # recognize COMMENTS
        elif entrada[counter] == "#":
            if len(val) != 0:
                l = []
                l.append("other")
                l.append(val)
                lista.append(l)
                val = ''
            val = entrada[counter]
            counter += 1
            while counter < len(entrada):
                # MULTI LINE COMMENTS
                if entrada[counter] == "*":
                    val += entrada[counter]
                    counter += 1
                    estado = 0
                    while counter < len(entrada):
                        val += entrada[counter]
                        if estado == 0:
                            if entrada[counter] == "*":
                                estado = 1
                        elif estado == 1:
                            if entrada[counter] == "#":
                                l = []
                                l.append("comment")
                                l.append(val)
                                lista.append(l)
                                val = ''
                                break
                        counter += 1
                    break
                # LINE COMMENT
                else:
                    val += entrada[counter]
                    counter += 1
                    while counter < len(entrada):
                        if entrada[counter] == '\n':
                            val += entrada[counter]
                            l = []
                            l.append("comment")
                            l.append(val)
                            lista.append(l)
                            val = ''
                            break
                        val += entrada[counter]
                        counter += 1
                    break
                val += entrada[counter]
                counter += 1
        # recognize CHAINS
        elif entrada[counter] == "\"":
            if len(val) != 0:
                l = []
                l.append("other")
                l.append(val)
                lista.append(l)
                val = ''
            val = entrada[counter]
            counter += 1
            while counter < len(entrada):
                if entrada[counter] == "\"":
                    val += entrada[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += entrada[counter]
                counter += 1
        # recognize CHARS
        elif entrada[counter] == "\'":
            if len(val) != 0:
                l = []
                l.append("other")
                l.append(val)
                lista.append(l)
                val = ''
            val = entrada[counter]
            counter += 1
            while counter < len(entrada):
                if entrada[counter] == "\'":
                    val += entrada[counter]
                    l = []
                    l.append("string")
                    l.append(val)
                    lista.append(l)
                    val = ''
                    break
                val += entrada[counter]
                counter += 1
        else:
            if len(val) != 0:
                try:
                    num = int(val)
                    l = []
                    l.append("numero")
                    l.append(num)
                    lista.append(l)
                    val = ''
                except:
                    l = []
                    l.append("other")
                    l.append(val)
                    lista.append(l)
                    val = ''
            try:
                num = int(entrada[counter])
                l = []
                l.append("numero")
                l.append(num)
                lista.append(l)
            except:
                l = []
                l.append("other")
                l.append(entrada[counter])
                lista.append(l)
        counter +=1
    for s in lista:
        # search reserved words in DICTIONARY of reserved
        for key in Grammar.reservadas:
            if type(s[1]) is str and key == s[1].lower():
                s[0] = 'reservada'
    return lista
def posicion(event):    #ACTUALIZAR POSICION
    pos.config(text = "[" + str(editor.index(INSERT)).replace(".",",") + "]" )
def paintText():
    global contentFile
    contentFile = editor.get(1.0, "end")
    editor.delete(1.0, "end")  # delete text in text area
    input = recorrerInput(contentFile)
    # to print colors of words
    for s in input[:-1]:
        editor.insert(INSERT, s[1], s[0])
# Creating tkinter window -----------------------
root = Tk()
root.title("ScrolledText Widget")
root.config(bg="gray17")
root.geometry("1050x500")

# functions for file ------------------------------
file = ""   # path from file in memory
contentFile = ""
def openFile():
    global file
    global contentFile
    # get name file
    file = filedialog.askopenfilename(title="open")
    extension = file[len(file)-3:len(file)]
    if extension == "jpr":
        # open file
        fileOpen = open(file)
        contentFile = fileOpen.read()
        editor.delete(1.0, "end")  # delete text in text area
        input = recorrerInput(contentFile)
        # to print colors of words
        for s in input:
            editor.insert(INSERT, s[1], s[0])
        fileOpen.close()
    else:
        messagebox.showinfo("ERROR open file", "File isn't type .jpr")
def newFile():
    global file
    file = ""
    editor.delete(1.0, END)
def saveFile():
    global file
    if file == "":
        saveAs()
    else:
        save_file = open(file, "w")
        save_file.write(editor.get(1.0, END))
        save_file.close()
def saveAs():
    global file
    save = filedialog.asksaveasfilename(title="Save File", initialdir="C:/")
    save_file = open(save, "w+")
    save_file.write(editor.get(1.0, END))
    save_file.close()
    file = save

def interpret():
    console.delete(1.0, "end")
    paintText()
    console.insert(INSERT, Grammar.generateCode(contentFile))
def initComponents():
    # create bar and menu ---------------------------------------
    barMenu = Menu(root)
    mnuFile = Menu(barMenu)
    # create commands of menus
    mnuFile.add_command(label="Open", command=openFile)
    mnuFile.add_command(label="New", command=newFile)
    mnuFile.add_command(label="Save", command=saveFile)
    mnuFile.add_command(label="Save as", command=saveAs)
    # add menus at the bar menu
    barMenu.add_cascade(label="File", menu=mnuFile)

    # create options ------------------------------------------
    mnuOptions = Menu(barMenu)
    # create commands of menus
    mnuOptions.add_command(label="Interpret", command=interpret)
    mnuOptions.add_command(label="Color", command=paintText)
    mnuOptions.add_command(label="Report Errors", command=Grammar.reportErrors)
    # add menus at the bar menu
    barMenu.add_cascade(label="Options", menu=mnuOptions)
    # indicate that bar menu will be in the window
    root.config(menu=barMenu)
    root.mainloop()
#ELEMENTOS --------------------------------------------------------------
frame = Frame(root, bg="gray60")
canvas = Canvas(frame)
scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)
scrollbar2 = Scrollbar(frame, orient=HORIZONTAL, command=canvas.xview)
scrollable_frame = Frame(canvas, bg="gray")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(xscrollcommand=scrollbar2.set, yscrollcommand=scrollbar.set, width = 1250, height = 700)

pos = ttk.Label(scrollable_frame)
pos.grid(column = 1, row = 1)
editor = st.ScrolledText(scrollable_frame, undo = True, width = 60, height = 20, wrap='none')
lines = Canvas(scrollable_frame, width = 30, height = 320, background = 'gray60')
console = st.ScrolledText(scrollable_frame, undo = True, width = 60, height = 20, wrap='none')
btnNext = Button(scrollable_frame, width = 10, height = 1, text="Next")
# CAMBIO DE COLORES
editor.tag_config('reservada', foreground='blue')
editor.tag_config('string', foreground='orange')
editor.tag_config('numero', foreground='purple')
editor.tag_config('comment', foreground='gray')
editor.tag_config('other', foreground='black')

editor.tag_config('operacion', foreground='gold')
#editor.tag_config('signo', foreground='gray')
# set position to widgets
pos.grid(column = 1, row = 1)
btnNext.grid(column = 2, row = 1)
lines.grid(column = 0, row = 3)
editor.grid(column = 1, row = 3, pady = 25, padx = 0)
console.grid(column = 2, row = 3, pady = 25, padx = 0)
# FUNCIONALIDADES EN EL TECLADO
editor.bind('<Return>', lineas)
editor.bind('<BackSpace>', lineas)
editor.bind('<<Change>>', lineas)
editor.bind('<Configure>', lineas)
editor.bind('<Motion>', lineas)
editor.bind('<KeyPress>', posicion)
editor.bind('<Button-1>', posicion)
# for editor
frame.grid(sticky='news')
canvas.grid(row=0,column=1)
scrollbar.grid(row=0, column=2, sticky='ns')
scrollbar2.grid(row=1, column=1, sticky='ns')
# ----------------------------------------------------------------

initComponents()

