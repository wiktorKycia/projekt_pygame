from tkinter import *
from subprocess import *
def fun():
    call(["python", "test2.py"])
    
root = Tk()
but = Button(root, command=fun)
but.pack()
root.mainloop()