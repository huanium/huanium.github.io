# Huan Bui
# Sept 20, 2017
# CS152 Project 3
#
# thermocline.py
#
# Unix command to run program:
# cat 3100_iSIC.csv | grep '06/02/2017' | grep -e ' 1:00' -e ' 2:00' | py thermocline.py

import sys

def density(temps):
    '''
        takes in parameter temps (which is a list of temperatures type float)
        return a list of densities (type float)
    '''
    rhos = []
    errorCount = 0

    for t in temps:
        rho = 1000 * (1 - (t + 288.9414) * (t - 3.9863)**2 / (508929.2*(t + 68.12963)))
        rhos.append(rho)

        if t < -273.15:
            errorCount += 1
    '''
    if errorCount == 0:
        print()
        print('No error data')
    else:
        print('There is error data')
    '''
    
    return rhos


def thermocline_depth(temps, depths):
    '''
        takes in lists (type float) of temperatures and depths
        returns thermodepth (depth where water density changes most rapidly)
    '''
    rhos = density(temps)
    drho_dz = []

    for i in range(len(rhos)-1):
        drho_dz.append((rhos[i+1] - rhos[i])/(depths[i+1] - depths[i]))
        #print(temps[i], rhos[i], drho_dz[i])    
        
    max_drho_dz = -1.0
    maxindex = -1
    for i in range(len(drho_dz)):
        if abs(drho_dz[i]) < 999 and drho_dz[i] > max_drho_dz: #ignore all -99999
            max_drho_dz = drho_dz[i]
            maxindex = i

    thermoDepth = (depths[maxindex] + depths[maxindex+1])/2
    #print(thermoDepth)
    #print(drho_dz)
    #print()
    #print(drho_dz)
    return thermoDepth
                    
def main(stdin):
    '''
        takes in data from stdin
        1/ prints datetime and thermocline values, separated by a comma
        2/ prints out minimum and maximum thermodepths and datetime of when such events occurred
    '''

    # these are the fields corresponding to the temperatures in order by depth
    # note the 0-indexing... !!!fields are numbered from 1
    fields = [8, 11, 14, 17, 20, 23, 26]

    # these are the depth values for each temperature measurement
    depths = [ 1, 3, 5, 7, 9, 11, 13 ]

    # create variables to hold the max depth, min depth, the datetime
    # of the max depth and the datetime of the min depth.  Give them
    # reasonable initial values (a small value for max depth, a large
    # value for min depth, and empty strings for the datetime variables.
    maxDepth = -1.0
    dateMaxDepth = ''
    minDepth = 100000.0
    dateMinDepth = ''
    
        # assign buf the first line of stdin and then start the standard while loop until buf is empty
    buf = stdin.readline()

    while buf.strip() != '':
        #print()
        words = buf.split(',') # split buf on commas and assign it to words

        datetime = words[0] # assign to datetime the value in words[0]
        temps = [] # assign to temps the empty list

        for i in range(len(depths)):    # loop over the number of items in depths (loop variable i)
            temps.append(float(words[fields[i]]))   # append to temps the result of casting words[ fields[i] ] to a float

        depth = thermocline_depth(temps, depths)# assign to depth the result of calling thermocline_depth with temps and depths as arguments

        #print(depth)
        #print(temps)
        #print(datetime, ',', depth)

        
        if depth > maxDepth:    # test if depth is greater than maxdepth and update maxdepth and maxtime if it is
            maxDepth = depth
            dateMaxDepth = datetime

            
        if depth < minDepth: # test if depth is less than mindepth and update mindepth and mintime if it is
            minDepth = depth
            dateMinDepth = datetime
                
        print(datetime, ',', depth)    # print out the datetime value and the depth value, separated by commas
        
        buf = stdin.readline()  # update buf with the next readline from stdin

    #print()
    #print()
    #print(dateMaxDepth, ',', maxDepth, ',', dateMinDepth, ',', minDepth)    # print out the minimum and maximum thermocline depth and the corresponding date/time


if __name__ == "__main__":
    main(sys.stdin)
