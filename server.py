import socket
from threading import Thread

MSG_SIZE = 1024
PORT = 1234
HOST = socket.gethostname()

chat_list = []

class Chat:
    def __init__(self, chatname):
        self.chatname = chatname
        self.participants = []

    def add_participant(self, p_name):
        self.participants += p_name

    def get_chatname(self):
        return self.chatname

def create_chat(clientsocket, addr, client_number):
    print("creating chat")
    chatname = clientsocket.recv(MSG_SIZE).decode()
    print("creating " + chatname)
    chat_list.append(Chat(chatname))
    clientsocket.send("chat created successfully".encode())
    #Transpot to created chat, for now

def on_new_client(clientsocket, addr, client_number):
    global chat_list
    msg = clientsocket.recv(MSG_SIZE).decode()

    if msg == "create chat":
        create_chat(clientsocket, addr, client_number)
    
    elif msg == "join chat":
        print("joining chat")
        c.send(str(len(chat_list)).encode())
        
        if c.recv(MSG_SIZE).decode() == "got chatnum":
            if chat_list:
                
                for i in chat_list:
                    c.send(i.get_chatname().encode())
                    if c.recv(MSG_SIZE).decode() != "got chat":
                        break
                    print("got chat")
                
                if c.recv(MSG_SIZE).decode() == "chatlist received!":
                    print("chatlist received")
                    chatname = c.recv(MSG_SIZE).decode()
                    chat = None
                    
                    for i in chat_list:
                        if i.get_chatname() == chatname:
                            chat = i
                            c.send((chat.get_chatname() + " successfully accessed").encode())
                    if chat == None:
                        c.send("theres no chat like that how did this even happen".encode())
                
                else:
                    c.send("dude how".encode())
            
            else:
                if c.recv(MSG_SIZE).decode() == "create chat":
                    create_chat(clientsocket, addr, client_number)
        else:
            print("something went wrong")

        


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    client_number = 0
    while True:
        (c, c_addr)= s.accept()
        Thread(target=on_new_client, args=(c, c_addr, client_number)).start()
        client_number += 1