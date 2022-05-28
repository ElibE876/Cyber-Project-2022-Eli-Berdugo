from ctypes.wintypes import MSG
import socket
import threading
from cryptography.fernet import Fernet
import userbank

MSG_SIZE = 1024
PORT = 1234
HOST = "0.0.0.0"

'''lock = threading.Lock()'''

chat_list = []
clients_list = []

running = True
path = "data.dt"
key = userbank.load_key()

class Client:
    def __init__(self, socket, addr, name):
        self.socket = socket
        self.addr = addr
        self.name = name
        '''self.inchat = False'''

    def get_socket(self):
        return self.socket

    def get_addr(self):
        return self.addr

    def set_name(self, name):
        self.name = name

    '''def get_inchat(self):
        return self.inchat

    def set_inchat(self, param):
        self.inchat = param'''

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
        print(participants)
        for client in self.clients:
            client.send(f":newparticipant{participants};{new_participant.get_name()} has joined the chat!".encode())
        self.handle(new_participant)

    def remove_participant(self, participant):
        self.clients.remove(participant)
        self.clientnames.remove(participant.get_name())
        participants = self.participants_str()
        print(participants)
        if len(self.clients) > 0:
            for client in self.clients:
                client.send(f":participantleft{participants};{participant.get_name()} has left the chat!".encode())


    def participants_str(self):
        self.clientnames.sort()
        participants = ""
        for name in self.clientnames[:-1]:
            participants += (name + ", ")
        participants += self.clientnames[-1]
        return participants
        
    def handle(self, client): 
        print(f"new connection {client.get_addr()}")
        '''client.set_inchat(True)'''
        chatroom = True
        
        while chatroom:
            # receive message
            '''if client.get_inchat():'''
            message = client.recv(MSG_SIZE)
            if message.decode()[:6] == ":leave":
                self.remove_participant(client)
                client.get_socket().close()
                chatroom = False
                '''elif message.decode()[:7] == ":invite":
                    client.set_inchat(False)
                    print("received invite req")
                    invited = client.recv(MSG_SIZE).decode()
                    client.send("not sure why this is needed".encode())
                    result = self.invite(client.get_name(), invited)
                    client.send(result.encode())
                    client.set_inchat(True)'''
            else:
                # broadcast message
                for member in self.clients:
                    '''if member.get_inchat():'''
                    member.send(message)

    '''def invite(self, inviter, invited):
        print('invite func')
        print(invited)
        for client in clients_list:
            if client.get_name() == invited and client.get_name() not in self.clientnames:
                lock.acquire()
                client.send(f":invited{self.chatname};{inviter}".encode())
                response = client.recv(MSG_SIZE).decode()
                print("received invited")
                while response != "invited":
                    client.send(f":invited{self.chatname};{inviter}".encode())
                    response = client.recv(MSG_SIZE).decode()
                if response == "ok":
                    lock.release()   
                    self.add_participant(client)
                    return "Invitation accepted!"
                elif response == "no":
                    lock.release() 
                    return "Invitation declined"
        print("not online")
        return "Requested user is not online"'''

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
                client.send(i.get_chatname().encode())
                if client.recv(MSG_SIZE).decode() != "got chat":
                    break
                print("got chat")
            
            if client.recv(MSG_SIZE).decode() == "chatlist received!":
                print("chatlist received")
                chatname = client.recv(MSG_SIZE).decode()
                chat = None
                
                for i in chat_list:
                    if i.get_chatname() == chatname:
                        chat = i
                        client.send((chat.get_chatname() + " successfully accessed").encode())
                        client.recv(MSG_SIZE)
                        chat.add_participant(client)
                if not chat:
                    client.send("theres no chat like that how did this even happen".encode())
            
            else:
                client.send("dude how".encode())
        else:
            if client.recv(MSG_SIZE).decode() == "create chat":
                create_chat(client)
    else:
        print("something went wrong")


def on_new_client(c,c_addr):
    global key
    global path
    try:
        print("new client")
        login_or_signup = c.recv(MSG_SIZE).decode()
        if login_or_signup == "signup":
            c.send("got signup".encode())
            while True:
                new_name = c.recv(MSG_SIZE).decode()
                print("got "+new_name)
                c.send("got name".encode())
                new_pass = c.recv(MSG_SIZE).decode()
                print(new_pass)
                result = userbank.add_user(path, key, new_name, new_pass)
                if result == "Username invalid":
                    c.send(result.encode())
                else:
                    print("checked ok")
                    c.send(result.encode())
                    break
        elif login_or_signup == "login":
            print("got login")
            c.send("got login".encode())
            while True:
                new_name = c.recv(MSG_SIZE).decode()
                if new_name == "login":
                    c.send("got login".encode())
                    new_name = c.recv(MSG_SIZE).decode()
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
        else:
            print(login_or_signup)
                

        client = Client(c, c_addr, new_name)
        clients_list.append(client)
        msg = client.recv(MSG_SIZE).decode()

        if msg == "create chat":
            create_chat(client)
        
        elif msg == "join chat":
            join_chat(client)

        else:
            print(msg)

    except Exception as burh:
            print(burh)
            c.close()


def main():
    global running
    global key
    global path
    userbank.decrypt_file(key,path)
    key = Fernet.generate_key()
    userbank.write_key(key)
    userbank.update_database(path,key)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while running:
            (c, c_addr) = s.accept()
            threading.Thread(target=on_new_client, args=(c,c_addr)).start()

if __name__ == "__main__":
    main()