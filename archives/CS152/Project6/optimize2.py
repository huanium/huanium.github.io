# Huan Bui
# CS152 Project 6
# Oct 18, 2017

#
#
#
#
#
#
#

import sys
import elephant
import random

# Executes a search to bring the result of the function optfunc to zero.
# min: minimum parameter value to search
# max: maximum parameter value to search
# optfunc: function to optimize
# parameters: optional parameter list to pass to optfunc
# tolerance: how close to zero to get before terminating the search
# maIterations: how many iterations to run before terminating the search
# verbose: whether to print lots of information or not

def optimize( min, max, optfunc, parameters = None, tolerance = 0.001, 
				maxIterations = 20, verbose=False):
	
	done = False
	
	while (done == False):
		testValue = (max+ min)/2
		if verbose == True:
			print(testValue)
			result = optfunc( testValue, parameters )
			print(result)
		
		if result > 0:
			max = testValue
		elif result < 0:
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

def testSim():
	opt = optimize(0.0, 0.5, elephant.elephantSim, verbose = True)
	print(opt)
	


if __name__ == "__main__":
    # testSim()
    evalParameterEffect( elephant.IDXProbAdultSurv, 0.80, 0.90, 0.01, verbose=True )
