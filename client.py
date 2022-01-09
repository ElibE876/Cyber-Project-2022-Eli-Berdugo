import socket
from tkinter import *

MSG_SIZE = 1024
PORT = 1234 

root = Tk()
root.title("OpenChat")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((socket.gethostname(), PORT))

    #Define functions
    def finish_creating(prompt, text_line, final_create):
        # Send name of new chat to server and have it be created
        c.send(text_line.get().encode())
        prompt.grid_forget()
        text_line.grid_forget()
        final_create.grid_forget()
        response = c.recv(MSG_SIZE).decode()
        
        if response != "chat created successfully":
            oops = Label(root, text="Something went wrong")
            oops.grid(row=0, column=0)
        else:
            yay = Label(root, text=response)
            yay.grid(row=0, column=0)

    def create_chat(clear1, clear2):
        # Screen to create a new for a new chat
        c.send("create chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        prompt = Label(root, text="Create a name for your chat:")
        prompt.grid(row=0, column=0)
        text_line = Entry(root, width=35)
        text_line.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        final_create = Button(root, text="Create", width=10, command=lambda: finish_creating(prompt, text_line, final_create))
        final_create.grid(row=3, column=0)

    def finish_joining(chatname):
        c.send(chatname.encode())
        print(c.recv(MSG_SIZE).decode())

    def join_chat(clear1, clear2):
        # Create screen for joining an existing chat
        c.send("join chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        try:
            chatnum = int(c.recv(MSG_SIZE).decode()) # Get number of open chats from server
            c.send("got chatnum".encode())
            
            if chatnum == 0:
                label = Label(root, text="There are no chats currently open.\nTry creating one!", pady=10)
                label.grid(row=0, column=0)
                create_button = Button(root, text="Create Chat", width=30, pady=10, command=lambda: create_chat(label, create_button))
                create_button.grid(row=1,column=0)
            else:
                label = Label(root, text="List of currently open chats:", pady=10)
                label.grid(row=0, column=0)
                for i in range(chatnum):
                    chatname = c.recv(MSG_SIZE).decode()
                    c.send("got chat".encode())
                    chat_button = Button(text=chatname, padx=50, command=lambda: finish_joining(chatname))
                    chat_button.grid(row=i+1, column=0)
                c.send("chatlist received!".encode())
        
        except Exception as error:
            print(error)

    # Create welcome buttons
    create_button = Button(root, text="Create Chat", width=30, pady=10, command=lambda: create_chat(create_button, join_button))
    join_button = Button(root, text="Join Chat", width=30, pady=10, command=lambda: join_chat(create_button, join_button))

    # Put welcome buttons on screen
    create_button.grid(row=0, column=0)
    join_button.grid(row=1, column=0)


    root.mainloop()