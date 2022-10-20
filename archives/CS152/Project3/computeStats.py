# Huan Bui
# Sept 20, 2017
# CS152 Project 3
#
# computeStats.py
#
# Unix command to run program:
# (first week of June - 1m)
# grep '06/0[17]/2017' 3100_iSIC.csv | cut -d ',' -f 9 | py computeStats.py
# (first week of June - 5m)
# grep '06/0[17]/2017' 3100_iSIC.csv | cut -d ',' -f 15 | py computeStats.py
# (first week of June - variable of choice: AirTemp)
# grep '06/0[1234567]/2017' 3100_iSIC.csv | cut -d ',' -f 30 | py computeStats.py
# 


import sys
import stats

def main(stdin):
    '''
        takes in parameter stdin from data, store every line of data (float)
        into list called templist, then prints out all relevant statistics
        min, max, mean, stdev.
    '''
    
    #assign mylist the empty list []
    templist = []

    #assign to buf the result of calling readline on stdin
    buf = stdin.readline()

    #while buf.strip is not equal to the empty string
        #append to mylist the result of casting buf to a float
        #assign to buf the result of calling readline on stdin

    while buf.strip() != '':
        templist.append(float(buf))
        buf = stdin.readline()

    print()
    print('Statistics: ')
    print()
    '''
    print('Min C: ', stats.min(templist)) #for task 3
    print('Min F: ', stats.celsius2fahrenheit(stats.min(templist)))
    print('Max C: ', stats.max(templist))
    print('Max F: ', stats.celsius2fahrenheit(stats.max(templist)))
    print('Mean C: ', stats.mean(templist))
    print('Mean F: ', stats.celsius2fahrenheit(stats.mean(templist)))
    print('Stdev C: ', stats.stdev(templist))
    print('Stdev F: ', stats.celsius2fahrenheit(stats.stdev(templist)))
    '''
    print('Min thermocline depth: ', stats.min(templist)) #for section 5 (June)
    print('Max thermocline depth: ', stats.max(templist))
    print('Mean: {0:f}'.format(stats.mean(templist)))
    print('Stdev: {0:f}'.format(stats.stdev(templist)))
    
if __name__ == "__main__":
    main(sys.stdin)
