# Huan Bui
# CS152 Project 7
# October 31, 2017
# 
# File name: 
# simulation.py
#
# run command:
#
#
#
#

import random
import sys
import elephant

class Simulation:

    def __init__(self,
                 percDart = 0.425,
                 cullStrategy = 0,
                 probCalfSurv = 0.85,
                 probAdultSurv = 0.996,
                 probSeniorSurv = 0.2,
                 calvingInterval = 3.1,
                 carryingCapacity = 7000):

        self.percDart = percDart
        self.cullStrategy = cullStrategy
        self.probCalfSurv = probCalfSurv
        self.probAdultSurv = probAdultSurv
        self.probSeniorSurv = probSeniorSurv
        self.calvingInterval = calvingInterval
        self.carryingCapacity = carryingCapacity

        population = []
        results = []

    # getter methods

    def getPercDart(self):
        return self.percDart

    def getCullStrategy(self):
        return self.cullStrategy

    def getProbCalfSurv(self):
        return self.probCalfSurv

    def getProbAdultSurv(self):
        return self.probAdultSurv

    def getProbSeniorSurv(self):
        return self.probSeniorSurv

    def getCalvingInterval(self):
        return self.calvingInterval

    def getCarryingCapacity(self):
        return self.carryingCapacity

    # setter methods

    def setPercDart(self, val):
        self.percDart = val

    def setCullStrategy(self, val):
        self.cullStrategy = val

    def setProbCalfSurv(self, val):
        self.probCalfSurv = val

    def setProbAdultSurv(self, val):
        self.probAdultSurv = val

    def setProbSeniorSurv(self, val):
        self.probSeniorSurv = val

    def setCalvingInterval(self, val):
        self.calvingInterval = val

    def setCarryingCapacity(self, val):
        self.carryingCapacity = val


    # sim

    def initPopulation(self):
        '''
	    takes in parameter list
	    returns elephant list
	'''
        self.population = []
        for i in range(self.getCarryingCapacity()):
            self.population.append(elephant.Elephant(self.getCalvingInterval()))

        return self.population


    def showPopulation(self):
        '''
	    prints population
	'''
        print('Showing population')
        for e in self.population:
            print(e)

    def incrementAge(self):
        '''
	    takes in self
	    return new pop with age + 1
	'''
        for e in self.population:
            e.incrementAge()
    
    def dartPopulation(self):
        '''
	    takes in self
	    call dart() for each elephant in the population
	'''
        for e in self.population:
            if e.isFemale()and e.isAdult() and random.random() < self.getPercDart():
                    e.dart()
        
    def cullElephants_0(self):
        '''
	    takes in self
	    returns numCulleds
	'''
        carryCap = self.getCarryingCapacity()
        numCulled = max(0, (len(self.population) - carryCap))
        random.shuffle(self.population)
        self.population = self.population[0:min(carryCap, len(self.population))]

        return numCulled
    
    def controlPopulation(self):
        '''
	    takes in self
	    select population control strategy
	    returns numCulled
	'''
        if self.percDart == 0:
            if self.cullStrategy == 0:
                numCulled = self.cullElephants_0()
            elif self.cullStrategy == 1:
                numCulled = self.cullElephants_1()
            elif self.cullStrategy == 2:
                numCulled = self.cullElephants_2()
        else:
            self.dartPopulation()
            numCulled = 0

        return numCulled
    
    def simulateMonth(self):
        '''
	    takes in self
	    calls progressMonth for each elephant in pop
	'''
        for e in self.population:
            if e.progressMonth() == True:
                self.population.append(elephant.Elephant(age = 1))

    def calcSurvival(self):
        '''
	    takes in self
	    determines if an elephant will die
	    based on survival probabilities
	'''
        pop = []
        for e in self.population:
            if e.isCalf():
                if random.random() < self.getProbCalfSurv():
                    pop.append(e)
            elif e.isJuvenile() or e.isAdult():
                if random.random() < self.getProbAdultSurv():
                    pop.append(e)
            else:
                if random.random() < self.getProbSeniorSurv():
                    pop.append(e)

        self.population = pop                                            
        
    def simulateYear(self):
        '''
	    takes in self
	    calls simulateMonths 12 times
	'''
        self.calcSurvival()
        self.incrementAge()
        for i in range(12):
            self.simulateMonth()                         

    def calcResults(self, numCulled):
        '''
	    takes in self, numculled
	    return a list of attributes of population
	'''
        numCalves = 0
        numJuv = 0
        numAdtM = 0
        numAdtF = 0
        numSen = 0

        for e in self.population:
            if e.isCalf():
                numCalves += 1
            if e.isJuvenile():
                numJuv += 1
            if e.isAdult():
                if e.isFemale():
                    numAdtF += 1
                else:
                    numAdtM += 1
            if e.isSenior():
                numSen += 1
        return [len(self.population), numCalves, numJuv, numAdtM,
                numAdtF, numSen, numCulled]

    def runSimulation(self, numYears, startFresh = True, adjust = True):
        '''
	    takes in self, numYears
	    return results: list of result from calcResults
	'''
        if startFresh == True:
            self.initPopulation()
            self.controlPopulation()
            self.results = []
            
        for y in range(numYears):
            self.simulateYear()
            numCulled = self.controlPopulation()
            self.results.append(self.calcResults(numCulled))
            if adjust:
                self.adjustPercDart()

        return self.results
    
    def writeDemographics(self, filename):
        '''
	    takes in self, filename
	    write to filename results
	'''
        f = open(filename, 'w')
        f.write("# Demographics, ")
        f.write("Darting Percentage: ")
        f.write(str(self.getPercDart()))
        f.write('\n')
        f.write("# Yr,Pop,Calves,Juvs,AdtM,AdtF,Sen,Culled\n")
        year = 0
        for item in self.results:
            year += 1
            f.write(str(year))
            f.write(',')
            for val in item:
                f.write(str(val))
                f.write(',')
            f.write('\n')

    def cullElephants_1(self):
        '''
	    takes in self
	    culls only adult females
	    return numCulled
	'''
        carryCap = self.getCarryingCapacity()
        numCulled = max(0, (len(self.population) - carryCap))

        popAdultFemale = []
        popRest = []
        for e in self.population:
            if e.isFemale() == True and e.isAdult() == True:
                popAdultFemale.append(e)
            else:
                popRest.append(e)

        random.shuffle(popAdultFemale)
        popAdultFemale = popAdultFemale[0:(len(popAdultFemale) - numCulled)]

        self.population = popRest + popAdultFemale
        random.shuffle(self.population)

        return numCulled

    def cullElephants_2(self):
        '''
	    takes in self
	    culls only juveniles
	    return numCulled
	'''
        carryCap = self.getCarryingCapacity()
        numCulled = max(0, (len(self.population) - carryCap))

        popJuv = []
        popNonJuv = []
        for e in self.population:
            if e.isJuvenile() == True:
                popJuv.append(e)
            else:
                popNonJuv.append(e)

        random.shuffle(popJuv)
        popJuv = popJuv[0:(len(popJuv) - numCulled)]

        self.population = popJuv + popNonJuv
        random.shuffle(self.population)

        return numCulled
      
    def decimate(self, per = 0.3):
        '''
	    takes in self, per
	    kills per of total population
	'''
        random.shuffle(self.population)
        self.population = self.population[0:int((1-per)*len(self.population))]
        

    def adjustPercDart(self, step = 0.01):
        '''
	    takes in self, step
	    adjust percDart according to the difference between
	    pop size and carryCap
	'''
        error = step*self.carryingCapacity
        if len(self.population) - self.carryingCapacity > error:
            self.percDart += 0.0005
        elif self.carryingCapacity - len(self.population) > error:
            self.percDart -= 0.0005
        

def test_simple():
    sim = Simulation()
    sim.setCarryingCapacity(20)
    sim.initPopulation()
    sim.showPopulation()
    sim.incrementAge()
    sim.showPopulation()
    #sim.dartPopulation()
    #sim.setCarryingCapacity(15)
    #print( "numCulled:", sim.cullElephants_0())
    #sim.showPopulation()

if __name__ == "__main__":
    test_simple()
    

    

        
