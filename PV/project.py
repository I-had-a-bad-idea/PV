import argparse
import json
import os
import cryptography.exceptions
from idna import encode
import base64
import pyperclip
from threading import Timer
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
import getpass


passwords : dict = {} #Just a dictionary, where the passwords are saved

master_key : str #The one key to encrypt them all

configs : dict = {
    "save_directory_path": "C:\\ProgramData\\PV\\",  #The directory for the password file
    "save_file_name": "PV_passwords",  #The name of the password file
    "timeout_time": 600,  #The time in seconds until the programm automatically stops
    "salt": None,  #the salt used for the user
    "power of iterations": 18,  #the power of 2 which is used as iterations for the kdf

}

nonce : bytes #number used once, used once for encryption, so it is not the same every time, which would make it easy to decrypt

VERSION : str = "1.4.1" #used to check what the file version is, so we dont try to load things that are not there

#oh look a version

configs_save_path : str = "C:\\ProgramData\\PV\\"  #not inside configs, as it should not change (otherwise we wont find it)
configs_file_name : str = "PV_configs"


def add_password(password_name: str, password: str):
    passwords[password_name] = password #that's it, just adding the password
    if password_name != master_key:
        print("Added ", password_name)

def remove_password(password_name: str):
    passwords.pop(password_name, None) #similar just getting rid of the password
    print("Removed ", password_name) 

def set_master_key(new_key: str, old_key: str):
    global master_key #otherwise it thinks it's a local one
    if master_key: 
        if old_key != master_key: #make sure the know the old key, before changing it
            print("Old master key is wrong")
            return
    remove_password(master_key) #remove old master_key from dict
    master_key = new_key #set the new key
    add_password(master_key, master_key) #add new one needed for authentification
    print("Changed master key")

def print_password_names():
    for password_name in passwords:
        if password_name != master_key: #We dont want to print the master key out, else everyone can see it
            print(password_name)

def set_iterations_power(iteration_amount: str):
    configs["power of iterations"] = int(iteration_amount)
    print("Set number of iterations to 2 **", iteration_amount)

#creates salt and encryption key
def derive_key() -> bytes:
    if not configs["salt"]:
        configs["salt"] = os.urandom(32)  #make random salt if not already there

    kdf = Scrypt(
        salt = configs["salt"],
        length = 32,  # 32 bytes = 256 bits
        n = 2 ** configs["power of iterations"],  #number of iterations
        r = 8, #block size
        p = 1, #parallelization 
        backend = default_backend()
    )
    return kdf.derive(master_key.encode())  #derieve the key from the given master key

def get_encrypted_passwords():
    global nonce

    passwords_string : str = json.dumps(passwords) #turn the dict into a str
    passwords_string_as_bytes : bytes = passwords_string.encode() #turn the str into bytes
    master_key_as_bytes : bytes = derive_key() #get key

    aesgcm : AESGCM = AESGCM(master_key_as_bytes) #create AESGCM with key
    
    nonce = os.urandom(32) #create new nonce every session
    
    encrypted_passwords : bytes = aesgcm.encrypt(nonce, passwords_string_as_bytes, None) #encrypt passwords
    encrypted_passwords_as_base64 : str = base64.b64encode(encrypted_passwords).decode() #convert them to make them safe for storing

    return encrypted_passwords_as_base64


#I have no clue, if this is secure 
#I mean its a good encryption thingy
#Who cares. I warned them if its not    #yeah, but that doesnt make it any better
#...
#Wait you're reading this, why?
#Poor soul having to look at my code, I am deeply sorry

#Should I delete this joke?
#Well, I am too lazy to do it now, so I will just leave it here


def get_decrypted_passwords(encrypted_passwords: str):
    global nonce

    master_key_deriviate : bytes = derive_key() #get key
    encrypted_passwords_as_bytes : bytes = base64.b64decode(encrypted_passwords) #convert them into something you can work with

    aesgcm : AESGCM = AESGCM(master_key_deriviate) 

    try:
        decrypted_passwords = aesgcm.decrypt(nonce, encrypted_passwords_as_bytes, None) #decrypt passwords
    except cryptography.exceptions.InvalidTag: #if invalid master_key
        return {"wrong": "master_key"} #just return some dict, where there isnt the master_key, as that is being checked later
                #cant be an emty one, as otherwise it sees it as a new user

    decrypted_passwords_string : str = decrypted_passwords.decode() #make it text
    if not decrypted_passwords_string: #if there are none
        return
    decrypted_passwords = json.loads(decrypted_passwords_string) #turn it back into a dict

    return decrypted_passwords 


def set_timeout_time(new_timeout_time: str):
    configs["timeout_time"] = int(new_timeout_time) #convert to int as waiting "600" can be difficult
    print("Set timeout time to ", configs["timeout_time"])  #possibly something else, this is why we dont use the argument


def set_save_path(new_save_path: str):
    old_save_path = configs["save_directory_path"] #save the old path to be able to revert
    delete_file(configs["save_directory_path"] + configs["save_file_name"])  #delete the old file, as to not have dozens of files lying around
    configs["save_directory_path"] = new_save_path #set new path to try and save
    try:
        save() #try to save  
    except OSError: #if for example we need admin rights
        print("Unable to save at this path, returning to previous")
        configs["save_directory_path"] = old_save_path 
        save() #save at the old path
        return
    print("Successfully changed save path to ", configs["save_directory_path"]) #let the user know
        

def set_file_name(new_file_name: str):
    old_file_name = configs["save_file_name"] #save the old name to be able to revert
    delete_file(configs["save_directory_path"] + configs["save_file_name"])   #delete the old file, as to not have dozens of files lying around
    configs["save_file_name"] = new_file_name  #set new name to try and save
    try:
        save() #try to save
    except OSError: #if unable to save, due to reasons 
        print("Unable to save with this name, returning to previous")
        configs["save_file_name"] = old_file_name #return and save with the old name
        save()
        return
    print("Successfully changed file name to ", configs["save_file_name"]) #let the user know


def cleanup():
    delete_file(configs["save_directory_path"] + configs["save_file_name"]) #delete passwords
    delete_file(configs_save_path + configs_file_name)  #delete configs

    print("Deleted all files made by PV")
    print("Thank you for using PV")

#helper function only
def get_password_(password_name: str):
    if password_name in passwords: 
        return passwords[password_name] #just gets the password for the given name
    return "" #if password doesnt exist returns nothing 

#the actual function you are looking for
def get_password(password_name: str, _print: bool):
    pyperclip.copy(get_password_(password_name)) #copies, what it gets, could be "" (nothing)
    if _print:
        print("Password_name: ", password_name) 
        print("Password: ", get_password_(password_name)) #prints, what it gets, could be "" (nothing)
    else:
        print("Copied ", password_name, " to clipboard")


def get_save_dict() -> dict:
    save_data : dict = {}

    save_data["version"] = VERSION       #the version of the save file, used to compare to current version
    save_data["passwords"] = get_encrypted_passwords()
    save_data["nonce"] = base64.b64encode(nonce).decode()     #have to do this because nonce is bytes

    return save_data

def get_configs_save_dict() -> dict:
    configs_save : dict = {}

    configs_save = configs

    #TODO think about removing this. Only usecase is backwards compatibility
    configs_save["salt"] = base64.b64encode(configs["salt"]).decode()  #salt is bytes and has to be converted to str to save
    configs_save["nonce"] = base64.b64encode(nonce).decode() #same as salt

    return configs_save

def save():

    save_data : dict = get_save_dict()

    print("Saves at: ", configs["save_directory_path"] + configs["save_file_name"])  #let them know where it was saved
    write_data_to_file(save_data, configs["save_directory_path"], configs["save_file_name"]) #actually save

    save_configs() #save configs because maybe they changed

    print("Saved") #tell them the saving is completed


def load_configs():
    global configs

    configs_in_file = read_data_from_file(configs_save_path + configs_file_name) #laod the configs from the file

    if not configs_in_file: #if no configs were saved we use the standard ones
        return
    
    configs = json.loads(configs_in_file) #set the configs

    configs["salt"] = base64.b64decode(configs["salt"]) #salt is bytes, we need to make it back into bytes from str
    configs["nonce"] = base64.b64decode(configs["nonce"]) #same as salt


    ## here are configs, that were added later and have to be checked when loading

    if not "power of iterations" in configs:
        configs["power of iterations"] = 18

#TODO maybe just remove this function, as it turned into a one-liner
def save_configs():
    global configs

    write_data_to_file(get_configs_save_dict(), configs_save_path, configs_file_name)


def export(directory_path: str, file_name: str):
    save_data : dict = get_save_dict() #gets the passwords, nonce, version, etc.

    save_data["configs"] = get_configs_save_dict()  #adds the configs to the save data, so they can be imported later

    write_data_to_file(save_data, directory_path, file_name)
    print("Exported to ", directory_path + file_name)

def import_(path: str):
    global configs
    global passwords
    global nonce
    global master_key

    if not os.path.exists(path):
        print("File does not exist")
        return
    
    print("Imports from: ", path)
    loaded_data = read_data_from_file(path) #load the data from the file
    
    if not loaded_data: #if the file was empty
        print("File is empty")
        return
    try:
        loaded_data = json.loads(loaded_data) #load the data as json
        loaded_passwords = loaded_data["passwords"]
        nonce = base64.b64decode(loaded_data["nonce"])  #nonce is bytes and has to be converted to bytes from str
        configs = loaded_data["configs"]  #configs are saved in the file, so we
        configs["salt"] = base64.b64decode(configs["salt"])  #salt is bytes, we need to make it back into bytes from str
    except TypeError:
        print("Not a valid file")
        return
    
    old_master_key = master_key  #save the old master key to be able to revert it, if the import fails
    master_key = getpass.getpass("Enter master key for imported passwords: ")   #ask for the master key to be able to decrypt the passwords
    
    decrypted_passwords = get_decrypted_passwords(loaded_passwords)

    if not decrypted_passwords: #if the enrcypted passwordsare empty
        print("No passwords in file")
        return

    if not master_key in decrypted_passwords:
        print("Wrong master key")
        master_key = old_master_key  #revert to old master key, as the new given was wrong
        return
    if not decrypted_passwords[master_key] == master_key: #if the master_key is in the dictionary
        print("Wrong master key")
        master_key = old_master_key
        return
    passwords = decrypted_passwords
    
    print("Import successful")
    

#returns true if correct master key
def authentification() -> bool:
    global master_key
    global passwords
    global nonce

    load_configs() #first load configs to have correct path, salt, iterations, etc.


    if not os.path.exists(configs["save_directory_path"] + configs["save_file_name"]): #if the save file is not there
        print("You do not have any passwords yet. Please think of a master key to use for PV")
        master_key = getpass.getpass("Enter the master key you want to use: ")

        return True 
    
    print("Passwords found. Please enter your master key to use PV.") #we did find a file here
    master_key = getpass.getpass("Enter your master key: ")
    
    print("Loads from: ", configs["save_directory_path"] + configs["save_file_name"]) #let them know from where the passwords are loaded
    loaded_data = read_data_from_file(configs["save_directory_path"] + configs["save_file_name"]) #load passwords

    try:
        loaded_data = json.loads(loaded_data) 
        loaded_passwords = loaded_data["passwords"]
        nonce = base64.b64decode(loaded_data["nonce"])  #nonce is bytes and has to be converted to bytes from str
    
    except TypeError:   #if they dont have a version newer than the one where versions were added
        loaded_passwords = loaded_data
        nonce = configs["nonce"]

    if not loaded_passwords: #if the file was empty
        return True
    
    
    decrypted_passwords = get_decrypted_passwords(loaded_passwords)

    if not decrypted_passwords: #if the enrcypted passwordsare empty
        return True
    
    passwords = decrypted_passwords

    if master_key in passwords:
        if passwords[master_key] == master_key: #if the master_key is in the dictionary
            return True

    return False


def cli_entry_point(): 
    welcome : str = r"""
================================
 Welcome to PV
-----------------------
 Simple. Local. Secure.
-----------------------
 github.com/I-had-a-bad-idea/PV
================================
"""    

    print(welcome)

    parser = argparse.ArgumentParser() #argparse setup
    subparsers = parser.add_subparsers(dest = "command")
   
    if not authentification():
        print("Wrong master_key")
        return #it has been wrong
    

    add_password(master_key, master_key) #add the master key password used for authentication (look above)
    
    print("Successfully authenticated!")


    #add all the commands
    add_commands(subparsers)


    t = Timer(configs["timeout_time"], timeout)
    t.start()

    while True: #just loop
        try:
            line = input("PV>\t") 
        except EOFError:
            break 
        if not line.strip():
            continue
        if line.strip().lower() in ["exit", "quit"]:
            print("Exiting PV") 
            save() #when exiting, save (only time they are being saved as of now)
            break
        
        try:
            t.cancel()
            args = parser.parse_args(line.split()) #get the arguments
            #the commands themselves
            args.command = args.command.lower()  #convert the command to lower case to not care about capital letters

            if args.command == "add":
                 add_password(args.password_name, args.password)
            elif args.command == "remove":
                 remove_password(args.password_name)
            elif args.command == "new_master_key":
                old_master_key = getpass.getpass("Enter old master key: ")
                if old_master_key != master_key:  #check if the old master key is correct
                    print("Old master key is wrong")
                    continue
                new_master_key = getpass.getpass("Enter new master key: ")
                set_master_key(new_master_key, old_master_key)
            elif args.command == "passwords":
                print_password_names()
            elif args.command == "password":
                get_password(args.password_name, args.print)
            elif args.command == "timeout":
                set_timeout_time(args.time)
            elif args.command == "save_path":
                set_save_path(args.path)
            elif args.command == "file_name":
                set_file_name(args.name)
            elif args.command == "iterations":
                set_iterations_power(args.power)
            elif args.command == "export":
                export(args.directory_path, args.file_name)
            elif args.command == "import":
                import_(args.path)
            elif args.command == "cleanup":
                cleanup()
                break
            else:
                parser.print_help() #print help, in case they have no idea what they are doing    like me :) 

            t = Timer(configs["timeout_time"], timeout) #after commands, in case the timeout_time got changed
            t.start()
        except SystemExit:
            continue
    t.cancel()

   

#for overtime. Connected to timer t in cli_entry_point()
def timeout():
    print("\nTimeout reached, exiting PV")
    save()  #save before exiting, so they dont lose their passwords
    os._exit(0)  #exit the programm


def delete_file(path: str):
    if not os.path.exists(path):
        return
    os.remove(path)

def write_data_to_file(data, directory_path: str, file_name: str):
    os.makedirs(directory_path, exist_ok = True)
    
    file = open(directory_path + file_name, "w") #opens the file with write access
    file.write(json.dumps(data)) #writes the configs as string
    file.close() #closes file


def read_data_from_file(path_to_file: str) -> str:
     if not os.path.exists(path_to_file):
         return ""  #return nothing if file doesnt exist
     file = open(path_to_file, "r") #open file with read access
     data = file.read() #read data
     file.close() #close file

     return data #return data from file
     
#adds all commands
def add_commands(subparsers):

    parser_add_password = subparsers.add_parser("add", help = "Add a new password")
    parser_add_password.add_argument("password_name", help = "The name of the password, which will be used for all commands")
    parser_add_password.add_argument("password", help = "The password itself")

    parser_remove_password = subparsers.add_parser("remove", help = "Remove a password")
    parser_remove_password.add_argument("password_name", help = "The name of the password to delete")

    parser_set_master_key = subparsers.add_parser("new_master_key", help = "Set a new master key")

    parser_get_password_names_list = subparsers.add_parser("passwords", help = "Shows all password names")

    parser_get_password = subparsers.add_parser("password", help = "Get a password")
    parser_get_password.add_argument("password_name", help = "The name of the password")
    parser_get_password.add_argument("--print", action = "store_true", help = "Print the password insteead of copying it to the clipboard")

    parser_set_timeout_time = subparsers.add_parser("timeout", help = "Set new timeout time")
    parser_set_timeout_time.add_argument("time", help = "The new timeout time")

    parser_set_save_path = subparsers.add_parser("save_path", help = "Configure the path to the save folder")
    parser_set_save_path.add_argument("path", help = "The path to the directory used for saving")

    parser_set_file_name = subparsers.add_parser("file_name", help = "Configure the save file name")
    parser_set_file_name.add_argument("name", help = "The new name for the file")

    parser_set_iteration_power = subparsers.add_parser("iterations", help = "Set the power of 2 used as iterations when generating key")
    parser_set_iteration_power.add_argument("power", help = "The power itself (only a full, positive number)")

    parser_cleanup = subparsers.add_parser("cleanup", help = "Deletes all files made by PV")

    parser_export = subparsers.add_parser("export", help = "Exports the passwords and configs to a file")
    parser_export.add_argument("directory_path", help = "The path to the directory where the export file should be saved")
    parser_export.add_argument("file_name", help = "The name of the export file")

    parser_import = subparsers.add_parser("import", help = "Imports passwords and configs from a file") 
    parser_import.add_argument("path", help = "The path to the file to import from")


def is_older_version(older: str, than: str) -> bool:
    if older.split(".")[0] > than.split(".")[0]:
        return False
    if older.split(".")[1] > than.split(".")[1]:
        return False
    if older.split(".")[2] > than.split(".")[2]:
        return False
    
    return True
