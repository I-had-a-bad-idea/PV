# PV: Password Vault (Probably Very Safe!)

![MIT License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Commit Activity](https://img.shields.io/github/commit-activity/m/I-had-a-bad-idea/PV)
![Last Commit](https://img.shields.io/github/last-commit/I-had-a-bad-idea/PV)
![Open Issues](https://img.shields.io/github/issues/I-had-a-bad-idea/PV)
![Closed Issues](https://img.shields.io/github/issues-closed/I-had-a-bad-idea/PV)
![Repo Size](https://img.shields.io/github/repo-size/I-had-a-bad-idea/PV)
![Contributors](https://img.shields.io/github/contributors/I-had-a-bad-idea/PV)

## Overview

- [WHAT IS PV?](#what-is-pv)
- [Why Would You Use This?](#why-would-you-use-this)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Quick Start](#quick-start)
- [Where are my secrets?](#where-are-my-secrets)
- [Can I change my master key?](#can-i-change-my-master-key)
- [Transfering data to a different device](#transfering-data-to-a-different-device)
- [Uninstallation/Cleanup](#uninstallationcleanup)
- [FAQ](#faq)
- [CONTRIBUTING](#contributing)
- [License](#license)
- [Disclaimer](#disclaimer)
- [Contact](#contact)

## WHAT IS PV?

PV is a CLI for managing your passwords, because sticky notes are only secure if you eat them. It uses a master key for encryption (not magic), and lets you add, remove, and list passwords. PV will store your secrets, judge your password choices (silently), and is designed as a base for your very own DIY password manager—because who needs LastPass when you have questionable Python skills?

> **Warning:** If you forget your master key, even PV can’t help you. PV is secure, not psychic.

---

## Why Would You Use This?

- **You trust your own Python more than most websites.**
- **You want to tell people you have a “custom password manager.”**
- **You believe GUIs are for cowards.**
- **You like living on the edge, and your edge is a terminal window.**
- **You want to fork a project that promises nothing except that it kind of works.**
- **You want to impress your friends with questionable cybersecurity choices.**
- **You like typing random commands and seeing what happens.**

---

## Features

- **AES-GCM Encryption!** No one knows how strong, but it’s there.
- **Master Key**: The one password to encrypt them all (and the one you really shouldn’t forget).
- **Key Derivation**: Turns your weak master key into a strong key for encryption.
- **Add/Remove/List passwords** (the holy trinity of password management)
- **CLI interface:** For people who fear GUIs, or just like typing.
- **No Cloud**: If you want your passwords stolen, you’ll have to do it yourself.
- **Extendable**: Use PV as a starting point for your own password manager. Go wild. If you make something awesome, tell me
- **Pythonic Code**: Written in Python. Easy to read, easy to break—wait, no, scratch that last part.
- **Clipboard**: Directly copies the password to your clipboard. No more squinting at your screen and mistyping “5” as “S”.

---

## Requirements

- Python 3.7+
- pip  (or sacrifice a rubber duck to the Python gods, whichever works)
- The following libraries, easily appeased via pip:
  - cryptography
  - idna
  - pyperclip

> **Note:** You do NOT need to install standard libraries like `os`, `base64`, or `threading`. Those are baked right into Python, just like existential dread.

---

## Installation

```bash
git clone https://github.com/I-had-a-bad-idea/PV.git
cd PV
pip install .
# Or whatever makes your Python happy
```

---

## Usage

```bash
pv       #in your favorurite terminal 
You do not have any passwords yet. Please think of a master key to use for PV #it knows if you have stored any passwords before
Enter the master key you want to use:    master_key 

#or
Passwords found. Please enter your master key to use PV.
Enter your master key:    master_key

# master_key should be the master key you want to use, not literally "master_key"


#now PV>     should appear. From now own you’re authenticated and can do whatever you desire

add        # Add a password (name, password)
passwords       # List all your secrets (only the names)
password        # Get a password by its name
remove     # Remove a password (bye-bye)
exit        # Save and exit PV (but why would you want to do that?)


# ...and other mysterious commands
```
> **Important:** Always exit with the command and dont just close the terminal or your changes will be lost


> For a description of all command look at the [Documentation](Documentation.md)


---

## Quick Start

```bash
# Install (see above)
pv

================================
 Welcome to PV
-----------------------
 Simple. Local. Secure.
-----------------------
 github.com/I-had-a-bad-idea/PV
================================


You do not have any passwords yet. Please think of a master key to use for PV
Enter the master key you want to use:   mysupersecretkey    # Key will be hidden. No peeking.

Successfully authenticated!

PV>     add github 123456
added  github

PV>     passwords
github

PV>     password github
copied  github  to clipboard

PV>     exit
Exiting PV
saves at:  C:\ProgramData\PV\PV_passwords
Saved


#everytime you want to access your passwords

pv
Passwords found. Please enter your master key to use PV.
Enter your master key:    mysupersecretkey      # Key won’t be visible. Still.

loads from:  C:\ProgramData\PV\PV_passwords
Successfully authenticated!
Welcome to PV

PV> password github --print
password_name: github
password: 123456

PV>     exit
Exiting PV
saves at:  C:\ProgramData\PV\PV_passwords
Saved

```

---

## Where are my secrets?

PV stores your (encrypted!) passwords in a file called `PV_passwords` in `C:\ProgramData\PV`. At least, unless you change the file location. Then that new location gets saved in the `PV_configs` file. Unless you move/delete that (in which case, I hope you remember where you put it). If you want to delete all your secrets, look at [cleanup](#uninstallationcleanup). If you want to move it to a USB stick and throw it in a volcano, go wild.

---

## Can I change my master key?

You can change your master key at any time. But remember: with great power comes great responsibility (to not forget your new master key).

[How to change your master key](Documentation.md/#new_master_key)

---

## Transfering data to a different device

You can use the [export](Documentation.md/#export) command and then the [import](Documentation.md/#import) command to transfer your data to another device.

---

## Uninstallation/Cleanup

Simply call the [cleanup](Documentation.md/#cleanup) command and PV will delete all files it made, and optionally uninstall the package (pip uninstall pv). No registry keys, no hidden files (unless you made some).

---

## FAQ

**Q: Is PV secure?**  
A: Secure-ish. If you don’t trust yourself, don’t trust PV.

**Q: Can I use PV as an actual password manager?**  
A: You can! But please don’t blame me if you lock yourself out of your online bingo account.

**Q: I forgot my master key, can you help?**  
A: No. Sorry. Not even a little bit. Try “psychic recovery.”

**Q: I ran a weird command and something funny happened.**  
A: Congratulations! You have discovered a feature (or a bug). Open an issue and share your findings.

---

## CONTRIBUTING

Thank you for even considering it. Seriously.

### Code

- Written in Python. If you can spell “def”, you’re probably qualified.
- Fork, make your changes, open a pull request. 
- Comment your code. Future you (and future me) will appreciate it.
- All code becomes part of the MIT-licensed soup I call PV.

### Ideas

 - Got a feature idea? 
 - Open a feature request! 
 - The more detail, the better. If you can make me laugh, even better.

### Bugs

- If you find a bug, congratulations! Open an issue.
- Try weird stuff. PV is tested, but let’s be honest, not that tested.
- Screenshots and dramatic stories are encouraged.

---

## License

MIT. Use it, break it, fix it, share it. Just don’t blame me if you lock yourself out of your cat’s email.

---

## Disclaimer

PV is a hobby project. Don’t use it to guard the nuclear codes. Or do, but that’s on you.

---

## Contact

Open an issue or PR right here on GitHub. Carrier pigeon support coming soon. If you have ideas or want to say hi, the issues tab is your friend.

---

Thanks for reading! Now go hoard some passwords.
