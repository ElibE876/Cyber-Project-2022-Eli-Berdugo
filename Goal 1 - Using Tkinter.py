# Creating a simple calculator to learn how to use Tkinter
from tkinter import *

root = Tk() #Create window
root.title("Simple Calculator")

text_line = Entry(root, width=35, borderwidth=5) # Create calculator "screen"
text_line.grid(row=0, column=0, columnspan=3, padx=10, pady=10) #Implement it into the window

first = 0 # The first number in the equation
action = "" # The mathematical function being performed

def num_click(number):
    # What happens when a number button is clicked
    current = text_line.get()
    text_line.delete(0, END)
    text_line.insert(0, current + str(number))

def peula(to_do):
    # Relating the function button to the actual function being performed, in a global variable
    global first, action
    first = int(text_line.get())
    if to_do == "add":
        action = "addition"
    elif to_do == "subtract":
        action = "subtraction"
    elif to_do == "multiply":
        action = "multiplication"
    elif to_do == "divide":
        action = "division"
    text_line.delete(0, END)

def equals_button():
    # What happens when the = button is pressed
    second = int(text_line.get()) # Second number in the equation (first is global variable "first")
    text_line.delete(0, END)
    if action == "addition":
        text_line.insert(0, first + second)
    elif action == "subtraction":
        text_line.insert(0, first - second)
    elif action == "multiplication":
        text_line.insert(0, first * second)
    elif action == "division":
        if second == 0:
            text_line.insert(0, "dude you just tried dividiמg by zero you can't do that")
        elif first % second == 0: 
            # Return integer (not double) if division is clean
            text_line.insert(0, int(first / second))
        else:
            text_line.insert(0, first / second)

def clear_row():
    global first, action
    first = 0
    action = ""
    text_line.delete(0, END)

# Create buttons
button_1 = Button(text="1", padx=40, pady=20, command=lambda: num_click(1))
button_2 = Button(text="2", padx=40, pady=20, command=lambda: num_click(2))
button_3 = Button(text="3", padx=40, pady=20, command=lambda: num_click(3))
button_4 = Button(text="4", padx=40, pady=20, command=lambda: num_click(4))
button_5 = Button(text="5", padx=40, pady=20, command=lambda: num_click(5))
button_6 = Button(text="6", padx=40, pady=20, command=lambda: num_click(6))
button_7 = Button(text="7", padx=40, pady=20, command=lambda: num_click(7))
button_8 = Button(text="8", padx=40, pady=20, command=lambda: num_click(8))
button_9 = Button(text="9", padx=40, pady=20, command=lambda: num_click(9))
button_0 = Button(text="0", padx=40, pady=20, command=lambda: num_click(0))
button_plus = Button(text="+", padx=40, pady=20, command=lambda: peula("add"))
button_minus = Button(text="-", padx=40, pady=20, command=lambda: peula("subtract"))
button_times = Button(text="*", padx=40, pady=20, command=lambda: peula("multiply"))
button_divide = Button(text="/", padx=40, pady=20, command=lambda: peula("divide"))
button_equals = Button(text="=", padx=40, pady=20, command=equals_button)
button_clear = Button(text="Clear", padx=125, pady=20, command=clear_row)

# Implement buttons on screen
button_7.grid(row=1, column=0)
button_8.grid(row=1, column=1)
button_9.grid(row=1, column=2)
button_4.grid(row=2, column=0)
button_5.grid(row=2, column=1)
button_6.grid(row=2, column=2)
button_1.grid(row=3, column=0)
button_2.grid(row=3, column=1)
button_3.grid(row=3, column=2)
button_plus.grid(row=4, column=0)
button_0.grid(row=4, column=1)
button_equals.grid(row=4, column=2)
button_minus.grid(row=5, column=0)
button_times.grid(row=5, column=1)
button_divide.grid(row=5, column=2)
button_clear.grid(row=6, column=0, columnspan=3)

root.mainloop()