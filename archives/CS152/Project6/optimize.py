# Huan Bui
# CS152 Project 6
# Oct 18, 2017
#
# File name
# optimize.py
#
# Run command:
# py optimize.py
#
#

import sys
import elephant
import random
import stats

# Executes a search to bring the result of the function optfunc to zero.
# min: minimum parameter value to search
# max: maximum parameter value to search
# optfunc: function to optimize
# parameters: optional parameter list to pass to optfunc
# tolerance: how close to zero to get before terminating the search
# maIterations: how many iterations to run before terminating the search
# verbose: whether to print lots of information or not

populationList = []

def optimize( min, max, optfunc, parameters = None, tolerance = 0.001, 
				maxIterations = 20, verbose=False):
	'''takes in and min, max, target function, parameters, tolerance,
        maxIterations, and verbose
        returns a value at which the target function has value approximately 0
        '''
	
	done = False
	
	while (done == False):
		testValue = (max+ min)/2
		if verbose == True:
			# print(testValue)
			result = optfunc( testValue, parameters )
			# print(result)
			global populationList
			populationList.append(result[1])
		if result[0] > 0:
			max = testValue
		elif result[0] < 0:
			min = testValue
		else:
			done = True
		if max - min < tolerance:
			done = True
		maxIterations -= 1
		if maxIterations <= 0:
			done = True
			
			
	return testValue			

# Evaluates the effects of the selected parameter on the dart percentage
# whichParameter: the index of the parameter to test
# testmin: the minimum value to test
# testmax: the maximum value to test
# teststep: the step between parameter values to test
# defaults: default parameters to use (default value of None)

def evalParameterEffect( whichParameter, testmin, testmax, teststep, defaults=None, verbose=False ):
        ''' takes in the specified parameter, testmin, testmax, teststep,
        dafault parameters, and verbose
        returns a list results which is a list of tuple
        containing the optimal percDart and the value of the target function
        at that optimal value
        '''
	if defaults == None:
		simParameters = elephant.defaultParameters()
	else:
		simParameters = defaults[:]
	results = []
	if verbose:
		print("Evaluating parameter {0:d} from {1:.3f} to {2:.3f} with step {3:.3f}".format(whichParameter, testmin, testmax, teststep))
	t = testmin
	while t < testmax:
		simParameters[whichParameter] = t
		percDart = optimize( 0.0, 0.5, elephant.elephantSim, simParameters,
    						verbose = True)
		results.append((t, percDart ))
		if verbose:
			print("{0:8.3f} \t{1:8.3f}".format(t, percDart))
		t += teststep
	if verbose:
		print("Terminating")
		print("Average Population: ", stats.mean(populationList))
		print("Standard Deviation: ", stats.stdev(populationList))
		for i in populationList:
                        print(i)
	return results

	
# a function that returns x - target
def target(x, pars):
    return x - 0.73542618


# Tests the binary search using a simple target function.
# Try changing the tolerance to see how that affects the search.
def testTarget():
    res = optimize( 0.0, 1.0, target, tolerance = 0.01, verbose=True)
    print(res)
    return

def testEsim():
	opt = optimize(0.0, 0.5, elephant.elephantSim, verbose = True)
	print(opt)
	

if __name__ == "__main__":
    # testEsim()
    evalParameterEffect( elephant.IDXProbAdultSurv, 0.98, 1.0, 0.001, verbose=True )
