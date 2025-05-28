
import argparse
import json
import base64
import os
from idna import encode

passwords : dict = {} #Just a dictionary, where the passwords are saved

master_key : str = "Test_key" #The one key to encrypt them all

save_directory_path : str = "E:\\"
save_file_name : str = "PV-save"

is_authenticated : bool = False

def add_password(password_name: str, password: str):
    passwords[password_name] = password #that's it, just adding the password




def remove_password(password_name: str):
    passwords.pop(password_name, None) #similar just getting rid of the password 
    #TODO add a check for the master_key before deleting

    

def set_master_key(new_key: str, old_key: str):
    global master_key #otherwise it thinks it's a local one
    if master_key: 
        if old_key != master_key: #make sure the know the old key, before changing it
            print("old master key is wrong, or something like that (still working on this message)")
            return
    remove_password(master_key)
    master_key = new_key #set the new key
    add_password(master_key, master_key)
    #TODO add an file update when changing the master_key as encryption changes
    
def print_password_names():
    for password_name in passwords:
        print(password_name)

def get_encrypted_passwords():
    passwords_string = json.dumps(passwords) #turn the dict into a str
    passwords_string_as_bytes = passwords_string.encode() #turn the str into bytes
    master_key_as_bytes = master_key.encode() #same with master key

    encrypted_passwords = bytes(
        passwords_string_as_bytes ^ master_key_as_bytes[i % len(master_key_as_bytes)]
        for i, passwords_string_as_bytes in enumerate(passwords_string_as_bytes) #funny shit, I dont understand
    )
    encrypted_passwords_as_base64 = base64.urlsafe_b64encode(encrypted_passwords) #make it safe for sending

    return encrypted_passwords_as_base64.decode() #back into text

#I have no clue, if this is secure
#It's probably not
#But who cares?
#...
#Wait you're reading this, why?
#Poor soul having to look at my code, I am deeply sorry

def get_decrypted_passwords(encrypted_passwords: str):
    encrypted_passwords_as_base64 = encrypted_passwords.encode() #turn it into bytes
    decrypted_passwords_as_bytes = base64.urlsafe_b64decode(encrypted_passwords_as_base64) #de-safe it? To be able to work on it
    master_key_as_bytes = master_key.encode() #again make it into bytes
    decrypted_passwords_string = bytes(
        encrypted_byte ^ master_key_as_bytes[i % len(master_key_as_bytes)]
        for i, encrypted_byte in enumerate(decrypted_passwords_as_bytes) #also dont understand this shit
    )

    decrypted_passwords_string = decrypted_passwords_string.decode() #make it text
    #FIXME breaks here if master_key is wrong
    decrypted_passwords = json.loads(decrypted_passwords_string) #turn it back into a dict

    return decrypted_passwords 


def save_passwords():
    os.makedirs(save_directory_path, exist_ok = True)
    print("saves at: ", save_directory_path + save_file_name)
    file = open(save_directory_path + save_file_name, "w")
    encrypted_passwords = get_encrypted_passwords()
    file.write(encrypted_passwords)
    file.close()

def load_passwords():
    global passwords
    os.makedirs(save_directory_path, exist_ok = True)
    print("loads from: ", save_directory_path + save_file_name)
    file = open(save_directory_path + save_file_name, "r")
    loaded_passwords = file.read()
    file.close()
    passwords = get_decrypted_passwords(loaded_passwords)
    if master_key in passwords:
        if passwords[master_key] == master_key:
                is_authenticated = True
                print("authenticated")
    
def get_password(password_name: str):
    if password_name in passwords:
        return passwords[password_name]
    return ""

def print_password(password_name: str):
    print("password_name: ", password_name)
    print("password: ", get_password(password_name))

def enter_master_key(entered_master_key: str):
    global master_key
    master_key = entered_master_key
    load_passwords()

def cli_entry_point(): #just the basic test function for now
    #TODO think of more useful help messages
    print("Welcome to PV")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = "command")

    parser_add_password = subparsers.add_parser("add", help = "Add a new password")
    parser_add_password.add_argument("password_name", help = "The name of the password")
    parser_add_password.add_argument("password", help = "The passworditself")

    parser_remove_password = subparsers.add_parser("remove", help = "Remove a password")
    parser_remove_password.add_argument("password_name", help = "The name of the password to delete")

    parser_set_master_key = subparsers.add_parser("new_master_key", help = "set new master key")
    parser_set_master_key.add_argument("new_master_key", help = "The new master key")
    parser_set_master_key.add_argument("old_master_key", help = "The old master key")

    parser_get_password_names_list = subparsers.add_parser("passwords", help = "Shows all password names")

    parser_get_password = subparsers.add_parser("password", help = "get a password")
    parser_get_password.add_argument("password_name", help = "The name of the password")

    parser_master_key = subparsers.add_parser("master_key", help = "Enter the master_key for authentification")
    parser_master_key.add_argument("master_key", help = "The master_key you chose")

    while True:
        try:
            line = input("PV>\t")
        except EOFError:
            break
        if not line.strip():
            continue
        if line.strip() in ("exit", "quit"):
            print("Exiting PV")
            break
        
        try:
            args = parser.parse_args(line.split())
            if args.command == "add":
                 add_password(args.password_name, args.password)
            elif args.command == "remove":
                 remove_password(args.password_name)
            elif args.command == "new_master_key":
                set_master_key(args.new_master_key, args.old_master_key)
            elif args.command == "passwords":
                print_password_names()
            elif args.command == "password":
                print_password(args.password_name)
            elif args.command == "master_key":
                enter_master_key(args.master_key)
            else:
                parser.print_help()
        except SystemExit:
            continue

    


  #  args = parser.parse_args()
    

    
    
    save_passwords()

