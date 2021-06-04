from tkinter import *
from tkinter import filedialog, messagebox
import tkinter.scrolledtext as st

# Creating tkinter window -----------------------
window = Tk()
window.title("ScrolledText Widget")
window.config(bg="gray17")
window.geometry("1050x500")
# Scrolled Text ---------------------------------
st_editor = st.ScrolledText(window,  # Creating scrolled text area for code
                            width=45,
                            height=15,
                            font=("Times New Roman", 15))

st_result = st.ScrolledText(window,  # Creating scrolled text area for code
                            width=45,
                            height=15,
                            font=("Times New Roman", 15))
st_editor.grid(row=0, column=0, padx=30, pady=20)
st_result.grid(row=0, column=1, padx=30, pady=10)
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
        st_editor.delete("1.0", "end")    # delete text in text area
        st_editor.insert(INSERT, content)
        fileOpen.close()
    else:
        messagebox.showinfo("ERROR open file", "File isn't type .jpr")
def newFile():
    global file
    file = ""
    st_editor.delete(1.0, END)
def saveFile():
    global file
    if file == "":
        saveAs()
    else:
        save_file = open(file, "w")
        save_file.write(st_editor.get(1.0, END))
        save_file.close()
def saveAs():
    global file
    save = filedialog.asksaveasfilename(title="Save File", initialdir="C:/")
    save_file = open(save, "w+")
    save_file.write(st_editor.get(1.0, END))
    save_file.close()
    file = save
def initComponents():
    # create bar and menu ---------------------------------------
    barMenu = Menu(window)
    mnuFile = Menu(barMenu)  # create menus
    # create commands of menus
    mnuFile.add_command(label="Open", command=openFile)
    mnuFile.add_command(label="New", command=newFile)
    mnuFile.add_command(label="Save", command=saveFile)
    mnuFile.add_command(label="Save as", command=saveAs)
    # add menus at the bar menu
    barMenu.add_cascade(label="File", menu=mnuFile)
    # indicate that bar menu will be in the window
    window.config(menu=barMenu)
    # Inserting Text
    st_editor.insert(INSERT, "insert code")
    # Inserting Text
    st_result.insert(INSERT, "result")
    window.mainloop()

initComponents()

