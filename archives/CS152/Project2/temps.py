# Huan Quang Bui
# Sept 13, 2017
# CS152 Project 2
#
# Command to run the program:
# grep /2014 blend.csv | cut -f 4,5 -d ',' | py temps.py
#

import sys

def main(stdin):
    '''
        takes parameter stdin, prints average high temperatures and average low temperatures
    '''
    
    # assign to buf the result of calling stdin.readline()
    buf = stdin.readline()   #reads lines from file (a line ends w \n)

    count = 0
    sumHi = 0.0
    sumLo = 0.0
    while buf.strip() != '':   #buf.strip() remove all space and give str

        #separating columns by commas into a LIST
        words = buf.split(',')

        #casting read data into float (original = string)
        hiTemp = float(words[0])
        loTemp = float(words[1])

        #number of temps averaged
        count += 1
        
        sumHi += hiTemp
        sumLo += loTemp
        
        #print('High: ',hiTemp, ', Low: ', loTemp)

        #read nxt line
        buf = stdin.readline()

    avgHi = sumHi/count
    avgLo = sumLo/count

    #normal printing
    #print('Average High: ',avgHi)
    #print('Average Low: ',avgLo)

    print('Average High: {0:6.2f}'.format(avgHi))
    print('Average Low: {0:6.2f}'.format(avgLo))

    #print('Average High: {0:f}, Average Low: {1:f}'.format(avgHi,avgLo)

if __name__ == "__main__":  #only invoked if run from cmd
    main(sys.stdin)
