from cryptography.fernet import Fernet
import os


class Crypt:

	def generate_key(self,path,username): #Generating the Key 
		key = Fernet.generate_key()
		with open(os.path.join(path,f"{username}.key"), "wb") as key_file:
			key_file.write(key)


	def load_key(self,path,username): #Load the key "Read the key that we already have generated"
		return open(os.path.join(path,f"{username}.key"), "rb").read()

	def encrypt(self,filename,key):#Encrypt Function
		f = Fernet(key)
		with open(filename,"rb") as file : #Open the file we want to encrypt
			file_data = file.read() #READ it data
		encrypt_data = f.encrypt(file_data) #Encrypt that data we have read

		with open(filename+".encrypted","wb") as file: #We open another file Where we gonna save encrypted data with adding .encrypted extention 
			file.write(encrypt_data)
		#remove the database after encrypting it 
		os.remove(filename)

	def decrypt(self,filename,endfile,key): #Decrypt Function who has 3 parameteres "filename" ==> the file we want to decrypt "endfile" ==> is the of the file that we are going to save decrypted data on it 
											#"key" the key we have encrypted the data with
		f = Fernet(key) 
		#if filename.endswith(".encrypted"):
		with open(filename,"rb") as file:	
			encrypted_data = file.read()

		decrypted_data = f.decrypt(encrypted_data)

		with open(endfile,"wb") as file0 :
			file0.write(decrypted_data)

		#remove the encrypted file after decrpyting the database
		os.remove(filename)


