import socket
from tkinter import *
from threading import Thread

MSG_SIZE = 1024
PORT = 1234 

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((socket.gethostname(), PORT))

class GUI:
    def __init__(self):
        # Chat window, currently hidden
        self.chatwindow = Tk()
        self.chatwindow.withdraw()
        
        self.name = c.recv(MSG_SIZE).decode()
        # Later will add login page
        self.root = Toplevel()
        self.root.title("Login")
        
        # Create welcome buttons
        self.create_button = Button(self.root, text="Create Chat", width=30, pady=10, command=lambda: self.create_chat(self.create_button, self.join_button))
        self.join_button = Button(self.root, text="Join Chat", width=30, pady=10, command=lambda: self.join_chat(self.create_button, self.join_button))

        # Put welcome buttons on screen
        self.create_button.grid(row=0, column=0)
        self.join_button.grid(row=1, column=0)

        self.chatwindow.mainloop()

    def create_chat(self, clear1, clear2):
        # Screen to create a name for a new chat
        c.send("create chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        prompt = Label(self.root, text="Create a name for your chat:")
        prompt.grid(row=0, column=0)
        text_line = Entry(self.root, width=35)
        text_line.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        final_create = Button(self.root, text="Create", width=10, command=lambda: self.finish_creating(prompt, text_line, final_create))
        final_create.grid(row=3, column=0)

    def finish_creating(self, prompt, text_line, final_create):
        # Send name of new chat to server and have it be created
        chatname = text_line.get()
        c.send(chatname.encode())
        prompt.grid_forget()
        text_line.grid_forget()
        final_create.grid_forget()
        response = c.recv(MSG_SIZE).decode()
        
        if response != "chat created successfully":
            print(response)
            oops = Label(self.root, text="Something went wrong")
            oops.grid(row=0, column=0)
        else:
            c.send("yay".encode())
            print("opening chatwindow")
            self.root.destroy()
            self.chat_layout(chatname)
            # the thread to receive messages
            rcv = Thread(target=self.receive)
            rcv.start()

    def join_chat(self, clear1, clear2):
        # Create screen for joining an existing chat
        c.send("join chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        try:
            chatnum = int(c.recv(MSG_SIZE).decode()) # Get number of open chats from server
            c.send("got chatnum".encode())
            
            if chatnum == 0:
                label = Label(self.root, text="There are no chats currently open.\nTry creating one!", pady=10)
                label.grid(row=0, column=0)
                create_button = Button(self.root, text="Create Chat", width=30, pady=10, command=lambda: self.create_chat(label, create_button))
                create_button.grid(row=1,column=0)
            else:
                label = Label(self.root, text="List of currently open chats:", pady=10)
                label.grid(row=0, column=0)
                for i in range(chatnum):
                    chatname = c.recv(MSG_SIZE).decode()
                    c.send("got chat".encode())
                    print("got")
                    chat_button = Button(self.root,text=chatname, padx=50, command=lambda: self.finish_joining(chatname))
                    chat_button.grid(row=i+1, column=0)
                c.send("chatlist received!".encode())
                print("chatlist received")
        
        except Exception as error:
            print(error)

    def finish_joining(self, chatname):
        c.send(chatname.encode())
        response = c.recv(MSG_SIZE).decode()
        if response == f"{chatname} successfully accessed":
            c.send("great".encode())
            self.root.destroy()
            self.chat_layout(chatname)
            # the thread to receive messages
            rcv = Thread(target=self.receive)
            rcv.start()

    def chat_layout(self, chatname):
        participant_list = c.recv(MSG_SIZE).decode()
        c.send("got participants".encode())
        self.chatwindow.deiconify()
        self.chatwindow.title(chatname)
        self.chatwindow.resizable(width = False,
                            height = False)
        self.chatwindow.configure(width = 470,
                            height = 550,
                            bg = "#17202A")
        self.labelHead = Label(self.chatwindow,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            text = participant_list,
                            font = "Helvetica 13 bold",
                            pady = 5)
        
        self.labelHead.place(relwidth = 1)
        self.line = Label(self.chatwindow,
                        width = 450,
                        bg = "#ABB2B9")
        
        self.line.place(relwidth = 1,
                        rely = 0.07,
                        relheight = 0.012)
        
        self.textCons = Text(self.chatwindow,
                            width = 20,
                            height = 2,
                            bg = "#17202A",
                            fg = "#EAECEE",
                            font = "Helvetica 14",
                            padx = 5,
                            pady = 5)
        
        self.textCons.place(relheight = 0.745,
                            relwidth = 1,
                            rely = 0.08)
        
        self.labelBottom = Label(self.chatwindow,
                                bg = "#ABB2B9",
                                height = 80)
        
        self.labelBottom.place(relwidth = 1,
                            rely = 0.825)
        
        self.entryMsg = Entry(self.labelBottom,
                            bg = "#2C3E50",
                            fg = "#EAECEE",
                            font = "Helvetica 13")
        
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.74,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.011)
        
        self.entryMsg.focus()
        
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Send",
                                font = "Helvetica 10 bold",
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))
        
        self.buttonMsg.place(relx = 0.77,
                            rely = 0.008,
                            relheight = 0.06,
                            relwidth = 0.22)
        
        self.textCons.config(cursor = "arrow")

        self.chatwindow.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
        
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1,
                        relx = 0.974)
        
        scrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(state = DISABLED)
    
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = Thread(target = self.sendMessage)
        snd.start()

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = c.recv(1024).decode()
                
                # insert messages to text box
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END,
                                    message+"\n\n")
                
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)
            except Exception as error:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!\n")
                c.close()
                break
        
    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            c.send(message.encode())   
            break

# create a GUI class object
g = GUI()