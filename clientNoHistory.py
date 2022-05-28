import socket
from tkinter import *
from tkinter import messagebox
from threading import Thread

MSG_SIZE = 1024
with open("server_address_nohistory.txt","r") as addr_file:
    content = addr_file.read().split(",")
    ADDR = content[0]
    PORT = int(content[1])

class GUI:
    def __init__(self):
        # create chat window, currently hidden
        self.chatwindow = Tk()
        self.chatwindow.withdraw()
        
        # create and set login window, first interface
        self.login = Toplevel()
        self.login.title("Login")
        self.login.resizable(width = False, height = False)
        self.login.configure(width = 400, height = 400)
        
        # create labels
        self.pls = Label(self.login, text = "Please login to continue", justify = CENTER, font = "Helvetica 14 bold")
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.05)

        self.labelName = Label(self.login,text = "Name: ", font = "Helvetica 12")
        self.labelName.place(relheight = 0.2, relx = 0.2, rely = 0.32)

        self.labelPass = Label(self.login, text = "Password: ", font = "Helvetica 12")
        self.labelPass.place(relheight = 0.2, relx = 0.2, rely = 0.55)
                             
        # create entry boxes for username and password
        self.entryName = Entry(self.login, font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.32)

        self.entryPass = Entry(self.login, font = "Helvetica 14", show="*")
        self.entryPass.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.55)
         
        # set the focus of the cursor
        self.entryName.focus()
                             

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

    # function for signing up
    def signUp(self):
        # tell server we're signing up
        c.send("signup".encode())
        c.recv(MSG_SIZE)
        
        # create and set up signup window
        self.login.destroy()
        self.signup = Toplevel()

        self.signup.title("Sign Up")
        self.signup.resizable(width = False, height = False)
        self.signup.configure(width = 400, height = 400)
        
        # create labels
        self.pls = Label(self.signup, text = "Enter account details:", justify = CENTER, font = "Helvetica 14 bold")
        self.pls.place(relheight = 0.15, relx = 0.2, rely = 0.05)

        self.labelName = Label(self.signup, text = "Name: ", font = "Helvetica 12")
        self.labelName.place(relheight = 0.2, relx = 0.2, rely = 0.32)
                             
        self.labelPass = Label(self.signup, text = "Password: ", font = "Helvetica 12")
        self.labelPass.place(relheight = 0.2, relx = 0.2, rely = 0.5)

        # create a entry box for
        # typing the username
        self.entryName = Entry(self.signup, font = "Helvetica 14")
        self.entryName.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.3)
         
        # set the focus of the cursor
        self.entryName.focus()
                             
        # create a entry box for
        # typing the username
        self.entryPass = Entry(self.signup, font = "Helvetica 14", show="*")
        self.entryPass.place(relwidth = 0.4, relheight = 0.12, relx = 0.4, rely = 0.5)
         

        # create a Continue Button
        # along with action
        self.go = Button(self.signup, text = "CONTINUE", font = "Helvetica 14 bold", command =lambda: self.goAhead("signup"))
        self.go.place(relx = 0.44, rely = 0.7)


    # this function serves both login and signup, since they are similar
    def goAhead(self, signUp):
        if signUp:
            self.name = self.entryName.get()
            self.password = self.entryPass.get()
            if self.name == "" or self.password == "":
                self.takenLabel = Label(self.signup, text = "please enter a name and password dude", font = "Helvetica 12", fg = "#ff0000")
                self.takenLabel.place(relheight = 0.2, relx = 0.2, rely = 0.8)
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
            self.name = self.entryName.get()
            self.password = self.entryPass.get()
            if self.name == "" or self.password == "":
                    self.takenLabel = Label(self.login, text = "please enter a name and password dude", font = "Helvetica 12", fg = "#ff0000")
                    self.takenLabel.place(relheight = 0.05, relx = 0.2, rely = 0.87)
            else:
                c.send("login".encode())
                if c.recv(MSG_SIZE).decode() == "got login":   
                    c.send(self.name.encode())
                    print("sent name")
                    if c.recv(MSG_SIZE).decode() == "got name":
                        c.send(self.password.encode())
                        print("sent pass")
                        if c.recv(MSG_SIZE).decode() == "Login failed":
                            print("fail")
                            self.takenLabel = Label(self.login, text = "Incorrect username or password", font = "Helvetica 12", fg = "#ff0000")
                            self.takenLabel.place(relheight = 0.1, relx = 0.2, rely = 0.87)
                        else:
                            print("Login successful")
                            self.proceed(self.login)
                        
    # screen for choosing to create/join chat
    def proceed(self, destroy):
        # user is now logged in
        if destroy:
            destroy.destroy()
        
        # Create welcome buttons
        self.root = Tk()
        self.root.title("Chat")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing_root)
        self.create_button = Button(self.root, text="Create Chat", width=30, pady=10, command=lambda: self.create_chat(self.create_button, self.join_button))
        self.join_button = Button(self.root, text="Join Chat", width=30, pady=10, command=lambda: self.join_chat(self.create_button, self.join_button))

        # Put welcome buttons on screen
        self.create_button.grid(row=0, column=0)
        self.join_button.grid(row=1, column=0)

    # function for if user quits before entering a chat
    def on_closing_root(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the program?"):
            c.send(":leave".encode())
            c.close()
            self.root.destroy()
            self.chatwindow.destroy()

    # function for if user quits while in chatroom
    def on_closing_chat(self):
        if messagebox.askokcancel("Quit", "Do you want to leave the chat?"):
            c.send(":leave".encode())
            self.chatwindow.withdraw()
            self.proceed(None)

    # Screen to create a name for a new chat
    def create_chat(self, clear1, clear2):

        c.send("create chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        prompt = Label(self.root, text="Create a name for your chat:")
        prompt.grid(row=0, column=0)
        text_line = Entry(self.root, width=35)
        text_line.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        final_create = Button(self.root, text="Create", width=10, command=lambda: self.finish_creating(text_line))
        final_create.grid(row=3, column=0)


    # Send name of new chat to server and have it be created
    def finish_creating(self, text_line):
        chatname = text_line.get()
        if chatname != "":
            c.send(chatname.encode())
            response = c.recv(MSG_SIZE).decode()
            
            if response != "chat created successfully":
                print(response)
                oops = Label(self.root, text="Something went wrong")
                oops.grid(row=3, column=0)
            else:
                c.send("successfully? yay".encode())
                print("opening")
                self.root.destroy()
                self.chat_layout(chatname)
                
                # start thread to receive messages
                self.rcv = Thread(target=self.receive)
                self.rcv.start()

    # Create screen for joining an existing chat
    def join_chat(self, clear1, clear2):
        c.send("join chat".encode())
        clear1.grid_forget()
        clear2.grid_forget()
        
        try:
            chatnum = c.recv(MSG_SIZE).decode() # Get number of open chats from server
            c.send("got chatnum".encode())
            
            if chatnum == "0": # create screen for if no chats are open
                label = Label(self.root, text="There are no chats currently open.\nTry creating one!", pady=10)
                label.grid(row=0, column=0)
                #button to create chat
                create_button = Button(self.root, text="Create Chat", width=30, pady=10, command=lambda: self.create_chat(label, create_button))
                create_button.grid(row=1,column=0)

            else:
                # create screen for selecting chat to join
                chatnum = int(chatnum)
                label = Label(self.root, text="List of currently open chats:", pady=10)
                label.grid(row=0, column=0)
                for i in range(chatnum):
                    chatname = c.recv(MSG_SIZE).decode()
                    c.send("got chat".encode())
                    chat_button = Button(self.root,text=chatname, padx=50, command=lambda chatname=chatname: self.finish_joining(chatname))
                    chat_button.grid(row=i+1, column=0)

                if c.recv(MSG_SIZE).decode() == "done?":
                    c.send("chatlist received!".encode()) # update server
                    print("chatlist received")
        
        except Exception as error:
            print(error)

    # finish the joining process and enter the chatroom
    def finish_joining(self, chatname):
        c.send(chatname.encode()) # send server requested chatroom to join
        print(chatname)
        response = c.recv(MSG_SIZE).decode()
        print(response)
        if response == f"{chatname} successfully accessed":
            c.send("great".encode())
            
            # destroy current window and open chatroom
            self.root.destroy()
            self.chat_layout(chatname)
            
            # start the thread to receive messages
            self.rcv = Thread(target=self.receive)
            self.rcv.start()

    # create the chatroom screen and layout
    def chat_layout(self, chatname):
        self.chatwindow.deiconify()
        self.chatwindow.title(chatname)
        self.chatwindow.resizable(width = False, height = False)
        self.chatwindow.configure(width = 470, height = 550, bg = "#17202A")

        self.line = Label(self.chatwindow, width = 450, bg = "#ABB2B9") 
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012)

        # create list of participants at top of window
        self.labelHead = Text(self.chatwindow, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 16 bold", pady = 5, height = 1)
        self.labelHead.tag_configure('current_user', font = "Helvetica 16 bold", foreground = "yellow")
        self.labelHead.tag_configure("center", justify='center')
        self.labelHead.place(relwidth = 1)

        # create text console for messages
        self.textCons = Text(self.chatwindow, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = "Helvetica 14", padx = 5, pady = 5)
        self.textCons.tag_configure('bold', font = "Helvetica 16 bold", foreground = "yellow")
        self.textCons.tag_configure('error', font = "Helvetica 16 bold", foreground = "red")
        self.textCons.place(relheight = 0.745, relwidth = 1, rely = 0.08)

        self.labelBottom = Label(self.chatwindow, bg = "#ABB2B9", height = 80)
        self.labelBottom.place(relwidth = 1, rely = 0.825)
        
        self.entryMsg = Entry(self.labelBottom, bg = "#2C3E50", fg = "#EAECEE", font = "Helvetica 13") # entry box for message sending
        
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.68, relheight = 0.06, rely = 0.008, relx = 0.083)
        self.entryMsg.focus()
        
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom, text = "Send", font = "Helvetica 10 bold", width = 20, bg = "#ABB2B9", command = lambda : self.sendButton(self.entryMsg.get()))   
        self.buttonMsg.place(relx = 0.77, rely = 0.008, relheight = 0.06, relwidth = 0.22)
        
        self.textCons.config(cursor = "arrow")

        self.chatwindow.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))

        # create an image Button
        self.buttonImg = Button(self.chatwindow, text = "+", font = "Helvetica 20 bold", width = 12, bg = "#ABB2B9")
        self.buttonImg.place(relx = 0.01, rely = 0.845, relheight = 0.13, relwidth = 0.07)
        
        self.textCons.config(cursor = "arrow")
        
        self.chatwindow.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))
        self.chatwindow.protocol("WM_DELETE_WINDOW", self.on_closing_chat) # direct to protocol for quiting chat
        
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.textCons.yview)
        
        self.textCons.config(state = DISABLED) # disallow typing directly into console

    # function to receive messages
    def receive(self):
        while True:
            try:
                message = c.recv(MSG_SIZE).decode() # receive message/update from server
                if message[:5] == ":left": # server lets this thread know that the main thread quit the chat
                    break
                elif message[:15] == ":newparticipant": # update participant list at top of screen and insert announcement to console
                    announcement = message.split(";")
                    participant_list = announcement[0][15:]
                    username_index = participant_list.find(self.name)
                    
                    if username_index != -1: # if current user is in the participant list, update the label
                        self.labelHead.config(state=NORMAL)
                        self.labelHead.delete("1.0", END)
                        if username_index == 0:
                            self.labelHead.insert(END, self.name, "current_user")
                            self.labelHead.insert(END, participant_list[username_index+len(self.name):])
                        elif username_index == len(participant_list) - len(self.name):
                            self.labelHead.insert(END, participant_list[:username_index])
                            self.labelHead.insert(END, self.name, "current_user")
                        else:
                            username_index = participant_list.find(", " + self.name + ",") + 2 # make sure the username we find isn't part of someone else's
                            if username_index != 1:
                                self.labelHead.insert(END, participant_list[:username_index])
                                self.labelHead.insert(END, self.name, "current_user")
                                self.labelHead.insert(END, participant_list[username_index+len(self.name):])
                        self.labelHead.tag_add("center", "1.0", "end")
                        self.labelHead.config(state = DISABLED)

                    message = announcement[1]
                
                elif message[:16] == ":participantleft": # update participant list at top of screen and insert announcement to console
                    announcement = message.split(";")
                    participant_list = announcement[0][16:]
                    username_index = participant_list.find(self.name)
                    
                    if username_index != -1: # if current user is in the participant list, update the label
                        self.labelHead.config(state=NORMAL)
                        self.labelHead.delete("1.0", END)
                        if username_index == 0:
                            self.labelHead.insert(END, self.name, "current_user")
                            self.labelHead.insert(END, participant_list[username_index+len(self.name):])
                        elif username_index == len(participant_list) - len(self.name):
                            self.labelHead.insert(END, participant_list[:username_index])
                            self.labelHead.insert(END, self.name, "current_user")
                        else:
                            username_index = participant_list.find(", " + self.name + ",") + 2 # make sure the username we find isn't part of someone else's
                            if username_index != 1:
                                self.labelHead.insert(END, participant_list[:username_index])
                                self.labelHead.insert(END, self.name, "current_user")
                                self.labelHead.insert(END, participant_list[username_index+len(self.name):])
                        self.labelHead.tag_add("center", "1.0", "end")
                        self.labelHead.config(state = DISABLED)
                        
                    message = announcement[1]

                # insert messages to text box
                if ":" in message[1:]: # check if it's normal message from other user
                    index = message.find(":")
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, message[:index]+":", 'bold')
                    self.textCons.insert(END, message[index+1:] + "\n\n")
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)
                
                else: # this means it's an announcement/update from the server
                    self.textCons.config(state = NORMAL)
                    self.textCons.insert(END, message + "\n\n", 'bold')
                    self.textCons.config(state = DISABLED)
                    self.textCons.see(END)            

            except Exception as error:
                # an error will be printed on the command line or console if there's an error
                print("An error occured!\n" + str(error))
                self.textCons.config(state = NORMAL)
                self.textCons.insert(END,"You have been disconnected from the server", 'error')
                self.textCons.config(state = DISABLED)
                self.textCons.see(END)   
                c.close()
                self.chatwindow.protocol("WM_DELETE_WINDOW", self.chatwindow.destroy) # close window if X pressed
                break

    # start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state = DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        
        snd = Thread(target=self.sendMessage)
        snd.start()

    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        message = (f"{self.name}: {self.msg}")
        c.send(message.encode())   

def main():
    global c
    # connect to server
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((ADDR, PORT))
        # create a GUI class object
        GUI()

    except:
        # window notifying client that the server is down
        server_down = Tk()
        server_down.title("Server down")
        server_down.resizable(width = False, height = False)
        server_down.geometry("700x300")
        
        # create & place label
        down = Label(server_down, text = "Couldn't connect to server. Please try again later.", font = "Helvetica 14 bold")
        down.place(relx=0.5,rely=0.5,anchor=CENTER)
        print("server down ",ADDR,PORT)
        server_down.mainloop()


if __name__ == "__main__":
    main()
