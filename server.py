from ctypes.wintypes import MSG
import socket
import threading
from cryptography.fernet import Fernet
import time
import userbank

MSG_SIZE = 1024
PORT = 1234
HOST = "0.0.0.0"

# lists of clients and chats in the whole server
chat_list = []
clients_list = []

# variables for checking user database
path = "data.dt"
key = userbank.load_key()

# this class defines users connected to the server
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

# this class defines existing chatrooms
class Chat:
    # initialize new chat with name and empty list of participants
    def __init__(self, chatname):
        self.chatname = chatname
        self.clients = []
        self.clientnames = []
        self.chat_history = ":chathistory"

    def get_chatname(self):
        return self.chatname

    # add new participant to current chatroom
    def add_participant(self, new_participant):
        self.clients.append(new_participant)
        self.clientnames.append(new_participant.get_name())
        participants = self.participants_str() # update str participant list to send to client (to appear at top of screen)
        print(participants)
        if len(self.chat_history) > 12:
            new_participant.send(self.chat_history.encode())

        message = f":newparticipant{participants};{new_participant.get_name()} has joined the chat!"
        self.chat_history += message + "\n"
        for client in self.clients:
            # send the existing participants an update, including new participant list
            client.send(message.encode())
        self.handle(new_participant) # handle outgoing messages from new participant

    # remove certain participant from current chatroom
    def remove_participant(self, participant):
        self.clients.remove(participant)
        self.clientnames.remove(participant.get_name()) # update participant list to send to client (to appear at top of screen)
        participants = self.participants_str()
        print(participants)
        message = f":participantleft{participants};{participant.get_name()} has left the chat!"
        self.chat_history += message + "\n"
        for client in self.clients:
            client.send(message.encode())

    # creates str object of alphabetically sorted list of participants, to appear at the top of client screen
    def participants_str(self):
        self.clientnames.sort()
        participants = ""
        if len(self.clientnames) > 0:
            for name in self.clientnames[:-1]:
                participants += (name + ", ")
            participants += self.clientnames[-1]
        return participants
        
    # function to handle outgoing messages from certain participant
    def handle(self, client): 
        print(f"new connection {client.get_addr()}")
        chatroom = True # participant is currently in the chatroom
        
        while chatroom:
            # receive outgoing message
            message = client.recv(MSG_SIZE)
            
            if message.decode()[:6] == ":leave":
                # handle participant quitting
                client.send(":left".encode())
                self.remove_participant(client)
                chatroom = False
                on_new_client(client.get_socket(), client.get_addr(), False, client)

            else:
                # broadcast message to other participants
                self.chat_history += message.decode() + "\n"
                for member in self.clients:
                    member.send(message)

# handle client request to create chat
def create_chat(client):
    print("creating chat")
    chatname = client.recv(MSG_SIZE).decode() # receive the new chat's name
    if chatname == ":leave": # handle unexpected request to quit
        client.get_socket().close()
        clients_list.remove(client)
    else:
        # create requested chat and add client to it
        print("creating " + chatname)
        new_chat = Chat(chatname)
        chat_list.append(new_chat)
        client.send("chat created successfully".encode())
        client.recv(MSG_SIZE)
        new_chat.add_participant(client)

# handle client request to join chat
def join_chat(client):
    global chat_list

    print("joining chat")
    client.send(str(len(chat_list)).encode()) # send number of open chats to client
    
    if client.recv(MSG_SIZE).decode() == "got chatnum":
        if chat_list:
            for i in chat_list:
                # send client the name of every open chat
                client.send(i.get_chatname().encode())
                if client.recv(MSG_SIZE).decode() != "got chat":
                    break
                print("got chat")
            client.send("done?".encode())
            
            if client.recv(MSG_SIZE).decode() == "chatlist received!":
                print("chatlist received")
                chatname = client.recv(MSG_SIZE).decode() # receive from client requested chatroom to join

                if chatname == ":leave": # handle unexpected request to quit
                    client.get_socket().close()
                    clients_list.remove(client)
                else:
                    requested = None
                    for chat in chat_list:
                        # find which chat is the requested one
                        if chat.get_chatname() == chatname:
                            requested = chat
                            client.send((chat.get_chatname() + " successfully accessed").encode())
                            client.recv(MSG_SIZE) # receives "great"
                            requested.add_participant(client)

                    if not requested:
                        client.send("theres no chat like that how did this even happen".encode())
            else:
                client.send("dude how".encode())
        else:
            # handles situation where there are no open chats
            response = client.recv(MSG_SIZE).decode()
            if response == "create chat":
                create_chat(client)
            elif response == ":leave":
                client.get_socket().close()
                clients_list.remove(client)      
    else:
        print("something went wrong")
        client.get_socket().close()
        clients_list.remove(client)

# handles new client joining & client switching chat
def on_new_client(c, c_addr, first_go, existing):
    # variables for accessing user database are global
    global key
    global path

    try:
        print("new client")
        if first_go: # client connecting now (not leaving a previous chatroom)
            
            login_or_signup = c.recv(MSG_SIZE).decode()
            
            if login_or_signup == ":login":
                print("got login")
                c.send("got login".encode())
                while True:
                    # receive username & password until correct
                    new_name = c.recv(MSG_SIZE).decode()
                    if new_name == ":login":
                        c.send("got login".encode())
                        new_name = c.recv(MSG_SIZE).decode()
                    elif new_name == ":signup":
                        login_or_signup = new_name
                        break
                    print("got name")
                    c.send("got name".encode())
                    new_pass = c.recv(MSG_SIZE).decode()
                    print("got pass")
                    if userbank.confirm_user(new_name, new_pass):
                        print("login success")
                        c.send("Login successful".encode())
                        break
                    else:
                        print("login fail")
                        c.send("Login failed".encode())
            
            if login_or_signup == ":signup":
                print("signup.")
                c.send("got signup".encode())
                while True:
                    # receive username & password until valid
                    new_name = c.recv(MSG_SIZE).decode()
                    print("got "+ new_name)
                    c.send("got name".encode())
                    new_pass = c.recv(MSG_SIZE).decode()
                    print(new_pass)
                    result = userbank.add_user(path, key, new_name, new_pass)
                    if result == "Username invalid":
                        c.send(result.encode())
                    else:
                        print("signed up successfully")
                        c.send(result.encode())
                        break

            
            # create Client object for new client and add them to server-wide client list
            client = Client(c, c_addr, new_name)
            clients_list.append(client)

        else:
            # if client is previously connected, they already have a Client object
            client = existing

        # receive decision to create or join a chat        
        msg = c.recv(MSG_SIZE).decode()

        if msg == "create chat":
            create_chat(client)
        
        elif msg == "join chat":
            join_chat(client)

        elif msg == ":leave":
            print(clients_list)
            client.get_socket().close()
            clients_list.remove(client)
            print(clients_list)

        else:
            print(msg)

    except Exception as uhoh:
        # all exceptions throughout the code are caught here
        print(uhoh)
        c.close()


def main():
    global key
    global path
    userbank.decrypt_file(key,path) # access encrypted data in database
    key = Fernet.generate_key()
    userbank.write_key(key)
    userbank.update_database(path,key) # update encryption in database with new key

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            # connect to new clients as long as server runs
            (c, c_addr) = s.accept()
            threading.Thread(target=on_new_client, args=(c,c_addr,True,None)).start() # start thread to handle each new client

if __name__ == "__main__":
    main()