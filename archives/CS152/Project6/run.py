# Huan Bui
# CS152 Project 6
# Oct 18, 2017
#
# file name
# run.py
#
# Running command
# py run.py -param <param Name> -testmin <testmin> -testmax <testmax> -teststep <teststep>
#
#

import sys
import optimize
import elephant
import argparse

def run( param, testmin, testmax, teststep ):
    '''takes in the parameter that the user wants to modify
    and the interval (min and max) and the steps
    returns results which is a list of tuple containing
    the value of the parameter
    and the optimal darting percentage at that parameter value
    '''

    if (param == 'probAdultSurv'):
        results = optimize.evalParameterEffect( elephant.IDXProbAdultSurv, testmin, testmax,
                                                teststep, verbose = True)
    elif (param == 'probCalfSurv'):
        results = optimize.evalParameterEffect( elephant.IDXProbCalfSurv, testmin, testmax,
                                                teststep, verbose = True)
    elif (param == 'probSeniorSurv'):
        results = optimize.evalParameterEffect( elephant.IDXProbSeniorSurv, testmin, testmax,
                                                teststep, verbose = True)
    elif (param == 'calvInterval'):
        results = optimize.evalParameterEffect( elephant.IDXCalvInterval, testmin, testmax,
                                                teststep, verbose = True)
    elif (param == 'carryCap'):
        results = optimize.evalParameterEffect( elephant.IDXCarryCap, testmin, testmax,
                                                teststep, verbose = True)
    else:
        print('Error')
        print('To specify parameter, type 1 of the below options, followed by min/max/step:')
        print('probAdultSurv')
        print('probCalfSurv')
        print('probSeniorSurv')
        print('calvInterval')
        print('carryCap')
        exit()
        
    return results

def main(argv):
    '''
    if len(argv) != 5:
        print('To specify parameter, type 1 of the below options, followed by min/max/step:')
        print('probAdultSurv')
        print('probCalfSurv')
        print('probSeniorSurv')
        print('calvInterval')
        print('carryCap')
        exit()
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-param", "--verbosity0", type=str,
                    help="specify parameter here", default='probAdultSurv')
    parser.add_argument("-testmin", "--verbosity1", type=float,
                    help="add test min here", default=0.98)
    parser.add_argument("-testmax", "--verbosity2", type=float,
                    help="add test max here", default=1.0)
    parser.add_argument("-teststep", "--verbosity3", type=float,
                    help="add test step here", default=0.001)
    args = parser.parse_args()

    param = args.verbosity0
    testmin = args.verbosity1
    testmax = args.verbosity2
    teststep = args.verbosity3

    '''
    param = str(argv[1])
    if (param == 'carryCap'):
        testmin = int(argv[2])
        testmax = int(argv[3])
        teststep = int(argv[4])
    else:
        testmin = float(argv[2])
        testmax = float(argv[3])
        teststep = float(argv[4])
    '''

    # carryingCap only accepts int arguments
    
    if (param == 'probAdultSurv'):
        fp = open('probAdultSurv.csv', 'w')
    elif (param == 'probCalfSurv'):
        fp = open('probCalfSurv.csv', 'w')
    elif (param == 'probSeniorSurv'):
        fp = open('probSeniorSurv.csv', 'w')
    elif (param == 'calvInterval'):
        fp = open('calvInterval.csv', 'w')
    elif (param == 'carryCap'):
        testmin = int(testmin)
        testmax = int(testmax)
        teststep = int(teststep)
        fp = open('carryCap.csv', 'w')
    
    results = run( param, testmin, testmax, teststep)
    
    fp.write('# Below are the values for ')
    fp.write(param)
    fp.write(' and their respective percDart')
    fp.write('\n')
    
    for result in results:
        # print(result[0], ',', result[1])
        fp.write(str(result[0]))
        fp.write(', ')
        fp.write(str(result[1]))
        fp.write('\n')

    fp.close()
    
if __name__ == "__main__":
    main(sys.argv)
