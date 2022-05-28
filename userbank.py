from operator import contains
from cryptography.fernet import Fernet

user_list = []

# store and extract key for decrypting file
def write_key(key):
    with open("key.key","wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key","rb").read()

# decrypt a specific line in the file
def decrypt_string(key : Fernet, s):
    return key.decrypt(s.encode()).decode()

# encrypt a specific line in the file
def encrypt_string(key : Fernet, s):
    word = key.encrypt(s.encode())
    return word

# decrypt all data in database file
def decrypt_file(key, path):
    f = Fernet(key)
    with open(path, "r") as file:
        encrypted_data = file.read()
    
    for encrypted_line in encrypted_data.splitlines():
        user = encrypted_line.split(",")
        if len(user) == 2: # valid user
            user_list.append([decrypt_string(f,user[0]),decrypt_string(f,user[1])])

    print(user_list)

# update and re-encrypt all data in database file
def update_database(path, key):
    with open(path, "wb") as file:
        for user in user_list:
            f = Fernet(key)
            file.write(encrypt_string(f,user[0]))
            file.write(b',')
            file.write(encrypt_string(f,user[1]))
            file.write(b'\n')
    
# add new user to database
def add_user(path, key, name, password):
    if not invalid_user(True, name, password): # makes sure user is valid
        append_user(path, key, name, password)
        return "username fine"
    else:
        return "Username invalid"
    
# adds the new user to the actual database file and list
def append_user(path, key, name, password):
    user_list.append([name, password])
    with open(path, "ab") as file:
        f = Fernet(key)
        file.write(encrypt_string(f,name))
        file.write(b',')
        file.write(encrypt_string(f,password))
        file.write(b'\n')

# checks if potential new user is valid for addition
def invalid_user(signup, name, password):
    if contains(name,',') or contains(name,':') or contains(password,',') or name == "":
        print("Invalid name or password")
        return True
    else:
        if signup:
            for user in user_list:
                if user[0] == name:
                    return True
        return False

# confirms details for user logging in
def confirm_user(name, password):
    if not invalid_user(False, name, password):
        for user in user_list:
            if user[0] == name and user[1] == password:
                return True    
        return False

# as the name suggests
def clear_database():
    global user_list
    user_list = []
    with open(path, "wb") as file:
        file.write("")