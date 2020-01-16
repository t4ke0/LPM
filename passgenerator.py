

import string 
import random


class PassGen:
	def __init__(self):
		self.upper = string.ascii_uppercase
		self.lower = string.ascii_lowercase
		self.digist = string.digits
		self.symbols = string.punctuation
		self.complex = string.printable

	#generate Uppercase password 
	def upperCasePass(self,r): # "r" is length of the password
		if isinstance(r,int):
			return "".join(random.choice(self.upper) for i in range(r))
		else : 
			return "The length must be integer"

	#generate lowercase password 

	def lowerCasePass(self,r): # "r" length of the password
		if isinstance(r,int):
			return "".join(random.choice(self.lower) for i in range(r))
		else : 
			return "The length must be an integer"

	#generate lowercase + uppercase password 

	def lowerupperPass(self,r): # "r" length of the password 
		self.upperlower = self.upper + self.lower
		if isinstance(r,int):
			return "".join(random.choice(self.upperlower) for i in range(r))
		else :
			return "The length must be an integer"


	# generate digits password 

	def digitPass(self,r):
		if isinstance(r,int):
			return "".join(random.choice(self.digist) for i in range(r))
		else :
			return "The length must be an integer"

	#generate digits + lowercase + uppercase password

	def lowerUpperDigitPass(self,r):
		self.mix = self.upper + self.lower + self.digist
		if isinstance(r,int):
			return "".join(random.choice(self.mix) for i in range(r))
		else : 
			return "The length must be an integer"


	#generate symbol password 

	def symbolPass(self,r):
		if isinstance(r,int):
			return "".join(random.choice(self.symbols) for i in range(r))
		else :
			return "The length must be an integer"


	#generate strong password generating it from lower and upper case letters ,numbers and symbols

	def complexPass(self,r):
		if isinstance(r,int):
			return "".join(random.choice(self.complex.strip()) for i in range(r)) #Trying strip here maybe should pass that func for all other func above
		else :
			return "The length must be an integer"
