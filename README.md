# Local Password Manager CLI version 

## Dependencies 

- cryptography 
- colorama  
- terminaltables
- pyperclip 
- sqlite3 


## Installation & Usage 

```
[python3] 

$ pip3 install <All dependencies above> 

$ python3 passmanager.py 

```
## How it works 

```
- After running the prog you should register and remember the Master passphrase.

- The program will generate an encryption key for encrypting and decrypting your credentialsdatabase. 

- After that you can login using your master passphrase and your encryption key path or just let it in the default path which is keys folder . 

- Remember your encryption key it will be named as your "username.key" & default path where all keys are stored is /keys folder 

- Program tested only on Linux so far . 

```
## Finally 

- If there is any issue fill free to submit it on the issue tracker section . 



