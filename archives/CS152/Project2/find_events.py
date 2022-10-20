# Huan Bui
# Sept 17, 2017
# CS152 Project 2
#
# find_events.py
# Reads through the data, extracts the values from each line
# and remembers the last three wind, gust, and PAR values
# if temperature drop exceeds 5%
# prints out the datetime, mix3, sumWind, sumGust, and sumPar
#
# Example Unix command for running the file
# cat blend.csv | py find_events.py (Win)
# cat blend.csv | python3 find_events.py (Mac)

import sys

def main(stdin):
    '''
        takes parameter stdin (from data), prints datetime (string), mix3,
        sumWind, sumGust, and sumPar (floats) if temperature drop exceed 5%
    '''
    mix0 = 0.0
    mix1 = 0.0
    mix2 = 0.0
    mix3 = 0.0

    wind0 = 0.0
    wind1 = 0.0
    wind2 = 0.0
    wind3 = 0.0

    gust0 = 0.0
    gust1 = 0.0
    gust2 = 0.0
    gust3 = 0.0
    
    par0 = 0.0
    par1 = 0.0
    par2 = 0.0
    par3 = 0.0
    
    datetime = ''

    buf = sys.stdin.readline()

    print('Date&time------------Mix-----Wind----Gust----PAR')

    while buf.strip() != '':

        mix3 = mix2
        mix2 = mix1
        mix1 = mix0
        
        wind3 = wind2
        wind2 = wind1
        wind1 = wind0

        gust3 = gust2
        gust2 = gust1
        gust1 = gust0

        par3 = par2
        par2 = par1
        par1 = par0
        
        words = buf.split(',')
        
        datetime = words[0]
        mix0 = float(words[1])
        wind0 = float(words[3])
        gust0 = float(words[4])
        par0 = float(words[5])
        sumWind = wind0 + wind1 + wind2 + wind3
        sumGust = gust0 + gust1 + gust2 + gust3
        sumPar = par0 + par1 + par2 + par3

        if (mix3 - mix0 > 5):
            print(datetime, ',', '{0:6.2f}'.format(mix3), ',', '{0:6.2f}'.format(sumWind), ',', '{0:6.2f}'.format(sumGust), ',', '{0:6.2f}'.format(sumPar))

        buf = stdin.readline()

if __name__ == "__main__":
    main(sys.stdin)
