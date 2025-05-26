
import json
import base64
from idna import encode

passwords : dict = {} #Just a dictionary, where the passwords are saved

master_key : str = "Test_key" #The one key to encrypt them all


def add_password(password_name: str, password: str):
    passwords[password_name] = password #that's it, just adding the password

    print("passwords after addition: ", passwords)

def remove_password(password_name: str):
    passwords.pop(password_name, None) #similar just getting rid of the password 
    #TODO add a check for the master_key before deleting

    print("passwords after deletion: ", passwords)

def set_master_key(new_key: str, old_key: str):
    global master_key #otherwise it thinks it's a local one
    if master_key: 
        if old_key != master_key: #make sure the know the old key, before changing it
            print("old master key is wrong, or something like that (still working on this message)")
            return
    
    master_key = new_key #set the new key
    #TODO add an file update when changing the master_key as encryption changes
    

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
    decrypted_passwords = json.loads(decrypted_passwords_string) #turn it back into a dict

    return decrypted_passwords 


def cli_entry_point(): #just the basic test function for now
    print("Hello World")

    add_password("Test_name", "Test_password")
    encpasswords = get_encrypted_passwords()
    print("encpasswords: ", encpasswords)
    print("decpasswords: ", get_decrypted_passwords(encpasswords))

    remove_password("Test_name")
