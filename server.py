import socket
from threading import Thread

MSG_SIZE = 1024
PORT = 1234
HOST = socket.gethostname()

chat_list = []
clients_list = []


class Client:
    def __init__(self, socket, addr, name):
        self.socket = socket
        self.addr = addr
        self.name = name

    def get_socket(self):
        return self.socket

    def get_addr(self):
        return self.addr

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def send(self, message):
        self.socket.send(message)
    
    def recv(self, msg_size):
        return self.socket.recv(msg_size)


class Chat:
    def __init__(self, chatname):
        self.chatname = chatname
        self.clients = []
        self.clientnames = []

    def add_participant(self, new_participant):
        self.clients.append(new_participant)
        self.clientnames.append(new_participant.get_name())
        participants = self.participants_str()
        for client in self.clients:
            client.send(f"newparticipant{participants};{new_participant.get_name()} has joined the chat!".encode())
        thread = Thread(target = self.handle,
                                args = (new_participant,))
        thread.start()

    def participants_str(self):
        self.clientnames.sort()
        participants = ""
        for name in self.clientnames[:-1]:
            participants += (name + ", ")
        participants += self.clientnames[-1]
        return participants
        
    def handle(self, client):
        print(f"new connection {client.get_addr()}")
        connected = True
        
        while connected:
            # receive message
            message = client.recv(MSG_SIZE)

            if message[:6] == "invite":
                invited = client.recv(MSG_SIZE).decode()
                result = self.invite(client.get_name(), invited)
                client.send(result.encode())
            else:
                # broadcast message
                for member in self.clients:
                    member.send(message)

    def invite(self, inviter, invited):
        for client in clients_list:
            if client.get_name() == invited:
                client.send(f"invited{self.chatname};{inviter}")
                response = client.recv(MSG_SIZE).decode()
                if response == "ok":
                    self.add_participant(client)
                    return "Invitation accepted!"
                else:
                    return "Invitation declined"
        return "requested member not online"

    def get_chatname(self):
        return self.chatname


def create_chat(client):
    print("creating chat")
    chatname = client.recv(MSG_SIZE).decode()
    print("creating " + chatname)
    new_chat = Chat(chatname)
    chat_list.append(new_chat)
    client.send("chat created successfully".encode())
    client.recv(MSG_SIZE)
    new_chat.add_participant(client)


def join_chat(client):
    global chat_list

    print("joining chat")
    client.send(str(len(chat_list)).encode())
    
    if client.recv(MSG_SIZE).decode() == "got chatnum":
        if chat_list:
            
            for i in chat_list:
                c.send(i.get_chatname().encode())
                if client.recv(MSG_SIZE).decode() != "got chat":
                    break
                print("got chat")
            
            if client.recv(MSG_SIZE).decode() == "chatlist received!":
                print("chatlist received")
                chatname = c.recv(MSG_SIZE).decode()
                chat = None
                
                for i in chat_list:
                    if i.get_chatname() == chatname:
                        chat = i
                        client.send((chat.get_chatname() + " successfully accessed").encode())
                        client.recv(MSG_SIZE)
                        chat.add_participant(client)
                if not chat:
                    c.send("theres no chat like that how did this even happen".encode())
            
            else:
                client.send("dude how".encode())
        else:
            if client.recv(MSG_SIZE).decode() == "create chat":
                create_chat(client)
    else:
        print("something went wrong")


def on_new_client(client):
    client.send(client.get_name().encode())
    msg = client.recv(MSG_SIZE).decode()

    if msg == "create chat":
        create_chat(client)
    
    elif msg == "join chat":
        join_chat(client)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    client_number = 0
    while True:
        (c, c_addr)= s.accept()
        new_name = "User" + str(client_number)
        new_client = Client(c, c_addr, new_name)
        Thread(target=on_new_client, args=(new_client,)).start()
        clients_list.append(new_client)
        client_number += 1