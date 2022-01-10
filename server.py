import socket
from threading import Thread

MSG_SIZE = 1024
PORT = 1234
HOST = socket.gethostname()

chat_list = []

class Chat:
    def __init__(self, chatname):
        self.chatname = chatname
        self.clientnames = []
        self.clients = []

    def add_participant(self, new_participant, addr, p_name):
        self.clients.append(new_participant)
        self.clientnames.append(p_name)
        participants = self.participants_str()
        for client in self.clients:
            client.send(f"newparticipant{participants};{p_name} has joined the chat!".encode())
        thread = Thread(target = self.handle,
                                args = (new_participant, addr))
        thread.start()

    def participants_str(self):
        self.clientnames.sort()
        participants = ""
        for member in self.clientnames[:-1]:
            new = member + ", "
            participants += new
        participants += self.clientnames[-1]
        return participants
        
    def handle(self, clientsock, addr):
        print(f"new connection {addr}")
        connected = True
        
        while connected:
            # receive message
            message = clientsock.recv(MSG_SIZE)

            # broadcast message
            for client in self.clients:
                client.send(message)

    def get_chatname(self):
        return self.chatname

def create_chat(clientsocket, addr, clientname):
    print("creating chat")
    chatname = clientsocket.recv(MSG_SIZE).decode()
    print("creating " + chatname)
    new_chat = Chat(chatname)
    chat_list.append(new_chat)
    clientsocket.send("chat created successfully".encode())
    clientsocket.recv(MSG_SIZE)
    new_chat.add_participant(clientsocket, addr, clientname)

def on_new_client(clientsocket, addr, client_number):
    global chat_list
    c_name = "User" + str(client_number)
    clientsocket.send(c_name.encode())
    msg = clientsocket.recv(MSG_SIZE).decode()

    if msg == "create chat":
        create_chat(clientsocket, addr, c_name)
    
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
                            c.recv(MSG_SIZE)
                            chat.add_participant(clientsocket, addr, c_name)
                    if chat == None:
                        c.send("theres no chat like that how did this even happen".encode())
                
                else:
                    c.send("dude how".encode())
            
            else:
                if c.recv(MSG_SIZE).decode() == "create chat":
                    create_chat(clientsocket, addr, c_name)
        else:
            print("something went wrong")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    client_number = 1
    while True:
        (c, c_addr)= s.accept()
        Thread(target=on_new_client, args=(c, c_addr, client_number)).start()
        client_number += 1