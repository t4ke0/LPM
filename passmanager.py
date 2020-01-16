#! /usr/bin/python3


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
		#Connecting with our database it's an sqlite3 db 
		self.con = sqlite3.connect("User.db") # DB for registration and login 
		self.cursor = self.con.cursor() # Cursor of registration and login db
		self.get_platform()
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

	def get_id(self,username):

		self.cursor.execute("SELECT ID FROM users WHERE USERNAME = '%s'" %(username.strip()))
		queryid = self.cursor.fetchone()
		return queryid[0]

	
	def get_user_db(self,username):
		self.cursor.execute("SELECT DBPATH FROM users WHERE USERNAME = '%s'" %(username))
		querydb = self.cursor.fetchone()
		return querydb[0]


	def get_user(self,username):
		self.cursor.execute("SELECT USERNAME FROM users WHERE  USERNAME='%s'" %(username))
		queryUser = self.cursor.fetchone()
		if queryUser is not None:
			return queryUser[0]
		else :
			return []

	def get_email(self,email):
		self.cursor.execute("SELECT EMAIL from users WHERE EMAIL='%s'" %(email))
		queryEmail = self.cursor.fetchone()
		if queryEmail is not None : 
			return queryEmail[0]
		else : 
			return []

	def getUserFromCredDb(self,username,category):
		self.c.execute("SELECT user FROM '%s' WHERE user = '%s'" %(category,username))
		queryuser = self.c.fetchone()
		if queryuser is not None :
			return queryuser[0]
		else : 
			return []

	def get_platform(self):
		if sys.platform == "linux":
			return os.system("clear")
		else : 
			return os.system("cls")

	def gen_passwd(self,number):
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
		username = input("Username : ")
		masterPw = getpass("Master Password : ")
		email = input("Email :")
		reg = re.findall(r'\S+@\S+',email)

		#Ensure that the username is not on our DB 
		if self.get_user(username) :
			print(self.red,"User already used! ",self.reset)
			print(self.red,"Please Try again !",self.reset)
			self.getUserStuff()
 
		elif self.get_email(email):
			print(self.red,"Email already used!",self.reset)
			print(self.red,"Please try again !",self.reset)
			self.getUserStuff()

		elif self.get_email == [] or self.get_user == []:
			pass

		elif reg :
			pass 

		else : 
			self.get_platform()
			print("Not a Valid email address")
			print("Retry Please !")
			Avatar.print_avatar()
			self.getUserStuff()

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
		self.cursor.execute("INSERT INTO users (username,password,email,DBPATH) \
			VALUES ('%s', '%s','%s' ,'%s')" %(username,pWeH,email,db_path))
		self.con.commit()
		#self.con.close()
		print(self.green,"We have generated a key for the encryption of your credentials database",self.reset)
		print(self.green,"Successfully registred !",self.reset)
		Avatar.print_avatar()
		print(f"{self.yellow}Login :{self.reset}")
		self.login()

	def login(self):
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
			pass 
		

		#Load the encryption key
		self.k_key = self.C.load_key(self.Dkey,self.userlogin.strip())
		#Ecrypt GLOBAL db 
		self.C.decrypt("User.db.encrypted",self.global_db,self.k_key)

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
			#Show to user his Stuff
			## First Screen Help ## 
			self.help_= (
			f"{self.yellow}[1]Credentials""\n"
			"[2]Generate Secure password""\n"
			"help show this Help menu\n"
			"clear clears the screen\n"
			f"Ctrl+ C to Exit{self.reset}""\n"
			)
			self.get_platform()
			Avatar.print_avatar() #Print the ascii art 
			print(self.help_)
			self.showUserStuff() 

		else : #else show logggin failed 
			print("Failed to login")
			self.C.encrypt(self.global_db,self.k_key) #If the user failed to login enrypt the global db again 
			self.getUserStuff()



###### END of Auxilary functions ######


	def getUserStuff(self):
		try : 
			self.w = input("Login/Register :")
			if self.w.strip() == "register" : # if user typed register show him the registration elements
				self.register()	
				
			elif self.w.strip() == "login" : # otherwise he want to login show him login elements 
				self.login()

			else : 
				print("Retry again")
				self.getUserStuff()
		except KeyboardInterrupt: 
			#self.conn.close() #Close the DB While closing the program
			print("Exiting ....")
			self.C.encrypt(self.global_db,self.k_key)
			filen = self.db
			self.C.encrypt(filen,self.key)
			self.get_platform() # clear terminal screen while exiting 
			sys.exit()
	
	def saveUserStuff(self,username,password,site,category): # replacing 
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
			self.get_platform()
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
			self.get_platform()
			Avatar.print_avatar()
			self.showUserStuff()

		elif q == "help":
			print(self.help_)
			self.showUserStuff()
		else : 
			self.showUserStuff()

### TODOs ### 

# TODO DELETE CREDS [DONE] delete by typing delete then username="" try to use arg parse if works use it to update the value . 
# TODO query creds by name of the site [ ]
# in show creds you can run delete , update commands from the input [DONE]
# TODO make usage beautifull [100%]
# TODO remove UPDATE function code and unuseful code [DONE]
# TODO parseargument with a better way [100%]
# TODO implement the new parser for that project [100%]

if __name__ == "__main__":
	m = Main()
	try : 
		m.getUserStuff()
	except AttributeError:
		sys.exit()




####### removed code ########

	#def update_value(self,category): 
		#try :
			#w = input(f"{self.yellow}Which value you wanna Update\n"
				#f'username,password,site{self.reset}\n'
				#f'{self.green}Update Credentials >>> {self.reset}')
#
			## if user want to update his password 
			#if w.lower().strip() == "password":
				#username = input("Username of the password you wanna change : ")
				#if username == self.getUserFromCredDb(username,category) :
					#newpw = input("New password: ")
					#self.c.execute("UPDATE '%s' SET pw='%s' WHERE user='%s' " %(category,newpw.strip(),username))
					#self.conn.commit()
					#print("Your password has been successfully updated")
					#self.update_value(category)
				#else : 
					#print("The Username is wrong")
					#self.update_value(category)
#
			## if user want to update his username 
			#elif w.lower().strip() == "username" :
				#user = input(f"{self.green}Old username :{self.reset}")
				#if user == self.getUserFromCredDb(user,category) :
					#newuser = input("New username: ")
					#self.c.execute("UPDATE '%s' SET user='%s' WHERE user='%s' " %(category,newuser.strip(),user))
					#self.conn.commit()
					#print(f"{self.green}Your username has been successfully updated{self.reset}")
					#self.update_value(category)
				#else : 
					#print(f"{self.red}Old username is Wrong!{self.reset}")
					#self.update_value(category)
#
			#elif w.lower().strip() == "site" :
				#user = input("Your Username on that site : ")
				#if user == self.getUserFromCredDb(user,category) :
					#newsite = input("New Site : ")
					#self.c.execute("UPDATE '%s' SET site ='%s' WHERE user='%s' "%(category,newsite.strip(),user))
					#self.conn.commit()
					#print("Site info has been successfully updated")
					#self.update_value(category)
				#else :
					#print("Username you have entred is wrong!")
					#self.update_value(category)
			#else : 
				#print(f"There is Nothing Called {w}")
				#self.update_value(category)
		#except KeyboardInterrupt :
			#self.showUserStuff()









		#elif Fst in cmds :
			#if Fst == "delete" and len(parse) == 3  :
				#snd = parse[1]
				#trd = parse[2]
				#if re.match(r"\d+",snd) and re.match(r"\w+",trd) : 
					## Here We delete cred 
					#try : 
						#self.c.execute("DELETE FROM '%s' WHERE ID = '%s'" %(trd,snd))
						#self.conn.commit()
						#print("Creds has been DELETED")
						#self.showCredUser()
					#except Exception as e : 
						#print("Error table name is incorrect")
				#else : 
					#print("the ID Must be an integer")
					#self.showCredUser()
#
			#elif Fst == "update" and len(parse) == 5 :
				#catg = parse[1] #Category 
				#typ = parse[2].strip("-") #TYPE 
				#npwd = parse[3]				
				#id_ = parse[4] #ID
				#if re.match(r"\d",id_) and re.match(r"\w+",catg) and re.match(r'\w+',typ):
					#try : 
						#if typ == "password":
							#self.c.execute("UPDATE '%s' SET pw='%s' WHERE ID = '%s'"%(catg,npwd,id_))
							#self.conn.commit()
							#print("password UPDATED")
							#self.showCredUser()
						#elif typ == "username" :
							#self.c.execute("UPDATE '%s' SET username='%s' WHERE ID = '%s'"%(catg,npwd,id_))
							#self.conn.commit()
							#print("username UPDATED")
							#self.showCredUser()
						#elif typ == "site" :
							#self.c.execute("UPDATE '%s' SET site='%s' WHERE ID = '%s'"%(catg,npwd,id_))
							#self.conn.commit()
							#print("site UPDATED")
							#self.showCredUser()
						#else :
							#print(f"Check if category is wrong  ==> {catg} or type of creds ==> {typ}")
							#self.showCredUser()
					#except Exception as e :
						#print("input wrong try again!")
				#else :
					#print("Error")
					#self.showCredUser()
#
			#elif Fst == "clear" :
				#os.system("clear") # to modify to work with windows systems 
				#self.showCredUser()
#
			#elif Fst == "add" and len(parse) == 8 :
				#catg = parse[1]
				#Usern= parse[2].strip('-')
				#Vuser= parse[3]
				#Pass = parse[4].strip('-')
				#Vpass= parse[5]
				#Site = parse[6].strip('-')
				#Vsite= parse[7]
#
				## if statement to make sure that the input is correct 
				#if re.match(r"\w+",catg) and re.match(r"\w+",Pass) and re.match(r"\w+",Site) :
					#self.c.execute("INSERT INTO '%s' (user,pw,site) \
						#VALUES ('%s','%s','%s')" %(catg,Vuser,Vpass,Vsite))
					#self.conn.commit()
					#print("Success")
					#self.showCredUser()
				#else : 
					#print("Failed Some arguments are not correct")
#


							#else : 
				#print("Error not enough args learn how to use cmds by typing help")
				#self.showCredUser()


""" 
print("Type one of this Categories Where you can store your password :")
		s = input(
			"Social""\n"
			"Email""\n"
			"Finance""\n"
			"Shopping""\n"
			"Other""\n"
			"Ctrl+c Return back""\n"
			"Set Category >> ")
		
		Site = input("Web site: ") #GET THE WEBSITE
		username = input("Email/username :") # GET THE USERNAME OR EMAIL
		password = getpass(stream=sys.stderr) # GET THE PASSWORD 
		check = input("Do u want to see the password u just have Entered y/n: ") #IF THE USER MAKE A MISTAKE IN HIS PW HE CAN SEE THE PASSWORD BY TYPING Y
		if check == 'y'.lower() or check == 'y'.upper() : # IF Y ==> Show the password
			print(password) # Print the password here
		else : # ELse pass 
			pass 

		modify = input("DO u want to modify the password y/n: ") # IF A USER WANT TO MODIFY HIS PASSWORD AFTER HE FOUND A MISTAKE ON IT 
		if modify == "y".lower() or modify == "y".upper() : # IF yes go modfiy
			npassword = getpass(steam=sys.stderr) # GET THE MODIFIED PASSWORD FROM THE USER
			password = npassword #REPLACE THE OLD ONE BY THE RECENT ONE 
		else : 
			pass 

		ss = s.lower().strip() #REMOVE ALL SPACES FROM USER INPUT "CATEGORY"
		#ID = self.get_id(self.userlogin)	#ID OF THE USER  #I'm not gonna use the id anymore cause we separate users db each one has his own one now 
"""