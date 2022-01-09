from tkinter import *
import time

root = Tk()

frame = LabelFrame(root)
frame.pack()

penis = Text(frame, height = 25, width = 52)
penis.pack()

def fuck():
    for i in range(3):
        penis.insert(END, "argentina\n")

butt = Button(root, text="fuck", command=fuck)
butt.pack()

root.mainloop()