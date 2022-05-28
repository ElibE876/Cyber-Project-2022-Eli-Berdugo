import socket
from tkinter import *
from tkinter import messagebox
from threading import Thread

MSG_SIZE = 1024
PORT = 1234

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((socket.gethostname(), PORT))

'''invited = False
invited_message = ""'''

class GUI:
    def __init__(self):
        # Chat window, currently hidden
        self.chatwindow = Tk()
        self.chatwindow.withdraw()
        
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 400)
        # create a Label
        self.pls = Label(self.login, text = "Please login to continue", justify = CENTER, font = "Helvetica 14 bold")
         
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.05)

        # create a Label
        self.labelName = Label(self.login,text = "Name: ", font = "Helvetica 12")
        self.labelName.place(relheight = 0.2, relx = 0.2, rely = 0.32)
                             
        # create a entry box for
        # typing the username
        self.entryName = Entry(self.login, font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.32)
         
        # set the focus of the cursor
        self.entryName.focus()

        # create a Label
        self.labelPass = Label(self.login, text = "Password: ", font = "Helvetica 12")
        self.labelPass.place(relheight = 0.2, relx = 0.2, rely = 0.55)
                             
        # create a entry box for
        # typing the password
        self.entryPass = Entry(self.login, font = "Helvetica 14", show="*")
        self.entryPass.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.55)
         

        # create a Continue Button
        # along with action
        self.go = Button(self.login,text = "CONTINUE",font = "Helvetica 14 bold",command =lambda: self.goAhead(False))
        self.go.place(relx = 0.6, rely = 0.75)
        
        # create a Sign Up Button
        # along with action
        self.go = Button(self.login, text = "SIGN UP", font = "Helvetica 14 bold", command = self.signUp)
        self.go.place(relx = 0.25,
                      rely = 0.75)
        
        self.login.mainloop()
        self.chatwindow.mainloop()

    def signUp(self):
        self.login.destroy()
        self.signup = Toplevel()
        c.send("signup".encode())
        c.recv(MSG_SIZE)

        # set the title
        self.signup.title("Sign Up")
        self.signup.resizable(width = False, height = False)
        self.signup.configure(width = 400, height = 400)
        
        # create a Label
        self.pls = Label(self.signup, text = "Enter account details:", justify = CENTER, font = "Helvetica 14 bold")
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.05)

        # create a Label
        self.labelName = Label(self.signup, text = "Name: ", font = "Helvetica 12")
        self.labelName.place(relheight = 0.2, relx = 0.2, rely = 0.32)
                             
        # create a entry box for
        # typing the username
        self.entryName = Entry(self.signup, font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.3)
         
        # set the focus of the cursor
        self.entryName.focus()

        # create a Label
        self.labelPass = Label(self.signup, text = "Password: ", font = "Helvetica 12")
        self.labelPass.place(relheight = 0.2, relx = 0.2, rely = 0.5)
                             
        # create a entry box for
        # typing the username
        self.entryPass = Entry(self.signup, font = "Helvetica 14", show="*")
         
        self.entryPass.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.5)
         
        # set the focus of the cursor
        self.entryPass.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.signup, text = "CONTINUE", font = "Helvetica 14 bold", command =lambda: self.goAhead("signup"))
         
        self.go.place(relx = 0.44, rely = 0.7)


    def goAhead(self, signUp):
        if signUp:
            self.name = self.entryName.get()
            self.password = self.entryPass.get()
            if self.name == "":
                self.takenLabel = Label(self.signup, text = "please enter a name dude", font = "Helvetica 12", fg = "#ff0000")
                self.takenLabel.place(relheight = 0.2, relx = 0.4, rely = 0.8)
            else:    
                c.send(self.name.encode())
                print("sent name")
                if c.recv(MSG_SIZE).decode() == "got name":
                    c.send(self.password.encode())
                    response = c.recv(MSG_SIZE).decode()
                    if response == "Username invalid":
                        self.takenLabel = Label(self.signup, text = "Username taken or contains comma/colon,\nor password contains comma!", font = "Helvetica 12", fg = "#ff0000")
                        self.takenLabel.place(relheight = 0.1, relx = 0.1, rely = 0.87)
                    else:
                        print(response)
                        self.proceed(self.signup)
        else:
            c.send("login".encode())
            self.name = self.entryName.get()
            self.password = self.entryPass.get()
            if self.name == "":
                    self.takenLabel = Label(self.login, text = "please enter a name dude", font = "Helvetica 12", fg = "#ff0000")
                    self.takenLabel.place(relheight = 0.05, relx = 0.4, rely = 0.87)
            else:
                if c.recv(MSG_SIZE).decode() == "got login":   
                    c.send(self.name.encode())
                    print("sent name")
                if c.recv(MSG_SIZE).decode() == "got name":
                    c.send(self.password.encode())
                    print("sent pass")
                    if c.recv(MSG_SIZE).decode() == "Login failed":
                        print("fail")
                        self.takenLabel = Label(self.login, text = "Login failed", font = "Helvetica 12", fg = "#ff0000")
                        self.takenLabel.place(relheight = 0.1, relx = 0.4, rely = 0.87)
                    else:
                        print("Login successful")
                        self.proceed(self.login)
                        
    def proceed(self, destroy):
        destroy.destroy()
        # Create welcome buttons
        self.root = Toplevel()
        self.root.title("Chat")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_root)
        self.create_button = Button(self.root, text="Create Chat", width=30, pady=10, command=lambda: self.create_chat(self.create_button, self.join_button))
        self.join_button = Button(self.root, text="Join Chat", width=30, pady=10, command=lambda: self.join_chat(self.create_button, self.join_button))

        # Put welcome buttons on screen
        self.create_button.grid(row=0, column=0)
        self.join_button.grid(row=1, column=0)

    def on_closing_root(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the program?"):
            c.close()

    def on_closing_chat(self):
        if messagebox.askokcancel("Quit", "Do you want to leave the chat?"):
            c.send(":leave".encode())
            self.proceed(self.chatwindow)

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
        
        if response != "chat created successfully": #'''and response[:8] != ":invited":'''
            print(response)
            oops = Label(self.root, text="Something went wrong")
            oops.grid(row=0, column=0)
        else:
            c.send("successfully? yay".encode())
            print("opening")
            self.root.destroy()
            self.chat_layout(chatname)
            
            # start thread to receive messages
            rcv = Thread(target=self.receive)
            rcv.start()
            '''if response[:8] == ":invited":
                self.invited(response, self.chatwindow, True)'''

    def join_chat(self, clear1, clear2):
        # Create screen for joining an existing chat
        c.send("join chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        try:
            chatnum = c.recv(MSG_SIZE).decode() # Get number of open chats from server
            c.send("got chatnum".encode())
            
            if chatnum == "0":
                label = Label(self.root, text="There are no chats currently open.\nTry creating one!", pady=10)
                label.grid(row=0, column=0)
                create_button = Button(self.root, text="Create Chat", width=30, pady=10, command=lambda: self.create_chat(label, create_button))
                create_button.grid(row=1,column=0) #'''elif chatnum[:8] == ":invited": self.invited(chatnum, self.root, False)'''
            else:
                chatnum = int(chatnum)
                label = Label(self.root, text="List of currently open chats:", pady=10)
                label.grid(row=0, column=0)
                for i in range(chatnum):
                    chatname = c.recv(MSG_SIZE).decode()
                    '''if chatname[:8] == ":invited":
                        self.invited(chatname, self.root, False)'''
                    c.send("got chat".encode())
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

        '''elif response[:8] == ":invited":
            self.invited(response, self.root, False)'''

    '''def invited(self, message, destroy, inchat):
        print("invited")
        c.send("invited".encode())
        chatAndInviter = message[8:].split(";")
        print(chatAndInviter)
        self.inviteWin = Toplevel()
        self.inviteWin.title("Invitation")
        self.inviteWin.resizable(width = False, height = False)
        self.inviteWin.configure(width = 300,height = 200)

        # create a Label
        self.invite = Label(self.inviteWin, text = f'You have been invited by {chatAndInviter[1]}\nto the chat "{chatAndInviter[0]}"!', justify = CENTER, font = "Helvetica 11")
        self.invite.place(relheight = 0.15, relx = 0.2, rely = 0.05)
        
        # create buttons
        self.go = Button(self.inviteWin, text = "ACCEPT", font = "Helvetica 14 bold", command =lambda: self.acceptInvite(self.inviteWin, destroy))
        self.go.place(relx = 0.2, rely = 0.55)
        
        self.decline = Button(self.inviteWin, text = "DECLINE", font = "Helvetica 14 bold", command =lambda: self.declineInvite(self.inviteWin, inchat))
        self.decline.place(relx = 0.55, rely = 0.55)

        self.inviteWin.mainloop()

    def acceptInvite(self, destroy1, destroy2):
        c.send("ok".encode())
        destroy1.destroy()
        self.proceed(destroy2)
    
    def declineInvite(self, destroy, inchat):
        c.send("no".decode())
        if not inchat:
            self.proceed(destroy)
        else:
            destroy.destroy()'''
        
    def chat_layout(self, chatname):
        self.chatwindow.deiconify()
        self.chatwindow.title(chatname)
        self.chatwindow.resizable(width = False, height = False)
        self.chatwindow.configure(width = 470, height = 550, bg = "#17202A")

        self.line = Label(self.chatwindow, width = 450, bg = "#ABB2B9") 
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        self.textCons = Text(self.chatwindow, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5)
        self.textCons.tag_configure('bold', font = "Helvetica 16 bold")
        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08)

        self.labelBottom = Label(self.chatwindow, bg = "#ABB2B9", height = 80)
        self.labelBottom.place(relwidth = 1, rely = 0.825)
        
        self.entryMsg = Entry(self.labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13")
        
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.68, relheight = 0.06, rely = 0.008, relx = 0.083)
        self.entryMsg.focus()
        
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom, text = "Send", font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9", command = lambda : self.sendButton(self.entryMsg.get()))   
        self.buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)
        
        self.textCons.config(cursor = "arrow")

        self.chatwindow.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))

        '''# create an Invite Button
        self.buttonInv = Button(self.chatwindow, text = "+", font = "Helvetica 20 bold", width = 12, bg = "#ABB2B9", command = self.invite)
        self.buttonInv.place(relx = 0.01, rely = 0.845, relheight = 0.13, relwidth = 0.07)'''        
        
        self.textCons.config(cursor = "arrow")
        
        self.chatwindow.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))
        self.chatwindow.protocol("WM_DELETE_WINDOW", self.on_closing_chat)
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1, relx = 0.974)
        
        scrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(state = DISABLED)

        '''global invited
        global invited_message
        if invited:
                self.invited(invited_message, self.chatwindow, True)
                invited = False'''

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        
        snd = Thread(target=self.sendMessage)
        snd.start()

    # function to receive messages
    def receive(self):
        '''global invited
        global invited_message'''
        while True:
            try:
                message = c.recv(MSG_SIZE).decode()
                if message[:15] == ":newparticipant":
                    announcement = message.split(";")
                    '''if self.labelHead:
                        self.labelHead.destroy()'''
                    self.labelHead = Label(self.chatwindow, bg = "#17202A", fg = "#EAECEE", text = announcement[0][15:], font = "Helvetica 13 bold", pady = 5)
                    self.labelHead.place(relwidth = 1)
                    message = announcement[1]
                elif message[:16] == ":participantleft":
                    announcement = message.split(";")
                    self.labelHead.destroy()
                    self.labelHead = Label(self.chatwindow, bg = "#17202A", fg = "#EAECEE", text = announcement[0][16:], font = "Helvetica 13 bold", pady = 5)
                    self.labelHead.place(relwidth = 1)
                    message = announcement[1]
                '''elif message[:8] == ":invited":
                    invited = True'''

                # insert messages to text box
                if ":" in message[1:]:
                    index = message.find(":")
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, message[:index]+":", 'bold')
                    self.textCons.insert(END, message[index+1:] + "\n\n")
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
                
                else:
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, message + "\n\n", 'bold')
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)            

            except Exception as error:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!\n" + str(error))
                c.close()
                break

    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        message = (f"{self.name}: {self.msg}")
        c.send(message.encode())   

    '''def invite(self):
        c.send(":invite".encode())
        self.invite = Toplevel()
        # set the title
        self.invite.title("Invite Users")
        self.invite.resizable(width = False, height = False)
        self.invite.configure(width = 400, height = 250)
        
        # create a Label
        self.pls = Label(self.invite, text = "Enter the username to invite", justify = CENTER, font = "Helvetica 14 bold")
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.05)

        # create a entry box for
        # typing the message
        self.entryUser = Entry(self.invite, font = "Helvetica 14")
        self.entryUser.place(relwidth = 0.6, relheight = 0.25, relx = 0.2, rely = 0.35)
         
        # set the focus of the cursor
        self.entryUser.focus()

        # create a Continue Button
        # along with action
        self.sendInvite = Button(self.invite, text = "INVITE", font = "Helvetica 14 bold", command = self.sendInvite)
        self.sendInvite.place(relx = 0.4, rely = 0.7)

        self.invite.mainloop()
    
    def sendInvite(self):
        c.send(self.entryUser.get().encode())
        print("invite pressed")
        response = c.recv(MSG_SIZE).decode()
        print(response)
        self.acceptedLabel = Label(self.invite, text = response, font = "Helvetica 12", fg = "#ff0000")
        self.acceptedLabel.place(relheight = 0.1, relx = 0.2, rely = 0.85)'''

def main():
    # create a GUI class object
    g = GUI()

if __name__ == "__main__":
    main()