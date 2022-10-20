# Huan Bui 
# Fall 2017
# CS 152 Project 7
# Oct 25, 2017
#
# First class design
#
# Elephant class

import random

class Elephant:

	calvInterval = 3.1
	percentDarted = 0.0
	juvAge = 12
	maxAge = 60
	probCalfSurv = 0.85
	probAdultSurv = 0.996
	probSeniorSurv = 0.20
	carryCap = 7000
	numYears = 200
	
	def __init__(self, calvingInterval = 3.1, age=None):
		if age != None:
			self.age = age
		else:
			self.age = random.randint(1, Elephant.maxAge)
		if random.random() < 0.5:
			self.gender = 'f'
		else:
			self.gender = 'm'
		self.monthsPregnant = 0
		self.monthsContraceptiveRemaining = 0

		if self.gender == 'f':
			if self.age > Elephant.juvAge and self.age <= Elephant.maxAge:
				if random.random() < 1.0/Elephant.calvInterval:
					self.monthsPregnant = random.randint(1, 22)
		#print("Init called!")
		#print()
		return 

	def getAge(self):
		return self.age
	
	def getGender(self):
		return self.gender
		
	def getMonthsPregnant(self):
		return self.monthsPregnant
		
	def getContraception(self):
		return self.monthsContraceptiveRemaining

	def isFemale(self):
		return self.gender == 'f'

	def isPregnant(self):
		return self.monthsPregnant > 0
		
	def isCalf(self):
		return self.getAge() <= 1
		
	def isJuvenile(self):
		return self.getAge() >= 2 and self.getAge() <= Elephant.juvAge

	def isAdult(self):
		return self.getAge() <= Elephant.maxAge and self.getAge() > Elephant.juvAge
	
	def isSenior(self):
		return self.getAge() > Elephant.maxAge
		
	def setAge(self, a):
		self.age = a
		
	def setGender(self, a):
		self.gender = a
		
	def setMonthsPregnant(self, a):
		self.monthsPregnant = a
		
	def setContraception(self, a):
		self.monthsContraceptiveRemaining = a
    	
       
	def incrementAge(self):
                '''the elephant's age is in self.age'''
		self.age += 1

	def dart(self, monthsEffective = 22):
                '''
		set self.pregnant to 0 and self.contraception to
		monthsEffective'''
                self.monthsPregnant = 0
                self.monthsContraceptiveRemaining = monthsEffective

	def progressMonth(self, calvingInterval=3.1):
                '''returns True if a baby should be made, False otherwise'''
		if self.isFemale() and self.isAdult():
			if self.getContraception() > 0:
				self.monthsContraceptiveRemaining -= 1
				
			elif self.getMonthsPregnant() > 0:
				if self.getMonthsPregnant() >= 22:
					self.monthsPregnant = 0
					return True
				else:
					self.monthsPregnant += 1
			
			else: # if not currently pregnant
				if random.random() < (1.0/(calvingInterval*12 - 22)):
					self.setMonthsPregnant(1)
		return False

	def __str__(self):
		s = "Age: %2d  Sex: %s" % (self.age, self.gender)
		if self.isFemale() and self.monthsContraceptiveRemaining > 0:
			s += "	Contraception: %d" % (self.monthsContraceptiveRemaining)
		elif self.gender == 'f' and self.monthsPregnant > 0:
			s += "	Pregnant: %d" % (self.monthsPregnant)
		return s

def test():
	print("Making 20 elephants")
	#random.seed(3)
	for i in range(20):
		# Make an Elephant object and store in the the variable e
		# e = Elephant()
		'''
		print('age: ', e.getAge())
		print('gender: ', e.getGender())
		print('monthsPregnant: ', e.getMonthsPregnant())
		print('monthsContraceptiveRemaining: ', e.getContraception())
		
		print('isFemale: ', e.isFemale())
		print('isPregnant: ', e.isPregnant())
		print('isCalf: ', e.isCalf())
		print('isJuvenile: ', e.isJuvenile())
		print('isAdult: ', e.isAdult())
		print('isSenior: ', e.isSenior())
		'''
		'''
		e.setAge(25)
		print( "set age to ", e.getAge() )
		e.setGender('m')
		print( "set gender to ", e.getGender() )
		e.setMonthsPregnant(4)
		print( "set months pregnant to ", e.getMonthsPregnant() )
		e.setContraception(20)
		print( "set Contraception to ", e.getContraception() )
		'''
		e = Elephant()
		print(e)
		e.progressMonth()
		print(e)
		e.dart()
		print(e)

if __name__ == "__main__":
	test()
