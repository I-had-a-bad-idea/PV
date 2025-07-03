

## Overview

- [Adding passwords](#add)
- [Removing passwords](#remove)
- [Listing Passwords](#passwords)
- [Getting a password](#password)
- [Cleaning up](#cleanup)
- [Configuring the save directory](#savepath)
- [Choosing a name for the file](#filename)


## Add
The add command is used to add a password.
It requires two arguments: password_name ; password

Example:

add github 123456

Here github is the password name you can use to reference the password and 123456 is the actual password.
> **Warning:** In case a password with the name github already exists it will be overwritten.


## Remove
The remove command is used to remove a password.
It requires one argument: password_name
It doesnt requires the password itself only its name.

Example:

remove github

Here the password with the name github is being removed. 


## Passwords
The command passwords can be used to list all passwords.
It doesnt require any arguments.

Example:

passwords

Now all the password names will be listed. The passwords itself wont be visible.


## Password
This command is used to access passwords.
It requires one argument: password_name
It has an optional flag to print the password instead of copying it: --print

Examples:

password github
password github --print

In the first example the password referenced by github gets copied to the clipboard. In the second one it prints it to the command line.


## Cleanup
The cleanup command deletes all files made by PV and exists the programm.
It doesnt require any arguments.

Example:

cleanup

Now all files create by PV will be deleted and the programm will stop.


## Savepath
The save_path command allows you to choose the directory, where your passwords are saved to.
It requires one argument: path

Example:

save_path C:\ProgramData\PV\Passwords

Now the password file be be saved in this directory. Keep in mind, that this isnt the full path to the file, as this is only the directory and the file name still misses.


## Filename
The file_name command allows you to choose the name of the password file.
It requires one argument: name

Example:

file_name PV_password_file

Now the password file will be named "PV_password_file". Best used in combination with [Save path](#savepath)


## Iterations
This command can be used to increase security at the cost of longer load/save times.

Example:

iterations 18

18 is the standard. It is recommended to increase this number as much as possible, without increasing load/save times too much. Beware that this number is used as the power of 2. Therefore a bigger increase can seriously increase times.

