from os import terminal_size
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import tkinter.scrolledtext as st
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

def posicion(event):    #ACTUALIZAR POSICION
    pos.config(text = "[" + str(editor.index(INSERT)).replace(".",",") + "]" )
# Creating tkinter window -----------------------
root = Tk()
root.title("ScrolledText Widget")
root.config(bg="gray17")
root.geometry("1050x500")

# functions for file ------------------------------
file = ""   # path from file in memory
def openFile():
    global file
    # get name file
    file = filedialog.askopenfilename(title="open")
    extension = file[len(file)-3:len(file)]
    if extension == "jpr":
        # open file
        fileOpen = open(file)
        content = fileOpen.read()
        editor.delete("1.0", "end")    # delete text in text area
        editor.insert(INSERT, content)
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

def initComponents():
    # create bar and menu ---------------------------------------
    barMenu = Menu(root)
    mnuFile = Menu(barMenu)  # create menus
    # create commands of menus
    mnuFile.add_command(label="Open", command=openFile)
    mnuFile.add_command(label="New", command=newFile)
    mnuFile.add_command(label="Save", command=saveFile)
    mnuFile.add_command(label="Save as", command=saveAs)
    # add menus at the bar menu
    barMenu.add_cascade(label="File", menu=mnuFile)
    # indicate that bar menu will be in the window
    root.config(menu=barMenu)

    root.mainloop()
#ELEMENTOS
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
editor = st.ScrolledText(scrollable_frame, undo = True, width = 60, height = 15)
lines = Canvas(scrollable_frame, width = 30, height = 240, background = 'gray60')
console = st.ScrolledText(scrollable_frame, undo = True, width = 60, height = 15)
btnNext = Button(scrollable_frame, width = 10, height = 1, text="Next")
# CAMBIO DE COLORES
editor.tag_config('reservada', foreground='red')
editor.tag_config('variable', foreground='maroon4')
editor.tag_config('string', foreground='green2')
editor.tag_config('operacion', foreground='gold')
editor.tag_config('etiqueta', foreground='purple')
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
initComponents()