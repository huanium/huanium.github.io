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

import random
    
def searchSortedList( myList, value ):
	
	done = False
	found = False
	count = 0
	maxIdx = len(myList) - 1
	minIdx = 0
	
	while done != True:
		count = count + 1
		
		testIndex = (maxIdx + minIdx)//2
		
		if myList[testIndex] < value:
			minIdx = testIndex + 1
		elif myList[testIndex] > value:
			maxIdx = testIndex - 1
		else:
			done = True
			found = True
		
		if maxIdx < minIdx:
			done = True
			found = False
	return (found, count )
'''    
def test():

    a = []
    for i in range(10000):
        a.append( random.randint(0,100000) )

    a.append(42)

    a.sort()

    print(searchSortedList( a, 42 ))

if __name__ == "__main__":
    test()
'''
