# Huan Bui
# Sept 20, 2017
# CS152 Project 3
#
# stats.py
#
# Unix command to run program:
# None because this is just a library that is used by other programs...

def sum(somelist):
    '''
        takes in a list of numbers
        returns the sum of all elements in list
    '''
    total = 0.0 #initializing sum

    for i in range(len(somelist)):
        total = total + somelist[i]

    return total


def mean(somelist):
    '''
        takes in a list of numbers
        returns the mean value of all the elements
    '''
    return sum(somelist)/len(somelist)

def max(somelist):
    '''
        takes in a list of numbers
        returns the maximum value of the list
    '''
    
    maxval = somelist[0]

    for i in range(len(somelist)):
        if somelist[i] > maxval:
            maxval = somelist[i]

    return maxval


def min(somelist):
    '''
        takes in a list of numbers
        returns the minimum value of the list
    '''
    minval = somelist[0]

    for i in range(len(somelist)):
        if somelist[i] < minval:
            minval = somelist[i]

    return minval

    
def variance(somelist):
    '''
        takes in a list of numbers
        returns the variance value of the list
    '''
    sumOfSquares = 0.0

    for i in range(len(somelist)):
        sumOfSquares += (somelist[i] - mean(somelist))**2

    return sumOfSquares/(len(somelist) - 1)


def stdev(somelist):
    '''
        takes in a list of numbers
        returns the standard deviance value of the list
    '''
    return (variance(somelist))**(1/2)

def celsius2fahrenheit(tempC):
    '''
        takes in float temperature in degree C
        returns float temperature in degree F
    '''
    tempF = (tempC*9/5) + 32
    
    return tempF

def test():
    '''
        test the above functions
    '''
    example = [1,2,3,4]
    
    exSum = sum(example)
    
    exMean = mean(example)
    
    print("Sum: ", exSum)
    print("Mean: ", exMean)
    print("Max: ", max(example))
    print("Min: ", min(example))
    print("Variance: ", variance(example))
    print("Stdev: ", stdev(example))

if __name__ == "__main__":
    test()
