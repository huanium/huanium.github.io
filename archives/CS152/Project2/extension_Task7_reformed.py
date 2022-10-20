# Huan Bui
# Sept 17, 2017
# CS152 Project 2
#
# extension_Task7_reformed.py
# Reads through the data, extracts the values from each line
# remembers the last n wind, gust, and PAR
# if temperature drops exceed 5%
# prints date and time, mix(n-1), sumWind, sumGust, sumPar
#
# Example of Unix command for running the file
# cat blend.csv | py extension_Task7_reformed.py (Win)
# cat blend.csv | python3 extension_Task7_reformed.py (Mac)

import sys

def main(stdin):
    '''
        takes parameter stdin (from data), prints datetime (string), mix(n-1),
        sumWind, sumGust, and sumPar (floats) if temperature drop exceed 5%
    '''
    n = 8 #n is number of 15-min intervals between n/2 hour(s)

    mix = [0.0]*n   #initializing lists of n elements
    wind = [0.0]*n
    gust = [0.0]*n
    par = [0.0]*n

    sumWind = 0.0
    sumGust = 0.0
    sumPar = 0.0

    datetime = ''

    buf = sys.stdin.readline()

    print('Date&time------------Mix-----Wind----Gust----PAR')

    while buf.strip() != '':
        
        for i in range(1,n):
            mix[n-i]= mix[n-1-i]    #shifting and updating
            wind[n-i] = wind[n-1-i]
            gust[n-i] = gust[n-1-i]
            par[n-i] = par[n-1-i]
            
        words = buf.split(',')
        
        datetime = words[0]
        mix[0] = float(words[1])
        wind[0]= float(words[3])
        gust[0] = float(words[4])
        par[0] = float(words[5])
        
        for i in range(0,n-1):
            sumWind += wind[i]
            sumGust += gust[i]
            sumPar += par[i]

        if (mix[n-1] - mix[0] > 5):
            print(datetime, ',', '{0:6.2f}'.format(mix[n-1]), ',', '{0:6.2f}'.format(sumWind), ',', '{0:6.2f}'.format(sumGust), ',', '{0:6.2f}'.format(sumPar))

        buf = stdin.readline()

if __name__ == "__main__":
    main(sys.stdin)
