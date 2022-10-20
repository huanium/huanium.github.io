# Huan Bui
# Sept 27, 2017
# CS152 Project 4

import sys
import random

def initPopulation(initSize, femProb):
	pop = []
	for i in range(initSize):
		ran = random.random()
		if ran < femProb:
			pop.append('f')
		else:
			pop.append('m')
	
	return pop

def simulateYear(pop, elNinoProb, stdRho, elNinoRho, probFemale, maxCapacity):
	
	elNinoYear = False
	if random.random() < elNinoProb:
		elNinoYear = True
	
	newpop = []
	
	for pen in pop:
		if len(newpop) > maxCapacity:
			break
		
		if elNinoYear == True:
			if random.random() < elNinoRho:
				newpop.append(pen)
		else: 
			newpop.append(pen)
			if random.random() < stdRho - 1.0:
				if random.random() < probFemale:
					newpop.append('f')
				else:
					newpop.append('m')
	return newpop

def runSimulation( N, initPopSize, probFemale, elNinoProb, stdRho, 
                    elNinoRho, maxCapacity, minViable ):
	
	population = initPopulation(initPopSize, probFemale)
	
	endDate = N # number of years
	
	for i in range(N):
		newPopulation = simulateYear(population, elNinoProb, stdRho, elNinoRho, probFemale, maxCapacity)
		
		if len(newPopulation) < minViable:
			endDate = i
			break
		if not('f' in newPopulation) or not('m' in newPopulation):
			endDate = i
			break
			
		population = newPopulation
		print(len(population))

	return endDate
	
# test function for initPopulations
def test():
    popsize = 10
    probFemale = 0.5

    pop = initPopulation(popsize, probFemale)

    print(pop)

def testSimYear():    
	pop = initPopulation(10, 0.5)
	
	newpop = simulateYear(pop, 1.0, 1.188, 0.4, 0.5, 2000)
	print("El Nino year")
	print(newpop)
	
	newpop = simulateYear(pop, 0.0, 1.188, 0.4, 0.5, 2000)
	print("Standard year")
	print(newpop)   

def testRunSim():

	# make sure initPopSize is larger than minViable
	runSimulation(1000, 500, 0.5, 1.0/7.0, 1.188, 0.41, 2000, 10) 
	
def main(sys.argv):
	if len(sys.argv) < 3:
		print("usage : py initPopulation.py <number of Simulations> <number of years between El Nino event')
		exit()
	
	numSim = int(argv[1])
	numYearElNino = int(argv[2])

        resultList = []

        initPopSize = 500
        probFemale = 0.5
        elNinoProb = 1.0/7.0
        stdRho = 1.188
        elNinoRho = 0.41
        maxCapacity = 2000
        minViable = 10

        for i in range(numSim):
                resultList.append(runSimulation(numSim, initPopSize, probFemale, elNinoProb,
                                stdRho, elNinoRho, maxCapacity, minViable))

        count = 0
        for result in resultList:
                if result < N:
                      count += 1

        print('Probability of extinction in', numSim, 'years: ', count/numSim)
	
if __name__ == "__main__":
    main(sys.argv)
