
import argparse
import json
import base64
import os
from idna import encode
from threading import Timer

passwords : dict = {} #Just a dictionary, where the passwords are saved

master_key : str = "Test_key" #The one key to encrypt them all

is_authenticated : bool = False

overtime : bool = False

configs : dict = {
    "save_directory_path": "C:\\ProgramData\\PV\\",  #The directory for the password file
    "save_file_name": "PV_passwords",  #The name of the password file
    "timeout_time": 600,  #The time in seconds until the programm automatically stops
}

configs_save_path : str = "C:\\ProgramData\\PV\\"  #not inside configs, as it should not change (otherwise we wont find it)
configs_file_name : str = "PV_configs"

def add_password(password_name: str, password: str):
    passwords[password_name] = password #that's it, just adding the password

def remove_password(password_name: str):
    passwords.pop(password_name, None) #similar just getting rid of the password 


def set_master_key(new_key: str, old_key: str):
    global master_key #otherwise it thinks it's a local one
    if master_key: 
        if old_key != master_key: #make sure the know the old key, before changing it
            print("old master key is wrong, or something like that (still working on this message)")
            return
    remove_password(master_key)
    master_key = new_key #set the new key
    add_password(master_key, master_key)

    
def print_password_names():
    for password_name in passwords:
        print(password_name)

def get_encrypted_passwords():
    passwords_string = json.dumps(passwords) #turn the dict into a str
    passwords_string_as_bytes = passwords_string.encode() #turn the str into bytes
    master_key_as_bytes = master_key.encode() #same with master key

    encrypted_passwords = bytes(
        passwords_string_as_bytes ^ master_key_as_bytes[i % len(master_key_as_bytes)]
        for i, passwords_string_as_bytes in enumerate(passwords_string_as_bytes) # XOR encryption (funny shit, I dont understand)
    )
    encrypted_passwords_as_base64 = base64.urlsafe_b64encode(encrypted_passwords)

    return encrypted_passwords_as_base64.decode() #back into text

#I have no clue, if this is secure (its not )
#It's probably not
#But who cares?
#...
#Wait you're reading this, why?
#Poor soul having to look at my code, I am deeply sorry

def get_decrypted_passwords(encrypted_passwords: str):

    encrypted_passwords_as_base64 = encrypted_passwords.encode() #turn it into bytes
    decrypted_passwords_as_bytes = base64.urlsafe_b64decode(encrypted_passwords_as_base64) 
    master_key_as_bytes = master_key.encode() #again make it into bytes
    decrypted_passwords_string = bytes(
        encrypted_byte ^ master_key_as_bytes[i % len(master_key_as_bytes)]
        for i, encrypted_byte in enumerate(decrypted_passwords_as_bytes) # still XOR (also dont understand this shit)
    )

    decrypted_passwords_string = decrypted_passwords_string.decode() #make it text
    #FIXME breaks here if master_key is wrong
    if not decrypted_passwords_string:
        return
    decrypted_passwords = json.loads(decrypted_passwords_string) #turn it back into a dict

    return decrypted_passwords 

def set_timeout_time(new_timeout_time: str):
    configs["timeout_time"] = int(new_timeout_time)
    print("Set timeout time to ", configs["timeout_time"])

def set_save_path(new_save_path: str):
    old_save_path = configs["save_directory_path"]
    delete_passwords_save_file()
    configs["save_directory_path"] = new_save_path
    try:
        save() #try to save 
    except OSError: #if for example we need admin rights
        print("unable to save at this path, returning to previous")
        configs["save_directory_path"] = old_save_path 
        save() #save at the old path
        

def set_file_name(new_file_name: str):
    old_file_name = configs["save_file_name"]
    delete_passwords_save_file()
    configs["save_file_name"] = new_file_name
    try:
        save() #try to save
    except OSError: #if unable to save, due to reasons
        print("unable to save with this name, returning to previous")
        configs["save_file_name"] = old_file_name #return and save with the old name
        save()

#used whe new path is set
def delete_passwords_save_file():
    if not os.path.exists(configs["save_directory_path"] + configs["save_file_name"]): #if there is no save file, there is nothing to delete
        return
    os.remove(configs["save_directory_path"] + configs["save_file_name"])

def get_password(password_name: str):
    if password_name in passwords: 
        return passwords[password_name] #just gets the password for the given name
    return "" #if password doesnt exist returns nothing 

def print_password(password_name: str):
    print("password_name: ", password_name) 
    print("password: ", get_password(password_name)) #prints, what is gets, could be ""


def save():
    os.makedirs(configs["save_directory_path"], exist_ok = True) #makes file/path if not there 
    print("saves at: ", configs["save_directory_path"] + configs["save_file_name"])
    file = open(configs["save_directory_path"] + configs["save_file_name"], "w") #opens the file for writing
    encrypted_passwords = get_encrypted_passwords() #encrypts the passwords
    file.write(encrypted_passwords) #writes the encrypted_passwords
    file.close() #closes file
    save_configs()


def load_configs():
    global configs
    if not os.path.exists(configs_save_path + configs_file_name): #if there is no config file, standard settings are used
        return
    file = open(configs_save_path + configs_file_name) #open file with read access
    configs = json.loads(file.read()) #get configs from file
    file.close() #close file

def save_configs():
    global configs
    os.makedirs(configs_save_path, exist_ok = True) #makes file/path if not there 
    file = open(configs_save_path + configs_file_name, "w") #opens the file with write access
    file.write(json.dumps(configs)) #writes the configs as string
    file.close() #closes file


def authenticate(entered_master_key: str):
    load_configs()
    global is_authenticated
    global master_key
    global passwords
    master_key = entered_master_key #apply key
    if not os.path.exists(configs["save_directory_path"] + configs["save_file_name"]): #if there is no save file, there are no passwors, therefore this is a new one
        is_authenticated = True #allow the key as the key chosen by the user
        return
    print("loads from: ", configs["save_directory_path"] + configs["save_file_name"]) 
    file = open(configs["save_directory_path"] + configs["save_file_name"], "r") #open file with read access
    loaded_passwords = file.read() #get encrypted passwords from file
    file.close() #close file
    if not loaded_passwords: #if there are no passwords in the file they must have been deleted
        is_authenticated = True #therefore it is fine if we authenticate them
        return
    decrypted_passwords = get_decrypted_passwords(loaded_passwords) #decrypt passwords
    if decrypted_passwords: #if they are not empty
        passwords = decrypted_passwords #set the passwords
    else: #if passwords are a dict, but empty
        is_authenticated = True #no passwords therefore doable
        return
    if master_key in passwords:
        if passwords[master_key] == master_key: #look for the master key in the passwords
                is_authenticated = True #if it is there accept teh user


def cli_entry_point(): #just the basic test function for now
    #TODO think of more useful help messages

    parser = argparse.ArgumentParser() #argparse setup
    subparsers = parser.add_subparsers(dest = "command")

    parser_master_key = subparsers.add_parser("authenticate", help = "Enter the master_key for authentification") #the authentication command
    parser_master_key.add_argument("master_key", help = "The master_key you chose")

    args = parser.parse_args()

    if args.command == "authenticate": #the authentication command has been called
        authenticate(args.master_key) #do authentication
    else:
        print("Please authenticate using   pv authenticate   ")
        return #ask for authentication
    if not is_authenticated:
        print("wrong master_key, or maybe I made a mistake")
        return #it has been wrong
    
    add_password(master_key, master_key) #add the master key password used for authentication (look above)
    
    print("Successfully authenticated!")
    print("Welcome to PV")


    #add all the commands
    parser_add_password = subparsers.add_parser("add", help = "Add a new password")
    parser_add_password.add_argument("password_name", help = "The name of the password")
    parser_add_password.add_argument("password", help = "The passworditself")

    parser_remove_password = subparsers.add_parser("remove", help = "Remove a password")
    parser_remove_password.add_argument("password_name", help = "The name of the password to delete")

    parser_set_master_key = subparsers.add_parser("new_master_key", help = "Set a new master key")
    parser_set_master_key.add_argument("new_master_key", help = "The new master key")
    parser_set_master_key.add_argument("old_master_key", help = "The old master key")

    parser_get_password_names_list = subparsers.add_parser("passwords", help = "Shows all password names")

    parser_get_password = subparsers.add_parser("password", help = "Get a password")
    parser_get_password.add_argument("password_name", help = "The name of the password")

    parser_set_timeout_time = subparsers.add_parser("timeout", help = "Set new timeout time")
    parser_set_timeout_time.add_argument("time", help = "The new timeout time")

    parser_set_save_path = subparsers.add_parser("save_path", help = "Configure the path to the save folder")
    parser_set_save_path.add_argument("path", help = "The path to the directory used for saving")

    parser_set_file_name = subparsers.add_parser("file_name", help = "Configure the save file name")
    parser_set_file_name.add_argument("name", help = "The new name for the file")

    t = Timer(configs["timeout_time"], timeout)
    t.start()

    while True: #just loop
        if overtime:
            print("inactive for too long")
            save()   #only breaks after an input, as input() blocks thread, but that is no problem as you are unable to do anything 
            break
        try:
            line = input("PV>\t") 
        except EOFError:
            break 
        if not line.strip():
            continue
        if line.strip() in ("exit", "quit"):
            print("Exiting PV") 
            save() #when exiting, save (only time they are being saved as of now)
            break
        
        try:

            t.cancel()
            args = parser.parse_args(line.split()) #get the arguments
            #the commands themselves
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
            elif args.command == "timeout":
                set_timeout_time(args.time)
            elif args.command == "save_path":
                set_save_path(args.path)
            elif args.command == "file_name":
                set_file_name(args.name)
            else:
                parser.print_help() #print help, in case they have no idea what they are doing (like me)

            t = Timer(configs["timeout_time"], timeout) #after commands, in case the timeput_time got changed
            t.start()
        except SystemExit:
            continue



def timeout():
    global overtime
    overtime = True
