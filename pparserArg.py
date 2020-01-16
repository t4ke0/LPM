
class ParseArg:

	def __init__(self):
		self.flagCmds= ["--username","--password","--site","--id","--category"]
		self.paramaterCmds = ['add','update','delete']


	#Parse a List of argument and returns a dictionary 
	def parse_arg(self,command): 
		resultDic = dict.fromkeys(x for x in self.paramaterCmds + self.flagCmds) 
		for i, cmd in enumerate(command) :
			if i == 0 and cmd in self.paramaterCmds :
				resultDic[cmd] = True # Replace the bool value with the right function
				for index, f in enumerate(command[(i+1):],start=(i+1)):
					if f in self.flagCmds :
						resultDic[f] = command[(index+1)]

		return resultDic



	def execute_Arg(self,dictt,func1,func2,func3) : 
		for cmd in self.paramaterCmds: 
			if dictt[cmd] is not None and cmd == 'delete' : 
				id_ = dictt['--id']
				category = dictt['--category']
				if id_ is not None and category is not None: 
					func1(id_,category.lower()) # replace with real func 
					break			
				else : 
					print("Error")
					break

			elif dictt[cmd] is not None and cmd =='add' :
				username = dictt['--username']
				password = dictt['--password']
				site = dictt['--site']
				category = dictt['--category']
				if username is not None and password is not None and site is not None and category is not None : 
					func2(username,password,site,category.lower()) # Replace with real func
					break
				else :
					print('Arg missed')
					break
					

			elif dictt[cmd] is not None and cmd == 'update' :
				username = dictt['--username']
				password = dictt['--password']
				site = dictt['--site']
				category = dictt['--category']
				id_ = dictt['--id']
				if category is not None and id_ is not None :
					func3(category.lower(),id_,username,password,site) # replace with real func 
					break

				else :
					print('You should specify the category and the id')
					break

		else :
			print("Wrong command")
			