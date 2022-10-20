# Huan Bui
# Sept 27, 2017
# CS152 Project 4
#
# penguin.py
#
# Unix command to call:
# py (or python3) penguin.py [numSim] [numYearElNino] [N] (optional)
#

import sys
import random
import argparse

simLoopCount = 0

def initPopulation(initSize, femProb):
    '''
        takes in two parameters "initial size of the population" and
        the "probability of an individual being female"
        returns a population (list) with 'f', and 'm' entries
    '''
    pop = []
    for i in range(initSize):
        ran = random.random()
        if ran < femProb:
            pop.append('f')
        else:
            pop.append('m')
    
    return pop

def simulateYear(pop, elNinoProb, stdRho, elNinoRho, probFemale, maxCapacity):
    '''
        takes in 6 parameters:
        population list, probability of an El Nino,
        growth factor in reg year
        growth factor in El Nino year, probability of a new female,
        and carrying capacity of the ecosystem
        returns a new population after one year
    '''
    elNinoYear = False
    if random.random() < elNinoProb:
        elNinoYear = True
    
    newpop = []
    
    for pen in pop:
        if len(newpop) > maxCapacity:   # no need to add
            break
        
        if elNinoYear == True:
            if random.random() < elNinoRho:
                newpop.append(pen)  # penguine survives El Nino
        else: 
            newpop.append(pen) # no El Nino so pen survives
            if random.random() < stdRho - 1.0:
                '''
                    if stdRho near 1
                    --> unlikely that random.random() < stdRho - 1.0
                    --> that means newpop is less likely to be appended
                    --> makes sense
                '''
                if random.random() < probFemale:
                    newpop.append('f')  #add a random individual
                else:
                    newpop.append('m')  #add a random individual
    return newpop

def runSimulation( N, initPopSize, probFemale, elNinoProb, stdRho, 
                    elNinoRho, maxCapacity, minViable ):
    '''
        takes in 8 parameter:
        N: (int) number of years simulated in 1 sim
        initPopSize: (int) inital population size
        probFemale: (float) probability a new individual is a female
        elNinoprob: (float) probability of El Nino occurring
        stdRho: (float) standard growth factor (should be greater than 1
        elNinoRho: (float) standard reduction factor (should be less than 1)
        maxCapacity: (int) carrying capacity of the population
        minviable: (int) below which point the population will die
        returns the year at which the population dies
        returns N if the population survives the simulation
    '''
    
    # make a random pop with determined size
    population = initPopulation(initPopSize, probFemale) 
    
    endDate = N # number of years
    
    for i in range(N):  #run sim N times (or N years)

        global simLoopCount
        simLoopCount += 1
        
        newPopulation = simulateYear(population, elNinoProb,
                        stdRho, elNinoRho, probFemale, maxCapacity) # simulate new 
        
        if len(newPopulation) < minViable: # population too small
            endDate = i
            break
        
        if not('f' in newPopulation) or not('m' in newPopulation): # un-reproductive
            endDate = i
            break
            
        population = newPopulation # population survives --> print population size

        # print('Pop size: ', len(population))
        # then population get fed into simulateYear() to get new population

    return endDate

def cepd(endDates, N):
    '''
        takes in endDates which is a list of the last year when the pop is viable
        and N which is the number of years the simulation ran
        returns a list of extinction probability
    '''
    CEPD = [0.0]*N
    
    for endDate in endDates:
        if endDate < N:
            for k in range(endDate, N):
                CEPD[k] += 1.0/len(endDates)
    return CEPD

# following 3 functions are test functions!
# I comment out so they are easier to ignore!

'''
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
'''

# main



def main(argv):
    '''
        takes in argument from command line including:
        (required) number of Simulations
        (required) El Nino cycle
        (optional) number of years in each simulation
        print results
    '''
    
    count = 0
    endDates = []
    #N = 201 #use this only for normal argv...with parse, no need!
    
    if len(sys.argv) < 3:
        print("usage : py initPopulation.py <number of Simulations> <number of years between El Nino event>")
        exit()
        
    #numSim = int(argv[1])
    #numYearElNino = int(argv[2])
    
    '''
        Below is the code for flags.
        This allows modifying N.
        However, can choose not to modify. Default value for N = 201
        Source: online python documentations 
    '''
    
    # prompts user to input numSim and numYearElNino
    # but also gives an option to modify N (years)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("numSim", type=int,
                    help="add number of Simluation")
    parser.add_argument("numYearElNino", type=int,
                    help="add number El Nino cycle")
    parser.add_argument("-N", "--verbosity", type=int,
                    help="add N here", default=201)
    args = parser.parse_args()

    numSim = args.numSim
    numYearElNino = args.numYearElNino
    N = args.verbosity
    
    initPopSize = 500
    probFemale = 0.5
    elNinoProb = 1.0/numYearElNino
    stdRho = 1.188
    elNinoRho = 0.41
    maxCapacity = 2000
    #maxCapacity = 3000
    minViable = 10
    
    for i in range(numSim):
        endDates.append(runSimulation(N, initPopSize, probFemale,
                    elNinoProb, stdRho, elNinoRho, maxCapacity, minViable))
    
    for endDate in endDates:
        if endDate < N: # the population cannot make it through N years
            count += 1
            
    print('Probability of extinction in', N, 'years: ', count/numSim)

    CEPD = cepd(endDates, N)

    # for i in range(0, len(CEPD), 10):
        # print('Year', i, ': {0:.2f}'.format(CEPD[i]))
    '''
    for i in range(len(CEPD)):
        print(i+1, ', {0:.2f}'.format(CEPD[i]))
    '''    
    print('Total loop count in runSim: ', simLoopCount) # no. loops in runSim

    
if __name__ == "__main__":
    #test()
    #testSimYear()
    #testRunSim
    main(sys.argv)
