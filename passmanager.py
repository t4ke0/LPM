#!/usr/bin/python3


from symmetric import Crypt 
from avatar import Avatar
from passgenerator import PassGen
from pparserArg import ParseArg

from getpass import getpass
from colorama import Style, Back , Fore
from terminaltables import AsciiTable
import sqlite3,sys,hashlib,re,os,shutil,time,pyperclip



#Mylastpass app is an app Where you can Store your passwords locally in a DB Securing it with a Master password and it's the only password you should remember




#Main class it's the First shit you can see When you execute the prog 
class Main:
	def __init__(self):
		self.clearScreen()
		self.progAvatar = Avatar.print_avatar()
		self.C = Crypt()
		self.G = PassGen()
		self.Parser = ParseArg()
		self.path_keys= "./keys"
		self.pathDir = "./main_cred_db"
		self.global_db = './User.db'

		#######Colors#######
		self.fore = Fore
		self.reset = Style.RESET_ALL
		self.green = self.fore.GREEN
		self.red = self.fore.RED
		self.yellow = self.fore.YELLOW
		#####################


# Auxilary functions 


	def get_user_db(self,username): # This Function queries User's credentials db 
		self.cursor.execute("SELECT DBPATH FROM users WHERE USERNAME = '%s'" %(username))
		querydb = self.cursor.fetchone()
		return querydb[0]

	def clearScreen(self): # Clear the Screen 
		if sys.platform == "linux":
			return os.system("clear")
		else : 
			return os.system("cls")

	def gen_passwd(self,number): # Generating Passwords
		digits = self.G.digist
		if number in digits :
			r = input("Password length: ")
			if number == "0" :
				Gnpassw = self.G.lowerCasePass(int(r))
			elif number == "1" :
				Gnpassw = self.G.upperCasePass(int(r))
			elif number == "2" :
				Gnpassw = self.G.lowerupperPass(int(r))
			elif number == "3" :
				Gnpassw = self.G.digitPass(int(r))
			elif number == "4" :
				Gnpassw = self.G.lowerUpperDigitPass(int(r))
			elif number == "5" :
				Gnpassw = self.G.symbolPass(int(r))
			elif number == "6" :
				Gnpassw = self.G.complexPass(int(r))
			else : 
				self.generatePassword()

			pyperclip.copy(Gnpassw)
			print(f"Your generated passsword : {Gnpassw}")
			print(self.green,"[+] Copied to clipboard",self.reset)
			self.generatePassword()
		else : 
			print("Excepted an integer !")
			self.generatePassword()



	def register(self):
		dir_ = os.listdir() 
		if self.global_db in dir_ : 
			#Connecting with our database it's an sqlite3 db 
			con = sqlite3.connect("User.db") # DB for registration and login 
			cursor = con.cursor() # Cursor of registration and login db
		else : 
			print("User.db Not found, maybe another user is registered before you !")
			self.getUserStuff()
		try : 
			username = input("Username : ")
			masterPw = getpass("Master Password : ")
			email = input("Email :")
			reg = re.findall(r'\S+@\S+',email)

			if reg :
				#Create a db for that particular user
				db_path = shutil.copy2("defaulcred.db",f"./main_cred_db/{username}.db")

				#Generate a symmetric key for the user
				self.C.generate_key(self.path_keys,username)
				key = self.C.load_key(self.path_keys,username)
				filename = db_path
				#encrypt the db with that generated key 
				self.C.encrypt(filename,key)

				#TAKE THE PASSWORD AND ENCRYPT IT BEFORE ENTER IT TO THE DB 
				pWe = hashlib.sha256(bytes(masterPw,('utf-8')))
				pWeH = pWe.hexdigest()

				#Store user stuff into DB
				cursor.execute("INSERT INTO users (username,password,email,DBPATH) \
					VALUES ('%s', '%s','%s' ,'%s')" %(username,pWeH,email,db_path))
				con.commit()
				
				#Encrypt  User.db 
				self.C.encrypt(self.global_db,key)
				print(self.green,"Encrypted User.db")
				print(self.green,"We have generated a key for the encryption of your credentials database")
				print(self.green,"Successfully registred !",self.reset)
				Avatar.print_avatar()
				print(f"{self.yellow}Login :{self.reset}")
				self.login()
				
			else : 
				self.clearScreen()
				print("Not a Valid email address")
				print("Retry Please !")
				Avatar.print_avatar()
				self.getUserStuff()

		except KeyboardInterrupt : 			
			self.clearScreen()
			sys.exit()

	def login(self):
		try : 
			self.userlogin = input("Username :")
			passwd = getpass("Master Password :")
			self.Dkey = input("Key Path ('What is this press <w>')Default [./keys]: ")

			if self.Dkey == 'w' :
				print("PATH OF THE ENCRYPTION/DECRYPTION KEY WE HAVE GENERATED FOR YOU ONCE YOU REGISTERED FOR AN ACCOUNT!\n")
				self.login()
			elif self.Dkey == "" :
				self.Dkey = self.path_keys
				pass
			else : 
				print("Key Path not Found!") 
				self.login()
			
			#Load the encryption key
			self.k_key = self.C.load_key(self.Dkey,self.userlogin.strip())
			#decrypt GLOBAL db
			self.C.decrypt("User.db.encrypted",self.global_db,self.k_key)

			#Connecting with our database it's an sqlite3 db 
			self.con = sqlite3.connect("User.db") # DB for registration and login 
			self.cursor = self.con.cursor() # Cursor of registration and login db

			# TAKE THE PASSWORD AND ENCRYPT IT THEN COMPARE IT WITH THE OTHER ONE ON THE DB 
			pswe = hashlib.sha256(bytes(passwd,("utf-8")))
			psweh = pswe.hexdigest()
			 
			self.cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(self.userlogin.strip(),psweh.strip())) # Ensure that the username and password are in our DB

			if self.cursor.fetchone() is not None:  #if True i mean if username & password are in out DB show to user his stuff 
				print(self.green,"Welcome",self.reset)
				#load user key
				self.key = self.C.load_key(self.path_keys,self.userlogin.strip()) #Load the User key that he generate When he registred 

				#decrypt the db
				find_dec = f"{self.userlogin.strip()}.db.encrypted" # Find the encrypted DB for each user
				dec_file = os.path.join("./main_cred_db",find_dec) 
				#os.path.join("./main_cred_db",f"{self.userlogin}.db") # get the name of the user db after encryption
				end_file = self.get_user_db(self.userlogin.strip()) #same above but instead of get in it manually i'm getting the db path from users database 

				self.C.decrypt(dec_file,end_file,self.key) #Decryption Function you can find the detail about this function in <symmetric.py> file 

				self.db = end_file
				if self.db == None :
					print(f"There is no username {self.userlogin} YOU are not registred yet")
					self.getUserStuff()
				self.conn = sqlite3.connect(self.db)
				self.c = self.conn.cursor()

				self.help_= (							## Help menu ## 
				f"{self.yellow}[1]Credentials""\n"
				"[2]Generate Secure password""\n"
				"help show this Help menu\n"
				"clear clears the screen\n"
				f"Ctrl+ C to Exit{self.reset}""\n"
				)
				self.clearScreen()
				Avatar.print_avatar() #Print the ascii art
				print(self.help_)
				self.showUserStuff()

			else : #else show logggin failed 
				print("Failed to login")
				self.C.encrypt(self.global_db,self.k_key) #If the user failed to login enrypt the global db again 
				self.getUserStuff()
		except KeyboardInterrupt : 
			self.C.encrypt(self.global_db,self.k_key)
			filen = self.db
			self.C.encrypt(filen,self.key)
			self.clearScreen()
			sys.exit()

###### END of Auxilary functions ######


	def getUserStuff(self): # Main menu 
		try :
			self.w = input("Login/Register :")
		except KeyboardInterrupt :
			self.clearScreen()
			sys.exit()
		if self.w.strip() == "register" : # if user typed register show him the registration elements
			self.register()	
				
		elif self.w.strip() == "login" : # otherwise he want to login show him login elements 
			self.login()

		else : 
			print("Retry again")
			self.getUserStuff()
	
	def saveUserStuff(self,username,password,site,category): 
		try : 
			self.c.execute("INSERT INTO '%s' (user,pw,site) \
				VALUES ('%s','%s','%s')" %(category,username,password,site)) #Inserting Crendentials into our DB 
			self.conn.commit()
			print(self.green,"Your Credentials has been saved Successfully !",self.reset)
			self.showCredUser()
		except Exception as e :
			print(f"Error {e}")
			self.showCredUser()

	def deleteUserStuff(self,id_,category):
		try : 
			self.c.execute("DELETE FROM '%s' WHERE ID = '%s'" %(category,id_))
			self.conn.commit()
			print("Creds has been DELETED")
			self.showCredUser()
		except Exception as e :
			print("Error table name is incorrect")
			self.showCredUser()

	def udpateUserStuff(self,category,id_,*args):
		try : 
			for i ,arg in enumerate(args) : 
				if args[i] is not None  and i == 0 :  
					self.c.execute("UPDATE '%s' SET user='%s' WHERE id='%s' " %(category,args[i],id_))
					self.conn.commit()
					print(f"Username updated to {arg}")

				elif args[i] is not None and i == 1 : 
					self.c.execute("UPDATE '%s' SET pw='%s' WHERE id='%s' " %(category,args[i],id_))
					self.conn.commit()
					print(f'Password updated to {arg}')

				elif args[i] is not None and i == 2 : 
					self.c.execute("UPDATE '%s' SET site='%s' WHERE id='%s' " %(category,args[i],id_))
					self.conn.commit()
					print(f"Site updated to {arg}")
					
			self.showCredUser()

		except TypeError :  
			print("Arguments Missing!!")
			self.showCredUser()


	def showCredUser(self):
		s = input(f"{self.green}Credentials >>> {self.reset}") 
		self.categories = ["Social","Email","Finance","Shopping","Other"]
		command = s.split()

		if s == "help".lower().strip() :
			print(self.green,'Categories ===> ',",".join([f.lower() for f in self.categories]),self.reset)
			print(
				f"{self.yellow}Enter one of the Categories above, OR "'\n',
				"\n" ,
				"delete --id <id> --category <category> \n",
				"\n" , 
				"update --category <category> --id <id> --username <username>* --password <password>* --site <site>* \n",
				"\n" , 
				"Note : You can Update username , password and site at once it's up to you it's optional \n"
				"\n" , 
				"add --username <username> --password <password> --site <site> --category <category>\n",
				"\n" , 
				"<help> Prints this help menu""\n",	
				"\n" , 
				"<clear> clears the screen""\n",
				"\n" , 
				f"Ctrl+c to return back{self.reset}""\n",
				)
			self.showCredUser()

		# Show user tables # Do not touch this   ^
		elif s.lower().strip() in [c.lower() for c in self.categories]: #If the input is a category in the categories's list and it's in lower case
			category = s.strip() #Remove all spaces from user inputs
			print(self.green,f"YOU ARE IN {category} CATEGORY",self.reset)
			self.c.execute("SELECT ID,user,pw,site FROM '%s' " %(category)) #removing ID here 
			data = self.c.fetchall() 
			
			table_data = [[
				"{}ID{}".format(self.yellow,self.reset),
				"{}Username{}".format(self.yellow,self.reset),
				"{}Password{}".format(self.yellow,self.reset),
				"{}Site{}".format(self.yellow,self.reset)
				]]
			table = AsciiTable(table_data)
			for I,U,P,S in data :			
				if S == None: #If there is no Site in the DB 
					S = "-"
				table_data.append([I,U,P,S])
			print(table.table)
			self.showCredUser() # redirect the user to the beginning of the function again 

		elif s.lower() == "clear" :
			self.clearScreen()
			Avatar.print_avatar()
			self.showCredUser()


		else : 
			self.Parser.parse_arg(command) # parse commands 
			self.Parser.execute_Arg(self.Parser.parse_arg(command),self.deleteUserStuff,self.saveUserStuff,self.udpateUserStuff) # execute function of each command 
			#print(self.red,f"ERROR Wrong category name ==> {s}",self.reset)
			self.showCredUser()

		
	def generatePassword(self): 
		h =(
		f"{self.yellow}[0] Only Lowercase password""\n"
			"[1] Only Uppercase password""\n"
			"[2] lowercase+uppercase letter password""\n"
			"[3] Only digits password""\n"
			"[4] lowercase + uppercase + digits""\n"
			"[5] Symbol password""\n"
			"[6] Mix between all previous cases" '\n'
			"Ctrl+c return back""\n"
			f"[help] to print this {self.reset}""\n"
		)
		print("h for help")
		q = input (f"{self.green}Password generator >>> {self.reset}")
		if q.lower().strip() == "h":
			print(h)
			self.generatePassword()

		self.gen_passwd(q)

		

	def showUserStuff(self):
		#Here Where the user can decide if he want to see his creds or to store them into the DB or generate a secure password
		q = input("menu >> ")


		if q == "1":
			try: 
				self.showCredUser()
			except KeyboardInterrupt:
				print("")
				self.showUserStuff()
		elif q =="2":
			try :
				self.generatePassword()
			except KeyboardInterrupt:
				print("")
				self.showUserStuff()
		elif q == "clear":
			self.clearScreen()
			Avatar.print_avatar()
			self.showUserStuff()

		elif q == "help":
			print(self.help_)
			self.showUserStuff()
		else : 
			self.showUserStuff()


if __name__ == "__main__":
	m = Main()
	try : 
		m.getUserStuff()
	except AttributeError:
		m.clearScreen()
		sys.exit()

# Todo Create for Each User who registred a separated global db or Allow for one User to be registred 