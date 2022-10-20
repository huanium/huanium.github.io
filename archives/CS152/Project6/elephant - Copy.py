# Huan Bui
# Oct 18, 2017
# CS152 Project 6
#
# elephant.py
#
# Unix command:
# py elephant.py <percent Dart>
#

import sys
import random
import stats

# assign param ID
IDXCalvInterval = 0
IDXPercentDarted = 1
IDXJuvAge = 2
IDXMaxAge = 3
IDXProbCalfSurv = 4
IDXProbAdultSurv = 5
IDXProbSeniorSurv = 6
IDXCarryCap = 7
IDXNumYears = 8

IDXGender = 0
IDXAge = 1 
IDXMonthsPregnant = 2
IDXMonthsContraceptiveRemaining = 3

def newElephant( parameters, age ):
	'''
		takes in parameter list and age
		returns elephant (list of attributes of 1 elephant)
	'''

	elephant = ['', 0, 0, 0]
	
	#assign gender
	if random.random() <= 0.5:
		elephant[IDXGender] = 'm'
	else:
		elephant[IDXGender] = 'f'
	
	# assign age	
	elephant[IDXAge] = age
	
	# if female, then 
	if elephant[IDXGender] == 'f':
		if elephant[IDXAge] > parameters[IDXJuvAge] and elephant[IDXAge] <= parameters[IDXMaxAge]:
			# test if elephant is pregnant
			if random.random() < 1.0/parameters[IDXCalvInterval]:
				elephant[IDXMonthsPregnant] = random.randint(1, 22)
	
	return elephant

def initPopulation(parameters):
	'''
		takes in parameter list
		returns elephant list
	'''	
	pop = []
	for i in range(parameters[IDXCarryCap]):
                pop.append(newElephant(parameters, random.randint(1, parameters[IDXMaxAge])))
	
	return pop
	
def incrementAge( pop ):
	'''
		takes in pop
		return new pop with age + 1
	'''
	for e in pop:
		e[IDXAge] = e[IDXAge] + 1
	
	return pop

def calcSurvival( parameters, pop ):
        '''
                takes in parameters list and pop list
                check if an elephant in the population survives
                if he/she survives, then append the elephant to the new population
                then increment age 
                return a new population list
        '''
        
        # uses max age, and 3 probs
        
        new_population = []
        
        for elephant in pop:
                
                if elephant[IDXAge] <= 1:
                        
                        if random.random() < parameters[IDXProbCalfSurv]:
                                new_population.append(elephant)
                                
                elif elephant[IDXAge] >= 2 and elephant[IDXAge] <= parameters[IDXMaxAge]:
                        
                        if random.random() < parameters[IDXProbAdultSurv]:                   
                                new_population.append(elephant)
                                
                else:
                        
                        if random.random() <= parameters[IDXProbSeniorSurv]:
                                new_population.append(elephant)
                                
        return incrementAge(new_population)

def dartElephants( parameters, pop ):
        '''
                takes in parameters and pop as inputs
                check if elephant is a female adult
                test if the elephant should be darted (using random)
                if it should be darted, set preg. month to 0
                set contraceptive field to 22
                return population with darted elephants
        '''

        # use dart prob, juv age, max age

        probDart = parameters[IDXPercentDarted]
        juvAge = parameters[IDXJuvAge]
        maxAge = parameters[IDXMaxAge]

        for elephant in pop:
                if elephant[IDXGender] == 'f':
                        if elephant[IDXAge] > juvAge and elephant[IDXAge] <= maxAge:
                                if random.random() < probDart:
                                        elephant[IDXMonthsPregnant] = 0
                                        elephant[IDXMonthsContraceptiveRemaining] = 22

        #print(pop)
        return pop


def cullElephants( parameters, population ):
        '''
                takes in parameter and population lists are inputs
                returna a list containing (1) new pop list and
                (2) number of elephants culled
        '''

        carryCap = parameters[IDXCarryCap]
        #print(len(population))
        numCulled = max(0,(len(population) - carryCap))
        random.shuffle(population)
        newPopulation = population[0:min(carryCap, len(population))]

        #print( newPopulation, numCulled)
        
        return ( newPopulation, numCulled )


def controlPopulation( parameters, population ):
        '''
                takes in parameters and population as inputs
                determines whether population should be darted or culled
                returns newPop list and numCulled (which will be
                0 if elephants are darted
                return type is tuple
        '''
        if parameters[IDXPercentDarted] == 0:
                (newpop, numCulled) = cullElephants( parameters, population )
                #print(numCulled)
        else:
                newpop = (dartElephants( parameters, population ))
                numCulled = 0
        return (newpop, numCulled)

def simulateMonth( parameters, population ):
        '''
                moves the simulation forward by 1 month
                modifies only females in thepopulation
                adds a new cals to the population when one is born
                inputs: parameters and population
                returns population list
        '''
        calvInterval = parameters[IDXCalvInterval]
        juvAge = parameters[IDXJuvAge]
        maxAge = parameters[IDXMaxAge]

        for e in population:
                gender = e[IDXGender]
                age = e[IDXAge]
                monthsPregnant = e[IDXMonthsPregnant]
                monthsContraceptive = e[IDXMonthsContraceptiveRemaining]

                if gender == 'f' and age > juvAge and age <= maxAge:
                        if monthsContraceptive > 0:
                                e[IDXMonthsContraceptiveRemaining] -= 1

                        elif monthsPregnant > 0:
                                if monthsPregnant >= 22:
                                        population.append(newElephant(parameters, 1))
                                        e[IDXMonthsPregnant] = 0
                                else:
                                        e[IDXMonthsPregnant] += 1
                        else:
                                if random.random() < (1.0 / (calvInterval*12 - 22)):
                                        e[IDXMonthsPregnant] = 1
        return population

def simulateYear( parameters, population ):
        '''
                takes in parameters and population as inputs
                simulateMonth 12 times
                returns new poplulation after 1 year (12 months)
        '''
        population = calcSurvival( parameters, population )

        for i in range(12):
                population = simulateMonth( parameters, population )

        return population

def calcResults( parameters, population, numCulled ):
        '''
                takes in parameters and population lists as inputs
                
                calculates how many:
                - calves
                - juveniles
                - adult males
                - adults females
                - seniors

                returns list of these values, population size, numCulled
        '''

        juvAge = parameters[IDXJuvAge]
        maxAge = parameters[IDXMaxAge]
        
        numCalves = 0
        numJuv = 0
        numAdultMales = 0
        numAdultFemales = 0
        numSeniors = 0

        for e in population:
                age = e[IDXAge]
                if age <= 1:
                        numCalves += 1
                elif age <= 12:
                        numJuv += 1
                elif age <= 60:
                        if e[IDXGender] == 'f':
                                numAdultFemales += 1
                        else:
                                numAdultMales +=1
                else:
                        numSeniors += 1
                
        return (len(population), numCalves, numJuv, numAdultMales, numAdultFemales,
                numSeniors, numCulled)

def runSimulation( parameters ):
        '''
                takes in parameters list and number of simulation as inputs
                creates new population, applies control procedures
                loops over N years, simulating the year, and keeps track of stats
                by append them to a list
                
        '''
        popsize = parameters[IDXCarryCap]
        # init the population
        population = initPopulation( parameters )

        #print('Year 0 size:', len(population))
        
        #print(population)
        [population,numCulled] = controlPopulation( parameters, population )
        
        # run the simulation for N years, storing the results
        results = []
        currentYear = 0
        # print(parameters[IDXNumYears])
        for i in range(parameters[IDXNumYears]):
                currentYear = i
                population = simulateYear( parameters, population )
                
                [population,numCulled] = controlPopulation( parameters, population )
                # print('Year', i, 'size:', len(population))
                results.append( calcResults( parameters, population, numCulled ) )
                if results[i][0] > 2 * popsize or results[i][0] == 0 : # cancel early, out of control
                        # print('Terminating early')
                        # print('Year', currentYear, 'size:', len(population))
                        break
        # print('Year', currentYear+1, 'size:', len(population))
	
        return results



def rearrange( results ):
        '''
                takes in the results list as inputs
                rearranges so that all popsize go to one sublist and so on
                returns rearranged results (list)
        '''

        arrangedResults = []
        
        popSize = []
        numCalves = []
        numJuv = []
        numAdtMales = []
        numAdtFemales = []
        numSen = []
        numCulled = []

        IDXPopSize = 0
        IDXNumCalves = 1
        IDXNumJuv = 2
        IDXNumAdultMales = 3
        IDXNumAdultFemales = 4
        IDXNumSeniors = 5
        IDXNumCulled = 6

        arrangedResults = [popSize, numCalves, numJuv, numAdtMales, numAdtFemales,
                    numSen, numCulled]
        
        for r in results:
                popSize.append(r[IDXPopSize])
                numCalves.append(r[IDXNumCalves])
                numJuv.append(r[IDXNumJuv])
                numAdtMales.append(r[IDXNumAdultMales])
                numAdtFemales.append(r[IDXNumAdultFemales])
                numSen.append(r[IDXNumSeniors])
                numCulled.append(r[IDXNumCulled])

        return arrangedResults

def main(argv):
        '''
                takes in command from the terminal
                form:
                <py elephant.py> <darting probability>
                uses the darting probability to run simulations
                prints out relevant statistics (modified for different tasks/extensions)
        '''

        if len(argv) != 2:
                print('Usage: <py elephant.py> <prob dart>')
                exit()

        
        calvInterval = 3.1
        percentDarted = float(argv[1])
        juvAge = 12
        maxAge = 60
        probCalfSurv = 0.85
        # probCalfSurv = 0.80
        # probCalfSurv = 0.90
        probAdultSurv = 0.996
        probSeniorSurv = 0.20
        carryCap = 7000
        # carryCap = 500
        numYears = 200

        avgPopSize = 0.0
        avgNumCalves = 0.0
        avgNumJuv = 0.0
        avgNumAdultMales = 0.0
        avgNumAdultFemales = 0.0
        avgNumSeniors = 0.0
        avgNumCulled = 0.0

        # indexing items in Results

        IDXPopSize = 0
        IDXNumCalves = 1
        IDXNumJuv = 2
        IDXNumAdultMales = 3
        IDXNumAdultFemales = 4
        IDXNumSeniors = 5
        IDXNumCulled = 6
	
        parameters = [calvInterval, percentDarted, juvAge, maxAge, probCalfSurv, 
			probAdultSurv, probSeniorSurv, carryCap, numYears]
        
        results = runSimulation( parameters )

        # print(results[-1])

        # below is the print command that can used to pipe output to .CSV

        year = 1
        for r in results:
                # prints year + total population in r, separated by a comma
                # I'm being lazy here but it's fine because the list is short.
                # I could initiate Indexing variables but that would be unncessary here
                print(year, ',', r[0])
                year += 1


        # below is the code for the original main() function
        '''

        l = len(results)
        
        for r in results:
                
                avgPopSize += r[IDXPopSize]/l
                avgNumCalves += r[IDXNumCalves]/l
                avgNumJuv += r[IDXNumJuv]/l
                avgNumAdultMales += r[IDXNumAdultMales]/l
                avgNumAdultFemales += r[IDXNumAdultFemales]/l
                avgNumSeniors += r[IDXNumSeniors]/l
                avgNumCulled += r[IDXNumCulled]/l
                
                #print(r[IDXPopSize])
        
        print('Average pop size: {0:0.1f}'.format(avgPopSize))
        print('Average num calves: {0:0.1f}'.format(avgNumCalves))
        print('Average num Juveniles: {0:0.1f}'.format(avgNumJuv))
        print('Average num Adult Males: {0:0.1f}'.format(avgNumAdultMales))
        print('Average num Adult Females: {0:0.1f}'.format(avgNumAdultFemales))
        print('Average num Seniors: {0:0.1f}'.format(avgNumSeniors))
        print('Average num Culled: {0:0.1f}'.format(avgNumCulled))


        '''

        # below is the code for extension 3
        '''
        

        name_statistics = ['Average Population Size:', 'Average Number of Calves:',
                           'Average Number of Juveniles:', 'Average Number of Adult Males:',
                           'Average Number of Adult Females:', 'Average Number of Seniors:',
                           'Average Number Culled:']
        
        for i in range(len(rearrange( results ))):
                print()
                print(name_statistics[i])
                print('Mean: {0:0.1f}'.format(stats.mean(rearrange(results)[i])))
                print('Stdev: {0:0.1f}'.format(stats.stdev(rearrange(results)[i])))
        '''

        
           

# initial test function                
'''
def test():

    # assign each parameter from the table above to a variable with an informative name
	calvInterval = 3.1
	percentDarted = 0.0
	juvAge = 12
	maxAge = 60
	probCalfSurv = 0.85
	probAdultSurv = 0.996
	probSeniorSurv = 0.20
	#carryCap = 7000
	carryCap = 20
	numYears = 200
	
	# make the parameter list out of the variables
	parameters = [calvInterval, percentDarted, juvAge, maxAge, probCalfSurv, 
					probAdultSurv, probSeniorSurv, carryCap, numYears]
					
	paramNames = ['IDXCalvInterval', 'IDXPercentDarted', 'IDXJuvAge', 'IDXMaxAge', 
	'IDXProbCalfSurv', 'IDXProbAdultSurv', 'IDXProbSeniorSurv', 
	'IDXCarryCap', 'IDXNumYears']
					
    # print the parameter list
	for i in range(len(parameters)):
		print(paramNames[i], ':', parameters[i])
	
	# test newElephant()
	
	pop = []
	for i in range(15):
		pop.append(newElephant(parameters, random.randint(1, parameters[IDXMaxAge])))

	for e in pop:
		print(e)
	
		
	# test initPopulation()
	print()
	print() 
	print('<<<<< INITIAL POPULATION >>>>>>')
	pop = initPopulation( parameters )
	for e in pop:
		print(e)
		
	# test incrementAge()
	print()
	print()
	print('<<<<< INCREMENT AGE >>>>>>>')
	incrementAge(pop)
	for e in pop:
		print(e)

'''

def defaultParameters():
	'''
		takes in no arguments
		returns a list with all necessary parameters for the simulation 
		with their default values
	'''
	parameters = [3.1, 0.0, 12, 60, 0.85, 0.996, 0.20, 7000, 200]
	
	return parameters
	
def elephantSim( percDart, inputParameters = None ):
	'''
		docstrings go here!
	'''
	
	if inputParameters == None:
		parameters = defaultParameters()
	else:
		parameters = inputParameters
	
	parameters[IDXPercentDarted] = percDart
	results = runSimulation( parameters )
	
	# repeat simulation 4 more times
	# collect all results in a single list
	# results is a list of lists
	# each sub-list consists of total population and other stats
	for i in range(4):
		results = results + runSimulation(parameters)
	
	averagePopulation = 0.0
	
	for r in results:
		averagePopulation += r[0]/len(results)

	# so that optfunc returns 0 if optimal percDart found	
	return [int(parameters[IDXCarryCap] - averagePopulation), int(averagePopulation)]

if __name__ == "__main__":
    main(sys.argv)
